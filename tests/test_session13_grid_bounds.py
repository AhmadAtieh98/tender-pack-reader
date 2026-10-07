"""Session 13, E160 (the sealed blind-07 run, attempt 2): the grid detector took the letterhead's separator rule,
far above the table, as a table rule (8 horizontal rules = 7 rows), so the correct reading of the table (a header and
5 rows x 4 columns) was refused by RD3 and the run stopped at the readings step. A horizontal rule belongs to the
table only when vertical rules connect it to the next one: the table is the longest run of consecutive horizontal
rules whose bands are crossed by at least two vertical rules."""
from __future__ import annotations

import numpy as np

from tenderpack.regions import detect_grid


def _canvas(h: int = 1700, w: int = 1750) -> np.ndarray:
    return np.full((h, w), 255, dtype=np.uint8)


def _table(a: np.ndarray, y_lines: list[int], x_lines: list[int], thick: int = 3) -> None:
    for y in y_lines:
        a[y:y + thick, x_lines[0]:x_lines[-1] + thick] = 0
    for x in x_lines:
        a[y_lines[0]:y_lines[-1] + thick, x:x + thick] = 0


Y = [541, 678, 769, 859, 949, 1040, 1130]          # a header and 5 rows, as in the blind-07 image
X = [66, 391, 788, 1547, 1691]                     # 4 columns


def test_a_rule_above_the_table_is_not_a_table_rule():
    a = _canvas()
    a[230:233, 40:1700] = 0                        # the letterhead's separator rule (spans the width)
    _table(a, Y, X)
    g = detect_grid(a)
    assert (g.rows, g.cols) == (6, 4), (g.h_lines, g.v_lines)
    assert abs(g.h_lines[0] - 541) < 3 and abs(g.h_lines[-1] - 1130) < 3


def test_rules_below_and_above_the_table_are_not_table_rules():
    a = _canvas()
    a[120:123, 40:1700] = 0                        # a rule above
    _table(a, Y, X)
    a[1400:1403, 40:1700] = 0                      # a rule below (a footer line)
    g = detect_grid(a)
    assert (g.rows, g.cols) == (6, 4), (g.h_lines, g.v_lines)


def test_a_table_alone_is_unchanged():
    a = _canvas()
    _table(a, Y, X)
    g = detect_grid(a)
    assert (g.rows, g.cols) == (6, 4)
    assert [round(x) for x in g.h_lines] == [y + 1 for y in Y] and len(g.v_lines) == 5


def test_a_table_with_a_merged_caption_row_keeps_the_row():
    """A first row that spans every column (no vertical rule inside it) is still part of the table when the outer
    vertical rules bound it: the frame's two sides connect it to the next rule."""
    a = _canvas()
    y = [400] + Y
    _table(a, Y, X)
    a[400:403, X[0]:X[-1] + 3] = 0                 # the caption row's top rule
    a[400:541, X[0]:X[0] + 3] = 0                  # the frame's left side through the caption row
    a[400:541, X[-1]:X[-1] + 3] = 0                # and its right side
    g = detect_grid(a)
    assert (g.rows, g.cols) == (7, 4), (g.h_lines, g.v_lines)


def test_no_grid_without_vertical_rules():
    a = _canvas()
    for yy in (300, 500, 700):
        a[yy:yy + 3, 40:1700] = 0                  # three long rules, nothing connects them: not a table
    g = detect_grid(a)
    assert g.cols == 0 and g.rows <= 2             # rows are whatever the rules give; no table is claimed
