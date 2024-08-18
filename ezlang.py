import os
# run `pip install alive-progress` in the terminal if having issues.
from alive_progress import *
import shutil
import argparse
import json
import psutil
# run `pip install torch` in the terminal if having issues
import torch
from pick import pick
import sys
import datetime
import time

credits = "COHEJH, AverageNoB, Banjomoomintog"

mit_l = f'''Copyright (c) {datetime.datetime.now().year} {credits}
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.'''

parser = argparse.ArgumentParser(description='An Open-Source Compiler for the EZLang programming language.',)
parser.add_argument('--compile', metavar='FILE', help='The file to be compiled.')
args = parser.parse_args()

if len(sys.argv) == 1:

    settings = {}
    version = "v1.0.0"
    github = "https://github.com/Cohejh/EZLang"
    config_path = os.path.expanduser("~/Documents/EZLang/ez_config.json")
    
    def data_conversion(n:int) -> tuple[int, str]:
        i = 0
        k = n
        units = ["b", "KB", "MB", "GB", "TB"]
        while round(k / 1024) >= 1:
            k = round(k / 1024)
            i += 1
        return (k, units[i])

    ram = data_conversion(psutil.virtual_memory().total)

    main_menu = ["Licence →", "Credits →", "Quit"]

    # Check for a ez_config.json file.
    if os.path.exists(config_path):
        config = open(config_path, "r").read()
        settings = json.loads(config)
        main_menu.insert(0,"Config →")
        if settings["supports-ai"] == True:
            main_menu.insert(1,"AI Settings (Experimental) →")
    else:
        # Create settings
        settings["version"] = version
        settings["github"] = github
        settings["zip"] = True
        settings["check-update"] = True
        if (ram[0] >= 8) and ((ram[1] == "GB") or (ram[1] == "TB")):
            settings["supports-ai"] = True
        else:
            settings["supports-ai"] = False
        if (ram[0] >= 32) and (torch.cuda.is_available() == True):
            settings["ai-model"] = "xl"
        elif (ram[0] >= 16) and (torch.cuda.is_available() == True):
            settings["ai-model"] = "standard"
        else:
            settings["ai-model"] = "nano"
        main_menu.insert(0,"Full Install →")

    options,index = pick(main_menu,"EZLang Menu", "=>")
    if options == "Licence":
        print(mit_l)
    elif options == "Quit":
        sys.exit()
    elif options == "Credits":
        print("EZLang Credits:")
        time.sleep(0.5)
        print("Lead Developer - COHEJH")
        time.sleep(0.5)
        print("Official Finder Of Problems - AverageNoB")
        time.sleep(0.5)
        print("Guy Who Has Yet To Push A Commit To The Repo - Banjomoomintog")
    elif options == "Full Install":
        print("Installing EZLang...")
        os.mkdir(config_path.removesuffix("ez_config.json"))
        open(config_path, "w").write(json.dumps(settings))
        print("Installed EZLang.")

    # Need to add more options later.
    
        
        
    # The Main Compile Function
def compile(f:str,z:bool):
    # Keep track of data types
    data_tracker = {}
    imported_libs = []
    
    # Finally fixed and implemented nested function. Outputs an ugly mess of brackets, but it works...
    def return_bracket_indices(text:str) -> list[list[int]]:
        stack = []
        result = []
        for index, char in enumerate(text):
            if (char == '('):
                stack.append(index)
            elif (char == ')'):
                if stack:
                    opening_index = stack.pop()
                    result.append([opening_index, index])
        result.sort(key=lambda x: x[1])
        if result != []:
            return result[::-1]
        else: 
            return None
    
    def return_curly_bracket_indices(text:str) -> list[list[int]]:
        stack = []
        result = []
        for index, char in enumerate(text):
            if (char == '{'):
                stack.append(index)
            elif (char == '}'):
                if stack:
                    opening_index = stack.pop()
                    result.append([opening_index, index])
        result.sort(key=lambda x: x[1])
        if result != []:
            return result[::-1]
        else: 
            return None
    
    def replace_quotation(s:str) -> str:
        if len(s) > 1:
            if s.count("\"") > 2:
                return s[0] + s[1:-1].replace("\"", "\\\"") + s[-1]
        return s
    
    def count_indents(string:str) -> int:
        return len(string) - len(string.lstrip(' '))
    
    def return_original_var(s:str) -> str:
        return s.removeprefix("ez_usrdata_").upper()
    
    def convert_line(s:str,indents:int=None) -> str:
        proposed_line = s.rstrip()
        ind = count_indents(proposed_line)
        proposed_line = proposed_line.lstrip()
        # Backslashes prohibited in fstrings, so here's a workaround:
        b_quot = "\""
        b_sing = "\'"
        b_back = "\\"
        repeats = 0
        
        # Little script to remove (Nx) repeat function. Must run before Nested function handler.
        if proposed_line.endswith("x)"):
            end_i = proposed_line.rfind("(")
            repeats = int(proposed_line[end_i:].removeprefix("(").removesuffix("x)"))
            proposed_line = proposed_line[:end_i]
        
        if len(data_tracker) != 0:
            for key in data_tracker:
                if (key in proposed_line) and (data_tracker[key] != "file") and (proposed_line[:proposed_line.find(key)].count("\"") % 2 == 0):
                    proposed_line = proposed_line.replace(key,f"ez_usrdata_{key.lower()}")
        
        split_version = proposed_line.split()
        
        if return_bracket_indices(proposed_line) != None:
            for bracket in return_bracket_indices(proposed_line):
                if (proposed_line[:bracket[0]].count("\"") % 2 == 0):
                    inner_expression = convert_line(proposed_line[bracket[0] + 1:bracket[1]])
                    proposed_line = f"{proposed_line[:bracket[0] + 1]}{inner_expression}{proposed_line[bracket[1]:]}"
        
        # Resolve {} seperately, due to different syntax
        if return_curly_bracket_indices(proposed_line) != None:
            for bracket in return_curly_bracket_indices(proposed_line):
                inner_expression = convert_line(proposed_line[bracket[0] + 1:bracket[1]])
                proposed_line = f"{proposed_line[:bracket[0] + 1]}{inner_expression.replace(b_quot,b_sing)}{proposed_line[bracket[1]:]}"
                
        if proposed_line.startswith("say"):
            proposed_line = f"print({proposed_line[4:].strip()})"
            
        elif proposed_line.startswith("ask"):
            proposed_line = f"input({proposed_line[4:].strip()})"
            
        elif proposed_line.startswith("//"):
            proposed_line = f"#{proposed_line.removeprefix('//')}"
            
        elif proposed_line.startswith("create"):
            # Bunch of stuff it could be: list, variable, file, folder
            if split_version[2] == "variable":
                proposed_line = f"ez_usrdata_{split_version[-1].lower()} = \"\""
                data_tracker[split_version[-1]] = "variable"
                
            elif split_version[2] == "list":
                proposed_line = f"ez_usrdata_{split_version[-1].lower()} = []"
                data_tracker[split_version[-1]] = "list"
                
            elif split_version[2] == "file":
                proposed_line = f"open({split_version[-1].lower()}, \"w\").close()"
                data_tracker[split_version[-1]] = "file"
                
            else:
                if "os" not in imported_libs:
                    proposed_line = f"import os\n{' ' * ind}os.mkdir({split_version[-1].lower()})"
                    imported_libs.append("os")
                    
                else:
                    proposed_line = f"os.mkdir({split_version[-1].lower()})"
                data_tracker[split_version[-1]] = "file"
        elif proposed_line.startswith("add"):
            # Add to end of string? or add list items? Or even file. Because of the way we handle variables we need a `try`.
            try:
                if data_tracker[return_original_var(split_version[-1])] == "list":
                    proposed_line = f"{split_version[-1]}.extend([{proposed_line[proposed_line.find(b_quot):proposed_line.rfind(b_quot) + 1]}])"
                    
                else:
                    proposed_line = f"{split_version[-1]} = {split_version[-1].lower()} + {proposed_line[proposed_line.find(b_quot):proposed_line.rfind(b_quot) + 1]}')"
            
            except KeyError:
                proposed_line = f"open({split_version[-1]}, \"a\").write({replace_quotation(proposed_line.removeprefix('add ').removesuffix(f' to {split_version[-1]}'))})"
        
        elif proposed_line.startswith("write"):
            proposed_line = f"open({split_version[-1]}, \"a\").write({replace_quotation(proposed_line.removeprefix('write ').removesuffix(f' to {split_version[-1]}'))})"
        
        elif proposed_line.startswith("insert"):
            proposed_line = f"{split_version[-4].lower()}.insert({int(split_version[-1]) - 1}, {proposed_line[proposed_line.find(b_quot):proposed_line.rfind(b_quot) + 1]})"
        
        elif proposed_line.startswith("remove"):
            proposed_line = f"{split_version[-1].lower()}.pop({int(split_version[2]) - 1})"
        
        elif proposed_line.startswith("set"):
            if data_tracker[return_original_var(split_version[1])] == "list":
                proposed_line = f"{split_version[1]} = [{proposed_line.removeprefix(f'set {split_version[1]} to ')}]"
            
            else:
                proposed_line = f"{split_version[1]} = {proposed_line.removeprefix(f'set {split_version[1]} to ')}"
        
        # In this case, we need "for ", with a space, as it may get confused with "forever".
        elif proposed_line.startswith("for "):
            # For loop detected, which we need to handle.
            data_tracker[split_version[2]] = "iterable"
            proposed_line = f"for ez_usrdata_{split_version[2].lower()} in {split_version[-1].removesuffix(':')}:"
        
        elif proposed_line.startswith("do"):
            proposed_line = f"for ez_core_repeatfunc in range({split_version[1]}):"
        
        elif proposed_line.startswith("wait"):
            if "time" not in imported_libs:
                proposed_line = f"import time\n{' ' * ind}time.sleep({split_version[1].removesuffix('s')})"
                imported_libs.append("time")
            
            else:
                proposed_line = f"time.sleep({split_version[1].removesuffix('s')})"
        
        elif proposed_line.startswith("forever:"):
            proposed_line = "while (True):"
        
        elif proposed_line.startswith("if") or proposed_line.startswith("elif") or proposed_line.startswith("else if"):
            # Fix Else if: Replace with elif.
            if proposed_line.startswith("else if"):
                proposed_line = f"elif{proposed_line[7:]}"
            
            # Probably the hardest thing to implement
            # Shall we just go with replace()?   
            proposed_line = proposed_line.replace("is in", "in")
            proposed_line = proposed_line.replace("is not in", "not in")
            proposed_line = proposed_line.replace("is not", "!=")
            proposed_line = proposed_line.replace("is greater than", ">")
            proposed_line = proposed_line.replace("is less than", "<")
            proposed_line = proposed_line.replace("is greater or equal to", ">=")
            proposed_line = proposed_line.replace("is less or equal to", "<=")
            proposed_line = proposed_line.replace("is","==")
        
        elif proposed_line.startswith("read"):
            if split_version[1] != "line":
                
                if split_version[1] == "every":
                    proposed_line = f"open({proposed_line[proposed_line.find('of') + 2:]}, \"r\").readlines()"
                
                else:
                    proposed_line = f"open({proposed_line.removeprefix('read ')}, \"r\").read()"
            
            else:
                proposed_line = f"open({proposed_line[proposed_line.find('of') + 3:]}, \"r\").readline({int(split_version[2]) - 1})"
        
        elif proposed_line.startswith("delete"):
            
            if split_version[1] == "file":
                if "os" not in imported_libs:
                    proposed_line = f"import os\n{' ' * ind}os.remove({proposed_line.removeprefix('delete file ')})"
                    imported_libs.append("os")
                
                else:
                    proposed_line = f"os.remove({proposed_line.removeprefix('delete file ')})"
            
            elif split_version[1] == "folder":
                if "os" not in imported_libs:
                    proposed_line = f"import os\n{' ' * ind}os.rmdir({proposed_line.removeprefix('delete folder ')})"
                    imported_libs.append("os")
                
                else:
                    proposed_line = f"os.rmdir({proposed_line.removeprefix('delete folder ')})"
            
            else:
                proposed_line = f"del {proposed_line[proposed_line.find(' ', 7):]}"
        
        elif proposed_line.startswith("change"):
            
            if "os" not in imported_libs:
                proposed_line = f"import os\n{' ' * ind}os.chdir({proposed_line.removeprefix('change directory to ')})"
                imported_libs.append("os")
            
            else:
                proposed_line = f"os.chdir({proposed_line.removeprefix('change directory to ')})"
        
        elif proposed_line.startswith("overwrite"):
            
            if split_version[1] == "line":
                if "ez_corelib_overwrite" not in imported_libs:
                    proposed_line = f"def ez_corelib_overwrite(file_name, line_num, text):\n{' ' * ind}{' ' * indents}lines = open(file_name, 'r').readlines()\n{' ' * ind}{' ' * indents}lines[line_num] = text\n{' ' * ind}{' ' * indents}out = open(file_name, 'w')\n{' ' * ind}{' ' * indents}out.writelines(lines)\n{' ' * ind}{' ' * indents}out.close()\n{' ' * ind}ez_corelib_overwrite({split_version[4]}, {int(split_version[2]) - 1}, {proposed_line.removeprefix(f'overwrite line {split_version[2]} of {split_version[4]} to ')})"
                    imported_libs.append("ez_corelib_overwrite")
                
                else:
                    proposed_line = f"ez_corelib_overwrite({split_version[4]}, {int(split_version[2]) - 1}, {proposed_line.removeprefix(f'overwrite line {split_version[2]} of {split_version[4]} to ')})"
            
            else:
                proposed_line = f"open({split_version[1]}, \"w\").write({proposed_line.removeprefix(f'overwrite {split_version[1]} to ')})"    
        
        
        
        # Add indents and repeats back in:
        if repeats != 0:
            proposed_line = (' ' * ind) + (f"for ez_core_repeatfunc in range({repeats}):\n{' ' * ind}{' ' * indents}") + proposed_line
        else:
            proposed_line = (' ' * ind) + proposed_line
            
        
        return proposed_line
    
    if z == True:
        os.mkdir(f"EZ_Compiled_{f.split('.')[0].capitalize()}")
    c = open(f,"r")
    code = c.readlines()
    indent_len = count_indents([item for item in code if count_indents(item) != 0][0])
    c.close()
    if z == True:
        os.chdir(f"EZ_Compiled_{f.split('.')[0].capitalize()}")
    output = open(f"{f.split('.')[0].lower()}.py", "a")
    with alive_bar(len(code), unit=" lines") as bar:
        for line in code:
            output.write(convert_line(line,indent_len) + "\n")
            bar()
    output.close()
    if z == True:
        os.chdir("..")
        shutil.make_archive(f"EZ_Compiled_{f.split('.')[0].capitalize()}", "zip")
        os.rmdir(f"EZ_Compiled_{f.split('.')[0].capitalize()}")
        
# Hi