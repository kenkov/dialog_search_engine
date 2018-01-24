#! /usr/bin/env python
# coding:utf-8


import sqlite3
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
            (input_text         text    not null,
             input_tokens       text    not null,
             response_text      text    not null,
             response_tokens    text    not null,
             id                 integer primary key)''')
        cur.execute('''
            CREATE TABLE posting_lists
            (word     text    primary key,
             postings blog    not null,
             df       integer not null)''')
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
        cur.executemany('''insert into dialogs values (?,?,?,?,?)''',
                        (d.encode() for d in dialogs))
        self._conn.commit()
        cur.close()

    def add_posting_lists(self, posting_lists):
        cur = self._conn.cursor()
        cur.executemany('''insert into posting_lists values (?,?,?)''',
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

    def search_df(self, word):
        cur = self._conn.cursor()
        cur.execute('select df from posting_lists where word=?',
                    (word,))
        res = cur.fetchone()
        if res:
            return res[0]
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
        cur.execute('select * from dialogs where id in (' +
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
