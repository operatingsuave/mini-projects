Date: 2026-04-09

What I asked AI to do:
- Help me build a word frequency analyzer for a Project Gutenberg book
- Help me figure out how to clean text properly (punctuation, curly quotes, contractions)
- Help me structure the code into clear functions
- Help me format the output into clean tables

What I didn't understand in the generated code:
- How `str.maketrans()` and `translate()` work together to remove punctuation
- How `sorted()` with a `key=lambda` sorts a dictionary by value
- What a list comprehension like `{w: c for w, c in counts.items() if ...}` does
- How f-strings with alignment like `f"{word:<{width}}"` work for formatting tables

What I learned:
- Dictionaries are great for counting things — `.get(key, 0)` lets you increment without checking if the key exists first
- Text cleaning is the hardest part of text analysis — curly quotes, contractions, and hyphens all need special handling
- Stop words (the, and, to, of) dominate any English text so you have to filter them out to see anything interesting
- `sorted()` can sort any iterable and the `key` parameter lets you control what it sorts by
- `string.punctuation` gives you all standard punctuation characters as a string
- Project Gutenberg files have headers and footers you need to strip before analyzing

If I kept working on this project, I would add:
- Compare two books side by side
- Detect the reading level of the text
