import os
import shutil

def main():
    copy_directory_contents("./static", "./public")

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



main()