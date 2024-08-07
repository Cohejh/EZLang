# Lets begin by opening a demo file:
import os
code = open("test.ez", "r").readlines()
prev_dir = os.getcwd()
os.mkdir("test")
os.chdir("test")

# Counts the number of indents, so that we can add them back in later...
def count_indents(s:str) -> int:
	return len(s) - len(s.lstrip())

# Returns a copy of the line, without the "(Nx)" at the end for repeats.
def fix_repeat(s:str) -> str:
	if s[-2:] == "x)":
		r = s[::-1]
		e = r.find("(")
		return s[:-(e + 1)]
	else:
		return s

output = open("test.py", "a")
for line in code:
	indents = count_indents(line) 
	proposed_line = ""
	
	# Get the command in a nice format
	fixed_cmd = line.lstrip()
	norepeat_cmd = fix_repeat(fixed_cmd)
	split_cmd = line.lstrip().split()
	# We need to add handlers for every function

	# Handler for say
	if split_cmd[0] == "say":
		if split_cmd[1][1] == "\"":
			proposed_line = (f"print({norepeat_cmd.removeprefix('say ').replace('\"','\\\"')})")
	

	output.write(f"{' ' * indents}{proposed_line}")
