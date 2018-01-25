#! /usr/bin/env python
# coding:utf-8

from dialog_search_engine.tokenizer import CaboChaContentWordTokenizer


class Document:
    def __init__(self, text, tokens):
        self._text = text
        self._tokens = tokens

    @property
    def text(self):
        return self._text

    @property
    def tokens(self):
        return self._tokens

    def encode(self):
        """データベースに格納する形式に変換する"""
        return self.text, " ".join(self.tokens)

    @classmethod
    def decode(cls, text, tokens_str):
        """データベースの形式からオブジェクトに変換する"""
        tokens = tokens_str.split(" ")
        return cls(text, tokens)

    def __str__(self):
        return f"Document({self._text}, {self._tokens})"

    def __eq__(self, doc):
        return self.text == doc.text and self.tokens == doc.tokens


class DocumentFactory:
    def __init__(self, tokenizer=CaboChaContentWordTokenizer()):
        self._tokenizer = tokenizer

    def build(self, text):
        tokens = self._tokenizer.tokenize(text)
        return Document(text, tokens)
