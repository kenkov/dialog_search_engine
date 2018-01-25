#! /usr/bin/env python
# coding:utf-8


from collections import defaultdict
from collections import namedtuple
from kovsearch.database import NotFoundException


ScoredDialog = namedtuple("ScoredDialog", ["score", "dialog"])


class IdfWeightedJaccardScorer:
    """Idf で重み付けした Jaccard スコアのよるスコアづけをするクラス"""
    def __init__(self, db):
        self._db = db

    def scores(self, query, dialogs):
        """
        Args:
            query (Document):
            dialog (List[Dialog]):
        """
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
        return sum(val/(df[key]+1) for key, val in dic.items())

    def _df_dict(self, query, dialogs):
        df = defaultdict(int)
        for word in query.tokens:
            if word not in df:
                try:
                    df[word] = self._db.search_df(word)
                except NotFoundException:
                    pass
        for dialog in dialogs:
            for word in dialog.input_doc.tokens:
                if word not in df:
                    try:
                        df[word] = self._db.search_df(word)
                    except NotFoundException:
                        pass
        return df

    def _freq_dic(self, tokens):
        dic = defaultdict(int)
        for token in tokens:
            dic[token] += 1
        return dic


class TfIdfWeightedJaccardScorer:
    def score(self, query, dialog, idf):
        pass
