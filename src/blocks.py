def markdown_to_blocks(markdown:str)->list:
    split_markdown = markdown.split("\n\n")
    block = []
    for item in split_markdown:
        stripped_item = item.strip()
        if stripped_item == "":
            continue
        block.append(stripped_item)
    return block