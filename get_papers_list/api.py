import requests
from typing import List, Dict, Optional
from xml.etree import ElementTree as ET

from .utils import is_pharma_company, is_academic_affiliation, extract_email
from .parser import parse_publication_date

def chunks(lst, n):
    """Yield successive n-sized chunks from list."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def fetch_pubmed_data(query: str, debug: bool = False) -> List[Dict]:
    if debug:
        print(f"[DEBUG] Starting PubMed fetch for query: {query}")

    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    
    try:
        params_search = {
            "db": "pubmed",
            "term": query,
            "retmax": "100",
            "retmode": "json",
        }
        r_search = requests.get(base_url + "esearch.fcgi", params=params_search, timeout=10)
        r_search.raise_for_status()
        data_search = r_search.json()
    except requests.RequestException as e:
        raise RuntimeError(f"[ERROR] Failed to search PubMed: {e}")
    except ValueError:
        raise RuntimeError("[ERROR] Invalid JSON response from PubMed search")

    pmid_list = data_search.get("esearchresult", {}).get("idlist", [])
    if debug:
        print(f"[DEBUG] Found {len(pmid_list)} papers")

    if not pmid_list:
        return []
    results = []
    seen_pmids = set()
    for batch in chunks(pmid_list, 50):  # Batch of 50 PMIDs
        try:
            params_fetch = {
                "db": "pubmed",
                "id": ",".join(batch),
                "retmode": "xml",
            }
            r_fetch = requests.get(base_url + "efetch.fcgi", params=params_fetch, timeout=10)
            r_fetch.raise_for_status()
            root = ET.fromstring(r_fetch.text)
        except requests.RequestException as e:
            raise RuntimeError(f"[ERROR] Failed to fetch PubMed details: {e}")
        except ET.ParseError:
            raise RuntimeError("[ERROR] Failed to parse XML response from PubMed")

   

    for article in root.findall(".//PubmedArticle"):
        medline = article.find("MedlineCitation")
        if medline is None:
            continue

        pmid = medline.findtext("PMID")
        if not pmid or pmid in seen_pmids:
            continue
        article_info = medline.find("Article")
        if article_info is None:
            continue

        title = article_info.findtext("ArticleTitle") or "[No Title Found]"
        pub_date_node = article_info.find("Journal/JournalIssue/PubDate")
        pub_date = parse_publication_date(pub_date_node)

        non_academic_authors = []
        company_affiliations = set()
        pharma_author_found = False
        corresponding_email = None

        author_list = article_info.find("AuthorList")
        if author_list is not None:
            for author in author_list.findall("Author"):
                last_name = author.findtext("LastName") or ""
                fore_name = author.findtext("ForeName") or ""
                full_name = f"{fore_name} {last_name}".strip()

                affiliation_info = author.find("AffiliationInfo")
                affiliation_text = ""
                if affiliation_info is not None:
                    affiliation_text = affiliation_info.findtext("Affiliation") or ""

                if affiliation_text and is_pharma_company(affiliation_text):
                    pharma_author_found = True
                    company_affiliations.add(affiliation_text.strip())

                if affiliation_text and not is_academic_affiliation(affiliation_text):
                    non_academic_authors.append(full_name)

                if not corresponding_email and affiliation_text:
                    email = extract_email(affiliation_text)
                    if email:
                        corresponding_email = email

        if not pharma_author_found:
            continue
        seen_pmids.add(pmid)
        results.append({
            "PubmedID": pmid,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": "; ".join(non_academic_authors) if non_academic_authors else "",
            "Company Affiliation(s)": "; ".join(company_affiliations) if company_affiliations else "",
            "Corresponding Author Email": corresponding_email or ""
        })

        if debug:
            print(f"[DEBUG] Added paper PMID {pmid} titled '{title}'")

    if debug:
        print(f"[DEBUG] Total papers after filtering: {len(results)}")

    return results
