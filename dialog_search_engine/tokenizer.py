#! /usr/bin/env python
# coding:utf-8


from cabocha import CaboChaAnalyzer


class CaboChaBasicTokenizer:
    """CaboCha による原型トークナイザ"""
    def __init__(self):
        self._analyzer = CaboChaAnalyzer()

    def tokenize(self, text):
        return [token.surface if token.genkei == "*" else token.genkei
                for token in self._analyzer.parse(text).tokens]


class CaboChaContentWordTokenizer:
    """CaboCha による内容語トークナイザ"""
    def __init__(self):
        self._analyzer = CaboChaAnalyzer()

    def tokenize(self, text):
        return [token.surface if token.genkei == "*" else token.genkei
                for token in self._analyzer.parse(text).tokens
                if token.pos in {"名詞", "形容詞", "動詞"}]
