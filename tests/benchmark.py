#!/usr/bin/env python

"""
Benchmark different terminal color libraries.

pip install termcolor colorama colr ansimarkup pastel plumbum
"""

from __future__ import print_function
from timeit import Timer


def benchmark(stmt, n=1000, r=3):
    setup = (
        "from ansimarkup import parse;"
        "from colorama import Style as S, Fore as F;"
        "from termcolor import colored;"
        "from colr import color;"
        "from plumbum import colors;"
        "from pastel import colorize"
    )
    timer = Timer(stmt, setup=setup)
    best = min(timer.repeat(r, n))

    usec = best * 1e6 / n
    return usec


def run_tests(title, tests):
    print(title)
    results = sorted((benchmark(v), k) for k, v in tests.items())
    for usec, name in results:
        print("  {:<12} {:01.4f} μs".format(name, usec))
    print()


tests_simple_1 = {
    "termcolor": 'colored("red bold", "red", attrs=["bold"])',
    "colorama": 'S.BRIGHT + F.RED + "red bold" + S.RESET_ALL',
    "colr": 'color("red bold", fore="red", style="bright")',
    "ansimarkup": 'parse("<r><b>red bold</b></r>")',
    "pastel": 'colorize("<fg=red;options=bold>red bold</>")',
    "plumbum": 'colors.red | colors.bold | "red bold"',
}

tests_simple_2 = {
    "termcolor": 'colored("red bold", "red", attrs=["bold"]) + colored("red", "red") + colored("bold", attrs=["bold"])',
    "colorama": 'S.BRIGHT + F.RED + "red bold" + S.RESET_ALL + F.RED + "red" + S.RESET_ALL + S.BRIGHT + "bold" + S.RESET_ALL',
    "colr": 'color("red bold", fore="red", style="bright") + color("red", fore="red") + color("bold", style="bright")',
    "ansimarkup": 'parse("<r><b>red bold</b>red</r><b>bold</b>")',
    "pastel": 'colorize("<fg=red;options=bold>red bold</><fg=red>red</><options=bold>red</>")',
    "plumbum": '(colors.red + colors.bold | "red bold") + (colors.red | "red") + (colors.bold | "bold")',
}

run_tests("Benchmark 1: <r><b>red bold</b></r>", tests_simple_1)
run_tests("Benchmark 2: <r><b>red bold</b>red</r><b>bold</b>", tests_simple_2)
