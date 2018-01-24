#! /usr/bin/env python
# coding: utf-8


import unittest
from dialog_search_engine.posting import Posting
from dialog_search_engine.posting import PostingList


class TestPosting(unittest.TestCase):
    def test_encode_decode(self):
        p = Posting(word="ご飯", id_=1025, tf=9)
        ep = p.encode()
        ans = ('ご飯', b'\x00\x00\x04\x01\x00\x00\x00\x09')
        self.assertEqual(ep, ans)

        dp = Posting.decode(*ans)
        self.assertEqual(dp, p)


class TestPostingList(unittest.TestCase):
    def test_encode_decode(self):
        postings = [
            Posting(word="ご飯", id_=1, tf=2),
            Posting(word="ご飯", id_=0, tf=3),
            Posting(word="ご飯", id_=3, tf=1),
        ]
        posting_list = PostingList(postings)
        sorted_postings = [
            Posting(word="ご飯", id_=0, tf=3),
            Posting(word="ご飯", id_=1, tf=2),
            Posting(word="ご飯", id_=3, tf=1),
        ]
        self.assertEqual(posting_list.posting_list, sorted_postings)

        epl = posting_list.encode()
        ans = ('ご飯',
               (b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x03'
                b'\x00\x00\x00\x01'
                b'\x00\x00\x00\x02'
                b'\x00\x00\x00\x03'
                b'\x00\x00\x00\x01'),
               3)
        self.assertEqual(epl, ans)
        self.assertEqual(PostingList.decode(*ans),
                         PostingList(sorted_postings))
