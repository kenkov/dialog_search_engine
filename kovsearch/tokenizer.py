#! /usr/bin/env python
# coding:utf-8


from cabocha.tokenizer import CaboChaBasicTokenizer


class CaboChaContentWordTokenizer(CaboChaBasicTokenizer):
    """CaboCha による内容語トークナイザ"""
    def __init__(self):
        pos = {"動詞",
               "形容詞",
               "名詞",
               "感動詞",
               }
        super().__init__(pos=pos)


class CaboChaContentWordVTagTokenizer(CaboChaBasicTokenizer):
    def tokenize(self, text):
        ret = []
        for chunk in self._analyzer.parse(text):
            ret.extend(self._get_surfaces(chunk))
        return ret

    def _get_surfaces(self, chunk):
        rets = []
        for token in chunk:
            if token.surface in {"の", "ん"}:
                continue
            if token.pos in {"名詞", "感動詞"}:
                rets.append(self._get_genkei(token))
            elif token.pos in {"形容詞", "動詞"}:
                flags = [self._get_genkei(token)]
                # 過去形のチェック
                if chunk.find(lambda tkn: tkn.pos == "助動詞" and tkn.genkei == "た"):
                    flags.append("タ")
                if chunk.find(lambda tkn: any([tkn.pos == "助動詞" and tkn.genkei == "か",
                                               tkn.pos == "助動詞" and tkn.genkei == "っけ",
                                               tkn.pos == "記号" and tkn.genkei == "？"])):
                    flags.append("？")
                rets.append("/".join(flags))
        return rets

    def _get_genkei(self, token):
        return token.surface if token.genkei == "*" else token.genkei


class CaboChaSemanticWordTokenizer(CaboChaBasicTokenizer):
    """文の意味を表す語の原型のリストを出力するトークナイザー"""
    def __init__(self):
        super().__init__(pos=None)

    def tokenize(self, text):
        return [token.surface if token.genkei == "*" else token.genkei
                for token in self._analyzer.parse(text).tokens
                if self._is_valid_token(token)]

    def _is_valid_token(self, token):
        """トークンが文の意味を表す場合は True を返す"""
        if token.surface in {"ん", "の"} and token.pos == "名詞":
            # 「書いたのです」「書いたんです」などの「の」「ん」は除く
            return False

        cond = [token.pos in {"動詞", "形容詞", "名詞", "感動詞",
                              "記号", "副詞",
                              "連体詞",  # 「あの」
                              "接続詞",
                              } or
                # 格助詞
                token.pos1 == "格助詞" or
                (token.pos1 == "副助詞" and token.surface == "まで") or
                (token.pos1 == "係助詞" and token.surface == "は") or
                # 過去形
                (token.pos == "助動詞" and token.genkei == "た") or  # 過去形の「た」
                # 否定形
                (token.pos == "助動詞" and token.genkei == "ん")  or # 「いきません」の「ん」
                (token.pos == "助動詞" and token.genkei == "ない") or
                # 欲求
                (token.pos == "助動詞" and token.genkei == "たい") or
                # 提案
                (token.pos == "助動詞" and token.genkei == "う") or
                # 疑問
                (token.pos == "助詞" and token.genkei == "か") or
                (token.pos == "助詞" and token.genkei == "っけ") or
                # 接続助詞
                #   例: #   「大阪に行っ**て**」「お腹が痛い**ので**」「立ち上がる**と**」
                (token.pos == "助詞" and token.pos1 == "接続助詞")
                ]
        return any(cond)



if __name__ == "__main__":
    import sys

    tokenizer = CaboChaContentWordVTagTokenizer()
    for line in sys.stdin:
        res = tokenizer.tokenize(line.strip("\n"))
        print(res)
