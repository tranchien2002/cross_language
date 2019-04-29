# -*- coding: utf-8 -*-
from underthesea import word_tokenize

class Article:
    def __init__(self, id, content = "", word = "", keyword = "", title=""):
        self.id = id
        self.content = content
        self.word = word
        self.keyword = keyword
        self.title = title
