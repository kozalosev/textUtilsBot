from app import msgdb


def test_database(tmpdir):
    msgdb._mock_database(str(tmpdir.join('messages.db')))
    rowid = msgdb.insert("Hello World")
    assert rowid == 1
    assert msgdb.select(rowid) == "Hello World"
