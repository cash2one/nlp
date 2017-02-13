from __future__ import absolute_import
from .textrank import TextRank

default_textrank = TextRank()

textrank = default_textrank.extract_tags


def set_stop_words(stop_words_path):
    default_textrank.set_stop_words(stop_words_path)
