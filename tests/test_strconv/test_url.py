from strconv.url import URLEncoder, URLDecoder, PunycodeEncoder, PunycodeDecoder


class TestURLEncoder:
    encoder = URLEncoder()

    def test_can_process(self):
        assert not self.encoder.can_process("Hello World")
        assert self.encoder.can_process("url:Hello World")
        assert self.encoder.can_process("url: Hello World")
        assert not self.encoder.can_process("url:Hello%20World")

    def test_process(self):
        assert self.encoder.transform("Hello World") == "Hello%20World"
        assert self.encoder.process("url:Hello World") == "Hello%20World"
        assert self.encoder.process("url: Hello World") == "Hello%20World"
        assert self.encoder.process("url:привет") == "%D0%BF%D1%80%D0%B8%D0%B2%D0%B5%D1%82"


class TestURLDecoder:
    decoder = URLDecoder()

    def test_can_process(self):
        assert not self.decoder.can_process("Hello%20World")
        assert self.decoder.can_process("url:Hello%20World")
        assert self.decoder.can_process("url: Hello%20World")
        assert not self.decoder.can_process("url:Hello World")

    def test_process(self):
        assert self.decoder.transform("Hello%20World") == "Hello World"
        assert self.decoder.process("url:Hello%20World") == "Hello World"
        assert self.decoder.process("url: Hello%20World") == "Hello World"
        assert self.decoder.process("url:Hello World") == "Hello World"
        assert self.decoder.process("url:%D0%BF%D1%80%D0%B8%D0%B2%D0%B5%D1%82") == "привет"


class TestPunycodeEncoder:
    encoder = PunycodeEncoder()

    def test_can_process(self):
        assert not self.encoder.can_process("привет")
        assert self.encoder.can_process("url:привет")
        assert self.encoder.can_process("url: привет")
        assert not self.encoder.can_process("url:xn--b1agh1afp")

    def test_process(self):
        assert self.encoder.transform("привет") == "xn--b1agh1afp"
        assert self.encoder.process("url:привет") == "xn--b1agh1afp"
        assert self.encoder.process("url: привет") == "xn--b1agh1afp"


class TestPunycodeDecoder:
    decoder = PunycodeDecoder()

    def test_can_process(self):
        assert not self.decoder.can_process("xn--b1agh1afp")
        assert self.decoder.can_process("url:xn--b1agh1afp")
        assert self.decoder.can_process("url: xn--b1agh1afp")
        assert not self.decoder.can_process("url: привет")
        assert not self.decoder.can_process("url: xn--привет")

    def test_process(self):
        assert self.decoder.transform("xn--b1agh1afp") == "привет"
        assert self.decoder.process("url:xn--b1agh1afp") == "привет"
        assert self.decoder.process("url: xn--b1agh1afp") == "привет"
