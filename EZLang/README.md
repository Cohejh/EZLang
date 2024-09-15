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
This function takes in some text as input, and prints it to `stdout`. It may accept the result of a function as its input.
### Example Usage:
```
say "Hello World!
```
```
Hello World!
```
## `ask` Function - Added in v1.0.0
This function takes in user keyboard input, until the enter key is pressed. **It does not save the output**.
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
## Example Usage:
```
create a new variable called AGE
```
