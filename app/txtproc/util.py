class classproperty(property):
    """
    Decorator for read-only class- and instance-wide properties.

    Don't pay much attention to PyCharm warnings. This decorator should be
    used as follows:

    >>> @classproperty
    >>> @classmethod
    >>> def foo(cls): pass

    See also: https://stackoverflow.com/a/1383402
    """
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()
