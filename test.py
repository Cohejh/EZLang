line = "say (say (say \"Hello\"))"        

def is_true_bracket(s:int,e:int,string:str) -> bool:
    if (string[:s].count("\"") % 2 == 0) and (string[e:].count("\"") % 2 == 0):
        return True
    else:
        return False

def contains_true_brackets(s:str) -> bool:
    try:
        extract_brackets(s)
        return True
    except IndexError:
        return False
    
def extract_brackets(text:str,si=0) -> str:
    ps = si
    l = text
    while l[ps] != "(":
        ps += 1
    pe = ps + 1
    # Bracket buffer checks that we account for nested functions.
    b = 1
    while (b != 0):
        if l[pe] == "(":
            b += 1
        elif l[pe] == ")":
            b -= 1
        pe += 1
    if (is_true_bracket(ps,pe,text)):
        return (text[ps:pe],ps,pe)
    else:
        return extract_brackets(text,(pe + 1))
        
def convert_line(s:str) -> str:
    if contains_true_brackets(s):
        proposed_line = f"{line[:extract_brackets(s)[1]]}{convert_line(extract_brackets(s)[0])}{line[extract_brackets(s)[2]:]}"
    return proposed_line

print(convert_line(line))