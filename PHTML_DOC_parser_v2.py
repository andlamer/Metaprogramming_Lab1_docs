import inspect
import os
import pyclbr
import sys
import io
import dis

TotalFiles = 0
Imports = []


class DocElement:
    name = ""
    type = ""
    parent = ""
    comments = ""
    signature = ""
    level = 0
    documentation = ""
    value = ""
    mro = []

    def __init__(self):
        self.mro = list()

    def ReturnFullName(self):
        if self.type == "module":
            return "\n" + "Name: " + self.name + " type: " + self.type + " \n" + "documentation: " + str(
                self.documentation) + " \n" + "comments: " + str(self.comments) + " \n"
        elif self.type == "attribute":
            return "\n" + "Name: " + self.name + " type: " + self.type + " value: " + self.value + " parents: " + self.parent + "\n"
        elif self.type == "class":
            return "\n" + "Name: " + self.name + " type: " + self.type + " \n" + "documentation: " + self.documentation + " \n" + "comments: " + self.comments + " \nsignature: " + self.signature + "\n" + "parents: " + self.parent + "\n"
        elif self.type == "function":
            return "\n" + "Name: " + self.name + " type: " + self.type + " \n" + "documentation: " + self.documentation + " \n" + "comments: " + self.comments + " \nsignature: " + self.signature + "\n" + "parents: " + self.parent + "\n"


class Import():
    name = ""
    imp_as = ""
    usages = []

    def __init__(self):
        self.usages = list()

    def ShowUsages(self):
        if self.imp_as != "":
            for i in self.usages:
                if __name__ == "__main__":
                    print(i)
        else:
            for i in self.usages:
                if __name__ == "__main__":
                    print(i)


def indentsize(line):
    expline = line.expandtabs()
    return len(expline) - len(expline.lstrip())


class Get_Documentation():
    DocElements = []
    Imports = []
    path = ""

    def __init__(self, path, direct, subdir):
        self.DocElements = list()
        self.path = path
        self.direct = direct
        self.subdir = subdir
        self.Imports = list()

    def get_mod_documentation(self, lineno, el_type, sgn_len):
        try:
            source = open(self.path, "r")
            lines = source.readlines()
        except:
            source = io.open(self.path, "r", encoding="utf-8")
            lines = source.readlines()
        if el_type == "module":
            start = 0
            if lines and lines[0][:2] == '#!': start = 1
            while start < len(lines) and lines[start].strip() in ('', '#'):
                start = start + 1
            if start < len(lines) and lines[start][:1] == '#':
                while start < len(lines) and lines[start][:1] == '#':
                    start = start + 1
            while start < len(lines) and lines[start].strip() in ('', '#'):
                start = start + 1
            if start < len(lines) and lines[start][:3] == '\"\"\"':
                doc_string = []
                end = start
                if lines[end].lstrip("\" ").find("\"\"\"") == -1:
                    doc_string.append(lines[end])
                    end += 1
                    while end < len(lines) and (lines[end].find('\"\"\"') == -1):
                        doc_string.append(lines[end])
                        end = end + 1
                    if end < len(lines) and lines[end].find('\"\"\"') != -1:
                        doc_string.append(lines[end])
                    else:
                        return ''.join(["ERROR. CLOSING \"\"\" NOT FOUND"])
                else:
                    doc_string.append(lines[end])
                return ''.join(doc_string)
        elif lineno > 0:
            start = lineno - 1 + sgn_len
            indent = indentsize(lines[start]) + 4
            start += 1
            while start < len(lines) and ((lines[start].strip() in ('')) or lines[start].lstrip().startswith('#')):
                start = start + 1
            if start < len(lines) and lines[start].lstrip()[:3] == '\"\"\"' and \
                    indentsize(lines[start]) == indent:
                doc_string = []
                end = start
                if lines[end].lstrip("\" ").find("\"\"\"") == -1:
                    doc_string.append(lines[end])
                    end += 1
                    while end < len(lines) and (lines[end].find('\"\"\"') == -1):
                        doc_string.append(lines[end])
                        end = end + 1
                    if end < len(lines) and lines[end].find('\"\"\"') != -1:
                        doc_string.append(lines[end])
                    else:
                        return ''.join(["ERROR. CLOSING \"\"\" NOT FOUND"])
                else:
                    doc_string.append(lines[end])
                return ''.join(doc_string)

    def get_attributes(self, lineno, parent_name, level, sgn_len, type):
        try:
            source = open(self.path, "r")
            lines = source.readlines()
        except:
            source = io.open(self.path, "r", encoding="utf-8")
            lines = source.readlines()
        if type != "module":
            start = lineno - 1 + sgn_len
            function_indent = indentsize(lines[start])
            indent = indentsize(lines[start]) + 4
            start += 1
            class_line = True
            while class_line and start < len(lines):
                if (lines[start].strip() in ('')) or (lines[start].lstrip().startswith("#")):
                    next_line = start + 1
                    if next_line < len(lines) and indentsize(lines[next_line]) == function_indent and not (
                            lines[next_line].startswith("#")) and not (
                            lines[next_line].startswith("\"\"\"")):
                        class_line = False
                    start += 1
                elif lines[start].find("=") != -1 and lines[start].partition("=")[0].find("#") == -1 and \
                        lines[start].partition("=")[0].find(".") == -1 and lines[start].partition("=")[0].find(
                    "(") == -1 and indentsize(lines[start]) == indent and \
                        lines[start][(lines[start].find("=") - 1)] not in ("-", "+", "=", "!", "%", "/", "\\"):
                    temp = DocElement()
                    temp.name = lines[start].partition("=")[0].strip()
                    temp.level = level
                    temp.parent = parent_name
                    temp.type = "attribute"
                    temp.mro = []
                    temp.documentation = None
                    temp.signature = None
                    val = ""
                    if lines[start].partition("=")[2].find("[") != -1:
                        a = lines[start].partition("=")[2]
                        if a.rstrip("\n").rstrip().endswith("]"):
                            for i in range(0, len(a)):
                                val += a[i]
                            start += 1
                        else:
                            for i in range(0, len(a)):
                                val += a[i]
                            start += 1
                            while start < len(lines) and not lines[start].rstrip('\n').rstrip().endswith("]"):
                                l = lines[start].strip()
                                for i in range(0, len(l)):
                                    val += l[i]
                                start += 1
                            if start < len(lines) and lines[start].rstrip('\n').rstrip().endswith("]"):
                                l = lines[start].strip()
                                for i in range(0, len(l)):
                                    val += l[i]
                                start += 1
                    elif lines[start].partition("=")[2].find("{") != -1:
                        a = lines[start].partition("=")[2]
                        if a.rstrip("\n").rstrip().endswith("}"):
                            for i in range(0, len(a)):
                                val += a[i]
                            start += 1
                        else:
                            for i in range(0, len(a)):
                                val += a[i]
                            start += 1
                            while start < len(lines) and not lines[start].rstrip('\n').rstrip().endswith("}"):
                                l = lines[start].strip()
                                for i in range(0, len(l)):
                                    val += l[i]
                                start += 1
                            if start < len(lines) and lines[start].rstrip('\n').rstrip().endswith("}"):
                                l = lines[start].strip()
                                for i in range(0, len(l)):
                                    val += l[i]
                                start += 1
                    elif lines[start].partition("=")[2].find("(") != -1:
                        a = lines[start].partition("=")[2]
                        if a.rstrip("\n").rstrip().endswith(")"):
                            for i in range(0, len(a)):
                                val += a[i]
                            start += 1
                        else:
                            for i in range(0, len(a)):
                                val += a[i]
                            start += 1
                            while start < len(lines) and not lines[start].rstrip('\n').rstrip().endswith(")"):
                                l = lines[start].strip()
                                for i in range(0, len(l)):
                                    val += l[i]
                                start += 1
                            if start < len(lines) and lines[start].rstrip('\n').rstrip().endswith(")"):
                                l = lines[start].strip()
                                for i in range(0, len(l)):
                                    val += l[i]
                                start += 1
                    elif lines[start].partition("=")[2].find("\"\"\"") != -1:
                        a = lines[start].partition("=")[2]
                        if a.rstrip("\n").rstrip().endswith("\"\"\"") and a.rstrip('\n').rstrip().find("\"\"\"") != len(
                                a) - 4:
                            for i in range(0, len(a)):
                                val += a[i]
                                start += 1
                        else:
                            for i in range(0, len(a)):
                                val += a[i]
                            start += 1
                            while start < len(lines) and not lines[start].rstrip('\n').rstrip().endswith("\"\"\""):
                                l = lines[start].strip()
                                for i in range(0, len(l)):
                                    val += l[i]
                                val += '\n'
                                start += 1
                            if start < len(lines) and lines[start].rstrip('\n').rstrip().endswith("\"\"\""):
                                l = lines[start].strip()
                                for i in range(0, len(l)):
                                    val += l[i]
                                start += 1
                    elif lines[start].partition("=")[2].rstrip('\n').rstrip().endswith("\\"):
                        a = lines[start].partition("=")[2]
                        for i in range(0, len(a)):
                            val += a[i]
                        start += 1
                        while start < len(lines) and lines[start].rstrip('\n').rstrip().endswith("\\"):
                            l = lines[start].lstrip()
                            for i in range(0, len(l)):
                                val += l[i]
                            start += 1
                        if start < len(lines) and not lines[start].rstrip('\n').rstrip().endswith("\\"):
                            l = lines[start].strip()
                            for i in range(0, len(l)):
                                val += l[i]
                            start += 1
                    else:
                        a = lines[start].partition("=")[2].strip()
                        for i in range(0, len(a)):
                            val += a[i]
                        start += 1
                    temp.value = val.strip()
                    self.DocElements.append(temp)
                elif lines[start].rstrip().startswith("\"\"\""):
                    if lines[start].lstrip("\" ").find("\"\"\"") == -1:
                        start += 1
                    while start < len(lines) and (lines[start].find('\"\"\"') == -1):
                        start = start + 1
                    start += 1
                else:
                    next_line = start + 1
                    if next_line < len(lines) and indentsize(lines[next_line]) == function_indent and not (
                            lines[next_line].startswith("#")) and not (
                            lines[next_line].startswith("\"\"\"")):
                        class_line = False
                    start += 1
        else:
            indent = 0
            start = 0
            i = 0
            while start < len(lines):
                if lines[start].find("=") != -1 and lines[start].partition("=")[0].find("#") == -1 and \
                        lines[start].partition("=")[0].find(".") == -1 and lines[start].partition("=")[0].find(
                    "(") == -1 and indentsize(lines[start]) == indent and \
                        lines[start][(lines[start].find("=") - 1)] not in ("-", "+", "=", "!", "%", "/", "\\") and \
                        lines[start].partition("=")[0].find("if ") == -1 and lines[start].partition("=")[0].find(
                    "while ") == -1:
                    temp = DocElement()
                    temp.name = lines[start].partition("=")[0].strip()
                    temp.level = level
                    temp.parent = parent_name
                    temp.type = "attribute"
                    temp.mro = []
                    temp.documentation = None
                    temp.signature = None
                    val = ""
                    if lines[start].partition("=")[2].find("[") != -1:
                        a = lines[start].partition("=")[2]
                        if a.rstrip("\n").rstrip().endswith("]"):
                            for i in range(0, len(a)):
                                val += a[i]
                            start += 1
                        else:
                            for i in range(0, len(a)):
                                val += a[i]
                            start += 1
                            while start < len(lines) and not lines[start].rstrip('\n').rstrip().endswith("]"):
                                l = lines[start].strip()
                                for i in range(0, len(l)):
                                    val += l[i]
                                start += 1
                            if start < len(lines) and lines[start].rstrip('\n').rstrip().endswith("]"):
                                l = lines[start].strip()
                                for i in range(0, len(l)):
                                    val += l[i]
                                start += 1
                    elif lines[start].partition("=")[2].find("{") != -1:
                        a = lines[start].partition("=")[2]
                        if a.rstrip("\n").rstrip().endswith("}"):
                            for i in range(0, len(a)):
                                val += a[i]
                            start += 1
                        else:
                            for i in range(0, len(a)):
                                val += a[i]
                            start += 1
                            while start < len(lines) and not lines[start].rstrip('\n').rstrip().endswith("}"):
                                l = lines[start].strip()
                                for i in range(0, len(l)):
                                    val += l[i]
                                start += 1
                            if start < len(lines) and lines[start].rstrip('\n').rstrip().endswith("}"):
                                l = lines[start].strip()
                                for i in range(0, len(l)):
                                    val += l[i]
                                start += 1
                    elif lines[start].partition("=")[2].find("(") != -1:
                        a = lines[start].partition("=")[2]
                        if a.rstrip("\n").rstrip().endswith(")"):
                            for i in range(0, len(a)):
                                val += a[i]
                            start += 1
                        else:
                            for i in range(0, len(a)):
                                val += a[i]
                            start += 1
                            while start < len(lines) and not lines[start].rstrip('\n').rstrip().endswith(")"):
                                l = lines[start].strip()
                                for i in range(0, len(l)):
                                    val += l[i]
                                start += 1
                            if start < len(lines) and lines[start].rstrip('\n').rstrip().endswith(")"):
                                l = lines[start].strip()
                                for i in range(0, len(l)):
                                    val += l[i]
                                start += 1
                    elif lines[start].partition("=")[2].find("\"\"\"") != -1:
                        a = lines[start].partition("=")[2]
                        if a.rstrip("\n").rstrip().endswith("\"\"\"") and a.rstrip('\n').rstrip().find("\"\"\"") != len(
                                a) - 4:
                            for i in range(0, len(a)):
                                val += a[i]
                                start += 1
                        else:
                            for i in range(0, len(a)):
                                val += a[i]
                            start += 1
                            while start < len(lines) and not lines[start].rstrip('\n').rstrip().endswith("\"\"\""):
                                l = lines[start].strip()
                                for i in range(0, len(l)):
                                    val += l[i]
                                val += '\n'
                                start += 1
                            if start < len(lines) and lines[start].rstrip('\n').rstrip().endswith("\"\"\""):
                                l = lines[start].strip()
                                for i in range(0, len(l)):
                                    val += l[i]
                                start += 1
                    elif lines[start].partition("=")[2].rstrip('\n').rstrip().endswith("\\"):
                        a = lines[start].partition("=")[2]
                        for i in range(0, len(a)):
                            val += a[i]
                        start += 1
                        while start < len(lines) and lines[start].rstrip('\n').rstrip().endswith("\\"):
                            l = lines[start].lstrip()
                            for i in range(0, len(l)):
                                val += l[i]
                            start += 1
                        if start < len(lines) and not lines[start].rstrip('\n').rstrip().endswith("\\"):
                            l = lines[start].strip()
                            for i in range(0, len(l)):
                                val += l[i]
                            start += 1
                    else:
                        a = lines[start].partition("=")[2].strip()
                        for i in range(0, len(a)):
                            val += a[i]
                        start += 1
                    temp.value = val.strip()
                    self.DocElements.append(temp)
                else:
                    start += 1

    def get_comments(self, lineno, el_type):
        try:
            source = open(self.path, "r")
            lines = source.readlines()
        except:
            source = io.open(self.path, "r", encoding="utf-8")
            lines = source.readlines()
        lineno -= 1
        if el_type == "module":
            # Look for a comment block at the top of the file.
            start = 0
            if lines and lines[0][:2] == '#!': start = 1
            while start < len(lines) and lines[start].strip() in ('', '#'):
                start = start + 1
            if start < len(lines) and lines[start][:1] == '#':
                comments = []
                end = start
                while end < len(lines) and lines[end][:1] == '#':
                    comments.append(lines[end].expandtabs())
                    end = end + 1
                return ''.join(comments)

        # Look for a preceding block of comments at the same indentation.
        elif lineno > 0:
            indent = indentsize(lines[lineno])
            end = lineno - 1
            if end >= 0 and lines[end].lstrip()[:1] == '#' and \
                    indentsize(lines[end]) == indent:
                comments = [lines[end].expandtabs().lstrip()]
                if end > 0:
                    end = end - 1
                    comment = lines[end].expandtabs().lstrip()
                    while comment[:1] == '#' and indentsize(lines[end]) == indent:
                        comments[:0] = [comment]
                        end = end - 1
                        if end < 0: break
                        comment = lines[end].expandtabs().lstrip()
                while comments and comments[0].strip() == '#':
                    comments[:1] = []
                while comments and comments[-1].strip() == '#':
                    comments[-1:] = []
                return ''.join(comments)
        pass

    def get_custom_imports(self, module):
        try:
            source = open(self.path, "r")
            lines = source.readlines()
        except:
            source = io.open(self.path, "r", encoding="utf-8")
            lines = source.readlines()
        line_number = 0
        if os.path.getsize(self.path) > 0:
            start = 0
            if lines and lines[0][:2] == '#!': start = 1
            while start < len(lines) and lines[start].strip() in ('', '#'):
                start = start + 1
            if start < len(lines) and lines[start][:1] == '#':
                while start < len(lines) and lines[start][:1] == '#':
                    start = start + 1
            while start < len(lines) and lines[start].strip() in ('', '#'):
                start = start + 1
            if start < len(lines) and lines[start][:3] == '\"\"\"':
                if lines[start].lstrip('\"').find('\"\"\"') != -1:
                    start += 1
                else:
                    start += 1
                    while start < len(lines) and (lines[start].find('\"\"\"') == -1):
                        start += 1
                    start += 1

            mod_lines = []
            for i in range(start, len(lines)):
                mod_lines.append(lines[i])

            for a in mod_lines:
                line_number += 1
                if a.startswith("import") or a.startswith("from"):
                    if a.startswith("import") and a.find(" as ") == -1:
                        i = 0
                        import_name = a[len("import ")::]
                        import_name = import_name.lstrip()
                        import_name = import_name.rstrip()
                        TempImport = Import()
                        TempImport.name = import_name
                        TempImport.imp_as = ""
                        for line in mod_lines:
                            i += 1
                            if line_number < i and line.find(import_name + ".") != -1:
                                line_num = i
                                line = line.lstrip()
                                line = line.rstrip()
                                if line.find("\"") == -1 and line.find('\'') == -1 and line.find('#') == -1:
                                    line = "line number: " + str(line_num) + "&nbsp &nbsp &nbsp source: &nbsp   " + line
                                    TempImport.usages.append(line)
                        TempImport.ShowUsages()
                        self.Imports.append(TempImport)

                    elif a.startswith("import") and a.find(" as ") != -1:
                        i = 0
                        import_name = a[len("import "):a.find(" as "):]
                        import_name = import_name.lstrip()
                        import_name = import_name.rstrip()
                        import_as_name = a[a.find(" as ") + 4::]
                        import_as_name = import_as_name.lstrip()
                        import_as_name = import_as_name.rstrip()
                        TempImport = Import()
                        TempImport.name = import_name
                        TempImport.imp_as = import_as_name
                        for line in mod_lines:
                            i += 1
                            if line_number < i and line.find(import_as_name + ".") != -1:
                                line_num = i
                                line = line.lstrip()
                                line = line.rstrip()
                                temp = line.partition(import_as_name)
                                if line.find("\"") == -1 and line.find('\'') == -1 and line.find('#') == -1:
                                    line = "line number: " + str(line_num) + "&nbsp &nbsp &nbsp source: &nbsp   " + line
                                    TempImport.usages.append(line)
                        TempImport.ShowUsages()
                        self.Imports.append(TempImport)
                    elif a.startswith("from"):
                        TempImport = Import()
                        a = a.rstrip()
                        a = a.lstrip()
                        TempImport.name = a
                        self.Imports.append(TempImport)
        source.close()

    def get_Imports(self):
        self.get_custom_imports(self.path)
        return self.Imports

    def get_markdown(self, module_name):
        temp = DocElement()
        temp.name = module_name
        temp.type = "module"
        temp.documentation = inspect.cleandoc(str(self.get_mod_documentation(0, temp.type, 0)))
        temp.comments = str(self.get_comments(0, temp.type))
        temp.parent = None
        temp.signature = None
        temp.value = None
        temp.level = 0
        lvl = temp.level + 1
        self.DocElements.append(temp)
        self.get_attributes(0, temp.name, lvl, 0, temp.type)
        print(module_name)
        try:
            modules = pyclbr.readmodule_ex(temp.name)
            for i in modules.items():
                if i[0] == "__path__":
                    module_name = module_name + "." + module_name
                    modules = pyclbr.readmodule_ex(module_name)
            for i in modules.items():
                if not (i[0].startswith("__")):
                    if hasattr(i[1], "methods"):
                        self.get_classes(i, temp.name, lvl)
                    else:
                        self.get_functions(i, temp.name, lvl)
        except:
            pass
        return self.DocElements

    def get_classes(self, item, parent_name, level):
        sign = self.get_signature(item[1].lineno)
        if (sign[1] != "Imported file"):
            temp = DocElement()
            temp.name = item[0]
            temp.type = "class"
            temp.signature = sign[1]
            temp.documentation = inspect.cleandoc(
                str(self.get_mod_documentation(item[1].lineno, temp.type, sign[0])))
            temp.comments = str(self.get_comments(item[1].lineno, temp.type))
            temp.level = level
            temp.parent = parent_name
            temp.value = None
            self.DocElements.append(temp)
            for i in item[1].super:
                if isinstance(i, pyclbr.Class):
                    temp.mro.append(i.name)
                elif isinstance(i, str):
                    temp.mro.append(i)
            lvl = level + 1
            self.get_attributes(item[1].lineno, temp.name, lvl, sign[0], temp.type)
            for i in item[1].children.items():
                if hasattr(i[1], "methods"):
                    self.get_classes(i, item[0], lvl)
                else:
                    self.get_functions(i, item[0], lvl)

    def get_functions(self, item, parent_name, level):
        sign = self.get_signature(item[1].lineno)

        if (sign[1] != "Imported file"):
            temp = DocElement()
            temp.name = item[0]
            temp.type = "function"

            temp.signature = sign[1]
            temp.documentation = inspect.cleandoc(
                str(self.get_mod_documentation(item[1].lineno, temp.type, sign[0])))
            temp.comments = str(self.get_comments(item[1].lineno, temp.type))
            temp.level = level
            temp.parent = parent_name
            temp.value = None
            self.DocElements.append(temp)
            lvl = level + 1
            for i in item[1].children.items():
                if hasattr(i[1], "super"):
                    self.get_classes(i, item[0], lvl)
            self.get_attributes(item[1].lineno, temp.name, lvl, sign[0], temp.type)

    def get_signature(self, lineno):
        try:
            source = open(self.path, "r")
            lines = source.readlines()
        except:
            source = io.open(self.path, "r", encoding="utf-8")
            lines = source.readlines()
        if lineno != 0:
            lineno -= 1
        signature = ""
        length = 0
        if lineno < len(lines) and lines[lineno].lstrip().startswith("class"):
            br_count = 0
            if lines[lineno].find("(") == -1:
                return [0, '']
            else:
                if lines[lineno].rstrip("\n").rstrip().endswith(":"):
                    length = 0
                    a = lines[lineno].rstrip(": \n")
                    for i in range(a.find("("), len(a)):
                        signature += a[i]
                        if a[i] == "(":
                            br_count += 1
                        if a[i] == ")":
                            br_count -= 1
                    if br_count == 0:
                        return [length, signature]
                    else:
                        return [length, signature]
                else:
                    a = lines[lineno].rstrip()
                    for i in range(a.find("("), len(a)):
                        signature += a[i]
                        if a[i] == "(":
                            br_count += 1
                        if a[i] == ")":
                            br_count -= 1
                    lineno += 1
                    length += 1
                    while lineno < len(lines) and not lines[lineno].rstrip('\n').rstrip().endswith(":"):
                        l = lines[lineno].strip()
                        for i in range(0, len(l)):
                            signature += l[i]
                            if l[i] == "(":
                                br_count += 1
                            if l[i] == ")":
                                br_count -= 1
                        lineno += 1
                        length += 1
                    if lineno < len(lines) and lines[lineno].rstrip('\n').rstrip().endswith(":"):
                        a = lines[lineno].strip()
                        for i in range(0, len(a) - 1):
                            signature += a[i]
                            if a[i] == "(":
                                br_count += 1
                            if a[i] == ")":
                                br_count -= 1
                        if br_count == 0:
                            return [length, signature]
                        else:
                            return [length, ""]
        elif lineno < len(lines) and lines[lineno].lstrip().startswith("def"):
            br_count = 0
            if lines[lineno].find("(") == -1:
                return [0, 'THERE IS NO SIGNATURE FOR FUNC']
            else:
                if lines[lineno].rstrip("\n").rstrip().endswith(":"):
                    length = 0
                    a = lines[lineno].rstrip(": \n")
                    for i in range(a.find("("), len(a)):
                        signature += a[i]
                        if a[i] == "(":
                            br_count += 1
                        if a[i] == ")":
                            br_count -= 1
                    if br_count == 0:
                        return [length, signature]
                    else:
                        return [length, signature]
                else:
                    a = lines[lineno].rstrip()
                    for i in range(a.find("("), len(a)):
                        signature += a[i]
                        if a[i] == "(":
                            br_count += 1
                        if a[i] == ")":
                            br_count -= 1
                    lineno += 1
                    length += 1
                    while lineno < len(lines) and not lines[lineno].rstrip('\n').rstrip().endswith(":"):
                        l = lines[lineno].strip()
                        for i in range(0, len(l)):
                            signature += l[i]
                            if l[i] == "(":
                                br_count += 1
                            if l[i] == ")":
                                br_count -= 1
                        lineno += 1
                        length += 1
                    if lineno < len(lines) and lines[lineno].rstrip('\n').rstrip().endswith(":"):
                        a = lines[lineno].strip()
                        for i in range(0, len(a) - 1):
                            signature += a[i]
                            if a[i] == "(":
                                br_count += 1
                            if a[i] == ")":
                                br_count -= 1
                        if br_count == 0:
                            return [length, signature]
                        else:
                            return [length, ""]
        else:
            return [0, "Imported file"]


def get_Doc_Elements(path, name, dir, subdir):
    dir.replace("\\",'/')
    if dir not in sys.path:
        sys.path.append(dir)
    Get_DOC = Get_Documentation(path, dir,subdir)

    return Get_DOC.get_markdown(name)


def get_Doc_Imports(path, name, dir):
    if dir not in sys.path:
        sys.path.append(dir)
    get_doc = Get_Documentation(path, dir,"")
    return get_doc.get_Imports()


ty = ("rfwrf", "rfqrf",
      "rqqrf")
