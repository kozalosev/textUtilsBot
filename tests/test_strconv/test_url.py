from strconv.url import URLEncoder, URLDecoder

url = "http://сайт.рф/путь;параметр=значение?запрос1=значение1&запрос2=значение2#хэш"
encoded_url = "http://xn--80aswg.xn--p1ai/%D0%BF%D1%83%D1%82%D1%8C;%D0%BF%D0%B0%D1%80%D0%B0%D0%BC%D0%B5%D1%82%D1%80=%D0%B7%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D0%B8%D0%B5?%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%811=%D0%B7%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D0%B8%D0%B51&%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%812=%D0%B7%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D0%B8%D0%B52#%D1%85%D1%8D%D1%88"


class TestURLEncoder:
    encoder = URLEncoder()

    def test_can_process(self):
        assert not self.encoder.can_process("сайт.рф")
        assert self.encoder.can_process("http://сайт.рф")
        assert self.encoder.can_process("https://сайт.рф/путь?параметр=значение#хэш")

    def test_process(self):
        assert self.encoder.process(url) == encoded_url


class TestURLDecoder:
    decoder = URLDecoder()

    def test_can_process(self):
        assert not self.decoder.can_process("xn--80aswg.xn--p1ai")
        assert not self.decoder.can_process("http://сайт.рф")
        assert self.decoder.can_process("http://xn--80aswg.xn--p1ai")
        assert self.decoder.can_process("http://xn--80aswg.xn--p1ai/путь")
        assert self.decoder.can_process("http://сайт.рф/%D0%BF%D1%83%D1%82%D1%8C")
        assert not self.decoder.can_process(url)
        assert self.decoder.can_process(encoded_url)

    def test_process(self):
        assert self.decoder.process(encoded_url) == url
        domain_and_path = "http://сайт.рф/путь"
        assert self.decoder.process("http://сайт.рф/%D0%BF%D1%83%D1%82%D1%8C") == domain_and_path
        assert self.decoder.process("http://xn--80aswg.xn--p1ai/путь") == domain_and_path
