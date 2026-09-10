import sys


def read_file(path: str, sep: str) -> list:
    """Reads a file and renders a list using given sep."""
    with open(path, mode="r") as file:
        content: str = file.read()
        list_content: list = content.split(sep)
        return list_content


def write_file(path: str, content: str):
    with open(path, mode="x") as file:
        file.write(content)


def parse_data(data: list[str]) -> dict[str, dict[str, str]]:
    """From raw data, translates into an info dict.
    
    Expected line format: 
    element_name = position: position_value, info_name: value, ...

    Return format:
    {
        element_name: {
            info_name: value,
            info_name: value
            ...
        },
        ...
    }
    """
    elements = {}
    for element in data:
        if not element:
            continue
        element_split = element.split("=")
        if len(element_split) != 2:
            raise AssertionError("Wrong format for element info, expected Name = infos")
        name = element_split[0].strip()
        infos = element_split[1]

        infos_dict = {}
        split_infos = infos.split(", ")
        for info in split_infos:
            split_info = info.split(":")
            if len(split_info) != 2:
                raise AssertionError("Wrong format for element info, expected 'info: value'")
            info_name = split_info[0].strip()
            info_value = split_info[1].strip()
            infos_dict[info_name] = info_value

        elements[name] = infos_dict
    return elements


def append_tab(
        base: str,
        addition: str,
        tab_level: int,
        tag: str,
        same_line: bool = False):
    """Splits the addition per line and adds line with tabulations."""
    split_addition: list[str] = addition.split("\n")
    tabs: str = "\t" * tab_level
    base += f"\n<{tag}>"
    for line in split_addition:
        if not line:
            continue
        if not same_line:
            base += "\n"
            base += tabs
        base += line
    if not same_line:
        base += "\n"
    base += f"</{tag}>"
    return base

def get_table(headers: list[str], elements: list[str]):
    """Creates a html table element, using given headers and elements"""
    if not isinstance(elements, list):
        raise AssertionError("elements should be a list")
    if not isinstance(headers, list):
        raise AssertionError("headers should be a list")
    res = "<table>"

    # Add headers
    str_headers = ""
    for header in headers:
        if not isinstance(header, str):
            raise AssertionError("header should be a str")
        str_headers += f"\t<th>{header}</th>\n"

    res = append_tab(res, str_headers, 1, tag="tr")

    # Add items - TODO not functional because adds only 1 line
    str_items = ""
    for items in elements:
        if not isinstance(items, str):
            raise AssertionError("element should be a str")
        str_items += f"\t<td>{items}</td>\n"

    res = append_tab(res, str_items, 1, tag="tr")
    res += "\n</table>"
    return res

class html:
    def __init__(self):
        self.title = "My page"
        self.body = ""

    def set_title(self, title: str):
        self.title = title

    def add_to_body(self, addition: str):
        self.body += "\n"
        self.body += addition

    def get_html(self):
        base = """<!DOCTYPE html>
<html lang="en">
<head>
\t<meta charset="utf-8">"""
        if self.title:
            base += "\n\t<title>"
            base += self.title
            base += "</title>"
        base += "\n</head>"
        base = append_tab(base, self.body, 1, tag="body")
        base += "\n</html>"
        return base


def format_html(data: dict[str, dict[str, str]]) -> str:
    file = html()
    file.set_title("Periodic table")

    headers = ["a", "b", "c"]
    elements = [["1", "2", "3"], ["1", "2", "3"]]
    table = get_table(headers, elements)
    file.add_to_body(table)

    return file.get_html()


if __name__ == '__main__':
    try:
        data: list[str] = read_file(path="periodic_table.txt", sep="\n")
        # print(data)
        data_dict = parse_data(data)
        # print(data_dict)
        html_res = format_html(data_dict)
        write_file("periodic_table.html", content=html_res)
    except Exception as e:
        print("Error:", e)