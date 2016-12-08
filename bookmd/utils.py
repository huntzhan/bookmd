# -*- coding: utf-8 -*-
from __future__ import (
    division, absolute_import, print_function, unicode_literals,
)
from builtins import *                  # noqa
from future.builtins.disabled import *  # noqa

import re


def load_file(path):
    return open(path, encoding='utf-8').read()


def extract_isbns(path):
    text = load_file(path)

    # isbn10 or isbn13.
    ISBN_PATTERN = r'(?<!\d)(\d{10}|\d{13})(?!\d)'
    isbns = re.findall(ISBN_PATTERN, text)

    return isbns
