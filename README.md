# Paperlist

## Overview
A command-line tool to fetch PubMed research papers matching a user query, filtering for papers with at least one author affiliated with pharmaceutical or biotech companies. Outputs results as CSV or to console.

## Features
- Supports full PubMed query syntax.
- Filters authors by affiliation heuristics.
- Outputs: PubmedID, Title, Publication Date, Non-academic Authors, Company Affiliations, Corresponding Author Email.
- CLI options: `--debug`, `--file` for output filename, and `--help`.
- Modular design with a reusable Python module.
- Typed Python with error handling and tests.

## Installation
Requires Python 3.10+. Uses [Poetry](https://python-poetry.org/) for dependency management.

```bash
git clone https://github.com/vishnukumar123595/Paperlist.git
cd Paperlist
poetry install
poetry run get-papers-list "cancer vaccine" --debug --file results.csv


# Few search keywords
# "tumor vaccine"

# "cancer immunotherapy"

# "neoantigen vaccine"

# "personalized cancer vaccine"

# "therapeutic cancer vaccine"

# "oncology vaccine development"