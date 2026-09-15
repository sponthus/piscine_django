import sys


def read_file(path: str, sep: str) -> list[str]:
    """Reads a file and renders a list using given sep."""
    with open(path, mode="r") as file:
        content: str = file.read()
        list_content: list = content.split(sep)
        return list_content


def write_file(path: str, content: str) -> None:
    with open(path, mode="w") as file:
        file.write(content)


def require_str_list(values: list[str], label: str) -> None:
    """Type checking for a list[str]. Raises TypeError."""
    if not isinstance(values, list):
        raise TypeError(f"{label} should be a list")
    for v in values:
        if not isinstance(v, str):
            raise TypeError(f"{label} items should be str")


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
            raise ValueError("Wrong format for element info, expected Name = infos")
        name = element_split[0].strip()
        infos = element_split[1]

        infos_dict = {}
        split_infos = infos.split(", ")
        for info in split_infos:
            split_info = info.split(":")
            if len(split_info) != 2:
                raise ValueError("Wrong format for element info, expected 'info: value'")
            info_name = split_info[0].strip()
            info_value = split_info[1].strip()
            infos_dict[info_name] = info_value

        elements[name] = infos_dict
    return elements


def render_tag(
        name: str,
        content: str,
        indent: int = 0,
        inline: bool = False) -> str:
    if inline:
        return f"\n<{name}>{content}</{name}>"
    pad = "\t" * indent
    lines = [line for line in content.splitlines() if line]
    inner = "\n".join(f"{pad}{line}" for line in lines)
    return f"\n<{name}>\n{inner}\n</{name}>"


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
    require_str_list(headers, "headers")
    if not isinstance(elements, list):
        raise TypeError("elements should be a list")

    header_row = render_tag("tr", "".join(render_tag("th", h, inline=True) for h in headers), indent=1)

    rows = []
    for row in elements:
        require_str_list(row, "row")
        rows.append(render_tag("tr", "".join(render_tag("td", cell, inline=True) for cell in row), indent=1))

    return render_tag("table", "\n".join([header_row, *rows]), indent=1)


class Element:
    def __init__(self, element_name: str, attributes: dict[str, str]):
        if not isinstance(element_name, str):
            raise TypeError("element_name should be a str")
        if not isinstance(attributes, dict):
            raise TypeError("element_data should be a dict")
        self.name = element_name
        pos_str = attributes.get("position", None)
        if pos_str is None:
            raise ValueError("Missing position on an element")
        self.pos = int(pos_str)
        self.attributes = attributes.copy()
        del self.attributes["position"]

    def get_attributes_html_list(self) -> str:
        attr_dict = {
            "number": "Nº",
            "small": "",
            "molar": "Mass: ",
            "electron": "e²: "
        }
        items: list[str] = []
        for attribute, value in self.attributes.items():
            if not isinstance(attribute, str):
                raise TypeError("attribute should be a str")
            if not isinstance(value, str):
                raise TypeError("value should be a str")
            attribute_translated = attr_dict.get(attribute, attribute)
            str_attribute = f"{attribute_translated}{value}"
            items.append(render_tag("li", str_attribute, inline=True))

        return render_tag("ul", "\n".join(items), indent=1)

    def get_div(self) -> str:
        content = "\n".join([
            render_tag("h4", self.name, indent=0, inline=True),
            self.get_attributes_html_list()
        ])
        return render_tag("div", content, indent=1)


class Html:
    def __init__(self):
        self.title = "My page"
        self.body = ""

    def set_title(self, title: str):
        self.title = title

    def add_to_body(self, addition: str):
        self.body += "\n"
        self.body += addition

    def get_html(self):
        head_lines = [
            '<meta charset="utf-8">'
        ]
        if self.title:
            head_lines.append(f"\t<title>{self.title}</title>")
        head_html = render_tag("head", "\n".join(head_lines), indent=1)

        body_html = render_tag("body", self.body, indent=1)

        return "\n".join([
            "<!DOCTYPE html>",
            '<html lang="en">',
            head_html,
            body_html,
            "</html>",
        ])


def format_html(data: dict[str, dict[str, str]]) -> str:
    """
    Builds the html to render periodic table from given data.

    Uses each element's position to position them in columns.
    """
    file = Html()
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
        element_object = Element(name, attributes)
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