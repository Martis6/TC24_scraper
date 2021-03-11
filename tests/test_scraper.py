from scraper.scraper import Scraper
import pytest
import pandas as pd


butai = Scraper(category="butai", city="vilniuje")
df = butai.scrape(25)

def test_get_total():
    assert isinstance(butai.get_total(), int)

def test_trim_spaces():
	assert butai.trim_spaces("    te  st   ") == "test"

def test_scrape_type():
	assert type(df) == pd.DataFrame

def test_scrape_length():
	assert len(df) == 25