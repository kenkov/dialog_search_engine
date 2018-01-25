#! /usr/bin/env python
# coding:utf-8

import unittest
from kovsearch.dialog import DialogFactory
from kovsearch.dialog import Dialog
from kovsearch.document import Document


class DocumentFactoryDouble:
    def build(self, text):
        return Document(text=text,
                        tokens=text.split(" "))


class TestDialogFactory(unittest.TestCase):
    def test_build(self):
        doc_factory = DocumentFactoryDouble()
        factory = DialogFactory(document_factory=doc_factory)
        input_text = "明日 は 晴れ"
        response_text = "ピクニック に 行こう"
        res = factory.build(input_text,
                            response_text,
                            id_=100)
        ans = Dialog(input_doc=doc_factory.build(input_text),
                     response_doc=doc_factory.build(response_text),
                     id_=100)
        self.assertEqual(res, ans)


class TestDialog(unittest.TestCase):
    def test_encode_decode(self):
        doc_factory = DocumentFactoryDouble()
        factory = DialogFactory(document_factory=doc_factory)
        input_text = "明日 は 晴れ"
        response_text = "ピクニック に 行こう"
        dialog = factory.build(input_text, response_text, id_=100)

        encoded_dialog = dialog.encode()
        self.assertEqual(encoded_dialog,
                         ("明日 は 晴れ", "明日 は 晴れ",
                          "ピクニック に 行こう", "ピクニック に 行こう",
                          100))
        decoded_dialog = Dialog.decode(*encoded_dialog)
        self.assertEqual(decoded_dialog, dialog)
