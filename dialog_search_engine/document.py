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

    def __str__(self):
        return f"Document({self._text}, {self._tokens})"


class DocmumentFactory:
    def __init__(self, tokenizer=CaboChaContentWordTokenizer()):
        self._tokenizer = tokenizer

    def build(self, text):
        tokens = self._tokenizer.tokenize(text)
        return Document(text, tokens)
