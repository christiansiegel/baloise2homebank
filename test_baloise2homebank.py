import unittest
import baloise2homebank
import os


class Baloise2HomebankTest(unittest.TestCase):
    out_filename_baloise = "test-output-baloise.csv"
    out_filename_cornercard = "test-output-cornercard.csv"

    def test_append_to_filename(self):
        actual = baloise2homebank.append_to_filename(
            "foo/bar.csv", "-test")
        self.assertEqual(actual, "foo/bar-test.csv")

    def test_convert_to_homebank_date(self):
        actual = baloise2homebank.convert_to_homebank_date(
            "2000-12-31", "%Y-%m-%d")
        self.assertEqual(actual, "31-12-2000")

    def test_convert_baloise_csv(self):
        baloise2homebank.convert_baloise_csv(
            "testdata/test-input-baloise.csv", self.out_filename_baloise)
        with open(self.out_filename_baloise) as out_file:
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

    def test_convert_baloise_csv(self):
        baloise2homebank.convert_cornercard_csv(
            "testdata/test-input-cornercard.csv", self.out_filename_cornercard)
        with open(self.out_filename_cornercard) as out_file:
            lines = out_file.readlines()
            self.assertEqual(len(lines), 3)
            self.assertEqual(
                lines[0].rstrip("\r\n"),
                "25-01-2018;1;;;IHRE ZAHLUNG;47.11;;")
            self.assertEqual(
                lines[1].rstrip("\r\n"),
                "24-01-2018;1;;;SBB CFF FFS Mobile Tic,Bern;-42.00;;")
            self.assertEqual(
                lines[2].rstrip("\r\n"),
                "09-02-2018;1;;;SOME SHOP,BASEL;-9999.00;;")

    def test_detect_input_format(self):
        self.assertEqual(
            baloise2homebank.detect_input_format(
                "README.md"),
            baloise2homebank.InputFormat.UNKNOWN)
        self.assertEqual(
            baloise2homebank.detect_input_format(
                "testdata/test-input-baloise.csv"),
            baloise2homebank.InputFormat.BALOISE)
        self.assertEqual(
            baloise2homebank.detect_input_format(
                "testdata/test-input-cornercard.csv"),
            baloise2homebank.InputFormat.CORNERCARD)

    def delete_if_exits(self, filename):
        if os.path.isfile(filename):
            os.remove(filename)

    def tearDown(self):
        self.delete_if_exits(self.out_filename_baloise)
        self.delete_if_exits(self.out_filename_cornercard)


if __name__ == "__main__":
    unittest.main()
