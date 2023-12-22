from opencc import OpenCC
from pypinyin import pinyin
from functools import reduce


class Converter:

    @staticmethod
    def to_traditional(hanzi: str) -> str:
        return Converter.convert('s2t.json', hanzi)

    @staticmethod
    def to_simplified(hanzi: str) -> str:
        return Converter.convert('t2s.json', hanzi)

    @staticmethod
    def to_pinyin(hanzi: str) -> str:
        flat_pinyin = [elem for py_sl in pinyin(hanzi) for elem in py_sl]
        return reduce(lambda a, b: a + b, flat_pinyin)

    @staticmethod
    def convert(ccdict: str, hanzi: str) -> str:
        converter = OpenCC(ccdict)
        return converter.convert(hanzi)
