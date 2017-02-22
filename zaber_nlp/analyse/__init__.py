from __future__ import absolute_import
from .textrank import TextRank

default_TextRank = TextRank()

Text_Rank = default_TextRank.extract_tags


def set_stop_words(stop_words_path):
    default_TextRank.set_stop_words(stop_words_path)
