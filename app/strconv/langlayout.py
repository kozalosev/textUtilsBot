"""Language layout switcher from EN to RU and vice versa."""

import string

from txtproc.abc import TextProcessor, Universal


class LanguageLayoutSwitcher(Universal, TextProcessor):
    def process(self, query: str, lang_code: str = "") -> str:
        """
        'ghbdtn' => 'привет'
        'руддщ' => 'hello'
        """
        en_weight = sum(c in string.ascii_letters for c in query)
        ru_weight = sum(c in _russian_letters for c in query)
        if ru_weight > en_weight:
            return query.translate(_layouts_match_table_ru_en)
        else:
            return query.translate(_layouts_match_table_en_ru)


_russian_letters = "абвгдеёжзийклмонпрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
_latin_layout = "qwertyuiop[]asdfghjkl;'\zxcvbnm,./`QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?~@#$^&"
_cyrillic_layout = "йцукенгшщзхъфывапролджэ\ячсмитьбю.ёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,Ё\"№;:?"

_layouts_match_table_en_ru = str.maketrans(_latin_layout, _cyrillic_layout)
_layouts_match_table_ru_en = str.maketrans(_cyrillic_layout, _latin_layout)
