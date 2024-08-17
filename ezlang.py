import os
line = "say (say (say \"Hello\"))"


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
    
    def count_indents(string:str) -> int:
        return len(string) - len(string.lstrip(' '))
    
    def convert_line(s:str,indents:int=None) -> str:
        proposed_line = s.strip()
        # Backslashes prohibited in fstrings, so here's a workaround:
        b_quot = "\""
        repeats = 0
        
        # Little script to remove (Nx) repeat function. Must run before Nested function handler.
        if proposed_line.endswith("x)"):
            end_i = proposed_line.rfind("(")
            repeats = int(proposed_line[end_i:].removeprefix("(").removesuffix("x)"))
            proposed_line = proposed_line[:end_i]
            proposed_line = proposed_line.strip()
            
        split_version = proposed_line.split()
        
        if return_bracket_indices(s) != None:
            for bracket in return_bracket_indices(s):
                inner_expression = convert_line(proposed_line[bracket[0] + 1:bracket[1]])
                proposed_line = f"{proposed_line[:bracket[0] + 1]}{inner_expression}{proposed_line[bracket[1]:]}"
                
        if proposed_line.startswith("say"):
            proposed_line = f"print({proposed_line[4:].strip()})"
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
                proposed_line = f"open({split_version[-1].lower()}, w)"
                data_tracker[split_version[-1]] = "file"
        elif proposed_line.startswith("add"):
            # Add to end of string? or add list items?
            if data_tracker[split_version[-1]] == "list":
                proposed_line = f"ez_usrdata_{split_version[-1].lower()}.extend([{proposed_line[proposed_line.find(b_quot):proposed_line.rfind(b_quot) + 1]}])"
            else:
                proposed_line = f"ez_usrdata_{split_version[-1].lower()} = ez_usrdata_{split_version[-1].lower()} + {proposed_line[proposed_line.find(b_quot):proposed_line.rfind(b_quot) + 1]}')"
        elif proposed_line.startswith("insert"):
            if data_tracker[split_version[-4]] == "list":
                proposed_line = f"ez_usrdata_{split_version[-4].lower()}.insert({proposed_line[proposed_line.find(b_quot):proposed_line.rfind(b_quot) + 1]},{int(split_version[-1]) - 1})"
            else:
                proposed_line = f"ez_usrdata_{split_version[-4].lower()}.insert()"
        return proposed_line
    
    os.mkdir(f.split(".")[0].capitalize())
    c = open(f,"r")
    code = c.readlines()
    indent_len = count_indents([item for item in code if count_indents(item) != 0][0])
    c.close()
    os.chdir(f.split(".")[0].capitalize())
    output = open(f"{f.split('.')[0].lower()}.py", "a")
    for line in code:
        output.write(convert_line(line,indent_len) + "\n")

def count_indents(string:str) -> int:
    return len(string) - len(string.lstrip(' '))
            
compile("test.ez")
