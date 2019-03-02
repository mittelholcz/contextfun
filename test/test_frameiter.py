import pytest
from contextfun.main import frameiter


DATA = range(5)

EXP = [
    [], [], [], [],
    [(0,), (1,), (2,), (3,), (4,)],
    [(0, 1), (1, 2), (2, 3), (3, 4)],
    [(0, 1, 2), (1, 2, 3), (2, 3, 4)],
    [(0, 1, 2, 3), (1, 2, 3, 4)],
    [(0, 1, 2, 3, 4)],
    [], [], [], [],
]

STREXP = [[tuple([str(x) for x in tup]) for tup in group] for group in EXP]

PAIRS = {
    'range': (DATA, EXP),
    'list': (list(DATA), EXP),
    'tuple': (tuple(DATA), EXP),
    'set': (set(DATA), EXP),
    'dict': ({x:x for x in DATA}, EXP),
    'str': (''.join([str(x) for x in DATA]), STREXP),
}


@pytest.fixture(params=PAIRS.keys())
def get_pairs(request):
    """return with pairs of input and expected output
    """
    pair = PAIRS[request.param]
    return pair


def test_empty():
    """testing with empty iterable
    """
    inp = range(0)
    outs =  [list(frameiter(inp, size)) for size in range(-3, 10)]
    for out in outs:
        assert out == []


def test_size(get_pairs):
    """testing "size" parameter in -3..9 range
    """
    inp, exps = get_pairs
    outs =  [list(frameiter(inp, size)) for size in range(-3, 10)]
    for out, exp in zip(outs, exps):
        assert out == exp


def test_before():
    """testing the "before" parameter
    """
    inp = DATA
    out = list(frameiter(inp, 3, before=2))
    exp = [
        (None, None, 0),
        (None, 0, 1),
        (0, 1, 2),
        (1, 2, 3),
        (2, 3, 4),
    ]
    assert out == exp


def test_after():
    """testing the "after" parameter
    """
    inp = DATA
    out = list(frameiter(inp, 3, after=2))
    exp = [
        (0, 1, 2),
        (1, 2, 3),
        (2, 3, 4),
        (3, 4, None),
        (4, None, None),
    ]
    assert out == exp


def test_fake():
    """testing with custom fake element
    """
    inp = DATA
    out = list(frameiter(inp, 3, fake='X', after=2))
    exp = [
        (0, 1, 2),
        (1, 2, 3),
        (2, 3, 4),
        (3, 4, 'X'),
        (4, 'X', 'X'),
    ]
    assert out == exp


def test_full():
    """use all parameters
    """
    inp = DATA
    out = list(frameiter(inp, 3, fake='X', before=1, after=1))
    exp = [
        ('X', 0, 1),
        (0, 1, 2),
        (1, 2, 3),
        (2, 3, 4),
        (3, 4, 'X'),
    ]
    assert out == exp


def test_exceptions():
    """testing with wrong parameter types
    """
    # non iterable
    with pytest.raises(TypeError):
        list(frameiter(None, 2))
    # non integer size
    with pytest.raises(ValueError):
        list(frameiter(None, 'x'))
    # non integer before
    with pytest.raises(TypeError):
        list(frameiter(range(5), 2, before='x'))
    # non integer after
    with pytest.raises(TypeError):
        list(frameiter(range(5), 2, after='x'))