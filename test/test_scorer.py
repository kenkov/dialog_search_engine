#! /usr/bin/env python
# coding: utf-8

import unittest
from kovsearch.dialog import DialogFactory
from test.test_dialog import DocumentFactoryDouble
from kovsearch.database import Database
from kovsearch.scorer import IdfWeightedJaccardScorer


class ScorerInterfaceTestMixin:
    def test_implements_scores(self):
        self.assertTrue(hasattr(self.object, "scores"))


class TestIdfWeightedJaccardScorer(unittest.TestCase,
                                   ScorerInterfaceTestMixin):
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
        self.scorer = IdfWeightedJaccardScorer(db)
        self.object = self.scorer
        self.query = doc_factory.build(text="ご飯 を 食べ たい")
        self.dialogs = dialogs

    def test_score(self):
        res = self.scorer.scores(self.query, self.dialogs)
        print(res)
