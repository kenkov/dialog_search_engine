#! /usr/bin/env python
# coding: utf-8

import unittest
from unittest.mock import Mock
from dialog_search_engine.indexer import SortBasedIndexer
from dialog_search_engine.dialog import DialogFactory
from test.test_dialog import DocumentFactoryDouble


class TestSortBasedIndexer(unittest.TestCase):
    def test_create_index(self):
        db = Mock()
        doc_factory = DocumentFactoryDouble()
        factory = DialogFactory(document_factory=doc_factory)

        indexer = SortBasedIndexer(db=db,
                                   dialog_factory=factory)
        sent_pairs = [
            ("ご飯 を 食べる", "美味しい"),
            ("ご飯 を 食べたい", "食べ て")
        ]
        indexer.create_index(sent_pairs)

        # 送信テスト
        db.create_table.assert_called_with()
        db.add_dialogs.assert_called()
        db.add_posting_lists.assert_called()
