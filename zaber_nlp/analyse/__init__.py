from __future__ import absolute_import

from .associatation import Association
from .textrank import TextRank

default_TextRank = TextRank()

Text_Rank = default_TextRank.extract_tags

default_Association = Association()

Associate = default_Association.str_match


def set_stop_words(stop_words_path):
    default_TextRank.set_stop_words(stop_words_path)
