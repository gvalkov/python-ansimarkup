from pytest import fixture
from ansimarkup import AnsiMarkup


@fixture()
def am():
    return AnsiMarkup()
