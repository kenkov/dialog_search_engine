#! /usr/bin/env python
# coding: utf-8


import unittest
from dialog_search_engine.posting import Posting
from dialog_search_engine.posting import PostingList


class TestPosting(unittest.TestCase):
    def test_encode_decode(self):
        p = Posting("ご飯", 1025, 9)
        ep = p.encode()
        ans = ('ご飯', b'\x00\x00\x04\x01\x00\x00\x00\x09')
        self.assertEqual(ep, ans)

        dp = Posting.decode(*ans)
        self.assertEqual(dp, p)


class TestPostingList(unittest.TestCase):
    def test_encode_decode(self):
        postings = [
            Posting("ご飯", 1, 2),
            Posting("ご飯", 0, 3),
            Posting("ご飯", 3, 1),
        ]
        posting_list = PostingList(postings)
        sorted_postings = [
            Posting("ご飯", 0, 3),
            Posting("ご飯", 1, 2),
            Posting("ご飯", 3, 1),
        ]
        self.assertEqual(posting_list.posting_list, sorted_postings)

        epl = posting_list.encode()
        ans = ('ご飯',
               b'\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x01')
        self.assertEqual(epl, ans)
        self.assertEqual(PostingList.decode(*ans),
                         PostingList(sorted_postings))
