# baloise2homebank

[![Build Status](https://travis-ci.com/christiansiegel/baloise2homebank.svg?branch=master)](https://travis-ci.com/christiansiegel/baloise2homebank)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-green.svg)](https://www.python.org/dev/peps/pep-0008/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)
[![gitpod-IDE](https://img.shields.io/badge/open--IDE-as--gitpod-blue.svg?style=flat&label=openIDE)](https://gitpod.io#https://github.com/christiansiegel/baloise2homebank)

Convert CSV account reports exported from [Baloise Bank SoBa](http://www.baloise.ch/) online banking or their credit card partner [Cornèrcard](https://www.cornercard.ch/) to a format that can be imported by the free personal finance software [Homebank](http://homebank.free.fr/).

# Usage

## Automatically detect input format

```bash
# python baloise2homebank.py my-exported-file.csv
```

## Force Baloise Bank SoBa cash account

```bash
# python baloise2homebank.py --baloise my-exported-file.csv
```

## Force Cornèrcard credit card account

```bash
# python baloise2homebank.py --cornercard my-exported-file.csv
```

# Run tests

```bash
# pytest
```
or
```bash
# python test_baloise2homebank.py
```
