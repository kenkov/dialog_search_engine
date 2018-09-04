#! /usr/bin/env python
# coding:utf-8


from collections import defaultdict
from collections import namedtuple
from kovsearch.database import NotFoundException
import math


ScoredDialog = namedtuple("ScoredDialog", ["score", "dialog"])


class IdfWeightedJaccardScorer:
    """Idf で重み付けした Jaccard スコアのよるスコアづけをするクラス"""
    def __init__(self, db):
        self._db = db
        self._num_dialogs = self._db.get_num_dialogs()

    def scores(self, query, dialogs):
        """
        Args:
            query (Document):
            dialog (List[Dialog]):
        """

        num_query_token = len(query.tokens)
        dialogs = [dia for dia in dialogs
                   if math.fabs(len(dia.input_doc.tokens) - num_query_token) < 4]

        # df 辞書の作成
        df = self._df_dict(query, dialogs)
        scores = [ScoredDialog(self._score(query, dialog, df), dialog)
                  for dialog in dialogs]

        return scores

    def _score(self, query, dialog, df):
        query_dic = self._freq_dic(query.tokens)
        dialog_dic = self._freq_dic(dialog.input_doc.tokens)

        intersection_dic = {key: min(query_dic[key], dialog_dic[key])
                            for key in query_dic.keys() & dialog_dic.keys()}
        union_dic = {key: max(query_dic[key], dialog_dic[key])
                     for key in query_dic.keys() | dialog_dic.keys()}

        score = (self._idf_score(df, intersection_dic) /
                 self._idf_score(df, union_dic))
        return score

    def _idf_score(self, df, dic):
        idf_dict = {key: math.log(self._num_dialogs / (df[key] + 1))
                    for key in dic}
        return sum(val * idf_dict[key] for key, val in dic.items())

    def _df_dict(self, query, dialogs):
        df = defaultdict(int)

        _words = set()
        for word in query.tokens:
            _words.add(word)
        for dialog in dialogs:
            for word in dialog.input_doc.tokens:
                _words.add(word)

        for key, val in self._db.search_dfs(list(_words)):
            df[key] = val

        return df

    def _freq_dic(self, tokens):
        dic = defaultdict(int)
        for token in tokens:
            dic[token] += 1
        return dic


class TfIdfWeightedJaccardScorer:
    def score(self, query, dialog, idf):
        pass
