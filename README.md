# Ansimarkup

<p>
    <a href="https://pypi.python.org/pypi/ansimarkup"><img alt="pypi version" src="https://img.shields.io/pypi/v/ansimarkup.svg"></a>
    <a href="https://github.com/gvalkov/python-ansimarkup/actions/workflows/tests.yml?query=branch:main"><img alt="Build status" src="https://img.shields.io/github/actions/workflow/status/gvalkov/python-ansimarkup/tests.yml?branch=main"></a>
    <a href="https://github.com/gvalkov/python-ansimarkup/blob/main/LICENSE.txt"><img alt="License" src="https://img.shields.io/pypi/l/ansimarkup"></a>
</p>

Ansimarkup is an XML-like markup for producing colored terminal text.

``` python
from ansimarkup import ansiprint as print

print("<b>bold text</b>"))
print("<red>red text</red>", "<red,green>red text on a green background</red,green>")
print("<fg #ffaf00>orange text</fg #ffaf00>")
```

## Installation

The latest stable version of ansimarkup can be installed from PyPi:

``` bash
python3 -m pip install ansimarkup
```

## Usage

### Basic

``` python
from ansimarkup import parse, ansiprint

# parse() converts the tags to the corresponding ansi escape sequence.
parse("<b>bold</b> <d>dim</d>")

# ansiprint() works exactly like print(), but first runs parse() on all arguments.
ansiprint("<b>bold</b>", "<d>dim</d>")
ansiprint("<b>bold</b>", "<d>dim</d>", sep=":", file=sys.stderr)
```

### Colors and styles

``` python
# Colors may be specified in one of several ways.
parse("<red>red foreground</red>")
parse("<RED>red background</RED>")
parse("<fg red>red foreground</fg red>")
parse("<bg red>red background</bg red>")

# Xterm, hex and rgb colors are accepted by the <fg> and <bg> tags.
parse("<fg 86>aquamarine foreground</fg 86>")
parse("<bg #00005f>dark blue background</bg #00005f>")
parse("<fg 0,95,0>dark green foreground</fg 0,95,0>")

# Tags may be nested.
parse("<r><Y>red text on a yellow foreground</Y></r>")

# The above may be more concisely written as:
parse("<r,y>red text on a yellow background</r,y>")

# This shorthand also supports style tags.
parse("<b,r,y>bold red text on a yellow background</b,r,y>")
parse("<b,r,>bold red text</b,r,>")
parse("<b,,y>bold regular text on a yellow background</b,,y>")

# Unrecognized tags are left as-is.
parse("<b><element1></element1></b>")
```

For a list of markup tags, please refer to [tags.py].

### User-defined tags

Custom tags or overrides for existing tags may be defined by creating a
new `AnsiMarkup` instance:

``` python
from ansimarkup import AnsiMarkup, parse

user_tags = {
    # Add a new tag (e.g. we want <info> to expand to "<bold><green>").
    "info": parse("<b><g>")

    # The ansi escape sequence can be used directly.
    "info": "e\x1b[32m\x1b[1m",

    # Tag names may also be callables.
    "err":  lambda: parse("<r>")

    # Colors may also be given convenient tag names.
    "orange": parse("<fg #d78700>"),

    # User-defined tags always take precedence over existing tags.
    "bold": parse("<dim>")
}

am = AnsiMarkup(tags=user_tags)

am.parse("<info>bold green</info>")
am.ansiprint("<err>red</err>")

# Calling the instance is equivalent to calling its parse method.
am("<b>bold</b>") == am.parse("<b>bold</b>")
```

### Alignment and length

Aligning formatted strings can be challenging because the length of the
rendered string is different that the number of printable characters.
Consider this example:

``` python
>>> a = '| {:30} |'.format('abc')
>>> b = '| {:30} |'.format(parse('<b>abc</b>'))
>>> print(a, b, sep='\n')
| abc                    |
| abc                            |
```

This can be addressed by using the `ansistring` function or the
`AnsiMarkup.string(markup)` method, which has the following useful
properties:

``` python
>>> s = ansistring('<b>abc</b>')
>>> print(repr(s), '->', s)
<b>abc</b> -> abc  # abc is printed in bold
>>> len(s), len(am.parse('<b>abc</b>'), s.delta
3, 11, 8
```

With the help of the `delta` property, it is easy to align the strings
in the above example:

``` python
>>> s = ansistring('<b>abc</b>')
>>> a = '| {:{width}} |'.format('abc', width=30)
>>> b = '| {:{width}} |'.format(s, width=(30 + s.delta))
>>> print(a, b, sep='\n')
| abc                            |
| abc                            |
```

### Other features

The default tag separators can be changed by passing the `tag_sep`
argument to `AnsiMarkup`:

``` python
from ansimarkup import AnsiMarkup

am = AnsiMarkup(tag_sep="{}")
am.parse("{b}{r}bold red{/b}{/r}")
```

Markup tags can be removed using the `strip()` method:

``` python
from ansimarkup import AnsiMarkup

am = AnsiMarkup()
am.strip("<b><r>bold red</b></r>")
```

The `strict` option instructs the parser to raise `MismatchedTag` if
opening tags don\'t have corresponding closing tags:

``` python
from ansimarkup import AnsiMarkup

am = AnsiMarkup(strict=True)
am.parse("<r><b>bold red")
# ansimarkup.MismatchedTag: opening tag "<r>" has no corresponding closing tag
```

### Command-line

Ansimarkup may also be used on the command-line. This works as if all
arguments were passed to `ansiprint()`:

    $ python -m ansimarkup
    Usage: python -m ansimarkup [<arg> [<arg> ...]]

    Example usage:
      python -m ansimarkup '<b>Bold</b>' '<r>Red</r>'
      python -m ansimarkup '<b><r>Bold Red</r></b>'
      python -m ansimarkup < input-with-markup.txt
      echo '<b>Bold</b>' | python -m ansimarkup

### Logging formatter

Ansimarkup also comes with a formatter for the standard library `logging` module. It can be used as:

``` python
import logging
from ansimarkup.logformatter import AnsiMarkupFormatter

log = logging.getLogger()
hdl = logging.StreamHandler()
fmt = AnsiMarkupFormatter()
hdl.setFormatter(fmt)
log.addHandler(hdl)

log.info("<b>bold text</b>")
```

### Windows

Ansimarkup uses the [colorama] library internally, which means that
Windows support for ansi escape sequences is available by first running:

``` python
import colorama
colorama.init()
```

For more information on Windows support, consult the \"Usage\" section
of the [colorama] documentation.

## Performance

While the focus of ansimarkup is convenience, it does try to keep
processing to a minimum. The [benchmark.py] script attempts to benchmark
different ansi escape code libraries:

    Benchmark 1: <r><b>red bold</b></r>
      colorama     0.2998 μs
      termcolor    3.2339 μs
      colr         3.6483 μs
      ansimarkup   6.8679 μs
      pastel       28.8538 μs
      plumbum      53.5004 μs

    Benchmark 2: <r><b>red bold</b>red</r><b>bold</b>
      colorama     0.8269 μs
      termcolor    8.9296 μs
      ansimarkup   9.3099 μs
      colr         9.6244 μs
      pastel       62.2018 μs
      plumbum      120.8048 μs

## Limitations

Ansimarkup is a simple wrapper around [colorama]. It does very little in
the way of validating that markup strings are well-formed. This is a
conscious decision with the goal of keeping things simple and fast.

Unbalanced nesting, such as in the following example, will produce
incorrect output:

    <r><Y>1</r>2</Y>

## Todo

-   Many corner cases remain to be fixed.
-   More elaborate testing. The current test suite mostly covers the \"happy paths\".
-   Replace `tag_list.index` in `sub_end` with something more efficient (i.e. something like an ordered MultiDict).

## Similar libraries

-   [pastel][]: bring colors to your terminal
-   [plumbum.colors][]: small yet feature-rich library for shell script-like programs in Python
-   [colr][]: easy terminal colors, with chainable methods

## License

Ansimarkup is released under the terms of the [Revised BSD License].

  [tags.py]: https://github.com/gvalkov/python-ansimarkup/blob/main/ansimarkup/tags.py
  [colorama]: https://pypi.python.org/pypi/colorama
  [benchmark.py]: https://github.com/gvalkov/python-ansimarkup/blob/main/tests/benchmark.py
  [pastel]: https://github.com/sdispater/pastel
  [plumbum.colors]: https://plumbum.readthedocs.io/en/latest/cli.html#colors
  [colr]: https://pypi.python.org/pypi/Colr/
  [Revised BSD License]: https://github.com/gvalkov/python-ansimarkup/blob/main/LICENSE.txt
