from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            split_node = node.text.split(delimiter)
            if len(split_node) % 2 == 0:
                raise Exception ("Unclosed Delimiter")

            for i in range(0, len(split_node)):
                if split_node[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_node[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_node[i], text_type))
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple]:
    #funct takes raw markdown text -> returns a list of tuples
    #each tuple contains = (alt text, url of markdown image)
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text: str) -> list[tuple]:
    #funct takes raw markdown text -> extracts markdown links instead of images -> returns a list of tuples
    #each tuple contains = (anchor text, urls)
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches