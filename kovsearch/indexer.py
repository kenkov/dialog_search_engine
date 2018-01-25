#! /usr/bin/env python
# coding:utf-8


from collections import Counter
from kovsearch.posting import Posting
from kovsearch.posting import PostingList
from kovsearch.dialog import DialogFactory


class SortBasedIndexer:
    """インデックス構築器"""
    def __init__(self,
                 db,
                 dialog_factory=DialogFactory()):
        self._db = db
        self._dialog_factory = dialog_factory

    def create_index(self, sent_pairs):
        postings, dialogs = self._get_posting_dialog(sent_pairs)
        posting_lists = self._get_posting_lists(postings)

        self._db.create_table()
        self._db.add_dialogs(dialogs)
        self._db.add_posting_lists(posting_lists)

    def _get_posting_lists(self, posting):
        sorted_posting = list(sorted(posting,
                                     key=lambda pos: (pos.word, pos.id_)
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
        postings = []
        dialogs = []
        for i, (src, tgt) in enumerate(sent_pairs):
            dialog = self._dialog_factory.build(input_text=src,
                                                response_text=tgt,
                                                id_=i)
            dialogs.append(dialog)
            count = Counter(dialog.input_doc.tokens)
            for word, tf in count.items():
                item = Posting(word, i, tf)
                postings.append(item)
        return postings, dialogs
