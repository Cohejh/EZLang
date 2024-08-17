import os
# run `pip install alive-progress` in the terminal if having issues.
from alive_progress import *

def compile(f:str):
    # Keep track of data types
    data_tracker = {}
    
    # Finally fixed and implemented nested function. Outputs an ugly mess of brackets, but it works...
    def return_bracket_indices(text:str) -> list[list[int]]:
        stack = []
        result = []
        for index, char in enumerate(text):
            if char == '(':
                stack.append(index)
            elif char == ')':
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
                
        if proposed_line.startswith("say"):
            proposed_line = f"print({replace_quotation(proposed_line[4:].strip())})"
        elif proposed_line.startswith("ask"):
            proposed_line = f"input({replace_quotation(proposed_line[4:].strip()).removeprefix(b_back)})"
        elif proposed_line.startswith("//"):
            proposed_line = f"#{proposed_line.removeprefix('//')}"
        elif proposed_line.startswith("create"):
            # Bunch of stuff it could be: list, variable, file
            if split_version[2] == "variable":
                proposed_line = f"ez_usrdata_{split_version[-1].lower()} = \"\""
                data_tracker[split_version[-1]] = "variable"
            elif split_version[2] == "list":
                proposed_line = f"ez_usrdata_{split_version[-1].lower()} = []"
                data_tracker[split_version[-1]] = "list"
            else:
                proposed_line = f"open({split_version[-1].lower()}, \"w\").close()"
                data_tracker[split_version[-1]] = "file"
        elif proposed_line.startswith("add"):
            # Add to end of string? or add list items? Or even file. Because of the way we handle variables we need a `try`.
            try:
                if data_tracker[return_original_var(split_version[-1])] == "list":
                    proposed_line = f"{split_version[-1]}.extend([{proposed_line[proposed_line.find(b_quot):proposed_line.rfind(b_quot) + 1]}])"
                else:
                    proposed_line = f"{split_version[-1]} = {split_version[-1].lower()} + {proposed_line[proposed_line.find(b_quot):proposed_line.rfind(b_quot) + 1]}')"
            except KeyError:
                proposed_line = f"open({split_version[-1]}, \"a\").write({replace_quotation(proposed_line.removeprefix('add ').removesuffix(f' to {split_version[-1]}'))}).close()"
        elif proposed_line.startswith("insert"):
            proposed_line = f"{split_version[-4].lower()}.insert({proposed_line[proposed_line.find(b_quot):proposed_line.rfind(b_quot) + 1]},{int(split_version[-1]) - 1})"
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
        
        # Add indents and repeats back in:
        if repeats != 0:
            proposed_line = (' ' * ind) + (f"for ez_core_repeatfunc in range({repeats}):\n{' ' * ind}{' ' * indents}") + proposed_line
        else:
            proposed_line = (' ' * ind) + proposed_line
            
        
        return proposed_line
    
    os.mkdir(f"EZ_Compiled_{f.split('.')[0].capitalize()}")
    c = open(f,"r")
    code = c.readlines()
    indent_len = count_indents([item for item in code if count_indents(item) != 0][0])
    c.close()
    os.chdir(f"EZ_Compiled_{f.split('.')[0].capitalize()}")
    output = open(f"{f.split('.')[0].lower()}.py", "a")
    with alive_bar(len(code), unit=" lines") as bar:
        for line in code:
            output.write(convert_line(line,indent_len) + "\n")
            bar()

def count_indents(string:str) -> int:
    return len(string) - len(string.lstrip(' '))
            
compile("test.ez")
