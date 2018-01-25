#! /usr/bin/env python
# coding:utf-8


from kovsearch.document import Document
from kovsearch.document import DocumentFactory


class Dialog:
    def __init__(self, input_doc, response_doc, id_):
        self.input_doc = input_doc
        self.response_doc = response_doc
        self.id_ = id_

    @classmethod
    def decode(cls,
               input_text,
               input_tokens_str,
               response_text,
               response_tokens_str,
               id_):
        input_doc = Document.decode(input_text, input_tokens_str)
        response_doc = Document.decode(response_text, response_tokens_str)
        return Dialog(input_doc, response_doc, id_)

    def encode(self):
        return (self.input_doc.encode() +
                self.response_doc.encode() +
                (self.id_,))

    def __eq__(self, other):
        return (self.input_doc == other.input_doc and
                self.response_doc == other.response_doc,
                self.id_ == other.id_)


class DialogFactory:
    def __init__(self,
                 document_factory=DocumentFactory()):
        self._doc_factory = document_factory

    def build(self, input_text, response_text, id_=0):
        input_doc = self._doc_factory.build(input_text)
        response_doc = self._doc_factory.build(response_text)
        return Dialog(input_doc, response_doc, id_=id_)
