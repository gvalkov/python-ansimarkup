from __future__ import print_function

import re

from colorama import Style

from .tags import style, background, foreground, all_tags
from .compat import builtins


class AnsiMarkupError(Exception):
    pass

class MismatchedTag(AnsiMarkupError):
    pass


class AnsiMarkup:
    re_tag_start = re.compile(r'<([^/>]+)>')
    re_tag_end   = re.compile(r'</([^>]+)>')

    def __init__(self, tags=None, always_reset=False):
        self.user_tags = tags if tags else {}
        self.always_reset = always_reset

    def parse(self, text):
        tags, results = [], []

        text = self.re_tag_start.sub(lambda m: self.sub_start(m, tags, results), text)
        text = self.re_tag_end.sub(lambda m: self.sub_end(m, tags, results), text)

        if self.always_reset:
            if not text.endswith(Style.RESET_ALL):
                text += Style.RESET_ALL

        return text

    def ansiprint(self, *args, **kwargs):
        args = (self.parse(str(i)) for i in args)
        builtins.print(*args, **kwargs)

    def strip(self, text):
        '''Return string with markup tags removed.'''

        # TODO: This also strips unknown tags.
        text = self.re_tag_start.sub('', text)
        text = self.re_tag_end.sub('', text)
        return text

    def __call__(self, text):
        return self.parse(text)

    def sub_start(self, match, tag_list, res_list):
        tag = match.group(1)

        # User-defined tags take preference over all other.
        if tag in self.user_tags:
            utag = self.user_tags[tag]
            res = utag() if callable(utag) else utag

        # Substitute on a direct match.
        elif tag in all_tags:
            res = all_tags[tag]

        # An alternative syntax for setting the foreground color (e.g. <fg red>).
        elif tag.startswith('fg '):
            res = foreground.get(tag[3:], match.group())

        # An alternative syntax for setting the background color (e.g. <bg red>).
        elif tag.startswith('bg '):
            res = background.get(tag[3:].upper(), match.group())

        # Shorthand formats (e.g. <red,blue>, <bold,red,blue>).
        elif ',' in tag:
            el_count = tag.count(',')

            if el_count == 1:
                fg, bg = tag.split(',')
                res = foreground.get(fg, '') + background.get(bg.upper(), '')

            elif el_count == 2:
                st, fg, bg = tag.split(',')
                res = style[st] + foreground.get(fg, '') + background.get(bg.upper(), '')

        # If nothing matches, return the full tag (i.e. <unknown>text</...>).
        else:
            return match.group()

        tag_list.append(tag)
        res_list.append(res)
        return res

    def sub_end(self, match, tag_list, res_list):
        tag = match.group(1)

        if tag_list:
            try:
                idx = tag_list.index(tag)
            except ValueError:
                raise MismatchedTag('closing tag "</%s>" has no corresponding opening tag' % tag)

            res = ''.join(res_list[:idx])

            del tag_list[idx]
            del res_list[idx]
            return Style.RESET_ALL + res
        else:
            return Style.RESET_ALL

        return match.group()
