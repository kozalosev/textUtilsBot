from strconv.langlayout import LanguageLayoutSwitcher


class TestLayoutSwitcher:
    en = "Z j,kf;fkcz c hfcrkflrjq b ,erdjq @`@"
    ru = "Я облажался с раскладкой и буквой \"ё\""

    switcher = LanguageLayoutSwitcher()

    def test_en_ru(self):
        assert self.switcher.process(self.en) == self.ru

    def test_ru_en(self):
        assert self.switcher.process(self.ru) == self.en
