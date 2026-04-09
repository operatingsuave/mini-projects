# Word Frequency Analyzer

A Python program that analyzes the word frequency of a text file and finds patterns in the language.

## What It Does

The program loads a text file, cleans the text, counts every word, and shows:
- Basic stats (total words, unique words, average word length, vocabulary richness)
- The top 20 most common words, with and without stop words
- The longest words that appear frequently

## What I Analyzed

I used *Alice's Adventures in Wonderland* by Lewis Carroll, downloaded from Project Gutenberg.

## What I Found

- The book has about 26,600 words and 2,650 unique words, giving it a vocabulary richness of ~10%.
- "alice" appears 386 times — far more than any other meaningful word. The next closest is "little" at 129.
- The top words reveal the main characters: queen, king, mock turtle, hatter, gryphon, caterpillar.
- "little" and "down" are among the most common — Carroll uses "little" constantly to describe things, and "down" makes sense given the rabbit hole.
- The longest frequently-used word is "breadandbutter" (6 times) — turns out Gutenberg merges hyphenated words.

## What Surprised Me

- How much stop words dominate. "the" alone accounts for over 6% of the entire book.
- Once you remove stop words, the character names jump right to the top. The word frequencies basically tell you who the important characters are.
- "thought" appears 74 times — Alice does a lot of thinking.

## How to Run

From inside the `mini_project_2_text` folder:

```bash
python analyzer.py
```

To analyze a different text file:

```bash
python analyzer.py path/to/file.txt
```

## Two-Pass Reflection

The whole program uses only built-in Python — `string`, `sys`, dictionaries, and lists. No external libraries.

Doing it with plain dicts was straightforward. `counts.get(word, 0) + 1` is simple and clear. Sorting a dict by value with `sorted()` and a lambda was the trickiest part but still only one line.
