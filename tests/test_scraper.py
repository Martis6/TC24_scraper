from scraper.scraper import Scraper
import pytest
import pandas as pd

def test_get_total():
	butai = Scraper(category="butai", city="vilniuje")
    assert isinstance(butai.get_total(), int)

def test_trim_spaces():
	butai = Scraper(category="butai", city="vilniuje")
	assert butai.trim_spaces("    te  st   ") == "test"

def test_scrape_type():
	butai = Scraper(category="butai", city="vilniuje")
    df = butai.scrape(25)
	assert type(df) == pd.DataFrame

def test_scrape_length():
	butai = Scraper(category="butai", city="vilniuje")
    df = butai.scrape(25)
	assert len(df) == 25