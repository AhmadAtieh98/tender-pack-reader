#!/bin/bash
# Session 14, part 6: a rehearsal driven through the interview package's panel (upload-to-results) from an unzipped
# package with its .venv built and its host model pinned, with a planned interruption that lands RIGHT AFTER an
# analysis batch's submission is recorded (batches/<batch>.submission.json: the MCP server writes it at once) while
# that batch's host session is still ending, so that the resume must reuse a submission made just before the stop;
# then a resume from the panel's Resume action. Clock lines and the job logs go to the rehearsal folder.
# Usage: run_blind_panel.sh FOLDER PDF REHEARSAL_DIR OUTDIR
set -u
FOLDER="$1"; PDF="$2"; R="$3"; O="$4"
PY=$FOLDER/.venv/bin/python
PANEL_DIR=$FOLDER/staging/panel
mkdir -p "$R" "$O"
clock() { date -u "+$1 %Y-%m-%d %H:%M:%S UTC" | tee -a $R/clock.txt; }
jst() { $PY -c "import json,sys; print(json.load(open(sys.argv[1])).get('status',''))" "$1" 2>/dev/null; }
cd "$FOLDER"
clock "panel start"
$PY -m tenderpack panel --port 0 --panel-dir "$PANEL_DIR" > $O/panel.out 2>&1 &
PANEL_PID=$!
for i in $(seq 1 60); do grep -q "operating panel at" $O/panel.out && break; sleep 1; done
URL=$(grep -o "http://127.0.0.1:[0-9]*/t/[A-Za-z0-9_-]*/" $O/panel.out | head -1)
echo "panel url: ${URL:-NONE} (pid $PANEL_PID)"; [ -n "$URL" ] || { echo "panel did not start"; kill $PANEL_PID 2>/dev/null; exit 2; }
clock "upload (the panel's New addendum form, route host)"
curl -s -o $O/upload_response.html -w "upload http %{http_code} redirect %{redirect_url}\n" -F "pdf=@$PDF" -F "addendum=ADD-03" -F "route=host" "${URL}addendum/start"
sleep 3
JOB=$(ls -t $PANEL_DIR/jobs/*/job.json 2>/dev/null | head -1); echo "job record: $JOB"
RID=$($PY -c "import json,sys; d=json.load(open(sys.argv[1])); print(d.get('meta',{}).get('run_id',''))" "$JOB")
PID=$($PY -c "import json,sys; d=json.load(open(sys.argv[1])); print(d.get('pid',''))" "$JOB")
echo "$RID" > $R/run.id; echo "run id $RID, job pid $PID" | tee -a $R/clock.txt
RUN=$FOLDER/staging/ai/runs/$RID; CP=$RUN/checkpoint.json
# 1. wait until the first analysis batch is done (an answer taken), or the job ends
for i in $(seq 1 720); do
  if [ -f "$CP" ] && $PY -c "import json,sys; d=json.load(open(sys.argv[1])); b=d.get('batches',{}); sys.exit(0 if b.get('analysis-001',{}).get('status')=='done' else 1)" "$CP" 2>/dev/null; then break; fi
  s=$(jst "$JOB"); if [ -n "$s" ] && [ "$s" != "running" ] && [ "$s" != "queued" ]; then clock "the run job ended before analysis-001 (job status $s): no interruption"; cp "$JOB" $O/job_run.json; cat $(dirname "$JOB")/output.log >> $R/run.log; kill $PANEL_PID 2>/dev/null; exit 4; fi
  sleep 5
done
clock "analysis-001 done; now waiting for the NEXT analysis submission record to appear"
# 2. the next analysis submission record (a batch whose session is still ending): SIGTERM within a second of it
SEEN=$(ls $RUN/batches/analysis-*.submission.json 2>/dev/null | wc -l)
for i in $(seq 1 3600); do
  NOW=$(ls $RUN/batches/analysis-*.submission.json 2>/dev/null | wc -l)
  if [ "$NOW" -gt "$SEEN" ]; then NEWREC=$(ls -t $RUN/batches/analysis-*.submission.json | head -1); break; fi
  s=$(jst "$JOB"); if [ -n "$s" ] && [ "$s" != "running" ]; then clock "the run job ended before a further submission (job status $s): no interruption"; cp "$JOB" $O/job_run.json; cat $(dirname "$JOB")/output.log >> $R/run.log; kill $PANEL_PID 2>/dev/null; exit 4; fi
  sleep 0.5
done
clock "submission recorded: $(basename ${NEWREC:-none}); SIGTERM to pid $PID (planned interruption, right after the submission)"
kill -TERM "$PID" 2>/dev/null
for i in $(seq 1 24); do s=$(jst "$JOB"); [ "$s" != "running" ] && break; sleep 5; done
clock "the interrupted job ended (status $s)"
$PY -m tenderpack ai run-status "$RID" > $O/status_after_sigterm.txt 2>&1; head -16 $O/status_after_sigterm.txt
clock "resume (the panel's Resume button)"
curl -s -o /dev/null -w "resume http %{http_code}\n" -X POST -d "from_step=" "${URL}runs/$RID/resume"
sleep 3
JOB2=$(ls -t $PANEL_DIR/jobs/*/job.json | head -1); echo "resume job: $JOB2"
for i in $(seq 1 1440); do st=$(jst "$JOB2"); [ "$st" != "running" ] && break; sleep 5; done
code=$($PY -c "import json,sys; print(json.load(open(sys.argv[1])).get('exit_code',''))" "$JOB2")
clock "end (resume job status $st exit $code)"
cp "$JOB" $O/job_run.json; cp "$JOB2" $O/job_resume.json
{ echo "== run job $(basename $(dirname $JOB))"; cat $(dirname "$JOB")/output.log; echo; echo "== resume job $(basename $(dirname $JOB2))"; cat $(dirname "$JOB2")/output.log; } > $R/run.log
kill $PANEL_PID 2>/dev/null
$PY -m tenderpack ai run-status "$RID" > $O/status_final.txt 2>&1; head -18 $O/status_final.txt
echo "done: run $RID exit $code"
