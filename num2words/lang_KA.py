# -*- coding: utf-8 -*-
# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

"""Georgian (`ka`) cardinal / ordinal / year / date / time number-to-words.

Georgian uses a vigesimal (base-20) system for 21-99: numbers between
multiples of 20 are constructed as `<base>და<remainder>`, joined as
one word. Multiples of 20 (ოცი 20, ორმოცი 40, სამოცი 60, ოთხმოცი 80)
have their own forms; midpoints (30, 50, 70, 90) are `<base>+10`.

This breaks the EU-template `low/mid/high_numwords` machinery, so we
extend `Num2Word_Base` directly (like Russian) and override
`to_cardinal` with a recursive decomposition that handles vigesimal
explicitly. We rely on the base class only for negative + float
dispatch (the float branch reads digits as `<int> მძიმე <d> <d>`,
the standard Georgian comma-decimal convention).

Ordinals: regular rule is "drop the cardinal's final vowel (ი or ა),
prepend მე, append ე". For compound numbers (21st, 47th, …) only the
last cardinal element is ordinalised; the vigesimal prefix stays.
Compound and high-number forms may need correction by a native
speaker — the test cases are conservative starting points; iterate
based on listening tests + user feedback.
"""

from __future__ import unicode_literals

from .base import Num2Word_Base

ONES = {
    0: 'ნული',
    1: 'ერთი', 2: 'ორი', 3: 'სამი', 4: 'ოთხი',
    5: 'ხუთი', 6: 'ექვსი', 7: 'შვიდი', 8: 'რვა', 9: 'ცხრა',
}

TEENS = {
    10: 'ათი', 11: 'თერთმეტი', 12: 'თორმეტი', 13: 'ცამეტი',
    14: 'თოთხმეტი', 15: 'თხუთმეტი', 16: 'თექვსმეტი',
    17: 'ჩვიდმეტი', 18: 'თვრამეტი', 19: 'ცხრამეტი',
}

# Standalone vigesimal multiples — independent words.
BASE20 = {20: 'ოცი', 40: 'ორმოცი', 60: 'სამოცი', 80: 'ოთხმოცი'}

# Compounding prefix = base20 form with trailing ი dropped + და.
BASE20_PREFIX = {
    20: 'ოცდა', 40: 'ორმოცდა', 60: 'სამოცდა', 80: 'ოთხმოცდა',
}

HUNDREDS = {
    1: 'ასი', 2: 'ორასი', 3: 'სამასი', 4: 'ოთხასი',
    5: 'ხუთასი', 6: 'ექვსასი', 7: 'შვიდასი',
    8: 'რვაასი', 9: 'ცხრაასი',
}

# Standalone first-ordinal is irregular (პირველი). All others follow
# the regular rule (drop final vowel, prepend მე, append ე) including
# compound 1: მეერთე.
ORDINAL_FIRST_STANDALONE = 'პირველი'

MONTHS = {
    1: 'იანვარი', 2: 'თებერვალი', 3: 'მარტი', 4: 'აპრილი',
    5: 'მაისი', 6: 'ივნისი', 7: 'ივლისი', 8: 'აგვისტო',
    9: 'სექტემბერი', 10: 'ოქტომბერი', 11: 'ნოემბერი', 12: 'დეკემბერი',
}

VOWELS = ('ა', 'ე', 'ი', 'ო', 'უ')


def _drop_final_vowel(word):
    """Strip a trailing ი or ა — the Georgian elision rule used both
    when compounding cardinals (`ორასი` → `ორას` before a remainder)
    and when forming ordinals (`ერთი` → `ერთ`, `რვა` → `რვ`)."""
    if word and word[-1] in ('ი', 'ა'):
        return word[:-1]
    return word


def _ordinalise(word):
    """Regular ordinal: drop final vowel, prepend მე, append ე."""
    return 'მე' + _drop_final_vowel(word) + 'ე'


class Num2Word_KA(Num2Word_Base):
    def setup(self):
        self.negword = "მინუს"
        self.pointword = "მძიმე"
        self.errmsg_nonnum = "მხოლოდ რიცხვის გადაყვანაა შესაძლებელი"
        self.errmsg_floatord = "ნაწილადის რიგობითი ფორმა არ არსებობს: %s"
        self.errmsg_negord = "უარყოფითი რიცხვის რიგობითი ფორმა არ არსებობს: %s"
        self.errmsg_toobig = "abs(%s) უნდა იყოს %s-ზე ნაკლები"
        # Up to 999_999_999_999. Trillions+ raise OverflowError; rare
        # in article TTS, and a clear error beats a silently-wrong word.
        self.MAXVAL = 10 ** 12

    # ----- cardinals --------------------------------------------------

    def _under_100(self, n):
        if n < 10:
            return ONES[n]
        if n < 20:
            return TEENS[n]
        # vigesimal: base in {20, 40, 60, 80}, remainder r in [0, 19].
        base = (n // 20) * 20
        r = n - base
        if r == 0:
            return BASE20[base]
        # 21..29 / 41..49 / …: prefix + ONES[r]; clean compound, one word.
        if r < 10:
            return BASE20_PREFIX[base] + ONES[r]
        # 30, 31..39 / 50, 51..59 / …: prefix + TEENS[r] (TEENS[10] = ათი
        # gives the +10 form for free — ოცდა + ათი = ოცდაათი).
        return BASE20_PREFIX[base] + TEENS[r]

    def _under_1000(self, n):
        h, r = divmod(n, 100)
        if h == 0:
            return self._under_100(r)
        if r == 0:
            return HUNDREDS[h]
        # ორასი → ორას; then space + remainder.
        return _drop_final_vowel(HUNDREDS[h]) + ' ' + self._under_100(r)

    def _scale(self, n, divisor, scale_word):
        """Common shape for thousands / millions / billions.

        n           input number
        divisor     1_000 / 1_000_000 / 1_000_000_000
        scale_word  'ათასი' / 'მილიონი' / 'მილიარდი'
        """
        count, remainder = divmod(n, divisor)
        if count == 1:
            head = scale_word
        else:
            head = self._stringify(count) + ' ' + scale_word
        if remainder == 0:
            return head
        # Drop the trailing ი of scale_word (last char of head).
        return _drop_final_vowel(head) + ' ' + self._stringify(remainder)

    def _stringify(self, n):
        if n < 100:
            return self._under_100(n)
        if n < 1000:
            return self._under_1000(n)
        if n < 1_000_000:
            return self._scale(n, 1000, 'ათასი')
        if n < 1_000_000_000:
            return self._scale(n, 1_000_000, 'მილიონი')
        return self._scale(n, 1_000_000_000, 'მილიარდი')

    def to_cardinal(self, value):
        try:
            assert int(value) == value
        except (ValueError, TypeError, AssertionError):
            return self.to_cardinal_float(value)

        n = int(value)
        if n < 0:
            return self.negword + ' ' + self.to_cardinal(-n)
        if n >= self.MAXVAL:
            raise OverflowError(self.errmsg_toobig % (n, self.MAXVAL))
        return self._stringify(n)

    # ----- ordinals ---------------------------------------------------

    def to_ordinal(self, value):
        self.verify_ordinal(value)
        n = int(value)

        # Standalone "1st" is irregular; compound 1 (e.g. 21st) uses
        # the regular მეერთე form.
        if n == 1:
            return ORDINAL_FIRST_STANDALONE

        # Numbers expressible as a single Georgian cardinal "word"
        # (1-19; 20/40/60/80; 100/200/…/900; bare scale words like
        # ათასი/მილიონი) ordinalise in place via the regular rule.
        if n < 20:
            return _ordinalise(self._under_100(n))
        if n < 100 and n % 20 == 0:  # 20, 40, 60, 80
            return _ordinalise(BASE20[n])
        if n < 1000 and n % 100 == 0:  # 100, 200, ..., 900
            return _ordinalise(HUNDREDS[n // 100])
        if n in (1000, 1_000_000, 1_000_000_000):
            scale = {1000: 'ათასი', 1_000_000: 'მილიონი',
                     1_000_000_000: 'მილიარდი'}[n]
            return _ordinalise(scale)

        # Compound numbers: ordinalise only the last cardinal element.
        # Splitting strategies differ by shape:
        #   21..99 (non-base20 multiples) → cardinal is one word
        #     (e.g., ოცდაერთი). The "last element" is the ONES[r] or
        #     TEENS[r] suffix; insert მე at the boundary.
        #   100+ → cardinal has spaces; ordinalise the whitespace-last
        #     word, leave the rest alone.
        if n < 100:
            base = (n // 20) * 20
            r = n - base
            tail = TEENS[r] if r >= 10 else ONES[r]
            # Compound 1: regular მეერთე (NOT პირველი). Same rule.
            return BASE20_PREFIX[base] + _ordinalise(tail)
        # Multi-word: split, ordinalise last word, rejoin.
        head, _, last = self.to_cardinal(n).rpartition(' ')
        return head + ' ' + _ordinalise(last) if head else _ordinalise(last)

    def to_ordinal_num(self, value):
        self.verify_ordinal(value)
        # "მე-5" — the standard Georgian written form for ordinal numerals.
        return 'მე-%d' % int(value)

    # ----- morphology (public — used by TTS text normalization) -------
    #
    # Georgian has two distinct elision rules, and _drop_final_vowel
    # above implements neither of them: it is the *compounding* rule
    # (ორასი → ორას before a remainder, ერთი → ერთ inside ordinals).
    # Attributive position keeps ა (რვა საათზე, never რვ საათზე),
    # while vowel-initial suffixes elide any final vowel (რვა → რვის).

    def stem_attr(self, word):
        """Attributive stem: a numeral before a case-marked noun (or a
        noun before a consonant-initial suffix) drops a final ი but
        keeps other vowels — ხუთი→ხუთ, წუთი→წუთ, but რვა→რვა, მეოცე→მეოცე."""
        if word.endswith('ი'):
            return word[:-1]
        return word

    def stem_vowel(self, word):
        """Stem before a vowel-initial suffix: any final vowel elides —
        ხუთი+ის→ხუთის, რვა+ის→რვის, მეოცე+ის→მეოცის."""
        if word and word[-1] in VOWELS:
            return word[:-1]
        return word

    def join_suffix(self, word, suffix):
        """Join a spoken word with a Georgian case suffix or particle,
        picking the stem by whether the suffix starts with a vowel."""
        if not suffix:
            return word
        if suffix[0] in VOWELS:
            return self.stem_vowel(word) + suffix
        return self.stem_attr(word) + suffix

    def attr_cardinal(self, value):
        """Cardinal in attributive position — only the last word stems:
        17 → ჩვიდმეტ, 110 → ას ათ (not ას ათ*ი*), 8 → რვა."""
        head, _, last = self.to_cardinal(value).rpartition(' ')
        stemmed = self.stem_attr(last)
        return head + ' ' + stemmed if head else stemmed

    # ----- dates & times ----------------------------------------------

    def to_date(self, day, month, year):
        """Spoken date in broadcast order: '<year> წლის <day> <month>'.
        Day 1 is the ordinal პირველი; every other day is a cardinal
        (ოთხი ივლისი, ოცდაექვსი მაისი)."""
        day, month, year = int(day), int(month), int(year)
        if not 1 <= day <= 31:
            raise ValueError('day out of range: %d' % day)
        if month not in MONTHS:
            raise ValueError('month out of range: %d' % month)
        day_word = (ORDINAL_FIRST_STANDALONE if day == 1
                    else self.to_cardinal(day))
        return '%s წლის %s %s' % (
            self.to_cardinal(year), day_word, MONTHS[month])

    def to_time(self, hour, minute, second=None, suffix=None):
        """Spoken clock time.

        Without ``suffix`` the form is nominative: 17:35 → 'ჩვიდმეტი
        საათი და ოცდათხუთმეტი წუთი'. With ``suffix`` (e.g. 'ზე' from a
        following 'საათზე' in the source text) the case lands on the
        last unit and earlier units take the linking dative '-სა':
        'ჩვიდმეტ საათსა და ოცდათხუთმეტ წუთზე'; 17:00 → 'ჩვიდმეტ საათზე'.
        """
        hour, minute = int(hour), int(minute)
        if not 0 <= hour <= 23:
            raise ValueError('hour out of range: %d' % hour)
        if not 0 <= minute <= 59:
            raise ValueError('minute out of range: %d' % minute)
        if second is not None:
            second = int(second)
            if not 0 <= second <= 59:
                raise ValueError('second out of range: %d' % second)

        units = [(hour, 'საათი')]
        if minute or second:
            units.append((minute, 'წუთი'))
        if second:
            units.append((second, 'წამი'))

        if suffix is None:
            parts = ['%s %s' % (self.to_cardinal(n), noun)
                     for n, noun in units]
        else:
            parts = []
            for i, (n, noun) in enumerate(units):
                if i < len(units) - 1:
                    unit = self.stem_attr(noun) + 'სა'
                else:
                    unit = self.join_suffix(noun, suffix)
                parts.append('%s %s' % (self.attr_cardinal(n), unit))

        if len(parts) == 1:
            return parts[0]
        return ', '.join(parts[:-1]) + ' და ' + parts[-1]

    # to_year / to_currency / pluralize: defaults are fine. Georgian
    # reads years as plain cardinals (no "nineteen ninety-nine"
    # convention), so Num2Word_Base.to_year delegating to to_cardinal
    # is correct.
