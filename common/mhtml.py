from lxml import etree

parser = etree.HTMLParser()


def get_tree_from_html(html_doc: str):
    tree = etree.fromstring(html_doc, parser)
    return tree


def get_html_from_tree(tree):
    return etree.tostring(tree).decode()


def get_tbody_from_tree(tree):
    tbody = tree.find(".//tbody")
    return tbody


def get_row_list_from_tbody(tbody):
    # Using XPath to the all the rows in tbody
    row_list = tbody.xpath(".//tr")
    return row_list


def get_a_element_of_link(text: str, link: str):
    a_element = etree.Element("a")
    a_element.text = text
    a_element.set("href", link)
    return a_element


def get_div_element_for_p_tags(commit_message: str):
    # Create a parent div to contain the paragraphs
    div_element = etree.Element("div")
    lines = commit_message.split("\n")

    # Wrap each line in a <p> tag and append it to the div
    for line in lines:
        p_element = etree.Element("p")
        p_element.text = line
        div_element.append(p_element)

    return div_element


def get_row_element_of_data_list(data_list: list):
    row_element = etree.Element("tr")
    for data in data_list:
        new_cell = etree.Element("td")
        if isinstance(data, str):
            new_cell.text = data
        elif isinstance(data, list):
            for data_item in data:
                new_cell.append(data_item)
        else:
            new_cell.append(data)
        row_element.append(new_cell)
    return row_element


def insert_row_to_tbody(tbody, seq, row):
    tbody.insert(seq, row)
    return tbody


def append_row_to_tbody(tbody, row):
    tbody.append(row)
    return tbody
