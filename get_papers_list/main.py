import argparse
import csv
import sys
from typing import List, Dict

from .api import fetch_pubmed_data

def write_csv(filename: str, data: List[Dict]) -> None:
    if not data:
        print("No data to write.")
        return

    fieldnames = [
        "PubmedID",
        "Title",
        "Publication Date",
        "Non-academic Author(s)",
        "Company Affiliation(s)",
        "Corresponding Author Email"
    ]

    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def print_results(data: List[Dict]) -> None:
    if not data:
        print("No results found.")
        return

    for paper in data:
        print(f"PubmedID: {paper['PubmedID']}")
        print(f"Title: {paper['Title']}")
        print(f"Publication Date: {paper['Publication Date']}")
        print(f"Non-academic Author(s): {paper['Non-academic Author(s)']}")
        print(f"Company Affiliation(s): {paper['Company Affiliation(s)']}")
        print(f"Corresponding Author Email: {paper['Corresponding Author Email']}")
        print("-" * 80)

def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with pharma/biotech authors.")
    parser.add_argument("query", type=str, help="Search query (PubMed syntax supported)")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debug information")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename")

    args = parser.parse_args()

    if args.debug:
        print(f"[DEBUG] Running query: {args.query}")

    try:
        results = fetch_pubmed_data(args.query, debug=args.debug)
    except Exception as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)

    if args.debug:
        print(f"[DEBUG] Fetched {len(results)} papers")

    if args.file:
        write_csv(args.file, results)
        if args.debug:
            print(f"[DEBUG] Results written to {args.file}")
    else:
        print_results(results)

if __name__ == "__main__":
    main()
