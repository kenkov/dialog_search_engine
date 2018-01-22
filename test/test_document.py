#! /usr/bin/env python
# coding:utf-8

import unittest
from dialog_search_engine.document import DocmumentFactory
from dialog_search_engine.document import Document


class TokenizerDouble:
    def tokenize(self, text):
        return ["明日", "晴れ"]


class TestDocumentFactory(unittest.TestCase):
    def test_build(self):
        factory = DocmumentFactory(tokenizer=TokenizerDouble())
        text = "明日は晴れ"
        res = factory.build(text)
        ans = Document(text="明日は晴れ",
                       tokens=["明日", "晴れ"])
        self.assertEqual(res, ans)
