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

        if elements.get(name, None):
            raise ValueError("double element in periodic_table.txt")
        elements[name] = infos_dict
    return elements


def build_stylesheet() -> str:
    return """
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 1rem;
    font-family: Arial, sans-serif;
    background: #f7f7f7;
    color: #222;
}

h1, h2, h3 {
    text-align: center;
    margin: 0.4rem 0;
}

table {
    border-collapse: collapse;
    table-layout: fixed;
    width: 85%;
    margin: 1rem auto;
    background: white;
}

th, td {
    border: 1px solid #555;
    padding: 0.35rem;
    vertical-align: top;
    text-align: center;
}

th {
    background: #2f2f2f;
    color: #fff;
    font-weight: 600;
}

td > div {
    min-height: 72px;
}

td h4 {
    margin: 0 0 0.3rem 0;
    font-size: 0.95rem;
    overflow-wrap: break-word;
    word-break: break-word;
}

td ul {
    margin: 0;
    padding: 0;
    list-style: none;
    font-size: 0.8rem;
}

.pos-0  { background: #48757a; }
.pos-1  { background: #a05050; }
.pos-2  { background: #936b99; }
.pos-3  { background: #936b99; }
.pos-4  { background: #936b99; }
.pos-5  { background: #936b99; }
.pos-6  { background: #936b99; }
.pos-7  { background: #936b99; }
.pos-8  { background: #936b99; }
.pos-9  { background: #936b99; }
.pos-10 { background: #936b99; }
.pos-11 { background: #936b99; }
.pos-12 { background: #48757a; }
.pos-13 { background: #48757a; }
.pos-14 { background: #48757a; }
.pos-15 { background: #48757a; }
.pos-16 { background: #48757a; }
.pos-17 { background: #a05050; }
"""


def render_tag(
        name: str,
        content: str,
        indent: int = 0,
        inline: bool = False,
        style_class: str = "") -> str:
    if style_class:
        open_tag = f'{name} class="{style_class}"'
    else:
        open_tag = name
    if inline:
        return f"<{open_tag}>{content}</{name}>"
    pad = "\t" * indent
    lines = [line for line in content.splitlines() if line]
    inner = "\n".join(f"{pad}{line}" for line in lines)
    return f"<{open_tag}>\n{inner}\n</{name}>"


def get_table(headers: list[str], elements: list[list[str]]) -> str:
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

    header_row = render_tag("tr", "\n".join(render_tag("th", h, inline=True) for h in headers), indent=1)

    rows = []
    for row in elements:
        require_str_list(row, "row")
        rows.append(render_tag("tr", "\n".join(render_tag("td", cell, inline=True) for cell in row), indent=1))

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
        print(self.attributes)
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
            render_tag(
                "h4",
                self.name,
                indent=0,
                inline=True,
                style_class=f"pos-{self.pos}"
            ),
            self.get_attributes_html_list()
        ])
        return render_tag(
            "div",
            content,
            indent=1,
        )


class Html:
    def __init__(self):
        self.title = "My page"
        self.body = ""

    def set_title(self, title: str) -> None:
        self.title = title

    def add_to_body(self, addition: str) -> None:
        if self.body:
            self.body += "\n"
        self.body += addition

    def get_html(self) -> str:
        head_lines = [
            '<meta charset="utf-8">',
            '<link rel="stylesheet" href="periodic_table.css">'
        ]
        if self.title:
            head_lines.append(f"<title>{self.title}</title>")
        head_html = render_tag("head", "\n".join(head_lines), indent=1)

        body_html = render_tag("body", self.body, indent=1)

        return "\n".join([
            "<!DOCTYPE html>",
            '<html lang="en">',
            head_html,
            body_html,
            "</html>",
        ])


def build_empty_grid(rows: int, cols: int, empty_content: str) -> list[list]:
    result: list = []
    for row in range(rows):
        result.append([])
        for _ in range(cols):
            result[row].append(empty_content)
    return result


def format_html(data: dict[str, dict[str, str]]) -> str:
    """
    Builds the html to render periodic table from given data.

    Uses each element's position to position them in columns.
    """
    page = Html()
    page.set_title("Periodic table")

    page.add_to_body(render_tag(
        name="h1",
        content="Periodic table of elements",
        indent=0,
        inline=True
    ))
    page.add_to_body(render_tag(
        name="h2",
        content="by sponthus",
        indent=0,
        inline=True
    ))
    page.add_to_body(render_tag(
        name="h3",
        content="Non-contractual representation",
        indent=0,
        inline=True
    ))

    headers: list = [str(i) for i in range(18)]
    elements: list[list] = build_empty_grid(
        rows=7,
        cols=18,
        empty_content="<div></div>"
    )

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
    page.add_to_body(table)

    return page.get_html()


if __name__ == '__main__':
    try:
        data: list[str] = read_file(path="periodic_table.txt", sep="\n")
        # print(data)
        data_dict = parse_data(data)
        # print(data_dict)
        html_res = format_html(data_dict)
        write_file("periodic_table.html", content=html_res)
        stylesheet = build_stylesheet()
        write_file("periodic_table.css", content=stylesheet)
    except Exception as e:
        print("Error:", e)