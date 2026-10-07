#!/bin/bash
# Session 14: resume an interrupted rehearsal run from the package's panel (the panel's Resume action) after an
# UNPLANNED interruption (the plan limit's 429 deferred the batches, then the container restart killed the job).
# Usage: resume_blind_panel.sh FOLDER RID REHEARSAL_DIR OUTDIR LABEL
set -u
FOLDER="$1"; RID="$2"; R="$3"; O="$4"; LABEL="$5"
PY=$FOLDER/.venv/bin/python
PANEL_DIR=$FOLDER/staging/panel
mkdir -p "$R" "$O"
clock() { date -u "+$1 %Y-%m-%d %H:%M:%S UTC" | tee -a $R/clock.txt; }
jst() { $PY -c "import json,sys; print(json.load(open(sys.argv[1])).get('status',''))" "$1" 2>/dev/null; }
cd "$FOLDER"
clock "$LABEL: panel restart for the resume"
$PY -m tenderpack panel --port 0 --panel-dir "$PANEL_DIR" > $O/panel_resume.out 2>&1 &
PANEL_PID=$!
for i in $(seq 1 60); do grep -q "operating panel at" $O/panel_resume.out && break; sleep 1; done
URL=$(grep -o "http://127.0.0.1:[0-9]*/t/[A-Za-z0-9_-]*/" $O/panel_resume.out | head -1)
echo "panel url: ${URL:-NONE} (pid $PANEL_PID)"; [ -n "$URL" ] || { echo "panel did not start"; kill $PANEL_PID 2>/dev/null; exit 2; }
JOB=$(grep -l "\"run_id\": \"$RID\"" $PANEL_DIR/jobs/*/job.json | head -1); echo "run job record: $JOB"
curl -s -o $O/run_page_before_resume.html "${URL}runs/$RID"
$PY -m tenderpack ai run-status "$RID" > $O/status_before_resume.txt 2>&1; head -16 $O/status_before_resume.txt
clock "resume (the panel's Resume button; the run job's status as the panel reads it: $(jst "$JOB"))"
curl -s -o /dev/null -w "resume http %{http_code}\n" -X POST -d "from_step=" "${URL}runs/$RID/resume"
sleep 3
JOB2=$(ls -t $PANEL_DIR/jobs/*/job.json | head -1); echo "resume job: $JOB2"
for i in $(seq 1 1440); do st=$(jst "$JOB2"); [ "$st" != "running" ] && break; sleep 5; done
code=$($PY -c "import json,sys; print(json.load(open(sys.argv[1])).get('exit_code',''))" "$JOB2")
clock "end (resume job status $st exit $code)"
cp "$JOB" $O/job_run.json; cp "$JOB2" $O/job_resume.json
{ echo "== run job $(basename $(dirname $JOB)) (killed by the container restart after the limit's 429 deferred its batches)"; cat $(dirname "$JOB")/output.log; echo; echo "== resume job $(basename $(dirname $JOB2))"; cat $(dirname "$JOB2")/output.log; } > $R/run.log
kill $PANEL_PID 2>/dev/null
$PY -m tenderpack ai run-status "$RID" > $O/status_final.txt 2>&1; head -18 $O/status_final.txt
echo "done: run $RID exit $code"
