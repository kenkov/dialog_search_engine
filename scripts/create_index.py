#! /usr/bin/env python
# coding:utf-8


if __name__ == '__main__':
    import sys
    from dialog_search_engine.tokenizer import CaboChaBasicTokenizer
    from dialog_search_engine.indexer import SortBasedIndexer

    filename = sys.argv[1]
    tokenizer = CaboChaBasicTokenizer()
    indexer = SortBasedIndexer(f":{filename}.db:", tokenizer)

    sent_pairs = [line.strip("\n").split("\t") for line in open(filename)]
    indexer.create_index(sent_pairs)
