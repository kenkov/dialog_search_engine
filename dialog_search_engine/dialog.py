#! /usr/bin/env python
# coding:utf-8


class Dialog:
    def __init__(self, id_, length, input_, response):
        self.id = id_
        self.length = length
        self.input = input_
        self.response = response

    @staticmethod
    def decode(id_, length, input_, response):
        return Dialog(id_, length, input_, response)

    def encode(self):
        return (self.id, self.length, self.input, self.response)

    def __eq__(self, other):
        return (self.id == other.id and
                self.length == other.length and
                self.input == other.input and
                self.response == other.response)

    def __str__(self):
        return f'Dialog(id={self.id},length="{self.length}",input="{self.input}",response="{self.response}")'

    def __repr__(self):
        return self.__str__()
