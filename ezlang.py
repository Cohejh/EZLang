# Lets begin by opening a demo file:
import os
code = open("test.ez", "r").readlines()
prev_dir = os.getcwd()
os.mkdir("test")
os.chdir("test")
def count_indents(s):
    return len(s) - len(s.lstrip())
output = open("test.py", "a")
for line in code:
	# We need to check if they are indenting correctly...
	if (int(count_indents(line)) % 4) != 0:
		os.chdir(prev_dir)
		os.rmdir("test")
		print("[Compiler Error]: Incorrect indentation! Use tabs or four spaces to indent.")

	
	# Get the command in a nice format
	split_cmd = line.lstrip().split()
	# We need to add handlers for every function

	# Handler for say
	if split_cmd[0] == "say":
		
