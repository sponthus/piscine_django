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


def get_table(headers: list[str], elements: list[list[str]]):
    """
    Creates a html table element, using given headers and elements.
    
    Expected format:
    - headers as a list of str
        -> Each one will be represented in a <th>, contained in global <tr>
    - elements as list of lists (rows)
        -> Each one will open a <tr>
    - rows as a list of str
        -> Each one will be represented in a <td>
    """
    if not isinstance(elements, list):
        raise AssertionError("elements should be a list")
    if not isinstance(headers, list):
        raise AssertionError("headers should be a list")
    res = ""
    table_content = ""

    # Add headers
    str_headers = ""
    for header in headers:
        if not isinstance(header, str):
            raise AssertionError("header should be a str")
        str_headers = append_tab(str_headers, header, 0, tag="th", same_line=True)

    table_content = append_tab(table_content, str_headers, 1, tag="tr")

    # Add items
    str_items = ""
    for row in elements:
        str_item = ""
        if not isinstance(row, list):
            raise AssertionError("row should be a list")
        for element in row:
            if not isinstance(element, str):
                raise AssertionError("element should be a str")
            str_item = append_tab(str_item, element, 1, tag="td", same_line=True)
        str_items = append_tab(str_items, str_item, 1, tag="tr")

    table_content += "\n"
    table_content += str_items

    res = append_tab(res, table_content, tab_level=1, tag="table")
    return res


class element:
    def __init__(self, element_name: str, attributes: dict[str, str]):
        if not isinstance(element_name, str):
            raise AssertionError("element_name should be a str")
        if not isinstance(attributes, dict):
            raise AssertionError("element_data should be a dict")
        self.name = element_name
        pos_str = attributes.get("position", None)
        if pos_str is None:
            raise AssertionError("Missing position on an element")
        self.pos = int(pos_str)
        self.attributes = attributes
        del self.attributes["position"]

    def get_name_html(self, tag: str) -> str:
        return append_tab("", self.name, tab_level=0, tag=tag, same_line=True)

    def get_attributes_list(self) -> str:
        attr_dict = {
            "number": "Nº",
            "small": "",
            "molar": "Mass: ",
            "electron": "e²: "
        }
        li_elements = ""
        for attribute, value in self.attributes.items():
            attribute_translated = attr_dict.get(attribute, attribute)
            # TODO: Secure types
            str_attribute = f"{attribute_translated}{value}"
            li_elements = append_tab(li_elements, str_attribute, tab_level=0, tag="li", same_line=True)
        return append_tab("", li_elements, tab_level=1, tag="ul")

    def get_div(self) -> str:
        res = ""
        content = ""
        content += self.get_name_html(tag="h4")
        content += "\n"
        content += self.get_attributes_list()
        return append_tab(res, content, tab_level=1, tag="div")


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

    headers: list = [str(i) for i in range(18)]
    elements: list = []
    for row in range(7):
        elements.append([])
        for _ in range(18):
            elements[row].append("<div></div>")

    last_pos = -1
    row = 0
    for name, attributes in data.items():
        element_object = element(name, attributes)
        pos = element_object.pos
        if last_pos >= pos:
            row += 1
        elements[row][pos] = element_object.get_div()
        last_pos = pos

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