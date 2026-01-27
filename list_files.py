
import os
import sys

def list_files(directory, f_out):
    f_out.write(f"Listing files in {directory}:\n")
    try:
        files = os.listdir(directory)
        for f in files:
            f_out.write(f"{repr(f)}\n")
    except FileNotFoundError:
        f_out.write(f"Directory not found: {directory}\n")

base_dir = r"c:\Users\anuna\OneDrive\Desktop\Haze\music"
subdirs = ["bahurani-picks", "morning-walk", "soft-break", "chai-and-chill", "neet-warrior", "chef-specials"]

with open("file_list.txt", "w", encoding="utf-8") as f_out:
    for subdir in subdirs:
        path = os.path.join(base_dir, subdir)
        list_files(path, f_out)
