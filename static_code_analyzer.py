import sys
import os
import re
import ast


class CodeAnalyzer:
    def __init__(self, path):
        self.file_path = path
        self.issues_table = []

    def analyze_code(self):
        with open(self.file_path, 'r') as file:
            file_lines = file.readlines()

            self.analyze_line_length(file_lines)
            self.analyze_indentations(file_lines)
            self.analyze_semicolons(file_lines)
            self.analyze_comment_spaces(file_lines)
            self.analyze_comment_TODO(file_lines)
            self.analyze_blank_lines(file_lines)
            self.analyze_class_def_names(file_lines)
            self.analyze_variables()

    def print_issues(self):
        sorted_issues = sorted(self.issues_table, key=lambda x: (int(x.split("Line")[1].split(":")[0])))

        for issue in sorted_issues:
            print(issue)

    def analyze_line_length(self, file):
        for i, line in enumerate(file, start=1):
            if len(line) > 79:
                issue = f"{self.file_path}: Line {i}: S001 Too long"
                self.issues_table.append(issue)

    def analyze_indentations(self, file):
        for i, line in enumerate(file, start=1):
            n = 0
            for char in line:
                if char == " ":
                    n += 1
                else:
                    if n % 4 != 0:
                        issue = f"{self.file_path}: Line {i}: S002 Indentation is not a multiple of four"
                        self.issues_table.append(issue)
                    break

    def analyze_semicolons(self, file):
        for i, line in enumerate(file, start=1):
            inside_string = False
            for char in line:
                if char == '#':
                    break
                elif char == '\'' or char == '\"':
                    if not inside_string:
                        inside_string = True
                    else:
                        inside_string = False
                elif inside_string:
                    pass
                elif char == ';':
                    issue = f"{self.file_path}: Line {i}: S003 Unnecessary semicolon"
                    self.issues_table.append(issue)
                    break
                else:
                    pass

    def analyze_comment_spaces(self, file):
        for i, line in enumerate(file, start=1):
            for j, char in enumerate(line):
                if char == '#' and j >= 3:
                    if line[j - 1] != ' ' or line[j - 2] != ' ':
                        issue = f"{self.file_path}: Line {i}: S004 At least two spaces required before inline comments"
                        self.issues_table.append(issue)
                        break
                    else:
                        break
                else:
                    pass

    def analyze_comment_TODO(self, file):
        for i, line in enumerate(file, start=1):
            for j, char in enumerate(line):
                if char == '#':
                    line = line[j:]
                    if line.lower().find('todo') != -1:
                        issue = f"{self.file_path}: Line {i}: S005 TODO found"
                        self.issues_table.append(issue)
                        break
                    else:
                        pass

    def analyze_blank_lines(self, file):
        n = 0
        for i, line in enumerate(file, start=1):
            if line.isspace():
                n += 1
            elif n <= 2:
                n = 0
                pass
            else:
                n = 0
                issue = f"{self.file_path}: Line {i}: S006 More than two blank lines used before this line"
                self.issues_table.append(issue)

    def analyze_class_def_names(self, file):
        for i, line in enumerate(file, start=1):

            if re.match(".*class", line):
                if not re.match(r".*class \w", line):
                    issue = f"{self.file_path}: Line {i}: S007 Too many spaces after 'class'"
                    self.issues_table.append(issue)
                elif not re.match(r".*class\s+[A-Z][a-zA-Z1-9]+[:(]", line):
                    cls_name = line.split("class ")[1].split(":")[0]
                    issue = f"{self.file_path}: Line {i}: S008 Class name {cls_name} should use CamelCase"
                    self.issues_table.append(issue)

            if re.match(".*def", line):
                if not re.match(r".*def \w", line):
                    issue = f"{self.file_path}: Line {i}: S007 Too many spaces after 'def'"
                    self.issues_table.append(issue)
                elif not re.match(r".*def\s+[a-z1-9_]+\(", line):
                    fnc_name = line.split("def ")[1].split("(")[0]
                    issue = f"{self.file_path}: Line {i}: S009 Function name {fnc_name} should use snake_case"
                    self.issues_table.append(issue)

    def analyze_variables(self):
        tree = ast.parse(open(self.file_path).read())

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self.check_function_arguments(node)
                self.check_function_variables(node)
                self.check_mutable_default_arguments(node)

    def check_function_arguments(self, node):
        for arg in node.args.args:
            if not re.match("[a-z1-9_]+", arg.arg):
                issue = (f"{self.file_path}: Line {node.lineno}: S010 Argument name "
                         f"'{arg.arg}' should be snake_case")
                self.issues_table.append(issue)

    def check_function_variables(self, node):
        for variable in node.body:
            if isinstance(variable, ast.Assign):
                for var in variable.targets:
                    if isinstance(var, ast.Name):
                        if not re.match("[a-z1-9_]+", var.id):
                            issue = (f"{self.file_path}: Line {var.lineno}: S011 Variable "
                                     f"{var.id} in function should be snake_case")
                            self.issues_table.append(issue)

    def check_mutable_default_arguments(self, node):
        for d_arg in node.args.defaults:
            if isinstance(d_arg, (ast.List, ast.Dict, ast.Set)):
                issue = f"{self.file_path}: Line {node.lineno}: S012 Default argument value is mutable"
                self.issues_table.append(issue)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python code_analyzer.py <file_or_directory>')
        sys.exit()
    else:
        _path = sys.argv[1]

    if os.path.isfile(_path):
        code = CodeAnalyzer(_path)
        code.analyze_code()
        code.print_issues()
    elif os.path.isdir(_path):
        for _file in os.listdir(_path):
            file_path = os.path.join(_path, _file)
            if os.path.isfile(file_path):
                name, extension = os.path.splitext(_file)
                if extension == ".py":
                    code = CodeAnalyzer(file_path)
                    code.analyze_code()
                    code.print_issues()
    else:
        print("Error: Invalid file/directory")
        sys.exit()
