import os
line = "say (say (say \"Hello\"))"


def compile(f:str):
    os.mkdir(f.split(".")[0].capitalize())
    c = open(f,"r")
    code = c.readlines()
    
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

    def convert_line(s:str) -> str:
        proposed_line = s
        if return_bracket_indices(s) != None:
            for bracket in return_bracket_indices(s):
                inner_expression = convert_line(proposed_line[bracket[0] + 1:bracket[1]])
                proposed_line = f"{proposed_line[:bracket[0] + 1]}{inner_expression}{proposed_line[bracket[1]:]}"
                
        if proposed_line.startswith("say"):
            proposed_line = f"print({proposed_line[4:].strip()})"
            
        return proposed_line
            
print(convert_line(line))
