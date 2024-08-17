# EZLang

Demo script in `test.ez`

Our current task is to make it translate between EZLang and python, line by line.
Before we can do that though, we have implemented one command, `say`. 
What we need to do, is make it recursively work for nested brackets,
that is, it detects brackets in code, and first translates what's inside the brackets.
So, if we start with `say (say \"Hello\")`, the following steps happen

1. `say (print("Hello"))`
2. `print(print("Hello"))`
   
This can be scaled up for larger brackets
The way we will probably implement it is by extracting the bracketed text, and running them through the main convert_line command.
