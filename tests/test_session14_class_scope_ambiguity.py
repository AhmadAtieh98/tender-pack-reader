"""Session 14 (W4), part 3 (b): a genuine ambiguity that was never raised (blind-07 COMPARISON.md "The deliberate
ambiguity": DA1, the composite asset; a pump set is mechanical equipment (5 years) and its motor electrical/I&C
equipment (7 years), and Table 42-1 says nothing about an asset in both classes).

The general gap: an addendum value whose scope two readings of the documents draw differently must raise a pending
judgment. A table that assigns different values by class (a column headed class / category / type / asset, or the
Arabic فئة / صنف / نوع) and states no rule for an item that falls in more than one class (none of its own words, notes
or title says 'more than one class', 'composite', 'each component', 'whichever is the longer', ...) gives such a value:
signals.class_scope_findings names it, and A1's Issues sheet lists it as a generated issue I-AUTO-CLASS-SCOPE-<table>,
HUMAN DECISION PENDING, conditional on a pending image reading where the table is one. Nothing is decided; no class
is chosen; no clarification is proposed (the route may be closed)."""
from __future__ import annotations

import pytest

from tenderpack import human_owned as H
from tenderpack import signals, stage2
from tenderpack.util import ROOT

HEAD = ["م", "فئة الأصول", "الحد الأدنى للعمر المتبقي (سنة)", "أقصى درجة للحالة"]


def _row(i, cls, life, grade, status="pending"):
    return {"unit_id": f"ADD-9:T42-1/image/r{i}", "kind": "table_row", "doc": "ADD-9", "pages": [3],
            "text": f"م: {i} | فئة الأصول: {cls} | الحد الأدنى للعمر المتبقي (سنة): {life} | أقصى درجة للحالة: {grade}",
            "cells": dict(zip(HEAD, [str(i), cls, life, grade])), "context": {"column_headings": HEAD},
            "reading": {"region": "ADD-9-p3-r1", "status": status}}


UNITS = [_row(1, "المنشآت المدنية والخرسانية", "٢٠", "٢"), _row(3, "المعدات الميكانيكية", "٥", "٣"),
         _row(4, "المعدات الكهربائية وأجهزة القياس والتحكم", "٧", "٣"),
         {"unit_id": "ADD-9:T42-1/image/note2", "kind": "paragraph", "doc": "ADD-9", "pages": [3],
          "text": "٢. يحدد المهندس المستقل العمر المتبقي لكل أصل في مسح الحالة."}]


def test_a_class_table_without_an_allocation_rule_raises_a_pending_judgment_synthetic():
    f = signals.class_scope_findings(UNITS)
    assert len(f) == 1, f
    x = f[0]
    assert x["table"] == "ADD-9:T42-1/image" and x["class_column"] == "فئة الأصول"
    assert "الحد الأدنى للعمر المتبقي (سنة)" in x["value_columns"]
    assert x["conditional_on"] == ["ADD-9-p3-r1"]
    assert "more than one class" in x["text"] and "no rule" in x["text"]


def test_an_allocation_rule_or_one_class_or_equal_values_raise_nothing_synthetic():
    rule = UNITS + [{"unit_id": "ADD-9:T42-1/image/note4", "kind": "paragraph", "doc": "ADD-9", "pages": [3],
                     "text": "4. Where an asset falls within more than one class, the longer remaining life applies."}]
    assert signals.class_scope_findings(rule) == []
    assert signals.class_scope_findings(UNITS[:1] + UNITS[3:]) == []                  # one class
    same = [_row(1, "a", "٥", "٣"), _row(2, "b", "٥", "٣")]
    assert signals.class_scope_findings(same) == []                                  # no value differs
    eng = [dict(_row(1, "x", "1", "1"), cells={"Parameter": "BOD5", "Limit": "10"},
                context={"column_headings": ["Parameter", "Limit"]}),
           dict(_row(2, "x", "1", "1"), cells={"Parameter": "COD", "Limit": "50"},
                context={"column_headings": ["Parameter", "Limit"]})]
    assert signals.class_scope_findings(eng) == []                                   # not a class table


def test_the_generated_issue_is_pending_and_names_its_rows_synthetic():
    iss = signals.class_scope_issues(UNITS, rows={"ADD-9-T42-1-03": ["ADD-9:T42-1/image/r3"],
                                                  "ADD-9-T42-1-04": ["ADD-9:T42-1/image/r4"],
                                                  "OTHER": ["VOL-I:1.1"]})
    assert len(iss) == 1
    i = iss[0]
    assert i["id"] == "I-AUTO-CLASS-SCOPE-ADD-9-T42-1-image"
    assert i["text"].startswith(H.HUMAN_DECISION_PENDING) and i["human_decision"] == H.HUMAN_DECISION_PENDING
    assert i["rows"] == ["ADD-9-T42-1-03", "ADD-9-T42-1-04"]
    assert "Conditional on the pending reading ADD-9-p3-r1" in i["text"]
    assert not i["show_in_a3"]


@pytest.fixture(scope="module")
def real():
    return stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)


def test_the_real_pack_has_no_class_table_so_nothing_is_raised(real):
    assert signals.class_scope_findings(real["units"]) == []
    assert not [i for i in stage2.collect_issues(real, None) if i["id"].startswith("I-AUTO-CLASS-SCOPE-")]


def test_blind07_table_42_1_reading_raises_it_labelled_regression():
    """Labelled regression on rehearsal material (never tender content): the committed blind-07 candidate reading of
    Table 42-1 (rehearsals/blind-07/candidate-curation/readings/ADD-03-p3-r1.yaml), its rows made into table-row units
    the way the reading's columns head them, with its notes. DA1 is raised; no class is chosen."""
    import yaml
    rd = yaml.safe_load((ROOT / "rehearsals/blind-07/candidate-curation/readings/ADD-03-p3-r1.yaml")
                        .read_text(encoding="utf-8"))
    t = rd["table"]
    heads = {c["key"]: c["heading"] for c in t["columns"]}
    units = [{"unit_id": f"{rd['unit_id']}/{row['key']}", "kind": "table_row",
              "cells": {heads[k]: str(v) for k, v in row["cells"].items()},
              "context": {"column_headings": list(heads.values())},
              "text": " | ".join(f"{heads[k]}: {v}" for k, v in row["cells"].items()),
              "reading": {"region": rd["region_id"], "status": "pending"}} for row in t["rows"]]
    for k in ("title", "qualifier", "notes"):
        blocks = t.get(k) or []
        for j, b in enumerate(blocks if isinstance(blocks, list) else [blocks]):
            for i, ln in enumerate(b.get("lines") or []):
                units.append({"unit_id": f"{rd['unit_id']}/{k}{j}-{i}", "kind": "paragraph",
                              "text": ln.get("source", ""), "translation": b.get("translation", "")})
    f = signals.class_scope_findings(units)
    assert [x["table"] for x in f] == [rd["unit_id"]], f
    assert any("الميكانيكية" in c for c in f[0]["classes"]) and any("الكهربائية" in c for c in f[0]["classes"])
    assert f[0]["conditional_on"] == [rd["region_id"]]
