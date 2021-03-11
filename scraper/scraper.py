import requests
from bs4 import BeautifulSoup
from numpy import random, nan
import pandas as pd
import re
import time

class Scraper:
  """
  Basic scraper for aruodas.lt listings. Currently scrapping part works 
  only with flats, however other parts work with any types (ie houses).
  You can specify the city or scrape information from the whole country.

  Note: 
      highly suggest to run get_total first to know maximum possible entries
      for given keywords.
  """
  def __init__(
      self, 
      category: str,
      city: str = None, 
      headers: dict = {"User-Agent": "Mozilla/5.0"},
  ):
    """
    Initialization function.
    
    Args:
        category (str): category to scrape ("butai", "sklypai", "namai").
        city (str, optional): to specify the city if needed (examples "vilniuje", "kaune").
        headers (dict): requests.get function headers.
    """
    self.headers = headers
    self.key = category
    self.city = city
    if self.city == None:
      self.URL = f"https://m.en.aruodas.lt/{self.key}/"
    elif self.city is not None:
      self.URL = f"https://m.en.aruodas.lt/{self.key}/{self.city}/"
    self.list = []
  
  def basic_request(self, URL: str) -> BeautifulSoup:
    """
    Function to get soup object.
    
    Args:
        URL (str): URL target for GET request.
    Returns:
        BeautifulSoup object.
    """
    page = requests.get(URL, headers=self.headers)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

  def get_total(self) -> int:
    """
    Function to get total listings in specified category.
    
    Returns:
        int: total listings count
    """
    soup = self.basic_request(URL=self.URL)
    total = int(re.search("\d+", str(soup.find("span", class_="search-select-dropdown-link"))).group(0))
    return total

  def trim_spaces(self, target: str) -> str:
    """
    Function to clean strings from excessive spaces.
    
    Args:
        target (str): raw string from webpage.
    Returns:
        str: clean string
    """
    return re.sub("\s{2,}", "", re.sub("\n", "", target))
    
  def scrape(self, entries: int) -> pd.DataFrame:
    """
    Main function for scraping the website.
    
    Args:
        entries (int): number of objects to scrape.
    Returns:
        pd.DataFrame: final dataframe with main info.
    """
    max_count = self.get_total()
    if entries > max_count:
      print(f"Your input ({entries}) exceeds maximum existing listings count ({max_count})")
      entries = max_count
    else:
      pages_nr = int(round((entries+12)/25,0))
      for pg in range(1, pages_nr + 1):
        time.sleep(random.randint(0,3))
        URL = self.URL + f"puslapis/{pg}/"
        soup = self.basic_request(URL=URL)

        for i in soup.find_all("span", class_="result-item-info-v3"):
          price = self.trim_spaces(i.find("span", class_="item-price-main-v3").text)
          info = self.trim_spaces(i.find("span", class_="item-description-v3").text).split(", ")
          loc = self.trim_spaces(i.find("span", class_="item-address-v3").text).split(", ")
          if self.city == None:
            neighborhood = loc[1]
          elif self.city is not None:
            neighborhood = loc[0]
          
          all_materials = ["brick", "monolithic", "block house", "wooden house"]
          all_conditions = ["partial decoration", "fully equipped", "not equipped"]
          all_heat = ["central thermostat", "central", "gas", "electric", 
                      "geothermal", "aerothermal", "solid fuel", "sunbatteries"]
          if len(info) == 7:
            material = info[4]
            heating = info[5]
            condition = info[6]
          elif len(info) == 6:
            material, heating, condition = nan, nan, nan 
            if bool(set([info[4], info[5]]) & set(all_materials)):
              material = list(set([info[4], info[5]]) & set(all_materials))[0]
            elif bool(set([info[4], info[5]]) & set(all_heat)):
              heating = list(set([info[4], info[5]]) & set(all_heat))[0]
            elif bool(set([info[4], info[5]]) & set(all_conditions)):
              condition = list(set([info[4], info[5]]) & set(all_conditions))[0]
          
          self.list.append({
              "neighborhood": neighborhood,
              "price": int(re.findall("\d+", str(re.sub("\s{1,}", "", price)))[0]),
              "price_per_m2": int(re.findall("\d+", str(re.sub("\s{1,}", "", price)))[1]),
              "rooms": int(re.findall("\d+", info[0])[0]),
              "area_m2": int(re.findall("\d+", info[1])[0]),
              "floor": int(re.findall("\d+", info[2])[0]),
              "max_floors": int(re.findall("\d+", info[2])[0]),
              "year": int(re.findall("\d+", info[3])[0]),
              "build_material": material,
              "heating_type": heating,
              "condition": condition
          })
    return pd.DataFrame(self.list)