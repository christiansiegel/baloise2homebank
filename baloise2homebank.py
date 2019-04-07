#! /usr/bin/env python

import argparse
import csv
import os
from datetime import datetime


class BaloiseDialect(csv.Dialect):
    delimiter = ";"
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


def convert_csv(in_filename, out_filename):
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
                writer.writerow({
                    "date": convert_to_homebank_date(row["valuta"], "%d.%m.%Y"),
                    "paymode": 8,  # = Electronic Payment
                    "memo": row["buchungstext"].strip(),
                    "amount": row["gutschrift"] if row["gutschrift"] else "-" + row["belastung"]
                })


def append_to_filename(filename, text):
    root, ext = os.path.splitext(filename)
    return root + text + ext


def convert_to_homebank_date(date_string, input_format):
    date = datetime.strptime(date_string, input_format)
    return date.strftime("%d-%m-%Y")


def main():
    parser = argparse.ArgumentParser(
        description="Convert a Baloise Bank SoBa CSV export file to the Homebank CSV format.")
    parser.add_argument("filename", help="The CSV file to convert.")
    args = parser.parse_args()

    in_filename = args.filename
    out_filename = append_to_filename(in_filename, "-homebank")
    convert_csv(in_filename, out_filename)

    print("Baloise Bank SoBa file converted. Output file: '%s'" % out_filename)


if __name__ == "__main__":
    main()
