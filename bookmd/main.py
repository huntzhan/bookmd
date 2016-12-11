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

from .db import db_manager
from .utils import (
    extract_isbns_from_directory,
    replace_all_dsl,
    load_file,
    write_file,
    generate_list,
    generate_table,
)


def dirpath(dirname):
    return join(getcwd(), dirname)


ISBN_DIRPATH = dirpath('isbn')
BOOK_DATABASE = dirpath('.bookmd-db')


@click.command()
def init():
    # directories.
    for path in [ISBN_DIRPATH, BOOK_DATABASE]:
        if not exists(path):
            mkdir(path)


@click.command()
@db_manager(BOOK_DATABASE)
def query(db_manager):
    isbns = extract_isbns_from_directory(ISBN_DIRPATH)
    db_manager.books(isbns)


@click.command()
@click.argument('form')
@click.option('--keys', default=None)
@click.argument('dst', type=click.Path())
@db_manager(BOOK_DATABASE)
def template(db_manager, form, keys, dst):
    FORM_GENERATOR = {
        'list': generate_list,
        'table': generate_table,
    }

    if form not in FORM_GENERATOR:
        raise RuntimeError('invalid form.')

    write_file(dst, FORM_GENERATOR[form](db_manager.isbn2book, keys))


@click.command()
@click.argument('src', type=click.Path(exists=True))
@click.argument('dst', type=click.Path())
@db_manager(BOOK_DATABASE)
def transform(db_manager, src, dst):
    text = load_file(src)
    processed = replace_all_dsl(text, db_manager)
    write_file(dst, processed)


@click.group()
def entry_point():
    pass


entry_point.add_command(init)
entry_point.add_command(query)
entry_point.add_command(template)
entry_point.add_command(transform)
