#!/usr/bin/env python3

import sys
import datetime
import os

def main():
    if len(sys.argv) != 2:
        print("Usage: script.py <name>")
        sys.exit(1)

    name = sys.argv[1]
    print(f"Hello {name}")

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(os.environ.get('GITHUB_OUTPUT', ''), 'a') as output_file:
        output_file.write(f"time={current_time}\n")

if __name__ == "__main__":
    main()
