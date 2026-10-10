import json
from types import SimpleNamespace

from tenderpack.ai import regionread


def test_draft_reading_without_controller_attribution_reaches_evidence_checks(tmp_path):
    (tmp_path / "regions.json").write_text(json.dumps({"regions": []}))
    reading = {"region_id": "ADD-03-p1-r1", "unit_id": "ADD-03:image", "title": "Notice",
               "source": {"doc": "ADD-03", "page": 1, "bbox_pt": [0, 0, 100, 100]},
               "content_type": "text", "languages": ["en"], "method": "visual", "blocks": []}
    result = regionread.check(tmp_path, tmp_path / "pack.yaml", reading)
    assert result["parsed"], result
    assert not result["ok"]  # Missing image evidence remains a real failure.
    assert "prepared_by" not in reading  # The dry run must not mutate the caller's draft.


def test_table_reading_keeps_top_level_text_blocks_in_validation_and_emitted_units():
    from tenderpack.readings import Reading, reading_units
    reading = Reading.model_validate({
        "region_id": "ADD-03-p1-r1", "unit_id": "ADD-03:table", "title": "Table",
        "source": {"doc": "ADD-03", "page": 1, "bbox_pt": [0, 0, 100, 100]},
        "content_type": "table", "languages": ["en"], "method": "visual", "prepared_by": "fixture",
        "table": {"columns": [{"key": "value", "heading": "Value"}], "rows": [{"key": "row", "cells": {"value": "1"}}]},
        "blocks": [{"key": "footer", "lang": "en", "role": "note", "lines": [{"band": 1, "source": "Applies after completion."}]}]})
    assert [b.key for b in reading.all_blocks()] == ["footer"]
    units = reading_units(reading, SimpleNamespace(region_id=reading.region_id, bbox=[0, 0, 100, 100], crop=None),
                          {"status": "pending", "subject_sha256": "fixture"}, {})
    assert next(u for u in units if u["unit_id"] == "ADD-03:table/footer")["text"] == "Applies after completion."
    assert "Applies after completion." in next(u for u in units if u["kind"] == "table_row")["context"]["notes"]
