"""Session 14 (F4): the fixes for the final reviewer's findings outside the workflow files (R4-2, R4-4, R4-5, R4-6,
R4-11). Each test reproduced its finding before the fix.

R4-2   the owner's rule "an unresolved change must not show the old value as unchanged": in a candidate A1 a row whose
       candidate status is "UNRESOLVED (value in question)" never reads "unchanged since <stage>" in the Value column;
       the value state says "value in question (unresolved: <reason>)" with the status's own reason, and the review
       cards say the same (stage2.row_states, partial.in_question)
R4-5   get_addendum_page checks its own scope file (the hash recorded at prepare_scope, re-checked on every call; a
       changed scope file refuses every call) and serves no path outside the review's own folder (a scope entry naming
       a path outside it, or a symlink out of it, is refused)
R4-4   the MCP repair re-submission replaces ONLY the named failing items (any other item is refused with its id named;
       the first submission's valid items stay as first given) and a refused re-submission uses the one repair
R4-6   offline under every switch: offline.check_adapter and offline.check_http hold whether offline comes from
       TENDERPACK_OFFLINE, from --offline or from ai.yaml's offline key (one resolver, offline.is_offline)
R4-11  insert_table finds a table whose number is printed in Arabic-Indic digits when the op names it in Latin digits

The candidate of R4-2 is blind rehearsal 05's committed candidate (tests/fixtures/s12_blind05.py: synthetic material,
never the truth about the tender), whose op file leaves provisions on rows' units unresolved."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

import s12_blind05 as F
from tenderpack import partial as P
from tenderpack import stage2
from tenderpack.batches import states_block_html

# ---------------------------------------------------------------------------------------------- R4-2


@pytest.fixture(scope="module")
def cand(tmp_path_factory):
    return F.run(tmp_path_factory)["r"]


def test_r4_2_a_value_in_question_never_reads_unchanged_in_the_candidate_a1_or_on_its_card(cand, tmp_path_factory):
    from tenderpack.ai import workflow as WF
    r = cand
    unres = {k: [w for w in v if not w.startswith("STALE")] for k, v in P.unresolved_rows(r).items()}
    unres = {k: v for k, v in unres.items() if v}
    assert unres, "the candidate names rows through unresolved provisions on their units"
    ctx = SimpleNamespace(addendum=r["working"].stage, dir=tmp_path_factory.mktemp("f4-r4-2"), ws=None)
    status, default, _ = WF._row_statuses(ctx, r)
    states = stage2.row_states(r)
    a1 = {x["id"]: x for x in stage2.a1_table(r, stage2.collect_issues(r, None))["rows"]}
    head = "UNRESOLVED (value in question): "
    checked = 0
    for rid in unres:
        st = status.get(rid, default)
        if not st.startswith(head):
            continue                                # a row the run re-read or a person decided: its own status
        checked += 1
        reason = st[len(head):]
        for where, val in (("row_states", states[rid]["value"]), ("A1 Value column", a1[rid]["value_state"]),
                           ("review card", states_block_html(states[rid]))):
            assert "unchanged since" not in val, (where, rid, val)
            assert f"value in question (unresolved: {reason}" in val, (where, rid, st, val)
    assert checked, "rows with the status 'UNRESOLVED (value in question)'"
    # a row no unresolved provision names keeps its value state as it was
    other = next(rid for rid, s in states.items() if rid not in P.unresolved_rows(r) and
                 s["value"].startswith("unchanged since"))
    assert "value in question" not in states[other]["value"]


# ---------------------------------------------------------------------------------------------- R4-5

PDF06 = F.ROOT / "rehearsals/blind-06/input/ADD-03_Addendum_No_3.pdf"          # synthetic rehearsal input (test data)


def _sha(b: bytes) -> str:
    import hashlib
    return hashlib.sha256(b).hexdigest()


def _scope(tmp_path, qid="ADD-03-qr-f4"):
    from tenderpack.ai import quick_review as QR
    d = tmp_path / "staging" / "ai" / "quick-review" / qid
    d.mkdir(parents=True)
    return d, QR.prepare_scope(PDF06, d, "ADD-03", qid)


def test_r4_5_the_page_tool_checks_its_own_scope_file_and_a_changed_one_refuses_every_call(tmp_path):
    import json
    from tenderpack.ai import quick_review as QR
    from tenderpack.ai.tools import ToolError
    d, sc = _scope(tmp_path)
    sp = d / QR.SCOPE_FILE
    rec = sc.get("file_sha256")
    assert rec == _sha(sp.read_bytes()), "prepare_scope records the scope file's own sha256"
    ws = SimpleNamespace(addendum_scope=str(sp), addendum_scope_sha256=rec)
    assert QR.tool_get_addendum_page(ws, 4)["page"] == 4
    j = json.loads(sp.read_text(encoding="utf-8"))
    j["pages"][0]["text"] = "words the addendum does not print (session 14 test data)"
    sp.write_text(json.dumps(j), encoding="utf-8")                  # the scope changed after it was recorded
    for page, region in ((1, None), (2, None), (4, None), (4, 1)):
        with pytest.raises(ToolError, match="integrity failure: the scope file"):
            QR.tool_get_addendum_page(ws, page, region)
    # a server given a scope without its recorded hash serves nothing
    d2, sc2 = _scope(tmp_path, "ADD-03-qr-f4-b")
    with pytest.raises(ToolError, match="no recorded sha256"):
        QR.tool_get_addendum_page(SimpleNamespace(addendum_scope=str(d2 / QR.SCOPE_FILE), addendum_scope_sha256=None), 1)


def test_r4_5_the_page_tool_serves_no_path_outside_the_review_folder(tmp_path):
    import json
    import os
    from tenderpack.ai import quick_review as QR
    from tenderpack.ai.tools import ToolError
    d, sc = _scope(tmp_path)
    sp, base = d / QR.SCOPE_FILE, d / QR.SCOPE_DIR
    page1 = base / sc["pages"][0]["image"]["file"]
    outside = tmp_path / "outside.png"
    outside.write_bytes(page1.read_bytes())                         # the recorded bytes, outside the review's folder
    original = sp.read_text(encoding="utf-8")
    # (a) a scope entry naming a path outside the folder (relative or absolute), the scope re-anchored as if written so
    for name in (os.path.relpath(outside, base), str(outside)):
        j = json.loads(original)
        j["pages"][0]["image"]["file"] = name
        sp.write_text(json.dumps(j), encoding="utf-8")
        ws = SimpleNamespace(addendum_scope=str(sp), addendum_scope_sha256=_sha(sp.read_bytes()))
        with pytest.raises(ToolError, match="outside the quick review's folder"):
            QR.tool_get_addendum_page(ws, 1)
    # (b) a symlink inside the folder pointing out of it (the bytes are the recorded ones)
    sp.write_text(original, encoding="utf-8")
    ws = SimpleNamespace(addendum_scope=str(sp), addendum_scope_sha256=_sha(sp.read_bytes()))
    assert QR.tool_get_addendum_page(ws, 1)["page"] == 1
    page1.unlink()
    page1.symlink_to(outside)
    with pytest.raises(ToolError, match="outside the quick review's folder"):
        QR.tool_get_addendum_page(ws, 1)


# ---------------------------------------------------------------------------------------------- R4-4


@pytest.fixture(scope="module")
def rws(request, tmp_path_factory):
    from ai_fixture import workspace
    return workspace(tmp_path_factory.mktemp("f4-repair"), evidence=request.getfixturevalue("blind02_build"))


def _mcp(srv, n, args):
    import json
    r = srv.handle({"jsonrpc": "2.0", "id": n, "method": "tools/call",
                    "params": {"name": "submit_proposals", "arguments": args}})
    return json.loads(r["result"]["content"][0]["text"]), r["result"]["isError"]


def test_r4_4_the_repair_takes_only_the_named_items_and_refuses_every_other_item_and_statement(rws):
    from pathlib import Path

    import yaml

    import test_session14_payload_repair as PR
    from tenderpack.mcp_server import Server
    st = rws.identity().model_dump()
    s1 = {"id": "S1", "kind": "assumption", "text": "the period counts calendar days (session 14 test data)"}
    srv = Server(rws, None, tools=["submit_proposals"], submit_once=True)
    a, err = _mcp(srv, 1, {"proposal_set": PR._set(st, [{**PR._op(st), "statements": ["S1"]}, PR._row(st, PR.BAD_ROW)],
                                                   [s1]), "host_model": "test-host"})
    assert not err and [p["id"] for p in a["repair"]["problems"]] == ["ADD-03/2.4/row"], a
    # the re-submission: the named row repaired (citing a new statement S3), plus a sibling op resent changed citing a
    # new statement S2, and the sibling's statement S1 changed: only the row and S3 are taken
    s1x = {**s1, "text": "the period counts working days (session 14 test data)"}
    s2 = {"id": "S2", "kind": "assumption", "text": "a basis the first op never cited (session 14 test data)"}
    s3 = {"id": "S3", "kind": "assumption", "text": "the new clause is procedural (session 14 test data)"}
    b, err = _mcp(srv, 2, {"proposal_set": PR._set(st, [{**PR._row(st, PR.GOOD_ROW), "statements": ["S3"]},
                                                        {**PR._op(st, "one hundred and ninety (190) days"),
                                                         "statements": ["S1", "S2"]}], [s1x, s2, s3]),
                           "host_model": "test-host"})
    assert not err and b["repair_of"] == a["run_id"], b
    m = b["repair_merge"]
    assert m["replaced"] == ["ADD-03/2.4/row"], m
    assert set(m["refused"]) == {"ADD-03/3.1", "S1", "S2"}, m              # each named, with why
    assert all(k in m["why_refused"] for k in ("ADD-03/3.1", "S1", "S2")), m
    ps = yaml.safe_load((Path(b["staging"]) / "proposals.yaml").read_text())["proposal_set"]
    by = {it["id"]: it for it in ps["items"]}
    assert by["ADD-03/3.1"]["payload"]["new"] == "one hundred and eighty (180) days"        # as first given
    assert by["ADD-03/3.1"]["statements"] == ["S1"]
    sts = {s["id"]: s for s in ps["statements"]}
    assert sts["S1"]["text"] == s1["text"] and "S2" not in sts and sts["S3"]["text"] == s3["text"], sts


def test_r4_4_a_refused_re_submission_uses_the_one_repair(rws, monkeypatch):
    import test_session14_payload_repair as PR
    from tenderpack.ai import tools as T
    from tenderpack.mcp_server import Server
    st = rws.identity().model_dump()
    for once in (False, True):
        srv = Server(rws, None, tools=["submit_proposals"], submit_once=once)
        a, err = _mcp(srv, 1, {"proposal_set": PR._set(st, [PR._op(st), PR._row(st, PR.BAD_ROW)]),
                               "host_model": "test-host"})
        assert not err and a["repair"]["tries_left"] == 1, a
        real = T.call_tool

        def refusing(ws, name, args, caller="cli"):
            raise T.ToolError("refused by the controller (session 14 test)")
        monkeypatch.setattr(T, "call_tool", refusing)
        b, err = _mcp(srv, 2, {"proposal_set": PR._set(st, [PR._row(st, PR.GOOD_ROW)]), "host_model": "test-host"})
        assert err and "refused by the controller" in b["error"], b
        monkeypatch.setattr(T, "call_tool", real)
        c, err = _mcp(srv, 3, {"proposal_set": PR._set(st, [PR._row(st, PR.GOOD_ROW)]), "host_model": "test-host"})
        assert err and "repair already used" in c["error"], (once, c)


# ---------------------------------------------------------------------------------------------- R4-6


def _direct_builds_refused(OFF) -> None:
    """The session-14 last-line guards: a hosted adapter built directly, and an HTTP request to a hosted address."""
    from tenderpack.ai import config as C
    from tenderpack.ai.providers import base
    from tenderpack.ai.providers.anthropic import AnthropicProvider
    from tenderpack.ai.providers.host import HostProvider
    from tenderpack.ai.providers.openrouter import OpenRouterProvider
    cfg = C.load()
    with pytest.raises(OFF.OfflineError, match="offline mode"):
        AnthropicProvider("test-model", cfg["routes"]["anthropic"], {})
    with pytest.raises(OFF.OfflineError, match="offline mode"):
        OpenRouterProvider("vendor/m", cfg["routes"]["openrouter"], {})
    with pytest.raises(OFF.OfflineError, match="offline mode"):
        HostProvider("declared-model")
    with pytest.raises(OFF.OfflineError, match="not a loopback address"):
        base.http_json("GET", "https://api.anthropic.com/v1/models", {}, None, 5)


@pytest.mark.parametrize("switch", ["env", "flag", "config"])
def test_r4_6_the_last_line_guards_hold_under_each_offline_switch_alone(switch, monkeypatch):
    import copy

    from fake_ollama import NetGuard
    from tenderpack.ai import config as C
    from tenderpack.ai import offline as OFF
    guard = NetGuard(monkeypatch, allow_port=1)                     # nothing at all may be reached
    monkeypatch.delenv(OFF.ENV, raising=False)
    assert OFF.is_offline() is None                                 # connected: nothing switched on
    cfg = copy.deepcopy(C.load())
    if switch == "env":
        monkeypatch.setenv(OFF.ENV, "1")
    elif switch == "flag":
        OFF.activate(cfg, OFF.requested(cfg, flag=True))            # what every command does with --offline
    else:
        cfg["offline"] = True                                        # ai.yaml's key, nothing else
        OFF.activate(cfg, OFF.requested(cfg))
    assert OFF.is_offline(), switch
    _direct_builds_refused(OFF)
    assert guard.non_local() == [] and guard.processes == []


@pytest.mark.parametrize("switch", ["flag", "config"])
def test_r4_6_the_command_line_switches_the_whole_process_offline_before_any_command(switch, monkeypatch, tmp_path,
                                                                                      capsys):
    import copy

    import yaml

    from tenderpack.ai import config as C
    from tenderpack.ai import offline as OFF
    from tenderpack.cli import main
    monkeypatch.delenv(OFF.ENV, raising=False)
    cfg = copy.deepcopy(C.load())
    cfg["offline"] = switch == "config"
    cfgp = tmp_path / "ai.yaml"
    cfgp.write_text(yaml.safe_dump({k: v for k, v in cfg.items() if not k.startswith("_")}, sort_keys=False),
                    encoding="utf-8")
    # a command refused before it loads its configuration (an addendum id that is not ADD-NN)
    main(["ai", "quick-review", "not-an-addendum", "--config", str(cfgp)] + (["--offline"] if switch == "flag" else []))
    capsys.readouterr()
    assert OFF.is_offline(), switch
    _direct_builds_refused(OFF)


# ---------------------------------------------------------------------------------------------- R4-11


def _image_table(title: str, gid: str = "ADD-02:p2-image"):
    """A synthetic addendum table read from an image (its id is not 'T<number>'), its title as printed."""
    from test_session14_add03_ops import U
    return [U(gid, title, kind="table", page=2),
            U(f"{gid}/r1", "م: ١ | الفئة: مدني | السنوات: ٢٠", kind="table_row", page=2, parent=gid,
              cells={"م": "١", "السنوات": "٢٠"}),
            U(f"{gid}/r2", "م: ٢ | الفئة: ميكانيكي | السنوات: ٥", kind="table_row", page=2, parent=gid,
              cells={"م": "٢", "السنوات": "٥"})]


@pytest.mark.parametrize("title", [
    "Table 50-1: Minimum residual life (session 14 test data)",                    # Latin words, Latin digits
    "Table ٥٠-١: Minimum residual life (session 14 test data)",                    # Latin words, Arabic-Indic digits
    "جدول ٥٠-١: الحد الأدنى للعمر المتبقي",                                         # Arabic words, Arabic-Indic digits
    "الجدول رقم ٥٠-١ - الحد الأدنى للعمر المتبقي",                                  # with the article and 'رقم'
    "جدول 50-1: الحد الأدنى للعمر المتبقي",                                          # Arabic words, Latin digits
    "جدول ۵۰-۱: الحد الأدنى للعمر المتبقي",                                          # Extended Arabic-Indic digits
])
def test_r4_11_insert_table_finds_its_table_whichever_digits_print_the_number(title):
    from test_session14_add03_ops import P_TABLE, failed, res, run

    from tenderpack.amend import Op
    for number in ("50-1", "٥٠-١"):                         # the op names it in Latin digits (or as printed)
        op = Op(id="ADD-02/4.1", provision="ADD-02:4.1", type="insert_table", new_group="ADD-02:p2-image",
                into="VOL-V", number=number)
        by, _ = run([P_TABLE] + _image_table(title), [op])
        x = res(by, "ADD-02/4.1")
        assert x.applied, (title, number, failed(x))
        assert x.details["inserted_as"] == "VOL-V:T50-1" and x.details["number"] == "50-1", x.details
        assert all(by["ADD-02"].state[k].part_of == "VOL-V" for k in ("ADD-02:p2-image", "ADD-02:p2-image/r1"))


@pytest.mark.parametrize("title", ["جدول ٥٠-٢: الحد الأدنى للعمر المتبقي", "Table ٥٠-١٢: Minimum residual life",
                                   "جدول ١٥٠-١: الحد الأدنى للعمر المتبقي", "الحد الأدنى للعمر المتبقي ٥٠-١"])
def test_r4_11_insert_table_still_refuses_a_table_titled_with_another_number_or_no_table_word(title):
    from test_session14_add03_ops import P_TABLE, failed, res, run

    from tenderpack.amend import Op
    op = Op(id="ADD-02/4.1", provision="ADD-02:4.1", type="insert_table", new_group="ADD-02:p2-image", into="VOL-V",
            number="50-1")
    by, _ = run([P_TABLE] + _image_table(title), [op])
    x = res(by, "ADD-02/4.1")
    assert not x.valid and any("is not Table 50-1" in c["detail"] for c in failed(x)), (title, failed(x))
    assert by["ADD-02"].state["ADD-02:p2-image"].part_of is None
