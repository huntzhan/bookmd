# -*- coding: utf-8 -*-
from __future__ import (
    division, absolute_import, print_function, unicode_literals,
)
from builtins import *                  # noqa
from future.builtins.disabled import *  # noqa

import os
from bookmd.db import BookDBManager
from bookmd.utils import replace_all_dsl, extract_default_template


def test_simple():
    db_manager = BookDBManager(os.getcwd())
    db_manager.isbn2book = {
        '123': {
            'a': 'test 1',
            'b': {
                'c': 'nested',
            }
        },
        '234': {
            'a': 'test 2',
        }
    }

    text = (
        'mark 1 {{ isbn = "123" template = "{a} {b[c]} " }}'
        'mark 2 {{ isbn = "234" template = "{a}" }}'
    )

    ret = replace_all_dsl(text, db_manager)
    assert ret == 'mark 1 test 1 nested mark 2 test 2'


def test_extract_default_template():
    text = (
        'faefajeifajeig '
        '<!--  bookmd-default-template  : "abc"-->'
        'afjeaifajeif'
    )
    a, b = extract_default_template(text)
    assert 'bookmd' not in a
    assert 'abc' == b

    text = 'afjeifjaeif'
    a, b = extract_default_template(text)
    assert a == text
    assert b is None
