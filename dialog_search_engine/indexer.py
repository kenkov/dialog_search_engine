#! /usr/bin/env python
# coding:utf-8


from collections import Counter
from dialog_search_engine.posting import Posting
from dialog_search_engine.posting import PostingList
from dialog_search_engine.database import Database
from dialog_search_engine.dialog import Dialog


class SortBasedIndexer:
    """インデックス構築器"""
    def __init__(self, dbname, tokenizer):
        self._db = Database(dbname)
        self._tokenizer = tokenizer

    def create_index(self, sent_pairs):
        postings, dialogs = self._get_posting_dialog(sent_pairs)
        posting_lists = self._get_posting_lists(postings)

        self._db.init()
        self._db.add_dialogs(dialogs)
        self._db.add_posting_lists(posting_lists)

    def _get_dialogs(self, sent_pairs):
        dialogs = [Dialog(i, *pair)
                   for i, pair in enumerate(sent_pairs)]
        return dialogs

    def _get_posting_lists(self, posting):
        sorted_posting = list(sorted(posting,
                                     key=lambda pos: (pos.word, pos.id)
                                     ))
        postings = []
        posting_list = []
        for pos in sorted_posting:
            # ポスティングの語が新しくなった場合は
            # それまでのポスティングをポスティングリストとして追加
            if postings and pos.word != postings[-1].word:
                if postings:
                    posting_list.append(PostingList(postings))
                postings = []
            postings.append(pos)
        if postings:
            posting_list.append(PostingList(postings))
        return posting_list

    def _get_posting_dialog(self, sent_pairs):
        """文書集合からポスティングの集合を得るメソッド"""
        posting = []
        dialog = []
        for i, (src, tgt) in enumerate(sent_pairs):
            tokens = self._tokenizer.tokenize(src)
            dialog.append(Dialog(i, len(tokens), src, tgt))
            count = Counter(tokens)
            for word, tf in count.items():
                item = Posting(word, i, tf)
                posting.append(item)
        return posting, dialog


def test_SortBasedIndex():
    from tokenizer import CaboChaBasicTokenizer
    tokenizer = CaboChaBasicTokenizer()

    indexer = SortBasedIndexer(":memory:", tokenizer)
    sent_pairs = [
        ("ご飯を食べる", "美味しい"),
        ("ご飯を食べたい", "食べて")
    ]
    indexer.create_index(sent_pairs)
