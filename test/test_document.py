#! /usr/bin/env python
# coding:utf-8

import unittest
from kovsearch.document import DocumentFactory
from kovsearch.document import Document


class TokenizerDouble:
    def tokenize(self, text):
        return ["明日", "晴れ"]


class TestDocumentFactory(unittest.TestCase):
    def test_build(self):
        factory = DocumentFactory(tokenizer=TokenizerDouble())
        text = "明日は晴れ"
        res = factory.build(text)
        ans = Document(text="明日は晴れ",
                       tokens=["明日", "晴れ"])
        self.assertEqual(res, ans)


class TestDocument(unittest.TestCase):
    def test_encode_decode(self):
        text = Document(text="明日は晴れ",
                        tokens=["明日", "晴れ"])
        encoded_text = text.encode()
        self.assertEqual(encoded_text,
                         ("明日は晴れ", "明日 晴れ"))
        decoded_text = Document.decode(*encoded_text)
        self.assertEqual(decoded_text, text)
