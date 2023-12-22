"""Module which provides the Converter class to convert characters"""
from functools import reduce
from opencc import OpenCC
from pypinyin import pinyin


class Converter:
    """Class for pinyin, traditional and simplified
    chinese character conversions"""

    @staticmethod
    def to_traditional(hanzi: str) -> str:
        """Transform simplified chinese characters to traditional"""
        return Converter.convert("s2t.json", hanzi)

    @staticmethod
    def to_simplified(hanzi: str) -> str:
        """Transform traditional chinese characters to simplified"""
        return Converter.convert("t2s.json", hanzi)

    @staticmethod
    def to_pinyin(hanzi: str) -> str:
        """Transform Chinese characters to pinyin.
        We just take the first option from pypinyin."""
        flat_pinyin = [elem for py_sl in pinyin(hanzi) for elem in py_sl]
        return reduce(lambda a, b: a + b, flat_pinyin)

    @staticmethod
    def convert(ccdict: str, hanzi: str) -> str:
        """Generic convertion method"""
        converter = OpenCC(ccdict)
        return converter.convert(hanzi)
