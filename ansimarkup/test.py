from . logger import AnsiMarkupFormatter


import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG)

r = logging.StreamHandler()
r.setLevel(logging.DEBUG)
f = AnsiMarkupFormatter()
r.setFormatter(f)

log.addHandler(r)

log.info('<b>hello</b>')
