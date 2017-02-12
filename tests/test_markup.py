# flake8: noqa

from pytest import raises, mark
from colorama import Style as S, Fore as F, Back as B

from ansimarkup import *
from ansimarkup import parse as p


def test_flat():
	assert p('<b>1</b>') == p('<bold>1</bold>') == S.BRIGHT + '1' + S.RESET_ALL
	assert p('<d>1</d>') == p('<dim>1</dim>')   == S.DIM    + '1' + S.RESET_ALL

	assert p('<b>1</b><d>2</d>')  == S.BRIGHT + '1' + S.RESET_ALL    +    S.DIM + '2' + S.RESET_ALL
	assert p('<b>1</b>2<d>3</d>') == S.BRIGHT + '1' + S.RESET_ALL + '2' + S.DIM + '3' + S.RESET_ALL


def test_flat_colors():
	assert p('<r>1</r>') == p('<red>1</red>') == p('<fg red>1</fg red>') == F.RED + '1' + S.RESET_ALL
	assert p('<R>1</R>') == p('<RED>1</RED>') == p('<bg red>1</bg red>') == B.RED + '1' + S.RESET_ALL

	assert p('<r,y>1</r,y>') == p('<red,yellow>1</red,yellow>') == F.RED + B.YELLOW + '1' + S.RESET_ALL
	assert p('<b,r,y>1</b,r,y>') == p('<bold,red,yellow>1</bold,red,yellow>') == S.BRIGHT + F.RED + B.YELLOW + '1' + S.RESET_ALL
	assert p('<b,r,>1</b,r,>') == p('<bold,red,>1</bold,red,>') == S.BRIGHT + F.RED + '1' + S.RESET_ALL


def test_nested():
	assert p('0<b>1<d>2</d>3</b>4') == '0' + S.BRIGHT + '1' + S.DIM + '2' + S.RESET_ALL + S.BRIGHT + '3' + S.RESET_ALL + '4'


def test_errors():
	with raises(MismatchedTag):
		p('<b>1</d>')


def test_strip(am):
	assert am.strip('<b>1</b>2<d>3</d>') == '123'
	assert am.strip('<bold,red,yellow>1</bold,red,yellow>') == '1'


def test_options():
	am = AnsiMarkup(always_reset=True)
	am.parse('<b>1') == S.BRIGHT + '1' + S.RESET_ALL

	am = AnsiMarkup(always_reset=False)
	am.parse('<b>1') == S.BRIGHT + '1'


@mark.xfail
def test_limitations():
	assert p('<r><Y>1</r>2</Y>') == F.RED + B.YELLOW + '1' + S.RESET_ALL + B.YELLOW + '2' + S.RESET_ALL
