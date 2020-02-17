"""
Removes .txt and .mat strings in filenames in files in subdirs
"""

import os

to_remove = (
    ".txt",
    ".mat"
)

for dir in os.listdir("./"):
    if not os.path.isdir(dir):
        continue
    for fname in os.listdir(f"./{dir}/"):
        for substr in to_remove:
	        if substr in fname:
	            prefix = f"./{dir}/"
	            os.rename(prefix+fname, prefix+fname.replace(substr, ""))


