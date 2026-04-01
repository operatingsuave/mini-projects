Date: 2026-03-31

What I asked AI to do:
- Help me come up with a simple first Python mini project that felt personal
- Help me turn that idea into a working command-line app called Thoughts
- Help me structure the app with a menu, functions, input validation, and file saving
- Help me understand what each function in the code does

What I didn't understand in the generated code:
- How `os.path.join()` builds file paths
- How `re.sub()` cleans the title to make a safe filename
- Why `while True` is used for the menu loop
- How `with open(..., "w")` writes to a file and closes it automatically
- How `try` and `except KeyboardInterrupt` help the program exit cleanly

What I learned:
- Functions help break a program into smaller, organized parts
- `input()` is used to get user input, and `if` statements can validate it
- `while True` keeps the app running until the user chooses to quit
- `os.listdir()` can read files from a folder, and `open()` can write or read files
- `re.sub()` can remove unwanted characters from a string, which made it possible to turn a title into a filename
- I also learned that Python can be used to build something simple but real that saves files locally

If I kept working on this project, I would add:

- protection against duplicate filenames
- a search feature
- the ability to edit or delete a thought
- better formatting capabilities for the thought files