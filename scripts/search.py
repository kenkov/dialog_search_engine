#! /usr/bin/env python
# coding:utf-8


if __name__ == "__main__":
    from kovsearch.database import Database
    from kovsearch.index_searcher import IndexSearcher
    from kovsearch.scorer import IdfWeightedJaccardScorer
    import sys
    import datetime
    import logging

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.DEBUG)

    dbname = sys.argv[1]
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
            print("{:4f}\t{}\t{}\t{}\t{}".format(score,
                                       dialog.input_doc.text,
                                       "|".join(dialog.input_doc.tokens),
                                       dialog.response_doc.text,
                                       "|".join(dialog.response_doc.tokens)))
