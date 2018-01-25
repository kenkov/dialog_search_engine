#! /usr/bin/env python
# coding:utf-8


from collections import defaultdict
from kovsearch.database import NotFoundException
from kovsearch.document import DocumentFactory


class IndexSearcher:
    def __init__(self,
                 db,
                 scorer,
                 document_factory=DocumentFactory()):
        self._db = db
        self._scorer = scorer
        self._doc_factory = document_factory
        self._num_dialogs = self._db.get_num_dialogs()

    def search(self, query_text):
        """query から OR 検索を行う

        Args:
            query_test (str): クエリ文字列
        """
        query = self._doc_factory.build(query_text)
        score_dialogs = self._get_score_dialogs(query)

        return list(sorted(score_dialogs,
                           key=lambda sd: sd.score,
                           reverse=True))

    def _get_score_dialogs(self, query):
        id_score = defaultdict(int)
        for word in query.tokens:
            try:
                posting_list = self._db.search_posting_list(word)
                for pos in posting_list:
                    id_score[pos.id_] += 1
            except NotFoundException:
                pass

        dialogs = self._db.search_dialogs(id_score.keys())

        return self._scorer.scores(query, dialogs)
