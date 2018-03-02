from app.strconv import *
# noinspection PyProtectedMember
from app.strconv import split_every_n_characters


def test_escape_html():
    s = "Ensure <b>text</b> don't\nhave <i>HTML</i> tags"
    e = "Ensure &lt;b&gt;text&lt;/b&gt; don't\nhave &lt;i&gt;HTML&lt;/i&gt; tags"
    assert escape_html(s) == e


class TestSplitAtEachNthCharacter:
    def test_3_bytes(self):
        s = "101010101010101010101010"
        e = ['10101010', '10101010', '10101010']
        r = split_every_n_characters(8, s)
        assert r == e

    def test_small_chunks(self):
        s = "1010101010101"
        e = ['101', '010', '101', '010', '1']
        r = split_every_n_characters(3, s)
        assert r == e


class TestBinary:
    s = "Hello World"
    b = "01001000 01100101 01101100 01101100 01101111 00100000 01010111 01101111 01110010 01101100 01100100"
    f1 = "foo bar"
    f2 = "110001 110010 110011"

    def test_from_str(self):
        assert str_to_bin(self.s) == self.b

    def test_to_str(self):
        assert bin_to_str(self.b) == self.s

    def test_fails(self):
        assert bin_to_str(self.f1) is None
        assert bin_to_str(self.f2) is None


class TestHex:
    s = "Hello World"
    h = "48 65 6c 6c 6f 20 57 6f 72 6c 64"
    f1 = "foo bar"
    f2 = "48 65 6c 6c 6f e1"

    def test_from_str(self):
        assert str_to_hex(self.s) == self.h

    def test_to_str(self):
        assert hex_to_str(self.h) == self.s

    def test_fails(self):
        assert hex_to_str(self.f1) is None
        assert hex_to_str(self.f2) is None
