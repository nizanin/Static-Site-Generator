import os
import shutil

def copy_directory(src, dst):
    """
    Recursively copy all contents from src to dst.
    Deletes dst contents first to ensure a clean copy.
    """
    # Delete destination directory if it exists
    if os.path.exists(dst):
        print(f"Clearing destination: {dst}")
        shutil.rmtree(dst)
    
    # Recreate destination directory
    os.makedirs(dst, exist_ok=True)

    # Recursive copy helper
    def _copy(src_path, dst_path):
        if os.path.isdir(src_path):
            # Make directory in destination
            os.makedirs(dst_path, exist_ok=True)
            # Recurse into all items
            for item in os.listdir(src_path):
                _copy(os.path.join(src_path, item), os.path.join(dst_path, item))
        else:
            # Copy file
            shutil.copy2(src_path, dst_path)
            print(f"Copied file: {dst_path}")

    # Start recursion from root
    _copy(src, dst)