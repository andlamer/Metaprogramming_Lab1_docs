import os
from shutil import copyfile


def delete_all_html_elements(path):
    if os.path.exists(path):
        for entry in os.listdir(path):
            if entry.endswith(".html") or entry.endswith(".css"):
                os.remove(path + "/" + entry)


def copy_styles_to_folder(path):
    src = "PHTML_DOC_style.css"
    dst = path + "PHTML_DOC_style.css"
    if not os.path.exists(dst):
        copyfile(src, dst)
