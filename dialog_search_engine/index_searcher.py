#! /usr/bin/env python
# coding:utf-8


from collections import defaultdict
from dialog_search_engine.database import Database
from dialog_search_engine.database import NotFoundException


class IndexSearcher:
    def __init__(self, dbname, tokenizer):
        """
        Args:
            tokenizer: クエリをトークンに分割するトークナイザ
        """
        self._tokenizer = tokenizer
        self._db = Database(dbname)
        self._num_dialogs = self._db.get_num_dialogs()

    def search(self, query):
        """query から OR 検索を行う

        Args:
            query (str): クエリ
        """
        id_score_dialog = self._get_id_score_dialog(query)
        result = []
        for id_, (score, dialog) in id_score_dialog.items():
            res = ScoredDialog(score, dialog)
            result.append(res)

        return list(sorted(result, key=lambda sd: sd.score, reverse=True))

    def _get_id_score_dialog(self, query):
        words = self._tokenizer.tokenize(query)
        id_score = defaultdict(int)
        for word in words:
            try:
                posting_list = self._db.search_posting_list(word)
                # df = len(posting_list.posting_list)
                for pos in posting_list:
                    id_ = pos.id
                    # tf = math.sqrt(pos.tf)
                    # idf = math.log(self._num_dialogs / (df + 1)) + 1
                    # id_score[id_] += tf * idf
                    id_score[id_] += 1
            except NotFoundException:
                pass
        id_score_dialog = dict()
        dialogs = self._db.search_dialogs(id_score.keys())
        for dialog in dialogs:
            id_ = dialog.id
            # id_score_dialog[id_] = (id_score[id_] / math.sqrt(dialog.length),
            #                         dialog)

            # calculate F score
            prec = id_score[id_] / len(words)
            rec = id_score[id_] / dialog.length
            score = 2*prec*rec / (prec + rec)
            id_score_dialog[id_] = (score, dialog)
        return id_score_dialog


class ScoredDialog:
    def __init__(self, score, dialog):
        self.score = score
        self.dialog = dialog

    def __str__(self):
        return f"ScoredDialog(score={self.score},dialog={self.dialog})"

    def __repr__(self):
        return self.__repr__()


def test_IndexSearcher():
    from tokenizer import CaboChaContentWordTokenizer
    dbname = ":test:"
    tokenizer = CaboChaContentWordTokenizer()
    searcher = IndexSearcher(dbname, tokenizer)

    query = "お風呂に入って寝よう"
    res = searcher.search(query)
    for dialog in res[:10]:
        print(dialog)
