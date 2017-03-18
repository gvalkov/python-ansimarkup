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
    '''
    Produce colored terminal text with a tag-based markup.
    '''

    def __init__(self, tags=None, always_reset=False, tag_sep='<>'):
        '''
        Arguments
        ---------
        tags: dict
           User-supplied tags, which are a mapping of tag names to the strings
           they will be substituted with.
        always_reset: bool
           Whether or not ``parse()`` should always end strings with a reset code.
        tag_sep: str
           The opening and closing characters of each tag (e.g. ``<>``, ``{}``).
        '''
        self.user_tags = tags if tags else {}
        self.always_reset = always_reset

        self.re_tag_start, self.re_tag_end = self.compile_tag_regex(tag_sep)

    def parse(self, text):
        '''Return a string with markup tags converted to ansi-escape sequences.'''
        tags, results = [], []

        text = self.re_tag_start.sub(lambda m: self.sub_start(m, tags, results), text)
        text = self.re_tag_end.sub(lambda m: self.sub_end(m, tags, results), text)

        if self.always_reset:
            if not text.endswith(Style.RESET_ALL):
                text += Style.RESET_ALL

        return text

    def ansiprint(self, *args, **kwargs):
        '''Wrapper around builtins.print() that runs parse() on all arguments first.'''
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
            color = tag[3:]
            if color.isdigit() and int(color) <= 255:
                res = '\033[38;5;%sm' % color
            elif color.startswith('#'):
                res = '\033[38;2;%s;%s;%sm' % hex_to_rgb(color[1:])
            elif color.count(',') == 2:
                res = '\033[38;2;%s;%s;%sm' % tuple(color.split(','))
            else:
                res = foreground.get(color, match.group())

        # An alternative syntax for setting the background color (e.g. <bg red>).
        elif tag.startswith('bg '):
            color = tag[3:]
            if color.isdigit() and int(color) <= 255:
                res = '\033[48;5;%sm' % color
            elif color.startswith('#'):
                res = '\033[48;2;%s;%s;%sm' % hex_to_rgb(color[1:])
            elif color.count(',') == 2:
                res = '\033[48;2;%s;%s;%sm' % tuple(color.split(','))
            else:
                res = background.get(color.upper(), match.group())

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

    def compile_tag_regex(self, tag_sep):
        # Optimize the default:
        if tag_sep == '<>':
            tag_start = re.compile(r'<([^/>]+)>')
            tag_end   = re.compile(r'</([^>]+)>')
            return tag_start, tag_end

        if len(tag_sep) < 2:
            raise ValueError('tag_sep needs to have at least two element (e.g. "<>")')

        if tag_sep[0] == tag_sep[1]:
            raise ValueError('opening and closing characters cannot be the same')

        tag_start = r'{0}([^/{1}]+){1}'.format(tag_sep[0], tag_sep[1])
        tag_end   = r'{0}/([^{1}]+){1}'.format(tag_sep[0], tag_sep[1])
        return re.compile(tag_start), re.compile(tag_end)


def hex_to_rgb(value):
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))
    #return tuple(bytes.fromhex(value))
