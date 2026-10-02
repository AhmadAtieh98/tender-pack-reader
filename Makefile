# Stage 1 and Stage 2 workflow. Everything runs offline once the environment is installed.
PY ?= .venv/bin/python

.PHONY: setup evidence outputs drill test verify

setup:            ## create .venv from uv.lock (needs network once)
	uv sync --extra dev

evidence:         ## rebuild build/ (real pack) then build/fixture (synthetic mixed example); stops on a structural failure
	$(PY) -m tenderpack ingest
	$(PY) tests/fixtures/make_fixture.py build/fixture-src
	$(PY) -m tenderpack ingest --pack build/fixture-src/pack.yaml --out build/fixture

outputs:          ## Stage 2: A1/A2/A3/A5 from build/ into out/; stops on a structural failure (previous out/ kept)
	$(PY) -m tenderpack outputs --evidence build --out out

drill:            ## synthetic Addendum No. 3 through the same path (no curated op file: drafted) into build/drill, out-drill/
	$(PY) tests/fixtures/make_drill.py build/drill-src
	$(PY) -m tenderpack ingest --pack build/drill-src/pack.yaml --out build/drill
	$(PY) -m tenderpack outputs --evidence build/drill --pack build/drill-src/pack.yaml --out out-drill

test:
	$(PY) -m pytest -q -p no:cacheprovider

verify: test      ## rebuild twice in disposable directories and compare output hashes (Stage 1 and Stage 2)
	$(PY) -m tenderpack ingest --out /tmp/tenderpack-verify-a > /dev/null
	$(PY) -m tenderpack ingest --out /tmp/tenderpack-verify-b > /dev/null
	$(PY) -c "import json,sys; a=json.load(open('/tmp/tenderpack-verify-a/BUILD_MANIFEST.json'))['outputs']; b=json.load(open('/tmp/tenderpack-verify-b/BUILD_MANIFEST.json'))['outputs']; print('identical' if a==b else 'DIFFERENT'); sys.exit(a!=b)"
	$(PY) -m tenderpack outputs --evidence build --out /tmp/tenderpack-verify-out-a > /dev/null
	$(PY) -m tenderpack outputs --evidence build --out /tmp/tenderpack-verify-out-b > /dev/null
	diff -r /tmp/tenderpack-verify-out-a /tmp/tenderpack-verify-out-b && echo "stage 2 outputs identical"
