import os, shutil
from os import path
from blocks import markdown_to_html_node


def main():
    destination = path.abspath("public")
    source = path.abspath("static")
    if os.path.isdir(destination):
        shutil.rmtree(destination)
    copy_to_and_from_dir(source, destination)
    generate_page("content/index.md", "template.html", "public/index.html")

def copy_to_and_from_dir(source, destination):
    files = os.listdir(source)
    os.mkdir(destination)

    for filename in files:
        current_file = os.path.join(source, filename)
        destination_file = os.path.join(destination, filename)
        if os.path.isfile(current_file):
            shutil.copy(current_file, destination_file)
        else:
            copy_to_and_from_dir(current_file, destination_file)

def delete_dir_contents(destination):
    for filename in os.listdir(destination):
        file_path = os.path.join(destination, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
               os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def extract_title(markdown):
    if markdown.startswith("#"):
            hash_count = 0
            for char in markdown:
                if char == "#":
                    hash_count += 1
                else:
                    break
            if hash_count == 1 and len(markdown) > hash_count and markdown[hash_count] == " ":
                no_hash = markdown[hash_count:]
                joined_no_hash = "".join(no_hash)
                return joined_no_hash.strip()
            else:
                raise Exception ("Invalid Title")
    else:
        raise Exception ("Missing Title")

def generate_page(from_path, template_path, dest_path):
    print (f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        from_path_md = file.read()
    with open(template_path, "r") as file:
        template_path_template = file.read()
    node = markdown_to_html_node(from_path_md)
    html = node.to_html()
    title = extract_title(from_path_md)
    template_title = template_path_template.replace("{{ Title }}", title)
    template_replaced = template_title.replace("{{ Content }}", html)
    directories_needed = os.path.dirname(dest_path)
    os.makedirs(directories_needed, exist_ok=True)
    with open(dest_path, "w") as file:
                file.write(template_replaced)

main()