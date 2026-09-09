def var_to_dict(var: list[tuple]) -> dict:
    """Turns var containing list of tuple of (key, element) in a dict."""
    res = {}
    if not isinstance(var, list):
        raise AssertionError("var should be a list of tuples")
    for element in var:
        if not isinstance(element, tuple):
            raise AssertionError("var should be a list of tuples")
        if len(element) != 2:
            print(element, type(element), len(element))
            raise AssertionError("tuples should contain key and value")
        res[element[0]] = element[1]
    return res


def print_dict(dic: dict):
    """Prints full content of dic as 'element : key'."""
    if not isinstance(dic, dict):
        raise AssertionError("dic should be a dict")
    for key, element in dic.items():
        print(element, ":", key)


if __name__ == '__main__':
    d = [
        ('Hendrix', '1942'),
        ('Allman', '1946'),
        ('King', '1925'),
        ('Clapton', '1945'),
        ('Johnson', '1911'),
        ('Berry', '1926'),
        ('Vaughan', '1954'),
        ('Cooder', '1947'),
        ('Page', '1944'),
        ('Richards', '1943'),
        ('Hammett', '1962'),
        ('Cobain', '1967'),
        ('Garcia', '1942'),
        ('Beck', '1944'),
        ('Santana', '1947'),
        ('Ramone', '1948'),
        ('White', '1975'),
        ('Frusciante', '1970'),
        ('Thompson', '1949'),
        ('Burton', '1939')
    ]
    dic = var_to_dict(d)
    print_dict(dic)
