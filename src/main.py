from textnode import *
from htmlnode import *
from blocktypes import *
from nodedelimiter import *
import os
import shutil
import sys

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./static/template.html"
output_dir = "docs"

def main():
    if len(sys.argv) <= 1:
        basepath = "/"
    else:
        basepath = sys.argv[1] + "/"
    
    update_contents()
    generate_pages_recursively(dir_path_content, template_path, dir_path_public, basepath)

def get_file_paths(directory="static"):
    print("*******************")
    print("logging paths")
    print("*******************")
    static_content_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if ":Zone.Identifier" not in file:
                static_content_list.append(os.path.join(root, file))
                print(f"appended {file} in {root} directory...")
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            print(f"found directory {dir_path}, appending children...")
            get_file_paths(dir_path)
    return static_content_list

def copy_files(source, target):
    for file in get_file_paths(source):
        print(f"COPYING FROM: {file} TO TARGET: {target}")
        target_file = file.replace(source, target)
        os.makedirs(os.path.dirname(target_file), exist_ok=True) #this line creates directory if it doesnt exist, if it does it passes the okayge
        shutil.copy(file, target_file)

def remove_contents_of_directory(directory): # gets the directory, goes over every path in it, if its file it removes it and if its directory it removes it and its contents recursively
    for file in get_file_paths(directory):
        print(f"removing {file} from {directory} directory...")
        if os.path.exists(file):
            if os.path.isfile(file):
                os.remove(file)
            elif os.path.isdir(file):
                shutil.rmtree(file)
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                print(f"Removed empty directory: {dir_path}")

def update_contents():
    print("*******************")
    print("updating contents")
    print("*******************")

    remove_contents_of_directory(output_dir)
    copy_files(dir_path_static, output_dir)

    print("*******************")
    print("copying finished")
    print("*******************")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f">>>Generating page from {from_path} to {dest_path} using {template_path}")
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(from_path) as f:
        file_content = f.read()
    with open(template_path) as f:
        template_content = f.read()
    html_string = markdown_to_html_node(file_content).to_html()
    title = extract_title(file_content)
    new_content = template_content.replace("{{ Content }}", html_string).replace("{{ Title }}", title)
    new_content = new_content.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    with open(dest_path, "w") as f:
        f.write(new_content)
        
def generate_pages_recursively(dir_path_content, template_path, dest_dir_path, basepath):
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("generating pages recursively")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

    for file in get_file_paths(dir_path_content):
        dest_file_path = file.replace("content", output_dir).replace(".md", ".html")
        print(f"generating pages for {file}, using {template_path} and saving to {dest_dir_path}")
        if file.endswith(".md"):
            generate_page(file, template_path, dest_file_path, basepath)

        elif os.path.isdir(file):
            dir_name = os.path.basename(file)
            dest_dir = dir_path_content.replace("content", output_dir)
            print(f"current destination directory is {dest_dir} and directory name is {dir_name}")
            generate_pages_recursively(file, template_path, dest_dir, basepath)

main()