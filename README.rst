Ansimarkup
==========

.. class:: no-web no-pdf

|pypi| |build|


Ansimarkup is an XML-like markup for producing colored terminal text.


.. code-block:: python

  from ansimarkup import ansiprint as print

  print('<b>bold text</b>'))
  print('<red>red text</red>', '<red,green>red text on a green background</red,green>')


Installation
------------

The latest stable version of ansimarkup can be installed from pypi:

.. code-block:: bash

  $ pip install ansimarkup


Usage
-----

An annotated usage example:

.. code-block:: python

  from ansimarkup import parse, ansiprint

  # parse() converts the tags to the corresponding ansi escape codes.
  parse("<b>bold</b> <d>dim</d>")

  # ansiprint() works exactly like print(), but first runs parse() on all arguments.
  ansiprint("<b>bold</b>", "<d>dim</d>")
  ansiprint("<b>bold</b>", "<d>dim</d>", sep=':', file=sys.stderr)

  # Colors may be specified in one of several ways.
  parse("<red>red foreground</red>")
  parse("<RED>red background</RED>")
  parse("<fg red>red foreground</fg red>")
  parse("<bg red>red background</bg red>")

  # Tags may be nested.
  parse("<r><Y>red text on a yellow foreground</Y></r>")

  # The above may be more concisely written as:
  parse("<r,y>red text on a yellow background</r,y>")

  # This shorthand also supports style tags.
  parse("<b,r,y>bold red text on a yellow background</b,r,y>"
  parse("<b,r,>bold red text</b,r,>
  parse("<b,,y>bold regular text on a yellow background</b,,y>

  # Unrecognized tags are left as-is.
  parse("<b><element1></element1></b>")

For a list of markup tags, please refer to `tags.py`_.

Ansimarkup may also be used as a command-line script::

  $ python -m ansimarkup "<b>bold</b>" "<red>red</red>"


Ansimarkup uses the colorama_ library internally, which means that Windows
support for ansi escape sequences is available by first running:

.. code-block:: python

  import colorama
  colorama.init()

For more information on Windows support, consult the "Usage" section of the
colorama_ documentation.

Limitations
-----------

Ansimarkup is a simple wrapper around colorama. It does very little in the way
of validating that markup strings are valid. This is a conscious decision with
the goal of keeping things simple and fast.

Unbalanced nesting, such as in the following example, will produce incorrect
output::

  <r><Y>1</r>2</Y>


License
-------

Ansimarkup is released under the terms of the `Revised BSD License`_.


.. |pypi| image:: https://img.shields.io/pypi/v/ansimarkup.svg?style=flat-square&label=latest%20stable%20version
    :target: https://pypi.python.org/pypi/ansimarkup
    :alt: Latest version released on PyPi

.. |build| image:: https://img.shields.io/travis/gvalkov/python-ansimarkup/master.svg?style=flat-square&label=build
    :target: http://travis-ci.org/gvalkov/python-ansimarkup
    :alt: Build status

.. _tags.py:   https://github.com/gvalkov/python-ansimarkup/blob/master/ansimarkup/tags.py
.. _colorama:  https://pypi.python.org/pypi/colorama
.. _`Revised BSD License`: https://raw.github.com/gvalkov/python-ansimarkup/master/LICENSE
