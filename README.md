# Contextfun

[![license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/mittelholcz/contextfun/blob/master/LICENSE)
[![pypi](https://img.shields.io/badge/pypi-0.7.0-blue.svg)](https://pypi.org/project/contextfun/)

The *contextfun* python package provides functions for context-based
filtering and mapping.

We can filter a list with the Python's own
[*filter()*](https://docs.python.org/3/library/functions.html#filter)
function, based on the properties of items.
For example, we can filter out prime numbers (`filter(is_prime, range(10))`).
But what if we are interested in numbers standing in the list before prime
numbers?
Or numbers that have at least two prime numbers in their three radius context?

Similarly, we can replace items in a list, based on their properties with
Python's own [*map()*](https://docs.python.org/3/library/functions.html#map>)
function. For example, we can replace prime numbers with zeros
(`map(lambda x: 0 if is_prime(x) else x, range(10))`).
But what if we want replace numbers standing in the list after prime numbers?
Or numbers that have at most three prime numbers in their context?

This package can help to resolve this problem with their *contextual_filter()* and
*contextual_map()* functions.

## 1 Install

You can install *contextfun* easily from PyPI:

```shell
pip install contextfun
```

## 2 Usage

### 2.1 Filtering

**contextual_filter**(*iterable, predicate, before=0, after=0, quantifier=all*)

With *contextual_filter* we can filter items of iterables based on their
context. The function returns a generator of the filtered items.

*iterable*:
The iterable to filter.

*predicate*:
A function which can be applied for items of the context. Its input is an
item of the *iterable*, its output is Boolean
(`predicate(obj: object) -> bool`).

The context can be defined with the parameters *before* and *after*.
The context of an item consists of the *before* items standing in the
iterable before it, and the *after* items following it.
The current item itself is never a part of its context.
The context is truncated at the beginning and the end of the iterable.
For example, the -1, +2 context (`before=1, after=2`) of the items in the
list `[1, 2, 3, 4, 5]` are

    1: (2, 3)
    2: (1, 3, 4)
    3: (2, 4, 5)
    4: (3, 5)
    5: (4)

*quantifier*:
This parameter allows you to specify the part of the context for which the
*predicate* should be true.
Default is Python's own
[*all*](https://docs.python.org/3/library/functions.html#all) function.
In this case, the *predicate* should be true for all items of the context.
You can also choose the
[*any*](https://docs.python.org/3/library/functions.html#any) function from the
built-in functions.
According to this, the *predicate* must be true for at least one item of the
context.

You can also write your own custom function with the following restrictions:
(1) The only parameter of the function is the
`(predicate(x) for x in context)` generator, and
(2) the return value should be Boolean.
For example, the 'up to two' can be represented as
`lambda context: sum((1 for x in context if x)) <= 2`.

Remark: The default behavior (`quantifier=all`) may seem strange for empty
contexts, e.g.

```python
>>> for i in contextual_filter([1], lambda x: x%5==0, after=2):
...     print(i)
1
```

This is not a bug but follows the principles of predicate logic
(see [vacuous truth](https://en.wikipedia.org/wiki/Vacuous_truth)).

### 2.2 Mapping

**contextual_map**(*iterable, mapping, predicate, before=0, after=0, quantifier=all*)

With *contextual_map* you can map an iterable based on the context of its
items. This function returns a generator of the mapped iterable.

The parameters are the same as that of *contextual_filter()*
except the *mapping* parameter. It should be callable and will
be applied for the items of the iterable if its context fulfils the conditions
represented by *predicate* and *quantifier*.

### 2.3 Examples

Look for words in a text after 'the':

```python
>>> from contextfun import contextual_filter
>>> text = '''Alright but apart from the sanitation the medicine education
... wine public order irrigation roads the fresh-water system and public
... health what have the Romans ever done for us?'''.split()
>>> pred = lambda word: word == 'the'
>>> for word in contextual_filter(text, pred, before=1, quantifier=any):
...     print(word)
sanitation
medicine
fresh-water
Romans
```

Highlight the words after the word 'the' in a text:

```python
>>> from contextfun import contextual_map
>>> highlighter = lambda word: f'<b>{word}</b>'
>>> words = contextual_map(text, highlighter, pred, before=1, quantifier=any)
>>> ' '.join(words)
'Alright but apart from the <b>sanitation</b> the <b>medicine</b> education wine public order irrigation roads the <b>fresh-water</b> system and public health what have the <b>Romans</b> ever done for us?'
```

## 3 Development setup

Requirements:

* bash
* make
* python3.7
* [pipenv](https://pipenv.readthedocs.io/en/latest/)

Install other development dependencies:

```shell
make dev
```

Run automated test-suite:

```shell
make test
```

## 4 Release history

* 0.5.0
  * Work in progress
* 0.6.0
  * initial release
* 0.6.1
  * updated readme
* 0.7.0
  * performance improvement

## 5 Acknowledgments

* [@dlazesz](https://github.com/dlazesz)
* [@esztersimon](https://github.com/esztersimon)
* [@sassbalint](https://github.com/sassbalint)
