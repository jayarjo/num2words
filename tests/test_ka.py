# -*- coding: utf-8 -*-
# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from __future__ import unicode_literals

from unittest import TestCase

from num2words import num2words


class Num2WordsKATest(TestCase):
    """Georgian (`ka`) number-to-words conversion."""

    # ----- cardinals --------------------------------------------------

    def test_zero_and_units(self):
        self.assertEqual(num2words(0, lang="ka"), "ნული")
        self.assertEqual(num2words(1, lang="ka"), "ერთი")
        self.assertEqual(num2words(2, lang="ka"), "ორი")
        self.assertEqual(num2words(3, lang="ka"), "სამი")
        self.assertEqual(num2words(4, lang="ka"), "ოთხი")
        self.assertEqual(num2words(5, lang="ka"), "ხუთი")
        self.assertEqual(num2words(6, lang="ka"), "ექვსი")
        self.assertEqual(num2words(7, lang="ka"), "შვიდი")
        self.assertEqual(num2words(8, lang="ka"), "რვა")
        self.assertEqual(num2words(9, lang="ka"), "ცხრა")

    def test_teens(self):
        self.assertEqual(num2words(10, lang="ka"), "ათი")
        self.assertEqual(num2words(11, lang="ka"), "თერთმეტი")
        self.assertEqual(num2words(12, lang="ka"), "თორმეტი")
        self.assertEqual(num2words(15, lang="ka"), "თხუთმეტი")
        self.assertEqual(num2words(19, lang="ka"), "ცხრამეტი")

    def test_vigesimal_bases(self):
        self.assertEqual(num2words(20, lang="ka"), "ოცი")
        self.assertEqual(num2words(40, lang="ka"), "ორმოცი")
        self.assertEqual(num2words(60, lang="ka"), "სამოცი")
        self.assertEqual(num2words(80, lang="ka"), "ოთხმოცი")

    def test_vigesimal_plus_ten(self):
        # Mid-decade forms — base + 10.
        self.assertEqual(num2words(30, lang="ka"), "ოცდაათი")
        self.assertEqual(num2words(50, lang="ka"), "ორმოცდაათი")
        self.assertEqual(num2words(70, lang="ka"), "სამოცდაათი")
        self.assertEqual(num2words(90, lang="ka"), "ოთხმოცდაათი")

    def test_vigesimal_compounds(self):
        self.assertEqual(num2words(21, lang="ka"), "ოცდაერთი")
        self.assertEqual(num2words(25, lang="ka"), "ოცდახუთი")
        self.assertEqual(num2words(31, lang="ka"), "ოცდათერთმეტი")
        self.assertEqual(num2words(35, lang="ka"), "ოცდათხუთმეტი")
        self.assertEqual(num2words(47, lang="ka"), "ორმოცდაშვიდი")
        self.assertEqual(num2words(58, lang="ka"), "ორმოცდათვრამეტი")
        self.assertEqual(num2words(99, lang="ka"), "ოთხმოცდაცხრამეტი")

    def test_hundreds(self):
        self.assertEqual(num2words(100, lang="ka"), "ასი")
        self.assertEqual(num2words(101, lang="ka"), "ას ერთი")
        self.assertEqual(num2words(200, lang="ka"), "ორასი")
        self.assertEqual(num2words(247, lang="ka"), "ორას ორმოცდაშვიდი")
        self.assertEqual(num2words(500, lang="ka"), "ხუთასი")
        self.assertEqual(num2words(900, lang="ka"), "ცხრაასი")
        self.assertEqual(num2words(999, lang="ka"), "ცხრაას ოთხმოცდაცხრამეტი")

    def test_thousands(self):
        self.assertEqual(num2words(1000, lang="ka"), "ათასი")
        self.assertEqual(num2words(1001, lang="ka"), "ათას ერთი")
        self.assertEqual(num2words(1234, lang="ka"), "ათას ორას ოცდათოთხმეტი")
        self.assertEqual(num2words(2000, lang="ka"), "ორი ათასი")
        self.assertEqual(num2words(2024, lang="ka"), "ორი ათას ოცდაოთხი")
        # Year-shaped — to_year delegates to to_cardinal in Georgian.
        self.assertEqual(
            num2words(1999, lang="ka"),
            "ათას ცხრაას ოთხმოცდაცხრამეტი",
        )

    def test_millions_and_billions(self):
        self.assertEqual(num2words(1_000_000, lang="ka"), "მილიონი")
        self.assertEqual(num2words(2_000_000, lang="ka"), "ორი მილიონი")
        self.assertEqual(num2words(1_000_000_000, lang="ka"), "მილიარდი")

    def test_negative(self):
        self.assertEqual(num2words(-5, lang="ka"), "მინუს ხუთი")
        self.assertEqual(num2words(-1, lang="ka"), "მინუს ერთი")

    def test_decimal(self):
        # Comma-decimal convention: "<int> მძიმე <digit> <digit>…"
        self.assertEqual(num2words(3.14, lang="ka"), "სამი მძიმე ერთი ოთხი")

    def test_overflow(self):
        from num2words.lang_KA import Num2Word_KA
        n2w = Num2Word_KA()
        with self.assertRaises(OverflowError):
            n2w.to_cardinal(10**13)

    # ----- ordinals ---------------------------------------------------

    def test_ordinal_first_irregular(self):
        # Standalone 1st is the only irregular form.
        self.assertEqual(num2words(1, lang="ka", to="ordinal"), "პირველი")

    def test_ordinal_units(self):
        self.assertEqual(num2words(2, lang="ka", to="ordinal"), "მეორე")
        self.assertEqual(num2words(3, lang="ka", to="ordinal"), "მესამე")
        self.assertEqual(num2words(5, lang="ka", to="ordinal"), "მეხუთე")
        self.assertEqual(num2words(7, lang="ka", to="ordinal"), "მეშვიდე")
        self.assertEqual(num2words(8, lang="ka", to="ordinal"), "მერვე")
        self.assertEqual(num2words(9, lang="ka", to="ordinal"), "მეცხრე")

    def test_ordinal_teens_and_tens(self):
        self.assertEqual(num2words(10, lang="ka", to="ordinal"), "მეათე")
        self.assertEqual(num2words(15, lang="ka", to="ordinal"), "მეთხუთმეტე")
        self.assertEqual(num2words(20, lang="ka", to="ordinal"), "მეოცე")
        self.assertEqual(num2words(40, lang="ka", to="ordinal"), "მეორმოცე")

    def test_ordinal_compound_under_100(self):
        # Compound 21st: regular მეერთე for the last element (NOT the
        # standalone-irregular პირველი).
        self.assertEqual(num2words(21, lang="ka", to="ordinal"), "ოცდამეერთე")
        self.assertEqual(num2words(47, lang="ka", to="ordinal"), "ორმოცდამეშვიდე")

    def test_ordinal_hundred_and_thousand(self):
        self.assertEqual(num2words(100, lang="ka", to="ordinal"), "მეასე")
        self.assertEqual(num2words(1000, lang="ka", to="ordinal"), "მეათასე")
        self.assertEqual(num2words(1_000_000, lang="ka", to="ordinal"), "მემილიონე")

    def test_ordinal_num(self):
        self.assertEqual(num2words(1, lang="ka", to="ordinal_num"), "მე-1")
        self.assertEqual(num2words(5, lang="ka", to="ordinal_num"), "მე-5")
        self.assertEqual(num2words(21, lang="ka", to="ordinal_num"), "მე-21")

    def test_to_year_is_cardinal(self):
        # Georgian doesn't use English's "nineteen ninety-nine" pair convention.
        self.assertEqual(
            num2words(2024, lang="ka", to="year"),
            num2words(2024, lang="ka"),
        )

    # ----- morphology helpers ------------------------------------------

    def _ka(self):
        from num2words import CONVERTER_CLASSES
        return CONVERTER_CLASSES["ka"]

    def test_stem_attr_drops_final_i_keeps_a(self):
        ka = self._ka()
        self.assertEqual(ka.stem_attr("ხუთი"), "ხუთ")
        self.assertEqual(ka.stem_attr("წუთი"), "წუთ")
        self.assertEqual(ka.stem_attr("რვა"), "რვა")
        self.assertEqual(ka.stem_attr("მეოცე"), "მეოცე")

    def test_stem_vowel_drops_any_final_vowel(self):
        ka = self._ka()
        self.assertEqual(ka.stem_vowel("ხუთი"), "ხუთ")
        self.assertEqual(ka.stem_vowel("რვა"), "რვ")
        self.assertEqual(ka.stem_vowel("მეოცე"), "მეოც")

    def test_join_suffix_consonant_initial(self):
        ka = self._ka()
        self.assertEqual(ka.join_suffix("ხუთი", "ზე"), "ხუთზე")
        self.assertEqual(ka.join_suffix("რვა", "ს"), "რვას")
        self.assertEqual(ka.join_suffix("მეოცე", "ში"), "მეოცეში")
        self.assertEqual(ka.join_suffix("საათი", "ზე"), "საათზე")

    def test_join_suffix_vowel_initial(self):
        ka = self._ka()
        self.assertEqual(ka.join_suffix("სამი", "ის"), "სამის")
        self.assertEqual(ka.join_suffix("რვა", "ის"), "რვის")
        self.assertEqual(ka.join_suffix("მეოცე", "ის"), "მეოცის")
        self.assertEqual(ka.join_suffix("საათი", "ამდე"), "საათამდე")

    def test_attr_cardinal_stems_last_word_only(self):
        ka = self._ka()
        self.assertEqual(ka.attr_cardinal(17), "ჩვიდმეტ")
        self.assertEqual(ka.attr_cardinal(8), "რვა")
        self.assertEqual(ka.attr_cardinal(110), "ას ათ")

    # ----- dates -------------------------------------------------------

    def test_to_date_broadcast_order(self):
        ka = self._ka()
        self.assertEqual(
            ka.to_date(4, 7, 2026),
            "ორი ათას ოცდაექვსი წლის ოთხი ივლისი",
        )

    def test_to_date_day_one_is_ordinal(self):
        ka = self._ka()
        self.assertEqual(
            ka.to_date(1, 1, 2025),
            "ორი ათას ოცდახუთი წლის პირველი იანვარი",
        )

    def test_to_date_rejects_out_of_range(self):
        ka = self._ka()
        with self.assertRaises(ValueError):
            ka.to_date(45, 7, 2026)
        with self.assertRaises(ValueError):
            ka.to_date(4, 13, 2026)

    # ----- times -------------------------------------------------------

    def test_to_time_nominative(self):
        ka = self._ka()
        self.assertEqual(
            ka.to_time(23, 50),
            "ოცდასამი საათი და ორმოცდაათი წუთი",
        )
        self.assertEqual(ka.to_time(17, 0), "ჩვიდმეტი საათი")

    def test_to_time_with_seconds(self):
        ka = self._ka()
        self.assertEqual(
            ka.to_time(9, 5, 30),
            "ცხრა საათი, ხუთი წუთი და ოცდაათი წამი",
        )

    def test_to_time_suffix_hour_only(self):
        ka = self._ka()
        self.assertEqual(ka.to_time(17, 0, suffix="ზე"), "ჩვიდმეტ საათზე")
        self.assertEqual(ka.to_time(8, 0, suffix="ზე"), "რვა საათზე")

    def test_to_time_suffix_with_minutes(self):
        ka = self._ka()
        self.assertEqual(
            ka.to_time(17, 35, suffix="ზე"),
            "ჩვიდმეტ საათსა და ოცდათხუთმეტ წუთზე",
        )

    def test_to_time_rejects_out_of_range(self):
        ka = self._ka()
        with self.assertRaises(ValueError):
            ka.to_time(24, 0)
        with self.assertRaises(ValueError):
            ka.to_time(12, 60)


class RomanToIntTest(TestCase):
    """Strict canonical Roman-numeral parsing."""

    def test_canonical_values(self):
        from num2words import roman_to_int
        for token, value in [
            ("I", 1), ("IV", 4), ("V", 5), ("IX", 9), ("X", 10),
            ("XXI", 21), ("XXXIX", 39), ("XL", 40), ("XC", 90),
            ("C", 100), ("CD", 400), ("MCMXCIX", 1999), ("MMXXVI", 2026),
        ]:
            self.assertEqual(roman_to_int(token), value)

    def test_rejects_non_canonical(self):
        from num2words import roman_to_int
        for bad in ["", "IIII", "VX", "IC", "XM", "ix", "ABC", "I I"]:
            with self.assertRaises(ValueError):
                roman_to_int(bad)
