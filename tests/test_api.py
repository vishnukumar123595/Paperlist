import pytest
import requests
from unittest.mock import patch, MagicMock
from get_papers_list.api import fetch_pubmed_data

# Mock JSON response for search
MOCK_SEARCH_RESPONSE = {
    "esearchresult": {
        "idlist": ["123456"]
    }
}

# Mock XML response for fetch
MOCK_FETCH_RESPONSE = """
<PubmedArticleSet>
    <PubmedArticle>
        <MedlineCitation>
            <PMID>123456</PMID>
            <Article>
                <ArticleTitle>Test Paper</ArticleTitle>
                <Journal>
                    <JournalIssue>
                        <PubDate>
                            <Year>2024</Year>
                        </PubDate>
                    </JournalIssue>
                </Journal>
                <AuthorList>
                    <Author>
                        <LastName>Doe</LastName>
                        <ForeName>Jane</ForeName>
                        <AffiliationInfo>
                            <Affiliation>PharmaCorp LLC</Affiliation>
                        </AffiliationInfo>
                    </Author>
                </AuthorList>
            </Article>
        </MedlineCitation>
    </PubmedArticle>
</PubmedArticleSet>
"""

@patch("get_papers_list.api.requests.get")
def test_fetch_pubmed_data(mock_get):
    # Mock the two requests calls: search and fetch
    mock_search = MagicMock()
    mock_search.json.return_value = MOCK_SEARCH_RESPONSE
    mock_search.raise_for_status = lambda: None
    
    mock_fetch = MagicMock()
    mock_fetch.text = MOCK_FETCH_RESPONSE
    mock_fetch.raise_for_status = lambda: None

    # Setup side effects for consecutive calls
    mock_get.side_effect = [mock_search, mock_fetch]

    results = fetch_pubmed_data("test query", debug=True)
    
    assert len(results) == 1
    paper = results[0]
    assert paper["PubmedID"] == "123456"
    assert paper["Title"] == "Test Paper"
    assert paper["Publication Date"] == "2024"
    assert "Jane Doe" in paper["Non-academic Author(s)"] or paper["Non-academic Author(s)"] == ""
    assert "PharmaCorp LLC" in paper["Company Affiliation(s)"]
def test_pubmed_search_network_error():
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError("Network down")

        with pytest.raises(RuntimeError, match="Failed to search PubMed:"):
            fetch_pubmed_data("cancer vaccine", debug=True)