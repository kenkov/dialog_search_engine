#! /usr/bin/env python
# coding: utf-8

import unittest
from dialog_search_engine.dialog import DialogFactory
from test.test_dialog import DocumentFactoryDouble
from dialog_search_engine.scorer import ScoredDialog
from dialog_search_engine.database import Database
from test.test_scorer import ScorerInterfaceTestMixin
from dialog_search_engine.index_searcher import IndexSearcher


class ScorerDouble:
    def scores(self, query, dialogs):
        return [ScoredDialog(score=1.0, dialog=d) for d in dialogs]


class TestScorerDouble(unittest.TestCase,
                       ScorerInterfaceTestMixin):
    def setUp(self):
        self.object = ScorerDouble()


class TestIndexSearcher(unittest.TestCase):
    def setUp(self):
        # Database の準備
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

        scorer = ScorerDouble()
        self.searcher = IndexSearcher(db=db,
                                      scorer=scorer,
                                      document_factory=doc_factory)

    def test_score(self):
        res = self.searcher.search(query_text="ご飯 が 欲しい")
        print(res)
