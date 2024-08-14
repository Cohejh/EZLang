lines = "say \"hello (red herring)\" (hello (nested function))"
line = "say \"()\" (say ss(ssss) )"

#out = convert_line(line)
#print(out)

#def convert_line(s:int):

def contains_brackets(s:str,o=0):
    ms = s
    if ("(" in s) and (")" in s):
        if is_true_bracket((ms.find("(") + o),(ms.find(")") + o),s):
            return True
        else:
            offset = (ms.find(")") + 1)
            ms = ms[offset:]
            print(contains_brackets(ms,offset))
            if contains_brackets(ms,offset):
                return True
    else:
        return False



def is_true_bracket(s:int,e:int,string:str) -> bool:
    if (string[:s].count("\"") % 2 == 0) and (string[e:].count("\"") % 2 == 0):
        return True
    else:
        return False

def extract_brackets(text:str,si=0):
    ps = si
    l = text
    while l[ps] != "(":
        ps += 1
    pe = ps + 1
    # Bracket buffer checks that we account for nested functions.
    b = 1
    i = 0
    while (b != 0):
        if l[pe] == "(":
            b += 1
            i = 1
        elif l[pe] == ")":
            b -= 1
        pe += 1
    print((ps,pe))
    if (is_true_bracket(ps,pe,text)):
        return text[ps:pe]
    
    
print(contains_brackets(line))