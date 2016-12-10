# -*- coding: utf-8 -*-
from __future__ import (
    division, absolute_import, print_function, unicode_literals,
)
from builtins import *                  # noqa
from future.builtins.disabled import *  # noqa

from functools import wraps

import click

click.disable_unicode_literals_warning = True


def enable_profile(func):
    import cProfile

    @click.option('--profile/--no-profile', default=False)
    @wraps(func)
    def wrapper(profile, *args, **kwargs):
        if profile:
            cProfile.runctx(
                'func(*args, **kwargs)', globals(), locals(),
                sort='cumtime',
            )
        else:
            return func(*args, **kwargs)

    return wrapper


_click_command = click.command


def click_command_with_profile(*args, **kwargs):

    def decorator(func):
        click_func = _click_command(*args, **kwargs)
        return click_func(enable_profile(func))

    return decorator


click.command = wraps(_click_command)(click_command_with_profile)
