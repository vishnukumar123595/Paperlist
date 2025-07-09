import re
from typing import Optional

PHARMA_KEYWORDS = [
    "pharma", "pharmaceutical", "biotech", "biotechnology",
    "inc", "ltd", "gmbh", "ag", "corp", "corporation", "llc",
]

NON_ACADEMIC_INDICATORS = [
    "university", "college", "institute", "hospital", "lab", "laboratory", "school"
]

EMAIL_REGEX_STANDARD = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", re.IGNORECASE)
EMAIL_REGEX_OBFUSCATED = re.compile(r"([a-zA-Z0-9_.+-]+)\s*\[at\]\s*([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", re.IGNORECASE)

def is_pharma_company(affiliation: str) -> bool:
    aff = affiliation.lower()
    return any(keyword in aff for keyword in PHARMA_KEYWORDS)

def is_academic_affiliation(affiliation: str) -> bool:
    aff = affiliation.lower()
    return any(keyword in aff for keyword in NON_ACADEMIC_INDICATORS)


def extract_email(affiliation_text: str) -> Optional[str]:
    """Extracts both standard and obfuscated emails from affiliation strings."""
    match = EMAIL_REGEX_STANDARD.search(affiliation_text)
    if match:
        return match.group().strip()

    # Try obfuscated format like "name [at] domain.com"
    match = EMAIL_REGEX_OBFUSCATED.search(affiliation_text)
    if match:
        local_part, domain = match.groups()
        return f"{local_part}@{domain}".replace(" ", "")

    return None
