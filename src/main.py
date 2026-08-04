import os, shutil
from os import path

def main():
    destination = path.abspath("public")
    source = path.abspath("static")
    if os.path.isdir(destination):
        shutil.rmtree(destination)
    return copy_to_and_from_dir(source, destination)

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

main()