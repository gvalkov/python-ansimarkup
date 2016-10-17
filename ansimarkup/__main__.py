from sys import argv, exit
from . import print_function


if len(argv) == 1:
    from textwrap import dedent
    usage = '''
    Usage: python -m ansimarkup <arg> [<arg> ...]

    Example usage:
      python -m ansimarkup '<b>Bold</b>' '<r>Red</r>'
      python -m ansimarkup '<b><r>Bold Red</r></b>'
    '''

    print(dedent(usage).strip())
    exit(0)
else:
    print_function(*argv[1:])
