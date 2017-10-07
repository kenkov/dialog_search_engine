#! /usr/bin/env python
# coding:utf-8


import sqlite3
from dialog_search_engine.posting import Posting
from dialog_search_engine.posting import PostingList
from dialog_search_engine.dialog import Dialog


class Database:
    def __init__(self, dbname):
        self._dbname = dbname
        self._conn = sqlite3.connect(dbname)

    def init(self):
        cur = self._conn.cursor()
        cur.execute('''
            CREATE TABLE dialogs
            (id      integer primary key,
            length   integer not null,
            input    text    not null,
            response text    not null)''')
        cur.execute('''
            CREATE TABLE posting_lists
            (word     text    primary key,
             postings blog    not null)''')
        # インデックスの作成
        # posting_lists(word) は sqlite_autoindexing される
        # のでインデックスを作成する必要なし
        cur.execute('''
            CREATE INDEX dialogs_index_id
            ON dialogs(id)''')

        self._conn.commit()
        cur.close()

    def add_dialogs(self, dialogs):
        cur = self._conn.cursor()
        cur.executemany('''insert into dialogs values (?,?,?,?)''',
                        (d.encode() for d in dialogs))
        self._conn.commit()
        cur.close()

    def add_posting_lists(self, posting_lists):
        cur = self._conn.cursor()
        cur.executemany('''insert into posting_lists values (?,?)''',
                        (pl.encode() for pl in posting_lists))
        self._conn.commit()
        cur.close()

    def search_posting_list(self, word):
        cur = self._conn.cursor()
        cur.execute('select * from posting_lists where word=?',
                    (word,))
        res = cur.fetchone()
        if res:
            return PostingList.decode(*res)
        else:
            raise NotFoundException()

    def search_dialog(self, id_):
        cur = self._conn.cursor()
        cur.execute('select * from dialogs where id=?',
                    (id_,))
        res = cur.fetchone()
        if res:
            return Dialog.decode(*res)
        else:
            raise NotFoundException()

    def search_dialogs(self, ids):
        ids = tuple(ids)
        cur = self._conn.cursor()
        cur.execute('select * from dialogs where id in (' + \
                    ",".join(['?'] * len(ids)) + ')',
                    ids)
        reses = cur.fetchall()
        return [Dialog.decode(*res) for res in reses]

    def get_num_dialogs(self):
        cur = self._conn.cursor()
        cur.execute('select count(id) from dialogs')
        res = cur.fetchone()
        return res[0]


class NotFoundException(Exception):
    """データベースで検索結果がなかった場合に送出される例外"""


def test_Database():
    dialogs = [
        Dialog(0, 2, "ご飯を食べる", "美味しい"),
        Dialog(1, 2, "ご飯を食べたい", "食べて")
    ]
    posting_lists = [
        PostingList([Posting("ご飯",   0, 1), Posting("ご飯",   1, 1)]),
        PostingList([Posting("食べる", 0, 1), Posting("食べる", 1, 1)])
    ]
    db = Database(":memory:")
    db.init()
    db.add_dialogs(dialogs)
    db.add_posting_lists(posting_lists)

    for i in range(len(dialogs)):
        assert db.search_dialog(i) == dialogs[i]

    assert db.search_posting_list("ご飯") == posting_lists[0]
    assert db.search_posting_list("食べる") == posting_lists[1]

    assert db.get_num_dialogs() == 2
