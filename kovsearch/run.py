#! /usr/bin/env python
# coding:utf-8

from kovsearch.database import Database
from kovsearch.indexer import SortBasedIndexer
from kovsearch.index_searcher import IndexSearcher
from kovsearch.scorer import IdfWeightedJaccardScorer
import datetime
import sys


class Runner:
    def create_index(self, filename, dbname):
        db = Database(dbname)
        indexer = SortBasedIndexer(db)
        sent_pairs = [line.strip("\n").split("\t")
                      for line in open(filename)]
        indexer.create_index(sent_pairs)

    def search(self, dbname):
        db = Database(dbname)
        scorer = IdfWeightedJaccardScorer(db)
        searcher = IndexSearcher(db=db, scorer=scorer)

        for line in sys.stdin:
            query = line.strip("\n")
            start_at = datetime.datetime.now()
            res = searcher.search(query)
            end_at = datetime.datetime.now()
            logging.info("{} answers, {}".format(len(res), end_at - start_at))
            for score_dialog in res[:5]:
                score = score_dialog.score
                dialog = score_dialog.dialog
                log_args = (score,
                            dialog.input_doc.text,
                            "|".join(dialog.input_doc.tokens),
                            dialog.response_doc.text,
                            "|".join(dialog.response_doc.tokens))

                print("{:4f}\t{}\t{}\t{}\t{}".format(*log_args))


if __name__ == '__main__':
    import fire
    import logging

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.DEBUG)

    fire.Fire(Runner)
