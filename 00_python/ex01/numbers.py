def read_file(path: str, sep: str) -> list:
    """Reads a file and renders a list using given sep."""
    with open(path, mode="r") as file:
        content: str = file.read()
        list_content: list = content.split(sep)
        return list_content


def print_data(data: list[str], strip: bool) -> None:
    """Prints the list of str in data, with option to strip whitespaces."""
    if not isinstance(data, list):
        raise AssertionError("data should be a list")
    for line in data:
        if strip:
            if not isinstance(line, str):
                raise AssertionError("A line is not str with strip option")
            line = line.strip()
        print(line)


if __name__ == '__main__':
    try:
        data = read_file(path="numbers.txt", sep=",")
        print_data(data, strip=True)
    except Exception as e:
        print("Error:", e)
