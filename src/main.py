import os
import shutil

from blocks import (
    markdown_to_html_node
)

def main():
    copy_directory_contents("./static", "./public")
    generate_page("./content/index.md", "./template.html", "./public/index.html")

def clear_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

def copy_directory_contents(src, dst):
    clear_directory(dst)
    
    def recursive_copy(src, dst):
        if not os.path.exists(dst):
            os.makedirs(dst)
        
        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            dst_path = os.path.join(dst, item)
            
            if os.path.isdir(src_path):
                recursive_copy(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)
    
    recursive_copy(src, dst)

def extract_title(markdown):
    if (len(markdown) > 0 and markdown.startswith("# ")):
        return markdown.splitlines()[0].lstrip("# ")
    else:
        raise Exception("No title found in markdown.")
    
def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def write_file(dest_path, content):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, 'w') as file:
        file.write(content)
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    markdown = read_file(from_path)
    template = read_file(template_path)
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    write_file(dest_path, template)

main()