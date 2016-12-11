# -*- coding: utf-8 -*-
from __future__ import (
    division, absolute_import, print_function, unicode_literals,
)
from builtins import *                  # noqa
from future.builtins.disabled import *  # noqa

import json
from os.path import basename, join
from functools import wraps

from .utils import (
    load_directory,
    load_file,
    write_file,
)
from .douban import (
    query_single_book,
    query_books_with_retry,
)


EXT = '.json'


def load_book_cache(path):
    return json.loads(load_file(path))


def dump_book_cache(path, obj):
    data = json.dumps(obj, sort_keys=True, indent=4)
    if isinstance(data, bytes):
        data = data.decode('utf-8')
    write_file(path, data)


def extract_isbn_from_name(name):
    return name[:-len(EXT)]


def isbn2name(name):
    return '{0}.json'.format(name)


# [isbn10 | isbn13].json
def validate_name(name):
    if not name.endswith(EXT):
        return False
    else:
        prefix = extract_isbn_from_name(name)
        return prefix.isdigit() and len(prefix) in (10, 13)


class BookDBManager(object):

    def __init__(self, dirpath):
        self.dirpath = dirpath

        self.isbn2book = {}
        self.new_isbns = []

        self.load_book_db()

    def load_book_db(self):
        for path in load_directory(self.dirpath, validate_name):
            name = basename(path)
            isbn = extract_isbn_from_name(name)

            self.isbn2book[isbn] = load_book_cache(path)

    def update_book_db(self):
        for isbn in self.new_isbns:
            dump_book_cache(
                join(self.dirpath, isbn2name(isbn)),
                self.isbn2book[isbn],
            )

    def book(self, isbn):
        if isbn not in self.isbn2book:
            self.isbn2book[isbn] = query_single_book(isbn)
            self.new_isbns.append(isbn)

        return self.isbn2book[isbn]

    def books(self, isbns):
        new_isbns = list(filter(
            lambda isbn: isbn not in self.isbn2book,
            isbns,
        ))

        ret = query_books_with_retry(new_isbns)
        not_found_isbns, request_error_isbns, new_isbn2book = ret

        if not_found_isbns:
            raise RuntimeError('not_found_isbns')
        if request_error_isbns:
            raise RuntimeError('request_error_isbns')

        self.isbn2book.update(new_isbn2book)
        self.new_isbns.extend(new_isbns)

        return map(self.isbn2book.get, isbns)


def db_manager(dirpath):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            db_manager = BookDBManager(dirpath)
            func(db_manager, *args, **kwargs)
            db_manager.update_book_db()

        return wrapper

    return decorator
