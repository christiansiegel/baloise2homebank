import unittest
import baloise2homebank
import os


class Baloise2HomebankTest(unittest.TestCase):
    out_filename = "test-output.csv"

    def test_append_to_filename(self):
        actual = baloise2homebank.append_to_filename(
            "foo/bar.csv", "-test")
        self.assertEqual(actual, "foo/bar-test.csv")

    def test_convert_to_homebank_date(self):
        actual = baloise2homebank.convert_to_homebank_date(
            "2000-12-31", "%Y-%m-%d")
        self.assertEqual(actual, "31-12-2000")

    def test_convert_csv(self):
        baloise2homebank.convert_csv("test-input.csv", self.out_filename)
        with open(self.out_filename) as out_file:
            lines = out_file.readlines()
            self.assertEqual(len(lines), 2)
            self.assertEqual(
                lines[0].rstrip("\r\n"),
                "01-02-2019;8;;;Gutschrift FooFinance Jane Doe Musterstrasse 1"
                " 4002 BASEL CH - - Info - - Pocket Money;0.01;;")
            self.assertEqual(
                lines[1].rstrip("\r\n"),
                "01-01-2019;8;;;Belastung Geldbezug Bancomat FOO BANK BASEL"
                " 01.01.19 / 13:37:42 Karten-Nr.: 12345678 Betrag: CHF 100.00;"
                "-100.00;;")

    def tearDown(self):
        if os.path.isfile(self.out_filename):
            os.remove(self.out_filename)


if __name__ == "__main__":
    unittest.main()
