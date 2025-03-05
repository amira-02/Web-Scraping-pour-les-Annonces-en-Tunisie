# tests/test_scraper.py
from scraping.scraper import scrape_annonces

def test_scraping():
    annonces = scrape_annonces()
    assert len(annonces) > 0
    assert "titre" in annonces[0]
    assert "prix" in annonces[0]
