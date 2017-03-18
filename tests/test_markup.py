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


def test_xterm_color():
	assert p('<fg 200>1</fg 200>') == '\x1b[38;5;200m' '1' '\x1b[0m'
	assert p('<bg 100><fg 200>1')  == '\x1b[48;5;100m' '\x1b[38;5;200m' '1'
	assert p('<fg 256>1')          == '<fg 256>1'


def test_xterm_hex():
	assert p('<fg #ff0000>1') == '\x1b[38;2;255;0;0m' '1'
	assert p('<bg #00A000><fg #ff0000>1') == '\x1b[48;2;0;160;0m' '\x1b[38;2;255;0;0m' '1'


def test_xterm_rgb():
	assert p('<fg 255,0,0>1') == p('<fg #ff0000>1') == '\x1b[38;2;255;0;0m' '1'
	assert p('<bg 0,160,0><fg 255,0,0>1') == p('<bg #00A000><fg #ff0000>1') == '\x1b[48;2;0;160;0m' '\x1b[38;2;255;0;0m' '1'


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


def test_usertags():
	user_tags = {
		'info':  F.GREEN + S.BRIGHT,
		'info1': p('<g><b>'),
		'call': lambda: F.BLUE + B.RED
	}
	am = AnsiMarkup(tags=user_tags)

	assert am.parse('<info>1</info>') == F.GREEN + S.BRIGHT + '1' + S.RESET_ALL
	assert am.parse('<info>1</info>') == am.parse('<info1>1</info1>')
	assert am.parse('<call>1</call>') == F.BLUE  + B.RED + '1' + S.RESET_ALL


def test_tag_chars():
	with raises(ValueError):
		am = AnsiMarkup(tag_sep='{')

	with raises(ValueError):
		am = AnsiMarkup(tag_sep='qq')

	am = AnsiMarkup(tag_sep='{}')

	r1 = p('0<b>1<d>2</d>3</b>4')
	r2 = am.parse('0{b}1{d}2{/d}3{/b}4')
	assert r1 == r2 == '0' + S.BRIGHT + '1' + S.DIM + '2' + S.RESET_ALL + S.BRIGHT + '3' + S.RESET_ALL + '4'

@mark.xfail
def test_limitations():
	assert p('<r><Y>1</r>2</Y>') == F.RED + B.YELLOW + '1' + S.RESET_ALL + B.YELLOW + '2' + S.RESET_ALL
