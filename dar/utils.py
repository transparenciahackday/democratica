#!/usr/bin/env python

def get_dates(sess, leg):
    pass

from haystack.utils import Highlighter
from django.utils.html import strip_tags

class MyHighlighter(Highlighter):
    prev_chars = 10

    def highlight(self, text_block):
        self.text_block = strip_tags(text_block)
        highlight_locations = self.find_highlightable_words()
        start_offset, end_offset = self.find_window(highlight_locations)
        start_offset -= self.prev_chars
        end_offset -= self.prev_chars
        return self.render_html(highlight_locations, start_offset, end_offset)

