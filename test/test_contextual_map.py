import pytest
from contextfun import contextual_map


QUANTIFIERS = {
    'all': all,
    'any': any,
}


@pytest.fixture(params=QUANTIFIERS.keys())
def get_input(request):
    """return with input parameters for contextual_map()
    """
    quantifier = QUANTIFIERS[request.param]
    inp = {
        'iterable': 'aababcabcdaaabaabcaabcd',
        'mapping': lambda ch: 'x',
        'predicate': lambda ch: ch =='a',
        'quantifier': quantifier,
    }
    return inp



def test_empty_iterable(get_input):
    """testing with empty iterable
    """
    inp = get_input
    inp['iterable'] = ''
    inp['before'] = 2
    inp['after'] = 2
    out = ''.join(contextual_map(**inp))
    exp = ''
    assert out == exp


def test_empty_context(get_input):
    """testing with empty context
    """
    inp = get_input
    out = ''.join(contextual_map(**inp))
    exp = 'x' * len(inp['iterable']) # quantifier == all
    if inp['quantifier'] == any:
        exp = inp['iterable']
    assert out == exp


def test_empty_iterable_and_context(get_input):
    """testing with empty iterable and context
    """
    inp = get_input
    inp['iterable'] = ''
    out = ''.join(contextual_map(**inp))
    exp = ''
    assert out == exp


def test_before(get_input):
    """testing the "before" parameter
    """
    inp = get_input
    inp['before'] = 2
    out = ''.join(contextual_map(**inp))
    #     'aababcabcdaaabaabcaabcd'
    exp = 'xxxabcabcdaaxxaaxcaaxcd' # quantifier == all
    if inp['quantifier'] == any:
        #     'aababcabcdaaabaabcaabcd'
        exp = 'axxxxxaxxdaxxxxxxxaxxxd'
    assert out == exp


def test_after(get_input):
    """testing the "after" parameter
    """
    inp = get_input
    inp['after'] = 2
    out = ''.join(contextual_map(**inp))
    #     'aababcabcdaaabaabcaabcd'
    exp = 'aababcabcxxaaxaabxaabcx' # quantifier == all
    if inp['quantifier'] == any:
        #     'aababcabcdaaabaabcaabcd'
        exp = 'xxxaxxabxxxxxxxaxxxabcd'
    assert out == exp


def test_full(get_input):
    """testing with all parameter
    """
    inp = get_input
    inp['before'] = 2
    inp['after'] = 1
    out = ''.join(contextual_map(**inp))
    #     'aababcabcdaaabaabcaabcd'
    exp = 'xaxabcabcdaaaxaabcaabcd' # quantifier == all
    if inp['quantifier'] == any:
        #     'aababcabcdaaabaabcaabcd'
        exp = 'xxxxxxaxxxxxxxxxxxxxxxd'
    assert out == exp


def test_exceptions(get_input):
    """testing with wrong parameter types
    """
    inp = get_input
    # non iterable
    with pytest.raises(TypeError):
        myinp = dict(inp)
        myinp['iterable'] = None
        list(contextual_map(**myinp))
    # non integer context
    with pytest.raises(TypeError):
        myinp = dict(inp)
        myinp['before'] = None
        list(contextual_map(**myinp))
    # non integer context
    with pytest.raises(TypeError):
        myinp = dict(inp)
        myinp['after'] = 'None'
        list(contextual_map(**myinp))
    # non callable map mapping
    with pytest.raises(TypeError):
        myinp = dict(inp)
        myinp['mapping'] = None
        myinp['after'] = 1
        list(contextual_map(**myinp))
    # non callable predicate
    with pytest.raises(TypeError):
        myinp = dict(inp)
        myinp['predicate'] = None
        myinp['after'] = 1
        list(contextual_map(**myinp))
    # non callable quantifier
    with pytest.raises(TypeError):
        myinp = dict(inp)
        myinp['quantifier'] = None
        myinp['after'] = 1
        list(contextual_map(**myinp))