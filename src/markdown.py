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

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    #take a list of text nodes and create a new list of nodes
    new_nodes = []
    
    #Check each node if multiple are present
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            remaining_text = node.text
            #make use of extraction functions to get markdown
            images = extract_markdown_images(remaining_text)
            if not images:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
                continue
            for alt, url in images:
                #split before and after the image/link
                before, after = remaining_text.split(f"![{alt}]({url})", 1)
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT)) #add the first text
                new_nodes.append(TextNode(alt, TextType.IMAGE, url)) #add the first image/link
                remaining_text = after
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
        else:
            new_nodes.append(node)
    return (new_nodes)

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    #take a list of text nodes and create a new list of nodes
    new_nodes = []
    
    #Check each node if multiple are present
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            remaining_text = node.text
            #make use of extraction functions to get markdown
            links = extract_markdown_links(remaining_text)
            if not links:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
                continue
            for alt, url in links:
                #split before and after the image/link
                before, after = remaining_text.split(f"[{alt}]({url})", 1)
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT)) #add the first text
                new_nodes.append(TextNode(alt, TextType.LINK, url)) #add the first image/link
                remaining_text = after
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
        else:
            new_nodes.append(node)
    return (new_nodes)

def text_to_textnodes(text):
    old_nodes = [TextNode(text, TextType.TEXT)]
    code_nodes = (split_nodes_delimiter(old_nodes, "`", TextType.CODE))
    bold_nodes = (split_nodes_delimiter(code_nodes, "**", TextType.BOLD))
    italic_nodes = (split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC))
    link_nodes = (split_nodes_link(italic_nodes))
    return (split_nodes_image(link_nodes))