import string
import sys


STOP_WORDS = {
    "the", "and", "to", "of", "a", "in", "it", "is", "was", "that",
    "i", "her", "she", "he", "you", "for", "not", "on", "with", "as",
    "at", "be", "this", "had", "but", "his", "they", "all", "so",
    "said", "no", "are", "if", "do", "or", "my", "one", "up", "an",
    "by", "we", "what", "me", "them", "very", "been", "would", "have",
    "its", "which", "were", "there", "their", "will", "when", "who",
    "out", "did", "your", "has", "him", "then", "could", "about",
    "into", "more", "some", "than", "can", "only", "just", "now",
    "how", "like", "from", "other", "any", "our", "own", "too",
    "dont", "im", "didnt", "youre", "thats", "wont", "cant", "shes",
    "hes", "ive", "youve", "doesnt", "wasnt", "couldnt", "wouldnt",
    "well", "oh", "upon", "much", "get", "got", "let", "go", "came",
    "come", "put", "say", "back", "way", "over", "make", "after",
}


def load_text(filepath):
    """Read a text file and return its contents as a string."""
    with open(filepath, "r") as f:
        return f.read()


def strip_gutenberg(text):
    """Remove Project Gutenberg header and footer."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"

    start = text.find(start_marker)
    if start != -1:
        start = text.index("\n", start) + 1
    else:
        start = 0

    end = text.find(end_marker)
    if end == -1:
        end = len(text)

    return text[start:end]


def clean_words(text):
    """Lowercase, strip punctuation, and split into a list of words."""
    text = text.lower()
    # Normalize curly quotes to straight ones, dashes to spaces
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", " ").replace("\u201d", " ")
    text = text.replace("\u2014", " ").replace("\u2013", " ")
    # Remove apostrophes (merges contractions: don't -> dont)
    text = text.replace("'", "")
    text = text.translate(str.maketrans("", "", string.punctuation))
    words = text.split()
    return words


def count_words(words):
    """Count how many times each word appears. Returns a dictionary."""
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


def top_words(counts, n=20):
    """Return the top n words by frequency as a list of (word, count) tuples."""
    sorted_words = sorted(counts.items(), key=lambda pair: pair[1], reverse=True)
    return sorted_words[:n]


def remove_stop_words(counts):
    """Return a new dictionary with stop words removed."""
    return {word: count for word, count in counts.items() if word not in STOP_WORDS}


def basic_stats(words):
    """Print basic stats about the text."""
    total = len(words)
    unique = len(set(words))
    avg_length = sum(len(w) for w in words) / total

    print(f"  Total words:    {total}")
    print(f"  Unique words:   {unique}")
    print(f"  Avg word length: {avg_length:.1f} characters")
    print(f"  Vocabulary richness: {unique / total:.2%}")


def longest_frequent_words(counts, min_count=5, n=10):
    """Find the longest words that appear at least min_count times."""
    frequent = {w: c for w, c in counts.items() if c >= min_count}
    by_length = sorted(frequent.items(), key=lambda pair: len(pair[0]), reverse=True)
    return by_length[:n]


def print_table(pairs, label_header="Word", count_header="Count"):
    """Print a list of (label, count) pairs as a formatted table."""
    if not pairs:
        print("  (no results)")
        return

    max_label = max(len(label_header), max(len(w) for w, _ in pairs))
    max_count = max(len(count_header), max(len(str(c)) for _, c in pairs))

    print(f"  {label_header:<{max_label}}  {count_header:>{max_count}}")
    print(f"  {'-' * max_label}  {'-' * max_count}")
    for word, count in pairs:
        print(f"  {word:<{max_label}}  {count:>{max_count}}")


def main():
    if len(sys.argv) < 2:
        filepath = "texts/alice.txt"
    else:
        filepath = sys.argv[1]

    print(f"\n--- Word Frequency Analyzer ---")
    print(f"\nLoading: {filepath}")

    text = load_text(filepath)
    text = strip_gutenberg(text)
    words = clean_words(text)

    print("\nBasic Stats:")
    basic_stats(words)

    all_counts = count_words(words)
    filtered_counts = remove_stop_words(all_counts)

    print("\nTop 20 Words (with stop words):")
    print_table(top_words(all_counts, 20))

    print("\nTop 20 Words (without stop words):")
    print_table(top_words(filtered_counts, 20))

    print("\nLongest words that appear 5+ times:")
    print_table(longest_frequent_words(filtered_counts))

    print()


if __name__ == "__main__":
    main()
