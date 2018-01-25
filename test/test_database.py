#! /usr/bin/env python
# coding: utf-8

import unittest
from dialog_search_engine.posting import Posting
from dialog_search_engine.posting import PostingList
from dialog_search_engine.dialog import DialogFactory
from test.test_dialog import DocumentFactoryDouble
from dialog_search_engine.database import Database


class TestDatabase(unittest.TestCase):
    def test_add_search_dialog(self):
        # prepare
        doc_factory = DocumentFactoryDouble()
        factory = DialogFactory(document_factory=doc_factory)
        dialogs = [factory.build(input_text="ご飯 を 食べる",
                                 response_text="美味しい",
                                 id_=0),
                   factory.build(input_text="ご飯 を 食べ たい",
                                 response_text="食べ て",
                                 id_=1)
                   ]
        db = Database(":memory:")
        db.create_table()
        db.add_dialogs(dialogs)

        # test
        self.assertEqual(db.search_dialog(id_=0),
                         dialogs[0])
        self.assertEqual(db.search_dialog(id_=1),
                         dialogs[1])
        self.assertEqual(db.search_dialogs(ids=[0, 1]),
                         dialogs)
        self.assertEqual(db.get_num_dialogs(), 2)

    def test_add_search_posting_list(self):
        postings_rice = [Posting(word="ご飯", id_=1, tf=2),
                         Posting(word="ご飯", id_=0, tf=3),
                         Posting(word="ご飯", id_=3, tf=1)]
        postings_eat = [Posting(word="食べる", id_=1, tf=2),
                        Posting(word="食べる", id_=0, tf=1)]
        posting_list_rice = PostingList(postings_rice)
        posting_list_eat = PostingList(postings_eat)
        db = Database(":memory:")
        db.create_table()
        db.add_posting_lists([posting_list_rice, posting_list_eat])

        # test
        self.assertEqual(db.search_posting_list("ご飯"),
                         posting_list_rice)
        self.assertEqual(db.search_posting_list("食べる"),
                         posting_list_eat)
        self.assertEqual(db.search_df("ご飯"), 3)
        self.assertEqual(db.search_df("食べる"), 2)
