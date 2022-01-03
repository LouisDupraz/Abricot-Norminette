import os
import sys
import os.path
from os import path

def check_include(files):
    for dos in files:
        if ((".h" in dos) != True):
            print("\033[1;31;40m[MAJOR]: [G6]:    Include folder should only contain .h files:   ", dos)

def check_control_structure(files):
    inside = open(files, "r")
    depth = 0
    nbr = 0
    for lines in inside:
        nbr+=1
        if ("if" in lines and not("else" in lines)):
            depth = 1
        if ("else if" in lines):
            depth += 1
        if ("else" in lines and not("if" in lines)):
            depth += 1
        if ("for" in lines or "while" in lines):
            depth += 1
        if (lines[0] == '{' or lines[0] == '}'):
            depth = 0
        if (depth > 3 or ("           " in lines and ("if" in lines or "else" in lines or "for" in lines or "while" in lines))):
            depth = 0
            print("\033[1;33;40m[MINOR]: [C1]:     There should not be more than 3 depth:        ", files,"line :", nbr)
            
def check_layout_inside_function(files):
    inside = open(files, "r")
    line = 0
    test = 0;
    index = 0
    for lines in inside:
        test += 1
        for char in lines:
            if (char == '\t' and ("Makefile" in files) != True):
                print("\033[1;33;40m[MINOR]: [L2]:     No tab should be replaced by an identation:   ", files, "line :", test)
    inside.close()
    inside = open(files, "r")
    line = 0
    prev_line = "02"
    for lines in inside:
        line += 1
        if (lines[0] != ' ' and lines[0] != '\n' and "(" in lines and ")" in lines and "{" in lines):
            print("\033[1;33;40m[MINOR]: [L4]:              Curly brackets misplaced:            ", files, "line :", line)
        if (lines[0] == ' ' and "{" in lines and not("if" in lines) and not("else" in lines) and not("for" in lines) and not("while" in lines) and not(")" in lines) and not("}" in lines)):
            print("\033[1;33;40m[MINOR]: [L4]:              Curly brackets misplaced:            ", files, "line :", line)
        if (prev_line[0] == ' ' and "}" in prev_line and not("if" in prev_line) and not("else" in prev_line) and not("for" in prev_line) and not("while" in prev_line) and "else" in lines and not("}" in lines)):
            print("\033[1;33;40m[MINOR]: [L4]:              Curly brackets misplaced:            ", files, "line :", line)
        prev_line = lines
    inside.close()
            
def check_function(files):
    inside = open(files, "r")
    line = 0
    for lines in inside:
        line += 1
        if len(lines) > 80:
            print("\033[1;31;40m[MAJOR]: [F3]: The length of a line should not exceed 80 columns:", files, "line :", line, "(", len(lines), "> 80 )")
    inside.close()
    inside = open(files, "r")
    counter = 0
    begin_line = 0
    line = 0;
    if (".c" in files):
        for lines in inside:
            line += 1
            if (lines[0] == '{'):
                counter = 1
                begin_line = line
            if (counter > 0):
                counter += 1
            if (lines[0] == '}'):
                if (counter - 3 > 20):
                    print("\033[1;31;40m[MAJOR]: [F4]:       A function should not exceed 20 lines:      ", files, "line :", begin_line, "(", counter - 3, "> 20 )")
                counter = 0
    inside.close()
    inside = open(files, "r")
    line = 0
    counter = 0
    for lines in inside:
        line += 1
        for char in lines:
            if (char == '(' and lines[0] != ' '):
                counter = 1
            if (counter > 0 and char == ','):
                counter += 1
            if (char == ')'):
                if (counter > 4):
                    print("\033[1;31;40m[MAJOR]: [F5]:   Function should not need more than 4 arguments: ", files, "line :", line,"(", counter, "> 4 )")
                counter = 0
    inside.close()
            
def check_global_scope(files):
    inside = open(files, "r")
    line_nbr = 0
    result = ""
    mid_res = ""
    for line in inside:
        if (line_nbr > 5):
            break
        if (line_nbr != 2 and line_nbr != 4):
            if (line_nbr == 1):
                for char in line:
                    mid_res += char
                    if (char == ','):
                        break
                mid_res += "\n"
                result += mid_res
            else:
                result += line
        line_nbr += 1
    if (".c" in  files):
        if (result != "/*\n** EPITECH PROJECT,\n** File description:\n*/\n"):
            print("\033[1;31;40m[MAJOR]: [G1]:              File header not correct:             ", files)
    if (files == "Makefile"):
        if (result != "##\n## EPITECH PROJECT,\n## File description:\n##\n"):
            print("\033[1;31;40m[MAJOR]: [G1]:              File header not correct:             ", files)
    inside.close()
    inside = open(files, "r")
    trailling_lines = 0;
    line_nbr = 0
    if (".c" in files):
        for lines in inside:
            line_nbr += 1
            if (lines == "\n"):
                trailling_lines += 1
            else:
                trailling_lines = 0
            if (trailling_lines == 2):
                trailling_lines = 0;
                print("\033[1;33;40m[MINOR]: [G2]:   There should be only one empty_line each time:  ", files, ": line:", line_nbr)
    inside.close()
    inside = open(files, "r")
    line = 0
    for lines in inside:
        line += 1
        index = 0
        for char in lines:
            if (char == ' ' and lines[index + 1] == '\n' and line > 7):
                print("\033[1;33;40m[MINOR]: [G8]:                  Trailling space:                 ", files, "line :", line)
            index += 1
    inside.close()
            
def check_file_organization(files):
    forbidden_files = [ ".o", ".gch", ".a", ".so", "~", "#", ".d" ]
    for ext in forbidden_files:
        if (ext in str(files)):
            print("\033[1;31;40m[MAJOR]: [O1]:    Delivery Folder should not contain", ext,"files:   ", files)
    if (any(ele.isupper() for ele in str(files)) == True and ("Makefile" in files) != True):
        print("\033[1;31;40m[MAJOR]: [O4]:          Name not in snake case convention:        ", files)
    inside = open(files, "r", encoding = "UTF-8")
    function_nbr = 0
    if (".c" in files):
        for lines in inside:
            if (lines[0] == '{'):
                function_nbr += 1
    if (function_nbr > 5):
        print("\033[1;31;40m[MAJOR]: [03]:          Too many functions in one file :         ", files, "(", function_nbr, "> 5 )")
    inside.close()

def check_coding_style(files):
    check_file_organization(files)
    if ".c" in files || "Makefile" in files || ".h" in files:
        check_global_scope(files)
        check_function(files)
        check_layout_inside_function(files)
        check_control_structure(files)

def browse_directory(directory, paths):
    for files in directory:
        test = paths + "/" + files
        if path.isdir(test):
            if (files == "include"):
                check_include(os.listdir(test))
            browse_directory(os.listdir(test), paths + "/" + str(files))
        else:
            if (".c" in files or ".h" in files or "Makefile" in files or ".o" in files):
                check_coding_style(paths + "/" + files)

def main():
    directory = os.listdir(".")
    paths = "."
    browse_directory(directory, paths)

main()
