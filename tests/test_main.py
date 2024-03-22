from click.testing import CliRunner
import unittest
from laoshi.main import cli_group


class MainTest(unittest.TestCase):

    def test_cc(self):
        runner = CliRunner()
        result = runner.invoke(cli_group, ["cc", "--to", "simplified", "龍"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, '龙\n')
