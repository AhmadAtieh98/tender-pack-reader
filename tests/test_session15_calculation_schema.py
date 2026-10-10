import pytest
from tenderpack.ai import tools


def test_wrong_calculation_names_fail_before_opening_workspace_with_exact_arguments():
    with pytest.raises(tools.ToolError, match='of.*percent|percent.*of'):
        tools.call_tool(None, 'calculate', {'kind':'percentage_of','args':{'percentage':25,'total':80}})


def test_all_supported_calculations_have_an_exact_argument_shape():
    schema=tools.TOOLS['calculate'].input_schema
    branches={b['properties']['kind']['const']: b['properties']['args'] for b in schema['oneOf']}
    assert set(branches)==set(tools.CALC_KINDS)
    assert set(branches['percentage_of']['required'])=={'percent','of'}
    assert branches['add_working_days']['properties']['n']['type']=='integer'
    assert branches['relative_change']['properties']['direction']['enum']==['increase','decrease']
