import unittest
from laoshi import converter


class ConverterTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_to_traditional(self):
        self.assertEqual(converter.Converter.to_traditional("龙"), "龍")

    def test_to_simplified(self):
        self.assertEqual(converter.Converter.to_simplified("龍"), "龙")

    def test_to_pinyin(self):
        self.assertEqual(converter.Converter.to_pinyin("你好"), "nǐhǎo")
        self.assertEqual(converter.Converter.to_pinyin("你"), "nǐ")
