import os
import PHTML_DOC_parser_util
import PHTML_DOC_elements_parser
import datetime

Generator_name = "PHTML_DOC"


class IndexList:
    path = ""
    IndexLists = []

    def __init__(self):
        self.IndexLists = list()

    def append_index_list(self, items, mod_name):
        for i in items:
            self.IndexLists.append(tuple([i, mod_name]))


def document_all_files(dir_name, destination, project_name, project_version, del_html):
    if os.getcwd() != destination.rstrip("/") and del_html:
        PHTML_DOC_parser_util.delete_all_html_elements(destination)
    index_list = IndexList()
    generate_tree_html(dir_name, 0, project_name, destination)
    generate_docmain_html(project_name, project_version, destination)
    if os.path.isdir(dir_name):
        for dirs, subdirs, files in os.walk(dir_name):
            for i in files:
                if i.endswith('.py'):
                    path = os.path.join(dirs, i)
                    direct = os.path.join(dirs)
                    subdir = direct.partition(dir_name)[2]
                    subdir = subdir.replace('\\', '.')
                    name = i.split('.py')[0]
                    elements = generate_elements(path, direct, subdir, name, destination, project_name)
                    index_list.append_index_list(elements, i)
    for i in index_list.IndexLists:
        if __name__ == "__main__":
            print(str(i[0].name + " from module " + i[1]))
    generate_index_list(index_list.IndexLists, destination, project_name)


def document_files_from_dir(dir_name, destination, project_name, project_version, del_html):
    if os.getcwd() != destination.rstrip("/") and del_html:
        PHTML_DOC_parser_util.delete_all_html_elements(destination)
    generate_tree_html(dir_name, 1, project_name, destination)
    generate_docmain_html(project_name, project_version, destination)
    index_list = IndexList()
    if os.path.isdir(dir_name):
        for i in os.listdir(dir_name):
            if i.endswith('.py'):
                path = dir_name + "/" + i
                name = i.split('.py')[0]
                elements = generate_elements(path, dir_name, "", name, destination, project_name)
                index_list.append_index_list(elements, i)
        for i in index_list.IndexLists:
            if __name__ == "__main__":
                print(str(i[0].name + " from module " + i[1]))
    generate_index_list(index_list.IndexLists, destination, project_name)


def document_one_file(path, destination, project_name, project_version, del_html):
    if os.getcwd() != destination.rstrip("/") and del_html:
        PHTML_DOC_parser_util.delete_all_html_elements(destination)
    index_list = IndexList()
    generate_tree_html(path, 2, project_name, destination)
    generate_docmain_html(project_name, project_version, destination)
    if os.path.isfile(path) and path.endswith('.py'):
        dir_name = os.path.dirname(path)
        file_name = path.split('/')[-1:][0]
        name = path.split('.py')[0]
        name = name.split('/')[-1:][0]
        elements = generate_elements(path, dir_name, "", name, destination, project_name)
        index_list.append_index_list(elements, file_name)
    for i in index_list.IndexLists:
        if __name__ == "__main__":
            print(str(i[0].name + " from module " + i[1]))
    generate_index_list(index_list.IndexLists, destination, project_name)


def generate_index_list(elements_list, folder_path, project_name):
    f = open("PHTML_DOC_indexlist.html", 'r')
    a = f.read()
    a = a.replace("%PRNAME%", project_name)
    for element in elements_list:
        if "<a>" + element[0].name + "</a><br>" not in a:
            letter = element[0].name[0]
            lineno = ""
            lineno += "<span class=\"badge badge-secondary\">" + letter.upper() + "</span><br>"
            i = a.find(lineno)
            if i >= 0:
                a = a[:i + len(lineno)] + "<a>" + element[0].name + "&nbsp" * 20 + " from " + element[
                    1] + "</a><br>" + a[i + len(
                    lineno):]
    result = open(folder_path + "indexlist.html", "w+")
    result.write(a)

def generate_elements(path, dir, subdir, name, folder_path, project_name):
    """used for module
     html generation"""
    elements = PHTML_DOC_elements_parser.getDocElements(path, name, dir)
    f = open("PHTML_DOC_element_temp.html", 'r', encoding="utf-8")
    a = f.read()
    ModuleLine = "<h3>Module description</h3><br>"

    names = "<h3>Module elements</h3>\n<ol class=\"list-group\" style=\"left:20px\">"
    import_cards = "<h3> Import details </h3>"
    attribution_cards = "<h3>Attributes details</h3>"
    class_cards = "<h3>Class details</h3>"
    function_cards = "<h3>Function details</h3>"

    universal_card1 = "<div class=\"card\" style=\"width: 80%\"><div class=\"card-body\"><h5 class=\"card-title\" id="
    universal_card2 = "</h5><p class=\"card-text\">"
    universal_card3 = "</p></div></div><br>"
    for item in elements:
        if item.type == "function":
            function_cards += universal_card1 + item.name + ">" + "Function " + item.name + universal_card2
            function_cards += "<h6>Comments: </h6>"
            for i in item.comments.split("\n"):
                function_cards += i + "<br>"
            function_cards += "<br>"
            function_cards += "<h6>Documentation:</h6>"
            for i in item.documentation.split("\n"):
                function_cards += i + "<br>"
            function_cards += "<br>"
            if item.parent != "":
                function_cards += "<h6>Parent of inner function: </h6>" + item.parent + "<br><br>"
            function_cards += "<h6>Signature:</h6>" + item.signature + "<br><br>"
            function_cards += universal_card3

    for item in elements:
        if item.type == "class":
            class_cards += universal_card1 + item.name + ">" + "Class " + item.name + universal_card2
            class_cards += "<h6>Comments: </h6>"
            for i in item.comments.split("\n"):
                class_cards += i + "<br>"
            class_cards += "<br>"
            class_cards += "<h6>Documentation:</h6>"
            for i in item.documentation.split("\n"):
                class_cards += i + "<br>"
            class_cards += "<br>"
            if item.parent != "":
                class_cards += "<h6>Parent of inner class: </h6>" + item.parent + "<br><br>"
            class_cards += "<h6>Superclasses:</h6>"
            for i in item.mro:
                class_cards += i + "<br>"
            class_cards += universal_card3

    for item in elements:
        if item.type == "attribute":
            attribution_cards += universal_card1 + item.name + ">" + "Attribute " + item.name + universal_card2
            attribution_cards += "<h6>Value: </h6>" + item.value.replace('<',
                                                                         '&lt') + "<br><br>" + "<h6>Parent: </h6>" + item.parent + "<br><br>"
            attribution_cards += universal_card3
    for item in PHTML_DOC_elements_parser.getDocImports(path, name, dir):
        if item.name != "":
            if item.imp_as != "" and not item.name.startswith('from'):
                names += "<li class=\"list-group-item\"><a href=#" + item.name + ">" + "import " + item.name + " as " + item.imp_as + "</a></li>\n"
                import_cards += universal_card1 + item.name + ">" + "Import " + item.name + " as " + item.imp_as + universal_card2
                for i in item.usages:
                    import_cards += i + "<br>"
                import_cards += universal_card3
            elif item.imp_as == "" and not item.name.startswith('from'):
                names += "<li class=\"list-group-item\"><a href=#" + item.name + ">" + "import " + item.name + "</a></li>\n"
                import_cards += universal_card1 + item.name + ">" + "Import " + item.name + universal_card2
                for i in item.usages:
                    import_cards += i + "<br>"
                import_cards += universal_card3
            else:
                names += "<li class=\"list-group-item\"><a href=#" + item.name + ">" + item.name + "</a></li>\n"
                import_cards += universal_card1 + item.name + ">" + item.name + universal_card2
                for i in item.usages:
                    import_cards += i + "<br>"
                import_cards += universal_card3
        else:
            names += " "
    for item in elements:
        if item.type == "module":
            module_name = item.name
            ModuleLine += "<h5>Module comments:</h5><br>"
            for i in item.comments.split("\n"):
                ModuleLine += i + "<br>"
            ModuleLine += "<h5>Module documentation:</h5><br>"
            for i in item.documentation.split("\n"):
                ModuleLine += i + "<br>"
        else:
            if item.name != "":
                names += "<li class=\"list-group-item\"><a href=#" + item.name + ">" + "&nbsp" * 8 * (
                        item.level - 1) + '> ' + item.type + ' ' + item.name + "</a></li>\n"
            else:
                names += " "
    names += "</ol>"
    a = a.replace("<h3>Module description</h3>", ModuleLine)
    a = a.replace("<h3>Module elements</h3>", names)
    a = a.replace("<h3>Import details</h3>", import_cards)
    a = a.replace("<h3>Attributes details</h3>", attribution_cards)
    a = a.replace("<h3>Class details</h3>", class_cards)
    a = a.replace("<h3>Function details</h3>", function_cards)
    a = a.replace("Project_Name", project_name)
    a = a.replace("%ELEMENTNAME%", module_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    PHTML_DOC_parser_util.copy_styles_to_folder(folder_path)
    if subdir != '':
        result = open(folder_path + subdir + '.' + module_name + ".html", "w+", encoding="utf-8")
    else:
        result = open(folder_path + module_name + ".html", "w+", encoding="utf-8")
    result.write(a)
    return elements


def generate_docmain_html(project_name, project_version, folder_path):
    f = open("PHTML_DOC_main.html", 'r')
    a = f.read()
    a = a.replace('%PRNAME%', project_name)
    a = a.replace('%PROJECTNAME%', project_name)
    a = a.replace('%PROJECTVERSION%', str(project_version))
    a = a.replace('%GENERATORNAME%', Generator_name)
    a = a.replace('%GENERATIONDATE%', str(datetime.datetime.today()))
    docmain = open(folder_path + "docmain.html", "w+")
    docmain.write(a)


def generate_tree_html(root, all_bool, name, folder_path):
    start = "<div class=\"list-group list-group-mine well\">"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    f = open("PHTML_DOC_tree.html", 'r')
    a = f.read()
    a = a.replace('%PRNAME%', name)
    insertion = ""
    level = root.count("\\")
    if all_bool == 0:
        tree = os.walk(root)
        count = 0
        for item in tree:
            dir_is_empty = True
            lvl = item[0].count("\\") - level
            if len(item[2]) > 0:
                for file in item[2]:
                    if file.endswith(".py"):
                        dir_is_empty = False
                if not dir_is_empty:
                    insertion += "<a class =\"list-group-item list-group-item-secondary\" >" + "<pre>" + lvl * "      " + (
                        os.path.relpath(item[0], start=root) if item[0] != root else item[0]) + "</pre>" + "</a>"
                    for file in item[2]:
                        if file.endswith(".py"):
                            direct = os.path.join(item[0])
                            subdir = direct.partition(root)[2]
                            subdir = subdir.replace('\\', '.')
                            count += 1
                            if subdir != "":
                                insertion += (
                                        "<a  href = \"" + folder_path + subdir + "." + file.split('.py')[0]
                                        + ".html\" class =\"list-group-item list-group-item-action "
                                          "list-group-item-primary\">" + "<pre>" + (
                                                lvl + 1) * "      " + file + "</pre>" + "</a>")
                            else:
                                insertion += (
                                        "<a  href = \"" + folder_path + "/" + file.split('.py')[0]
                                        + ".html\" class =\"list-group-item list-group-item-action "
                                          "list-group-item-primary\">" + "<pre>" + (
                                                lvl + 1) * "  " + file + "</pre>" + "</a>")
                else:
                    insertion += "<a class =\"list-group-item list-group-item-secondary\" >" + "<pre>" + lvl * "      " + (
                        os.path.relpath(item[0], start=root) if item[0] != root else item[0]) + "</pre>" + "</a>"

    elif all_bool == 1:
        insertion += "<a class =\"list-group-item\" >" + root + "</a>"
        lvl = root[0].count("/")
        for filename in os.listdir(root):
            if filename.endswith(".py"):
                insertion += (
                        "<a  href = \"" + folder_path + "/" + filename.split('.py')[
                    0] + ".html\" class =\"list-group-item list-group-item-action list-group-item-primary\">" + "<pre>" + (
                                lvl + 1) * "    " + filename + "</pre>" + "</a>")
    elif all_bool == 2:
        name = root.split('/')[-1:][0]
        name = name.split('.py')[0]
        insertion += "<a  href = \"" + folder_path + "/" + name + ".html\" class =\"list-group-item " \
                                                                  "list-group-item-action list-group-item-primary\">" \
                     + "<pre>" + name + "</pre>" + "</a> "
    index = a.find(start)

    a = a[:index + len(start)] + insertion + a[index + len(start):]
    result = open(folder_path + "tree.html", "w+")
    result.write(a)