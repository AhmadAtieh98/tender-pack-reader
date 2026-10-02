# Stage 1 workflow. Everything runs offline once the environment is installed.
PY ?= .venv/bin/python

.PHONY: setup evidence test verify

setup:            ## create .venv from uv.lock (needs network once)
	uv sync --extra dev

evidence:         ## rebuild build/ (real pack) then build/fixture (synthetic mixed example); stops on a structural failure
	$(PY) -m tenderpack ingest
	$(PY) tests/fixtures/make_fixture.py build/fixture-src
	$(PY) -m tenderpack ingest --pack build/fixture-src/pack.yaml --out build/fixture

test:
	$(PY) -m pytest -q -p no:cacheprovider

verify: test      ## rebuild twice in disposable directories and compare output hashes
	$(PY) -m tenderpack ingest --out /tmp/tenderpack-verify-a > /dev/null
	$(PY) -m tenderpack ingest --out /tmp/tenderpack-verify-b > /dev/null
	$(PY) -c "import json,sys; a=json.load(open('/tmp/tenderpack-verify-a/BUILD_MANIFEST.json'))['outputs']; b=json.load(open('/tmp/tenderpack-verify-b/BUILD_MANIFEST.json'))['outputs']; print('identical' if a==b else 'DIFFERENT'); sys.exit(a!=b)"
