from app.strconv.banner import spaced_text, BannerMaker


def test_spaced_text():
    assert spaced_text("hello world") == "h e l l o   w o r l d"


def test_processor():
    processor = BannerMaker()
    assert processor.process("hello world") == "<code>H E L L O   W O R L D</code>"
    assert processor.get_description("hello world") == "H E L L O   W O R L D"
