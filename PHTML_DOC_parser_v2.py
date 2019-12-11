import os
import sys

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

    def __init__(self, path):
        self.DocElements = list()
        self.path = path
        self.Imports = list()

    def get_mod_documentation(self, lineno, el_type):
        source = open(self.path, "r")
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
                doc_string.append(lines[end])
                end += 1
                while end < len(lines) and (lines[end].find('\"\"\"') == -1):
                    doc_string.append(lines[end])
                    end = end + 1
                if end < len(lines) and lines[end].find('\"\"\"') != -1:
                    doc_string.append(lines[end])
                else:
                    return ''.join(["ERROR. CLOSING \"\"\" NOT FOUND"])
                return ''.join(doc_string)
        elif lineno > 0:
            start = lineno + 1
            while start < len(lines) and lines[start].strip() in (''):
                start = start + 1
            if start < len(lines) and lines[start].lstrip()[:3] == '\"\"\"' and \
                    indentsize(lines[start]) == indent:
                doc_string = []
                end = start
                doc_string.append(lines[end])
                end += 1
                while end < len(lines) and (lines[end].find('\"\"\"') == -1):
                    doc_string.append(lines[end])
                    end = end + 1
                if end < len(lines) and lines[end].find('\"\"\"') != -1:
                    doc_string.append(lines[end])
                else:
                    return ''.join(["ERROR. CLOSING \"\"\" NOT FOUND"])
                return ''.join(doc_string)

    def get_comments(self, lineno, el_type):
        # try:
        #     lines, lnum = findsource(object)
        # except (OSError, TypeError):
        #     return None
        source = open(self.path, "r")
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

    def getcustomimports(self, module):
        source = open(self.path, "r")
        lines = source.readlines()
        line_number = 0
        if os.path.getsize(self.path) > 0:
            for a in lines:
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
                        for line in lines:
                            i += 1
                            if line_number < i and line.find(import_name + ".") != -1:
                                line_num = i
                                line = line.lstrip()
                                line = line.rstrip()
                                temp = line.partition(import_name)
                                if temp[0].find("\"") == -1 and temp[0].find('\'') == -1 and temp[0].find('#') == -1:
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
                        for line in lines:
                            i += 1
                            if line_number < i and line.find(import_as_name + ".") != -1:
                                line_num = i
                                line = line.lstrip()
                                line = line.rstrip()
                                temp = line.partition(import_as_name)
                                if temp[0].find("\"") == -1 and temp[0].find('\'') == -1 and temp[0].find('#') == -1:
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
        self.getcustomimports(self.path)
        return self.Imports

    def getmarkdown(self, module_name):
        temp = DocElement()
        temp.name = module_name
        temp.type = "module"
        temp.documentation = str(self.get_mod_documentation(0, temp.type))
        temp.comments = str(self.get_comments(60, "temp.type"))
        temp.parent = None
        temp.signature = None
        temp.value = None
        temp.level = 0


    def getattributes(self, module, parent_name, level):
        pass

    def getclasses(self, item, parent_name, level):
        pass

    def getfunctions(self, item, parent_name, level):
        pass


def getDocElements(path, name, dir):
    Get_DOC = Get_Documentation(path)
    Get_DOC.getmarkdown(name)

    return


def getDocImports(path, name, dir):
    return


getDocElements("E:/cpp/main.py", "main", "E:/cpp/")
