"""The owner's local operating panel (session 12, part 5): `tenderpack panel [--port N] [--open]`.

server.py  the HTTP server (127.0.0.1 only, a random token per start in the URL path), routes, file areas, uploads
jobs.py    real backend jobs: `<python> -m tenderpack ...` in a subprocess, one log folder per job
views.py   the plain HTML pages, built from the engine's own records with every value escaped

A1-A5 under out/ remain the deliverables; the panel opens them and runs the existing commands. It approves, accepts
and rejects nothing: a decision runs only from a form a person filled and confirmed (docs/PANEL.md)."""
