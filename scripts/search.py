#! /usr/bin/env python
# coding:utf-8


if __name__ == "__main__":
    from dialog_search_engine.index_searcher import IndexSearcher
    from dialog_search_engine.tokenizer import CaboChaContentWordTokenizer
    import sys
    import datetime

    dbname = sys.argv[1]
    tokenizer = CaboChaContentWordTokenizer()
    searcher = IndexSearcher(dbname, tokenizer)

    for line in sys.stdin:
        query = line.strip("\n")
        start_at = datetime.datetime.now()
        res = searcher.search(query)
        end_at = datetime.datetime.now()
        print("{} answers, {}".format(
            len(res),
            end_at - start_at
        ))
        for score_dialog in res[:10]:
            score = score_dialog.score
            dialog = score_dialog.dialog
            print("{:4f} {} {}".format(score,
                                       dialog.input,
                                       dialog.response))
