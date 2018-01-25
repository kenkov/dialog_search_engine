#! /usr/bin/env python
# coding:utf-8


if __name__ == '__main__':
    import sys
    from dialog_search_engine.database import Database
    from dialog_search_engine.indexer import SortBasedIndexer

    filename = sys.argv[1]
    dbname = sys.argv[2]
    db = Database(dbname)
    indexer = SortBasedIndexer(db)

    sent_pairs = [line.strip("\n").split("\t") for line in open(filename)]
    indexer.create_index(sent_pairs)
