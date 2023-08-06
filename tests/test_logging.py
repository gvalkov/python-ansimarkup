# flake8: noqa

import io, sys
import logging

from pytest import raises, mark, fixture
from colorama import Style as S, Fore as F, Back as B

from ansimarkup.logformatter import AnsiMarkupFormatter
from ansimarkup import parse as p


class CaptureLogHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self, io.StringIO())
        self.records = []
        self.output = ""

        if sys.version_info < (3, 0):
            old_write = self.stream.write

            def write(data):
                data = unicode(data.encode("utf8"))
                old_write(data)

            self.stream.write = write

    def close(self):
        logging.StreamHandler.close(self)
        self.stream.close()

    def emit(self, record):
        self.records.append(record)
        logging.StreamHandler.emit(self, record)
        self.stream.flush()
        self.last_msg = self.stream.getvalue().splitlines()[-1]


@fixture
def caplog():
    log = logging.Logger("test")
    hdl = CaptureLogHandler()
    fmt = AnsiMarkupFormatter()

    hdl.setFormatter(fmt)
    log.addHandler(hdl)

    return log, hdl


def test_basic(caplog):
    log, hdl = caplog

    log.info("<b>1</b>")
    assert hdl.last_msg == S.BRIGHT + "1" + S.RESET_ALL
