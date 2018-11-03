# 対話検索エンジン

Python 製の全文検索エンジンです。

## 使い方

インデックスの作成

```
$ python -m kovsearch.run create_index textfilename dbname
```

検索する

```
$ python -m kovsearch.run search dbname
```