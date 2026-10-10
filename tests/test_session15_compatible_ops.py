from tenderpack.amend import Op
from tenderpack.ai.controller import cross_item_conflicts


def op(ident, kind, **kw):
    return Op(id=ident, type=kind, provision='ADD-03:1', target='VOL-II:T/row', **kw)


def test_different_cells_of_one_row_can_change_together():
    a=op('A','set_value',column='limit',old='5',new='4')
    b=op('B','set_value',column='period',old='monthly',new='weekly')
    assert cross_item_conflicts([(0,a),(1,b)],[]) == {}


def test_same_cell_different_values_and_distinct_replacements_are_conflicts():
    a=op('A','set_value',column='limit',old='5',new='4')
    b=op('B','set_value',column='limit',old='5',new='3')
    assert set(cross_item_conflicts([(0,a),(1,b)],[])) == {0,1}
    a=op('A','replace_unit',replacement='ADD-03:T1')
    b=op('B','replace_unit',replacement='ADD-03:T2')
    assert set(cross_item_conflicts([(0,a),(1,b)],[])) == {0,1}


def test_append_and_independent_text_replacement_are_compatible():
    a=op('A','replace_text',old='thirty days',new='forty days')
    b=op('B','append_text',new='The bidder must submit a report.')
    assert cross_item_conflicts([(0,a),(1,b)],[],{'VOL-II:T/row':'Within thirty days.'}) == {}
    b=op('B','append_text',new='This thirty days period also applies.')
    assert set(cross_item_conflicts([(0,a),(1,b)],[],{'VOL-II:T/row':'Within thirty days.'})) == {0,1}
