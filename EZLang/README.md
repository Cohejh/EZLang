# EZLang Spec
Here you will find listed every EZLang feature/function that you will have to implement, if you wish to make your own compiler or interpreter for EZLang. Or, alternately, you can use it to learn how to program in EZLang.
## `(Nx)` Decorator - Added in v1.0.0
This function decorator goes at the end of a line, and makes a function repeat multiple times. The `N` parameter is a number decides how many times to repeat. 
### Example Usage:
```
say "Hello" (5x)
```
```
Hello
Hello
Hello
Hello
Hello
```
## `say` Function - Added in v1.0.0
This function takes in an input, and prints it to `stdout`. It has the following syntax:
```
say <INPUT>
```
### `<INPUT>` Parameter:
This can be almost any object, such as a string, a variable or a list. If `"` or `'` are in the string, they must be preceded with a backslash, like so: `\"`, `\'`
### Example Usage:
```
say "Hello World!
```
```
Hello World!
```
## `ask` Function - Added in v1.0.0
This function takes in user keyboard input after asking a prompt, until the enter key is pressed. **It does not save the output**. It has the following syntax:
```
ask <PROMPT>
```
### `<PROMPT>` Parameter:
The prompt can be any string, list or variable, as long as any quotation marks have a `\` preceding them, like so: `\"`
### Example Usage:
```
ask "What is your name?"
```
```
What is your name? <USER INPUT GOES HERE>
```
## Comments - Added in v1.0.0
This has no functional uses, but improves code readability. Comments are preceded by `//`. Best practice is to have a space between the `//` and the comment.
### Example Usage:
```
// This is a comment
```
## `create` Function - Added in v1.0.0
This function is used to create objects of multiple types, all of which use the same basic syntax:
```
create a <OBJECT> called <NAME>
```
**It does not output anything to `stdout`**
### `<OBJECT>` Parameter:
The Object parameter may be any of the following:
- `variable` - Creates a new variable
- `list` - Creates a new list
- `file` - Creates a new file
- `folder` - Creates a new folder
### `<NAME>` Parameter:
The Name parameter may be anything, as long as it follows the following rules:
1. It must be in full capitals. `AGE` is valid, but `AGe` is not.
2. It may not contain any spaces, underscores or dashes must be used instead. `YOUR-NAME` or `YOUR_NAME` are valid, but `YOUR NAME` is not.
### Example Usage:
```
create a new variable called AGE
```
## `add` function
This function adds either:
- Elements to a list
- Text to the end of a string (can be either a variable or an actual string)
- A new line of text to a file

It has the following syntax:
```
add <CONTENT> to <OBJECT>
```
### `<CONTENT>` Parameter:
This parameter can be almost anything, save for a some rules:
- If you wish to use `"` or `'`, you must preceed it with a backslash: `\"` or `\'`
- When using lists, the elements must be organised like this: `"Element 1","Element 2","Element 3"`
### `<OBJECT>` Parameter:
This parameter can be any already created object, except for a folder.
### Example Usage:
```
add "." to SENTENCE
```
## `write` Function - Added in v1.0.0
This function takes in some text and a file, and appends it to the file. It has the following syntax:
```
write <CONTENT> to <FILE>
```
### `<CONTENT>` Parameter:
This parameter can be almost anything, except for if you wish to use `"` or `'`, you must preceed it with a backslash: `\"` or `\'`
### `<OBJECT>` Parameter:
This parameter can be any previously created file or a new file. It must be enclosed in quotation marks.
### Example Usage:
```
write "This is a new line" to "test.txt"
```
## `insert` Function:
This function inserts an element into a list at a particular index. Unlike most programming languages, the index starts from `1`, not `0`. It has the following syntax:
```
insert <OBJECT> into <LIST> in position <INDEX>
```
### `<OBJECT>` Parameter:
This can be either a string, a variable, or a list.
### `<LIST>` Parameter:
This is any already-created list. The name must be in uppercase.
### `<INDEX>` Parameter:
This is the index, in which to insert the object into. This starts at `1` not `0`.
### Example Usage:
```
insert "Strawberry" into FRUITS in position 2
```
## `remove` Function:


