import xml.etree.ElementTree as ET
import pytest

# Example minimal XML snippet from PubMed
SAMPLE_XML = """
<PubmedArticleSet>
    <PubmedArticle>
        <MedlineCitation>
            <PMID>123456</PMID>
            <Article>
                <ArticleTitle>Sample Paper Title</ArticleTitle>
                <Journal>
                    <JournalIssue>
                        <PubDate>
                            <Year>2023</Year>
                            <Month>04</Month>
                            <Day>15</Day>
                        </PubDate>
                    </JournalIssue>
                </Journal>
                <AuthorList>
                    <Author>
                        <LastName>Smith</LastName>
                        <ForeName>John</ForeName>
                        <AffiliationInfo>
                            <Affiliation>BioPharma Inc</Affiliation>
                        </AffiliationInfo>
                    </Author>
                </AuthorList>
            </Article>
        </MedlineCitation>
    </PubmedArticle>
</PubmedArticleSet>
"""

def test_parse_pubmed_xml():
    root = ET.fromstring(SAMPLE_XML)
    article = root.find(".//PubmedArticle")
    pmid = article.find("MedlineCitation/PMID").text
    title = article.find("MedlineCitation/Article/ArticleTitle").text
    pub_year = article.find("MedlineCitation/Article/Journal/JournalIssue/PubDate/Year").text

    assert pmid == "123456"
    assert title == "Sample Paper Title"
    assert pub_year == "2023"
