"""Units against expectations read from the rendered pages (tests/golden/pack_expectations.yaml)."""
import re

from tenderpack.textnorm import normalize_latin


def test_every_content_span_in_exactly_one_unit(pack):
    checks = {c["id"]: c for c in pack["coverage"]["checks"]}
    assert checks["C02"]["ok"] and checks["C03"]["ok"], checks
    assert not pack["coverage"]["problems"]


def test_superscripts_classified(pack, golden):
    sup = pack["coverage"]["superscripts"]
    g = golden["superscripts"]
    assert len(sup) == g["total"]
    assert sum(s["class"] == "unit exponent" for s in sup) == g["unit_exponents"]
    assert sum(s["class"] == "footnote marker" for s in sup) == g["footnote_markers"]
    assert all(s["footnote"] for s in sup if s["class"] == "footnote marker")


def test_footnote_12_keeps_its_rejection_rule(pack, golden):
    g = golden["footnote_12"]
    fn = pack["by_id"][g["host"] + "#fn12"]
    assert fn["kind"] == "footnote" and fn["parent"] == g["host"]
    assert g["contains"] in fn["text"] and g["contains_exponent"] in fn["text"]
    assert fn["style"]["small_print"]
    host = pack["by_id"][g["host"]]
    assert host["text"].endswith("Form 4-B.¹²")
    assert "4-B.12" not in host["normalized"] and "Form 4-B." in host["normalized"]


def test_repeated_wording_lives_in_distinct_units(pack, golden):
    """Independent of any amendment logic: the trap exists in the volumes and segmentation keeps the
    occurrences apart. (The addenda quote the same words when amending them; those are not targets.)"""
    for item in golden["repeated_wording"]:
        hits = sorted(u["unit_id"] for u in pack["units"]
                      if u["kind"] == "clause" and u["doc"].startswith("VOL-")
                      and item["text"] in normalize_latin(u["text"]))
        assert hits == sorted(item["units"]), (item, hits)


def test_printed_pdd_fields(pack, golden):
    for item in golden["printed_pdd_fields"]:
        assert item["contains"] in pack["by_id"][item["unit"]]["text"]


def test_split_tables_join_with_row_pages(pack, golden):
    for t in golden["split_tables"]:
        table = pack["by_id"][t["unit"]]
        rows = table["children"]
        keys = [r if r.startswith(t["unit"].split(":")[0] + ":Q") else r.split("/")[-1] for r in rows]
        assert keys == t["rows"], (t["unit"], keys)
        assert [pack["by_id"][r]["pages"][0] for r in rows] == t["row_pages"]
        assert [h["page"] for h in table["table"]["repeated_headers"]] == t["repeated_header_pages"]


def test_caption_joins_table_on_next_page(pack, golden):
    g = golden["caption_across_pages"]
    t = pack["by_id"][g["unit"]]
    assert t["pages"] == g["pages"] and len(t["children"]) == g["rows"]
    assert t["label"].startswith("Table 1-1")


def test_small_print_notes(pack, golden):
    for n in golden["small_print_notes"]:
        u = pack["by_id"][n["unit"]]
        assert u["style"]["small_print"] and n["contains"] in u["text"], n


def test_list_items(pack, golden):
    for li in golden["list_items"]:
        parent = pack["by_id"][li["parent"]]
        labels = [pack["by_id"][c]["label"] for c in parent["children"] if pack["by_id"][c]["kind"] == "list_item"]
        assert labels == li["labels"]


def test_synthetic_fixture_structure(synthetic):
    e, by = synthetic["expected"], synthetic["by_id"]
    assert by["SYN-01:1.1"]["unit_exponents"] and "m³/day" in by["SYN-01:1.1"]["text"]
    fn = by["SYN-01:1.2#fn7"]
    assert e["p1"]["footnote"]["text_contains"] in fn["text"]
    t = by["SYN-01:T9-1"]
    assert [c.split("/")[-1] for c in t["children"]] == e["p2_p3_table"]["rows"]
    assert [by[c]["pages"][0] for c in t["children"]] == e["p2_p3_table"]["row_pages"]
    assert [h["page"] for h in t["table"]["repeated_headers"]] == [e["p2_p3_table"]["repeated_header_page"]]
    # mixed page: text before and after the image is captured, around a region unit
    order = [u["unit_id"] for u in synthetic["units"] if 4 in u.get("pages", [])]
    assert order.index("SYN-01:4.1") < order.index("SYN-01:region:SYN-01-p4-r1") < order.index("SYN-01:4.2")


def test_unit_ids_unique_and_stable_format(pack):
    ids = [u["unit_id"] for u in pack["units"]]
    assert len(ids) == len(set(ids))
    assert all(re.match(r"^[A-Z]+-[0-9A-Z]+:", i) for i in ids)


def test_minutes_items_are_separate_units(pack, golden):
    """A bold lead-in after a paragraph starts a new unit (E21: they had collapsed into one paragraph)."""
    for uid in golden["minutes_items"]:
        assert pack["by_id"][uid]["kind"] == "lead_in_paragraph", uid
    item3 = pack["by_id"]["ADD-01:AppB/item-3-evaluation"]["text"]
    assert "seventy / thirty" in item3 and "Item 4" not in item3
    # inside a clause, a wrapped line starting in bold stays part of the clause
    assert "November 2026" in pack["by_id"]["ADD-01:2.1"]["text"]
