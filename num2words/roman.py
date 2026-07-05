# -*- coding: utf-8 -*-
# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

"""Strict Roman-numeral parsing (language-agnostic).

Used by TTS text normalization to turn tokens like ``IX`` into numbers
a language converter can verbalize (typically as ordinals: Georgian
``IX საუკუნე`` → ``მეცხრე საუკუნე``). Only canonical uppercase forms
are accepted — ``IIII``, ``VX``, lowercase, or mixed garbage raise
``ValueError`` — so callers can safely fall through on anything that
merely *looks* Roman.
"""

from __future__ import unicode_literals

import re

_ROMAN_RE = re.compile(
    r'^(M{0,3})(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$')

_VALUES = [
    ('M', 1000), ('CM', 900), ('D', 500), ('CD', 400),
    ('C', 100), ('XC', 90), ('L', 50), ('XL', 40),
    ('X', 10), ('IX', 9), ('V', 5), ('IV', 4), ('I', 1),
]


def roman_to_int(token):
    """Parse a canonical Roman numeral into an int (``'IX'`` → ``9``)."""
    if not token or not _ROMAN_RE.match(token):
        raise ValueError('not a canonical Roman numeral: %r' % (token,))
    i, total = 0, 0
    for symbol, value in _VALUES:
        while token.startswith(symbol, i):
            total += value
            i += len(symbol)
    return total
