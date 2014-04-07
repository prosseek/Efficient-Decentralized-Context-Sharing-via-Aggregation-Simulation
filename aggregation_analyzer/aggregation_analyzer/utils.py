def starts_with(name, keys):
    """

    >>> keys = ["abc", "def", "xyz"]
    >>> print starts_with("abcdef", keys)
    abc
    >>> starts_with("k", keys)
    """
    for key in keys:
        #if key.startswith(name): return key
        if name.startswith(key): return key
    return None


if __name__ == "__main__":
    import doctest
    doctest.testmod()