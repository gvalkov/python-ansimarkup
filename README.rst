Ansimarkup
==========

.. class:: no-web no-pdf

|pypi| |build| |license|


Ansimarkup is an XML-like markup for producing colored terminal text.


.. code-block:: python

  from ansimarkup import ansiprint as print

  print("<b>bold text</b>"))
  print("<red>red text</red>", "<red,green>red text on a green background</red,green>")
  print("<fg #ffaf00>orange text</fg #ffaf00>")


Installation
------------

The latest stable version of ansimarkup can be installed from pypi:

.. code-block:: bash

  $ pip install ansimarkup


Usage
-----

Basic
~~~~~

.. code-block:: python

  from ansimarkup import parse, ansiprint

  # parse() converts the tags to the corresponding ansi escape sequence.
  parse("<b>bold</b> <d>dim</d>")

  # ansiprint() works exactly like print(), but first runs parse() on all arguments.
  ansiprint("<b>bold</b>", "<d>dim</d>")
  ansiprint("<b>bold</b>", "<d>dim</d>", sep=":", file=sys.stderr)


Colors and styles
~~~~~~~~~~~~~~~~~

.. code-block:: python

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

For a list of markup tags, please refer to `tags.py`_.


User-defined tags
~~~~~~~~~~~~~~~~~

Custom tags or overrides for existing tags may be defined by creating a new
``AnsiMarkup`` instance:

.. code-block:: python

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


Other features
~~~~~~~~~~~~~~

The default tag separators can be changed by passing the ``tag_sep`` argument to
``AnsiMarkup``:


.. code-block:: python

  from ansimarkup import AnsiMarkup

  am = AnsiMarkup(tag_sep="{}")
  am.parse("{b}{r}bold red{/b}{/r}")

Markup tags can be removed using the ``strip()`` method:

.. code-block:: python

  from ansimarkup import AnsiMarkup

  am = AnsiMarkup()
  am.strip("<b><r>bold red</b></r>")

Command-line
~~~~~~~~~~~~

Ansimarkup may also be used as a command-line script. This works as if all
arguments were passed to ``ansiprint()``::

  $ python -m ansimarkup "<b>bold</b>" "<red>red</red>"


Logging formatter
~~~~~~~~~~~~~~~~~

Ansimarkup also comes with a formatter for the standard library `logging`
module. It can be used as:

.. code-block:: python

  import logging
  from ansimarkup.logformatter import AnsiMarkupFormatter

  log = logging.getLogger()
  hdl = logging.StreamHandler()
  fmt = AnsiMarkupFormatter()
  hdl.setFormatter(fmt)
  log.addHandler(hdl)

  log.info("<b>bold text</b>")


Windows
~~~~~~~

Ansimarkup uses the colorama_ library internally, which means that Windows
support for ansi escape sequences is available by first running:

.. code-block:: python

  import colorama
  colorama.init()

For more information on Windows support, consult the "Usage" section of the
colorama_ documentation.


Performance
-----------

While the focus of ansimarkup is convenience, it does try to keep processing to
a minimum. The `benchmark.py`_ script attempts to benchmark different ansi
escape code libraries::

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


Limitations
-----------

Ansimarkup is a simple wrapper around colorama. It does very little in the way
of validating that markup strings are well-formed. This is a conscious decision
with the goal of keeping things simple and fast.

Unbalanced nesting, such as in the following example, will produce incorrect
output::

  <r><Y>1</r>2</Y>


Todo
----

- Many corner cases remain to be fixed.

- More elaborate testing. The current test suite mostly covers the
  "happy paths".

- Replace ``tag_list.index`` in ``sub_end`` with something more
  efficient (i.e. something like an ordered MultiDict).


Similar libraries
-----------------

- pastel_: bring colors to your terminal
- `plumbum.colors`_: small yet feature-rich library for shell script-like programs in Python
- colr_: easy terminal colors, with chainable methods


License
-------

Ansimarkup is released under the terms of the `Revised BSD License`_.


.. |pypi| image:: https://img.shields.io/pypi/v/ansimarkup.svg?style=flat-square&label=latest%20stable%20version
    :target: https://pypi.python.org/pypi/ansimarkup
    :alt: Latest version released on PyPi

.. |license| image:: https://img.shields.io/pypi/l/ansimarkup.svg?style=flat-square&label=license
    :target: https://pypi.python.org/pypi/ansimarkup
    :alt: BSD 3-Clause

.. |build| image:: https://img.shields.io/travis/gvalkov/python-ansimarkup/master.svg?style=flat-square&label=build
    :target: http://travis-ci.org/gvalkov/python-ansimarkup
    :alt: Build status


.. _tags.py:        https://github.com/gvalkov/python-ansimarkup/blob/master/ansimarkup/tags.py
.. _benchmark.py:   https://github.com/gvalkov/python-ansimarkup/blob/master/tests/benchmark.py

.. _colorama:       https://pypi.python.org/pypi/colorama
.. _pastel:         https://github.com/sdispater/pastel
.. _plumbum.colors: https://plumbum.readthedocs.io/en/latest/cli.html#colors
.. _colr:           https://pypi.python.org/pypi/Colr/
.. _`Revised BSD License`: https://raw.github.com/gvalkov/python-ansimarkup/master/LICENSE
