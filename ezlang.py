line = "say (say (say \"Hello\"))"

def parallel_nested_brackets():
    pass

def convert_line(s:str) -> str:
    if s.startswith("say"):
        return f"print({s[4:]})"