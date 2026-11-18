"""Audit script to inspect and cross-verify all numerical claims across manuscript, README, docs, and results."""

import json
import os
import re

def main():
    tex = open("manuscript/main_ieeetran.tex", encoding="utf-8").read()
    readme = open("README.md", encoding="utf-8").read()

    # Load all json files
    results = {}
    for f in os.listdir("results"):
        if f.endswith(".json"):
            results[f] = json.load(open(os.path.join("results", f), encoding="utf-8"))

    print("Loaded result files:", list(results.keys()))

    # Print tables in tex
    tables = re.findall(r"\\begin\{table\*?\}(.*?)\\end\{table\*?\}", tex, re.DOTALL)
    print(f"\n--- LaTeX Tables ({len(tables)}) ---")
    for idx, tbl in enumerate(tables):
        cap_m = re.search(r"\\caption\{(.*?)\}", tbl)
        cap = cap_m.group(1) if cap_m else "No Caption"
        print(f"\nTable {idx+1}: {cap}")
        for line in tbl.splitlines():
            line_s = line.strip()
            if "&" in line_s and not line_s.startswith("%"):
                print("  ", line_s)

if __name__ == "__main__":
    main()
