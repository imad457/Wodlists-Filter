#!/usr/bin/env python3
"""
filter_wordlist_interactive.py

Simple interactive wordlist filter:
- prompts for input file path
- prompts for output file path (default: results.txt)
- prompts for minimum length (default: 8)
- prompts whether to deduplicate (may use more memory)

Usage:
    python3 the filter
"""

import os
import sys

def prompt_input(prompt, default=None):
    try:
        if default:
            resp = input(f"{prompt} [{default}]: ").strip()
            return resp if resp != "" else default
        else:
            return input(f"{prompt}: ").strip()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
        sys.exit(1)

def confirm_yes_no(prompt, default="no"):
    default = default.lower()
    while True:
        resp = prompt_input(prompt, default).lower()
        if resp in ("y","yes"):
            return True
        if resp in ("n","no"):
            return False
        print("Please answer yes or no (y/n).")

def filter_wordlist(input_path, output_path, min_len=8, dedupe=False):
    if not os.path.isfile(input_path):
        print(f"[ERROR] Input file not found: {input_path}")
        return False

    total = 0
    kept = 0
    unique_count = None
    seen = set() if dedupe else None

    try:
        with open(input_path, "r", encoding="utf-8", errors="ignore") as fin, \
             open(output_path, "w", encoding="utf-8") as fout:
            for line in fin:
                total += 1
                pw = line.strip()
                if not pw:
                    continue
                if len(pw) < min_len:
                    continue
                if dedupe:
                    if pw in seen:
                        continue
                    seen.add(pw)
                fout.write(pw + "\n")
                kept += 1
                # Print a light progress update every 100k lines
                if total % 100000 == 0:
                    print(f"[...] processed {total:,} lines, kept {kept:,}")

    except Exception as e:
        print(f"[ERROR] Exception while processing: {e}")
        return False

    if dedupe:
        unique_count = len(seen)

    print("\n=== Summary ===")
    print(f"Input file: {input_path}")
    print(f"Output file: {output_path}")
    print(f"Total lines read: {total:,}")
    print(f"Kept (len >= {min_len}): {kept:,}")
    if dedupe:
        print(f"Unique entries (after dedupe): {unique_count:,}")
    print("Done.")
    return True

def main():
    print("=== Wordlist Filter (interactive) ===")
    input_path = prompt_input("Path to input wordlist (e.g. /usr/share/wordlists/your Wordlist)")
    if input_path == "":
        print("[ERROR] No input path provided.")
        return

    default_out = "results_of_wordlist.txt"
    output_path = prompt_input("Output file (where results will be saved)", default_out)

    # Minimum length
    while True:
        min_len_str = prompt_input("Minimum password length to keep (integer)", "8")
        try:
            min_len = int(min_len_str)
            if min_len <= 0:
                print("Please enter a positive integer.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer (e.g. 8).")

    # Deduplicate?
    dedupe = confirm_yes_no("Remove duplicate lines? (may use more memory) (y/n)", "no")

    print("\nSettings:")
    print(f" - Input: {input_path}")
    print(f" - Output: {output_path}")
    print(f" - Minimum length: {min_len}")
    print(f" - Deduplicate: {'yes' if dedupe else 'no'}")
    print("\nStart processing... (press Ctrl+C to stop)\n")

    success = filter_wordlist(input_path, output_path, min_len=min_len, dedupe=dedupe)
    if not success:
        print("[ERROR] Filtering failed.")
        sys.exit(2)

if __name__ == "__main__":
    main()
