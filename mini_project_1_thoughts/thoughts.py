import os
import re
from datetime import datetime


def make_filename(title):
    """Turn a title into a safe filename."""
    slug = title.lower().strip()
    slug = slug.replace(" ", "-")
    slug = re.sub(r"[^a-z0-9\-]", "", slug)
    return f"{slug}.md"


def add_thought():
    """Ask the user for a thought and save it as a markdown file."""
    print()
    title = input("Title: ").strip()
    if not title:
        print("A thought needs a title.")
        return

    place = input("Place: ").strip()

    note = input("Note: ").strip()
    if not note:
        print("A thought needs a note.")
        return

    filename = make_filename(title)
    filepath = os.path.join("thoughts", filename)

    date = datetime.now().strftime("%B %d, %Y")

    content = f"Date: {date}\n\n"
    content += f"Title: {title}\n\n"
    if place:
        content += f"Place: {place}\n\n"
    content += f"Note: {note}\n"

    with open(filepath, "w") as f:
        f.write(content)

    print(f"\nSaved to {filepath}")


def view_thoughts():
    """List saved thoughts and let the user read one."""
    files = sorted(os.listdir("thoughts"))
    files = [f for f in files if f.endswith(".md")]

    if not files:
        print("\nNo thoughts saved yet.")
        return

    print()
    for i, filename in enumerate(files, start=1):
        print(f"  {i}. {filename}")

    print()
    choice = input("Pick a number to read (or press Enter to go back): ").strip()
    if not choice:
        return

    try:
        index = int(choice) - 1
        if index < 0 or index >= len(files):
            print("That number is not on the list.")
            return
    except ValueError:
        print("That's not a valid number.")
        return

    filepath = os.path.join("thoughts", files[index])
    with open(filepath, "r") as f:
        print()
        print(f.read())


def main():
    """Run the Thoughts app."""
    print("\n--- Thoughts ---")

    while True:
        print("\n1. Add a thought")
        print("2. View thoughts")
        print("3. Quit")
        print()

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_thought()
        elif choice == "2":
            view_thoughts()
        elif choice == "3":
            print("\nBye!\n")
            break
        else:
            print("Please pick 1, 2, or 3.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nBye!\n")
