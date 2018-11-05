# 対話検索エンジン

Python製の全文検索エンジンです。

## 使い方

kovsearch では、はじめにインデックスを作成し、そのインデックスを使って
文を検索します。

インデックスの作成には `kovsearch.run` に `create_index` 引数を指定して実行します。

```
$ python -m kovsearch.run create_index textfilename dbname
```

検索には `kovsearch.run` に `search` 引数を指定して実行します。

```
$ python -m kovsearch.run search dbname
```