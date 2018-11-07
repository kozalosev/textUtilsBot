from strconv.util import escape_html


def test_escape_html():
    s = "Ensure <b>text</b> don't\nhave <i>HTML</i> tags"
    e = "Ensure &lt;b&gt;text&lt;/b&gt; don't\nhave &lt;i&gt;HTML&lt;/i&gt; tags"
    assert escape_html(s) == e
