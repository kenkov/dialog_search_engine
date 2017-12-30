#! /usr/bin/env python
# coding:utf-8


class Posting:
    """単語と ID の対応付けを表すポスティングのクラス
    付加情報として、単語が文書に出現する頻度 TF も所持する

    ポスティングの例
        語          ドキュメントID  TF
        -----------------------------------
        おはよう    1               2
    """
    def __init__(self, word, id, tf):
        self.word = word
        self.id = id
        self.tf = tf

    @staticmethod
    def decode(word, bytes_):
        assert len(bytes_) == 8
        id_ = int.from_bytes(bytes_[:4], byteorder="big")
        tf = int.from_bytes(bytes_[4:8], byteorder="big")
        return Posting(word, id_, tf)

    def encode(self):
        """ストレージへの保存形式にエンコードする
        id と tf をそれぞれ 4 byte の big endian エンコードする
        """
        bytes_ = self.id.to_bytes(4, byteorder="big") + \
            self.tf.to_bytes(4, byteorder="big")
        return (self.word, bytes_)

    def __eq__(self, other):
        return (self.word == other.word and
                self.id == other.id and
                self.tf == other.tf)

    def __hash__(self):
        hash((self.word, self.id, self.tf))

    def __str__(self):
        return f'Posting(word="{self.word}",id={self.id},tf={self.tf})'

    def __repr__(self):
        return self.__str__()


class PostingList:
    """ポスティングリストを表すクラス"""
    def __init__(self, postings):
        assert postings
        self.word = postings[0].word
        self.posting_list = list(sorted(postings,
                                        key=lambda pos: pos.id,))

    @staticmethod
    def decode(word, bytes_):
        len_bytes = len(bytes_)
        assert len_bytes % 8 == 0
        postings = [Posting.decode(word, bytes_[i:i+8])
                    for i in range(0, len_bytes, 8)]
        return PostingList(postings)

    def encode(self):
        encoded_poses = [pos.encode() for pos in self.posting_list]
        bytes_ = b''.join(b for w, b in encoded_poses)
        word = encoded_poses[0][0]

        return word, bytes_

    def __eq__(self, other):
        return self.posting_list == other.posting_list

    def __iter__(self):
        return iter(self.posting_list)

    def __str__(self):
        return f'PostingList(word="{self.word}",posting_list={self.posting_list})'

    def __repr__(self):
        return self.__str__()
