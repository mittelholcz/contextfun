#! /usr/bin/env python3

from itertools import repeat, chain


__all__ = ['contextual_filter', 'contextual_map']


def frameiter(iterable, size, fake=None, before=0, after=0):
    """Iter over iterable with a frame (size).

    Parameters
    ----------
    iterable : iterable object
    size : int
        size of frame
    fake : object
        object to enhance iterable (default None)
    before : int
        number of fake items inserted before the iterable (default 0)
    after : int
        number of fake items inserted after the iterable (default 0)

    Yields
    ------
    tuple
        size length tuple of items from iterable
    """
    size = int(size)
    before = repeat(fake, before)
    after = repeat(fake, after)
    iterable = chain(before, iterable, after)
    frame = []
    for i in iterable:
        frame.append(i)
        if len(frame) == size:
            yield tuple(frame)
            frame.pop(0)


def contextual_filter(iterable, predicate, before=0, after=0, quantifier=all):
    """Filtering iterable based on contextual condition.

    Parameters
    ----------
    iterable : iterable object
    predicate : function
        function, applied to items of context
    before : int
        length of left side context (default 0)
    after : int
        length of right side context (default 0)
    quantifier : function
        quantifier function (default all)

    Yields
    ------
    object
        filtered items from iterable
    """
    size = int(before) + int(after) + 1
    fake = object()
    iterable = ((x, predicate(x)) for x in iterable)
    for i in frameiter(iterable, size, fake=fake, before=before, after=after):
        context = i[:before] + i[before+1:]
        context = (x[1] for x in context if x != fake)
        if quantifier(context):
            yield i[before][0]


def contextual_map(iterable, mapping, predicate, before=0, after=0, quantifier=all):
    """Mapping iterable based on contextual condition.

    Parameters
    ----------
    iterable : iterable object
    mapping : function
        function, applied to filtered items of iterable
    predicate : function
        function, applied to items of context
    before : int
        length of left side context (default 0)
    after : int
        length of right side context (default 0)
    quantifier : function
        quantifier function (default all)

    Yields
    ------
    object
        items from iterable
    """
    size = before + after + 1
    fake = object()
    iterable = ((x, predicate(x)) for x in iterable)
    for i in frameiter(iterable, size, fake=fake, before=before, after=after):
        context = i[:before] + i[before+1:]
        context = (x[1] for x in context if x != fake)
        if quantifier(context):
            yield mapping(i[before][0])
        else:
            yield i[before][0]
