import pytest
from get_papers_list.utils import is_pharma_company, is_academic_affiliation, extract_email

def test_is_pharma_company():
    assert is_pharma_company("Acme Pharma Inc")
    assert is_pharma_company("BioTech LLC")
    assert not is_pharma_company("University Hospital")
    assert not is_pharma_company("Some Random Org")

def test_is_academic_affiliation():
    assert is_academic_affiliation("Department of Biology, University of Somewhere")
    assert is_academic_affiliation("National Laboratory")
    assert not is_academic_affiliation("BioTech Corp")
    assert not is_academic_affiliation("Pharmaceutical Inc")

def test_extract_email():
    text_with_email = "Contact: john.doe@biotech.com for details."
    text_without_email = "No email here!"
    assert extract_email(text_with_email) == "john.doe@biotech.com"
    assert extract_email(text_without_email) is None
