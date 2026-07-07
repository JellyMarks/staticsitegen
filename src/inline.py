from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    if text_type not in TextType:
        raise Exception ("Invalid TextType Option")

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