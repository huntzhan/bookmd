# -*- coding: utf-8 -*-
from __future__ import (
    division, absolute_import, print_function, unicode_literals,
)
from builtins import *                  # noqa
from future.builtins.disabled import *  # noqa

from os import getcwd, mkdir
from os.path import join, exists

import click
import bookmd.click_patch  # noqa

from .douban import query_books_with_retry
from .utils import (
    extract_isbns_from_directory,
    load_book_cache,
    dump_book_cache,
    replace_all_dsl,
    load_file,
    write_file,
    generate_list,
    generate_table,
)


ISBN_DIRNAME = 'isbn'
BOOK_DATABASE = '.bookmd-db'
BOOK_CACHE = 'bookmd.json'


def dirpath(dirname):
    return join(getcwd(), dirname)


def database_path(name):
    return join(dirpath(BOOK_DATABASE), name)


@click.command()
def init():
    # directories.
    for path in map(lambda dirname: dirpath(dirname),
                    [ISBN_DIRNAME, BOOK_DATABASE]):
        if not exists(path):
            mkdir(path)

    # files.
    BOOK_CACHE_PATH = database_path(BOOK_CACHE)
    if not exists(BOOK_CACHE_PATH):
        dump_book_cache(BOOK_CACHE_PATH, {})


@click.command()
def query():
    ISBN_DIRPATH = dirpath(ISBN_DIRNAME)
    BOOK_CACHE_PATH = database_path(BOOK_CACHE)

    isbns = extract_isbns_from_directory(ISBN_DIRPATH)
    isbn2book = load_book_cache(BOOK_CACHE_PATH)

    new_isbns = filter(
        lambda isbn: isbn not in isbn2book,
        isbns,
    )
    ret = query_books_with_retry(new_isbns)
    not_found_isbns, request_error_isbns, new_isbn2book = ret

    if not_found_isbns:
        raise RuntimeError('not_found_isbns')
    if request_error_isbns:
        raise RuntimeError('request_error_isbns')

    isbn2book.update(new_isbn2book)
    dump_book_cache(BOOK_CACHE_PATH, isbn2book)


@click.command()
@click.argument('form')
@click.option('--keys', default=None)
@click.argument('dst', type=click.Path())
def template(form, keys, dst):
    BOOK_CACHE_PATH = database_path(BOOK_CACHE)
    isbn2book = load_book_cache(BOOK_CACHE_PATH)

    FORM_GENERATOR = {
        'list': generate_list,
        'table': generate_table,
    }

    if form not in FORM_GENERATOR:
        raise RuntimeError('invalid form.')

    write_file(dst, FORM_GENERATOR[form](isbn2book, keys))


@click.command()
@click.argument('src', type=click.Path(exists=True))
@click.argument('dst', type=click.Path())
def transform(src, dst):
    BOOK_CACHE_PATH = database_path(BOOK_CACHE)

    text = load_file(src)
    isbn2book = load_book_cache(BOOK_CACHE_PATH)

    processed = replace_all_dsl(text, isbn2book)

    write_file(dst, processed)


@click.group()
def entry_point():
    pass


entry_point.add_command(init)
entry_point.add_command(query)
entry_point.add_command(template)
entry_point.add_command(transform)
