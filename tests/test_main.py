from click.testing import CliRunner
import os
import unittest
from laoshi.main import cli_group


class MainTest(unittest.TestCase):
    def test_cc(self):
        runner = CliRunner()
        result = runner.invoke(cli_group, ["cc", "--to", "simplified", "龍"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, "龙\n")

    def test_translate(self):
        runner = CliRunner()
        result = runner.invoke(cli_group, ["translate", "龍"])
        self.assertEqual(result.exit_code, 0)
        print(result.output)
        self.assertTrue("dragon" in result.output)

    def test_create_deck(self):
        runner = CliRunner()
        result = runner.invoke(cli_group, ["manage-deck", "create-deck", "test", "龍"])
        self.assertEqual(result.exit_code, 0)
        self.failIf(not os.path.isfile("./test.apkg"))
        os.remove("./test.apkg")
