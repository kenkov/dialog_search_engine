#! /usr/bin/env python
# coding:utf-8


from cabocha.tokenizer import CaboChaBasicTokenizer


class CaboChaContentWordTokenizer(CaboChaBasicTokenizer):
    """CaboCha による内容語トークナイザ"""
    def __init__(self):
        pos = {"動詞",
               "形容詞",
               "名詞",
               "感動詞",
               }
        super().__init__(pos=pos)
