from userutil import *


class TestGetUsernameOrFullname:
    sample_user = {
        'username': 'username',
        'first_name': 'foo',
        'last_name': 'bar'
    }

    def test_username(self):
        user = self.sample_user.copy()
        username = get_username_or_fullname(user)
        assert '@username' == username

    def test_fullname(self):
        user = self.sample_user.copy()
        del user['username']
        username = get_username_or_fullname(user)
        assert 'foo bar' == username

    def test_first_name(self):
        user = self.sample_user.copy()
        del user['username']
        del user['last_name']
        username = get_username_or_fullname(user)
        assert 'foo' == username
