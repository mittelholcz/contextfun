import pytest
from contextfun import contextual_filter


QUANTIFIERS = {
    'all': all,
    'any': any,
}


@pytest.fixture(params=QUANTIFIERS.keys())
def get_input(request):
    """return with input parameters for contextual_filter()
    """
    quantifier = QUANTIFIERS[request.param]
    inp = {
        'iterable': 'aababcabcdaaabaabcaabcd',
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
    out = ''.join(contextual_filter(**inp))
    exp = ''
    assert out == exp


def test_empty_context(get_input):
    """testing with empty context
    """
    inp = get_input
    out = ''.join(contextual_filter(**inp))
    exp = inp['iterable'] # quantifier == all
    if inp['quantifier'] == any:
        exp = ''
    assert out == exp


def test_empty_iterable_and_context(get_input):
    """testing with empty iterable and context
    """
    inp = get_input
    inp['iterable'] = ''
    out = ''.join(contextual_filter(**inp))
    exp = ''
    assert out == exp


def test_before(get_input):
    """testing the "before" parameter
    """
    inp = get_input
    inp['before'] = 2
    out = ''.join(contextual_filter(**inp))
    #     'aababcabcdaaabaabcaabcd'
    exp = 'aababbb' # quantifier == all
    if inp['quantifier'] == any:
        #     'aababcabcdaaabaabcaabcd'
        exp = 'ababcbcaabaabcabc'
    assert out == exp


def test_after(get_input):
    """testing the "after" parameter
    """
    inp = get_input
    inp['after'] = 2
    out = ''.join(contextual_filter(**inp))
    #     'aababcabcdaaabaabcaabcd'
    exp = 'dabcd' # quantifier == all
    if inp['quantifier'] == any:
        #     'aababcabcdaaabaabcaabcd'
        exp = 'aabbccdaaababca'
    assert out == exp


def test_full(get_input):
    """testing with all parameter
    """
    inp = get_input
    inp['before'] = 2
    inp['after'] = 1
    out = ''.join(contextual_filter(**inp))
    #     'aababcabcdaaabaabcaabcd'
    exp = 'abb' # quantifier == all
    if inp['quantifier'] == any:
        #     'aababcabcdaaabaabcaabcd'
        exp = 'aababcbcdaaabaabcaabc'
    assert out == exp


def test_exceptions(get_input):
    """testing with wrong parameter types
    """
    inp = get_input
    # non iterable
    with pytest.raises(TypeError):
        myinp = dict(inp)
        myinp['iterable'] = None
        list(contextual_filter(**myinp))
    # non integer context
    with pytest.raises(TypeError):
        myinp = dict(inp)
        myinp['before'] = None
        list(contextual_filter(**myinp))
    # non integer context
    with pytest.raises(ValueError):
        myinp = dict(inp)
        myinp['after'] = 'None'
        list(contextual_filter(**myinp))
    # non callable predicate
    with pytest.raises(TypeError):
        myinp = dict(inp)
        myinp['predicate'] = None
        myinp['after'] = 1
        list(contextual_filter(**myinp))
    # non callable quantifier
    with pytest.raises(TypeError):
        myinp = dict(inp)
        myinp['quantifier'] = None
        myinp['after'] = 1
        list(contextual_filter(**myinp))