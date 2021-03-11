## Aruodas.lt scraper

This basic scraper is for 2nd TC capstone project. It scrapes listings of flats from [aruodas.lt](https://www.aruodas.lt/). Its main objective is to return pandas DataFrame consisting of relevant information on flats.

DataFrame content:
- neighborhood
- price
- price_per_m2
- rooms
- area_m2
- floor
- max_floors
- year
- build_material
- heating_type
- condition

### Installation

```
pip install git+https://github.com/Martis6/TC24_scraper.git
```
### Usage

1. Import the class
```
from scraper.scraper import Scraper
```
2. Create an object and use the functions
```
butai = Scraper(category="butai", city="vilniuje")
butai.get_total()
```

### License

Scraper has a MIT-style license, as found in the [LICENSE](LICENSE) file.
