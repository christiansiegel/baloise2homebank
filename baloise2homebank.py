#! /usr/bin/env python

import argparse
import csv
import os
import re
import sys
from datetime import datetime


class InputFormat(object):
    UNKNOWN = 0
    BALOISE = 1
    CORNERCARD = 2


class BaloiseDialect(csv.Dialect):
    delimiter = ";"
    quotechar = "\""
    doublequote = False
    skipinitialspace = False
    lineterminator = "\r\n"
    quoting = csv.QUOTE_MINIMAL


class CornercardDialect(csv.Dialect):
    delimiter = ","
    quotechar = "\""
    doublequote = False
    skipinitialspace = False
    lineterminator = "\r\n"
    quoting = csv.QUOTE_MINIMAL


class HomebankDialect(csv.Dialect):
    delimiter = ";"
    quotechar = "\""
    doublequote = True
    skipinitialspace = False
    lineterminator = "\r\n"
    quoting = csv.QUOTE_MINIMAL


baloise_fieldnames = [
    "datum",
    "valuta",
    "buchungstext",
    "belastung",
    "gutschrift",
    "saldo_chf"
    "kontonummer",
    "kontoinhaber"
]


cornercard_fieldnames = [
    "datum",
    "beschreibung",
    "belastung",
    "gutschrift",
    "kartennummer"
    "karteninhaber"
]


homebank_fieldnames = [
    "date",
    "paymode",
    "info",
    "payee",
    "memo",
    "amount",
    "category",
    "tags"
]


def convert_baloise_csv(in_filename, out_filename):
    with open(in_filename, "r") as in_file:
        lines = in_file.readlines()
        transaction_lines = lines[1:]

        reader = csv.DictReader(
            transaction_lines,
            dialect=BaloiseDialect,
            fieldnames=baloise_fieldnames)

        with open(out_filename, "w") as out_file:
            writer = csv.DictWriter(
                out_file,
                dialect=HomebankDialect,
                fieldnames=homebank_fieldnames)
            for row in reader:
                date = convert_to_homebank_date(row["valuta"], "%d.%m.%Y")
                paymode = 8  # = Electronic Payment
                memo = row["buchungstext"].strip()
                if row["gutschrift"]:
                    amount = row["gutschrift"]
                else:
                    amount = "-" + row["belastung"]
                writer.writerow({
                    "date": date,
                    "paymode": paymode,
                    "memo": memo,
                    "amount": amount
                })


def convert_cornercard_csv(in_filename, out_filename):
    with open(in_filename, "r") as in_file:
        lines = in_file.readlines()
        transaction_lines = [
            l for l in lines if re.match(r"^\d{2}/\d{2}/\d{4}", l)
        ]

        reader = csv.DictReader(
            transaction_lines,
            dialect=CornercardDialect,
            fieldnames=cornercard_fieldnames)

        with open(out_filename, "w") as out_file:
            writer = csv.DictWriter(
                out_file,
                dialect=HomebankDialect,
                fieldnames=homebank_fieldnames)
            for row in reader:
                date = convert_to_homebank_date(row["datum"], "%d/%m/%Y")
                paymode = 1  # = Credit Card
                memo = row["beschreibung"].strip()
                if row["gutschrift"]:
                    amount = row["gutschrift"].replace(",", "")
                else:
                    amount = "-" + row["belastung"].replace(",", "")
                writer.writerow({
                    "date": date,
                    "paymode": paymode,
                    "memo": memo,
                    "amount": amount
                })


def detect_input_format(in_filename):
    with open(in_filename, "r") as in_file:
        first_line = in_file.readline()
        if "Datum;Valuta;Buchungstext;Belastung;Gutschrift" in first_line:
            return InputFormat.BALOISE
        if "Datum,Beschreibung,Belastung CHF,Gutschrift" in first_line:
            return InputFormat.CORNERCARD
    return InputFormat.UNKNOWN


def append_to_filename(filename, text):
    root, ext = os.path.splitext(filename)
    return root + text + ext


def convert_to_homebank_date(date_string, input_format):
    date = datetime.strptime(date_string, input_format)
    return date.strftime("%d-%m-%Y")


def main():
    parser = argparse.ArgumentParser(
        description="Convert a Baloise Bank SoBa or Cornercard CSV "
                    "export file to the Homebank CSV format.")
    parser.add_argument("filename", help="The CSV file to convert.")

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-a", "--auto", action="store_true",
        help="automatically detect input format (default)")
    group.add_argument(
        "-b", "--baloise", action="store_true",
        help="convert a Baloise Bank SoBa cash account CSV file")
    group.add_argument(
        "-c", "--cornercard", action="store_true",
        help="convert a Cornercard credit card account CSV file")

    parser.set_defaults(auto=True)
    args = parser.parse_args()

    in_filename = args.filename
    out_filename = append_to_filename(in_filename, "-homebank")

    detected_format = detect_input_format(in_filename)

    if args.baloise:
        if detected_format is not InputFormat.BALOISE:
            print("Warning: Detected input file does not match --baloise!")
        convert_baloise_csv(in_filename, out_filename)
        print("Baloise Bank SoBa file converted. "
              "Output file: '%s'" % out_filename)
    elif args.cornercard:
        if detected_format is not InputFormat.CORNERCARD:
            print("Warning: Detected input file does not match --cornercard!")
        convert_cornercard_csv(in_filename, out_filename)
        print("Cornercard file converted. "
              "Output file: '%s'" % out_filename)
    elif args.auto and detected_format is InputFormat.BALOISE:
        convert_baloise_csv(in_filename, out_filename)
        print("Baloise Bank SoBa file detected and converted. "
              "Output file: '%s'" % out_filename)
    elif args.auto and detected_format is InputFormat.CORNERCARD:
        convert_cornercard_csv(in_filename, out_filename)
        print("Cornercard file detected and converted. "
              "Output file: '%s'" % out_filename)
    else:
        print("Unknown input format!")
        sys.exit(1)


if __name__ == "__main__":
    main()
