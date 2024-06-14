import os
import shutil

from blocks import (
    markdown_to_html_node
)

def main():
    copy_directory_contents("./static", "./public")
    generate_pages_recursive("./content", "./template.html", "./public")

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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md'):
                markdown_file_path = os.path.join(root, file)
                html_file_path = os.path.join(dest_dir_path, os.path.relpath(markdown_file_path, dir_path_content))
                html_file_path = os.path.splitext(html_file_path)[0] + '.html'
                
                generate_page(markdown_file_path, template_path, html_file_path)

        for dir in dirs:
            nested_dir_path = os.path.join(root, dir)
            nested_dest_path = os.path.join(dest_dir_path, os.path.relpath(nested_dir_path, dir_path_content))
            if not os.path.exists(nested_dest_path):
                os.makedirs(nested_dest_path)
            generate_pages_recursive(nested_dir_path, template_path, nested_dest_path)   

main()