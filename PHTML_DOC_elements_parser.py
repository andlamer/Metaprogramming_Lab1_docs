import inspect
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
            return "\n" + "Name: " + self.name + " type: " + self.type + " \n" + "documentation: " + self.documentation + " \n" + "comments: " + self.comments + " \n"
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


class Get_Documentation():
    DocElements = []
    Imports = []
    path = ""

    def __init__(self, path):
        self.DocElements = list()
        self.path = path
        self.Imports = list()

    def getmarkdown(self, module):
        temp = DocElement()
        temp.name = module.__name__
        temp.type = "module"
        temp.documentation = str(inspect.getdoc(module))
        temp.comments = str(inspect.getcomments(module))
        temp.parent = None
        temp.signature = None
        temp.value = None
        temp.level = 0
        self.DocElements.append(temp)
        self.getcustomimports(self.path)
        self.getattributes(module, "", 1)
        self.getfunctions(module, "", 1)
        self.getclasses(module, "", 1)
        return self.DocElements

    def getattributes(self, module, parent_name, level):
        attributes = inspect.getmembers(module, lambda a: not (inspect.isroutine(a)))
        attr = [a for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))]
        for attrs in attr:
            if not (inspect.isclass(attrs[1])) and not (inspect.isfunction(attrs[1])) and not (
                    inspect.ismodule(attrs[1])):
                temp = DocElement()
                temp.name = str(attrs[0])
                temp.type = "attribute"
                temp.documentation = None
                temp.comments = None
                temp.parent = parent_name
                temp.level = level
                temp.value = str(getattr(module, attrs[0]))
                self.DocElements.append(temp)

    def getclasses(self, item, parent_name, level):
        for cl in inspect.getmembers(item, inspect.isclass):
            if cl and cl[0] != "__class__" and not cl[0].startswith("_") and ((
                                                                                      not inspect.ismodule(item) and cl[
                                                                                  1].__module__ == item.__module__) or (
                                                                                      inspect.ismodule(item) and cl[
                                                                                  1].__module__ == item.__name__)):
                # Consider anything that starts with _ private
                # and don't document it
                temp = DocElement()
                temp.name = str(cl[0])
                temp.type = "class"
                temp.documentation = str(inspect.getdoc(cl[1]))
                temp.comments = str(inspect.getcomments(cl[1]))
                temp.parent = parent_name
                temp.level = level
                temp.value = None
                for i in inspect.getmro(cl[1]):
                    if i.__name__ != cl[0]:
                        temp.mro.append(i.__name__)
                self.DocElements.append(temp)

                lvl = level + 1

                self.getfunctions(cl[1], cl[0], lvl)
                self.getclasses(cl[1], cl[0], lvl)
                self.getattributes(cl[1], cl[0], lvl)

    def getfunctions(self, item, parent_name, level):
        for func in inspect.getmembers(item, inspect.isfunction):
            temp = DocElement()
            temp.name = str(func[0])
            temp.type = "function"
            temp.documentation = str(inspect.getdoc(func[1]))
            temp.comments = str(inspect.getcomments(func[1]))
            temp.parent = parent_name
            temp.level = level
            temp.value = None
            temp.signature = str(inspect.signature(func[1]))
            self.DocElements.append(temp)
            lvl = level + 1
            if level == 1:
                self.getattributes(func[1], func[0], lvl)

    def getcustomimports(self, module):
        source = open(self.path, "r")
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

    def get_Imports(self):
        self.getcustomimports(self.path)
        return self.Imports


# def module_from_file(module_name, file_path):
#     spec = importlib.util.spec_from_file_location(module_name, file_path)
#     module = importlib.util.module_from_spec(spec)
#     mod = SourceFileLoader(module_name, file_path).load_module()
#     return mod


def getDocElements(path, name, dir):
    if dir not in sys.path:
        sys.path.append(dir)

    fname = __import__(name)
    get_doc = Get_Documentation(path)
    return get_doc.getmarkdown(inspect.getmodule(fname))


def getDocImports(path, name, dir):
    if dir not in sys.path:
        sys.path.append(dir)
    fname = __import__(name)
    get_doc = Get_Documentation(path)
    return get_doc.get_Imports()
