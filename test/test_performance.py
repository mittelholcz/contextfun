from contextfun import contextual_filter, contextual_map


class ExecutionCounterPredicate(object):
    def __init__(self):
        self.n = {}

    def __call__(self, x):
        self.n[x] = self.n.get(x, 0) + 1
        return True


def _predicate_called_once_per_item(f, **kwargs):
    span = 5
    iterable = [object() for i in range(span+1)]
    predicate = ExecutionCounterPredicate()
    list(f(iterable=iterable, predicate=predicate, before=span, **kwargs))
    assert predicate.n[iterable[0]] != span
    assert predicate.n[iterable[0]] == 1


def test_filter_calls_predicate_once_per_item():
    _predicate_called_once_per_item(contextual_filter)


def test_map_calls_predicate_once_per_item():
    _predicate_called_once_per_item(contextual_map, mapping=id)
