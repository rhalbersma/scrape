# Exercises in web scraping

[![Language](https://img.shields.io/badge/language-Python-blue.svg)](https://www.python.org/)
[![Standard](https://img.shields.io/badge/Python-3.8-blue.svg)](https://en.wikipedia.org/wiki/History_of_Python)
[![License](https://img.shields.io/badge/license-Boost-blue.svg)](https://opensource.org/licenses/BSL-1.0)
[![Lines of Code](https://tokei.rs/b1/github/rhalbersma/scrape?category=code)](https://github.com/rhalbersma/scrape)

## Overview

The `scrape` package defines four modules for scraping the following websites: 

| Module          | Topic | References |
| :-------------- | :---- | :--------- |
| `cardmarket`    | the [cardmarket.com](https://www.cardmarket.com/en/Magic/Products/Search) market place for Magic: The Gathering | |
| `mga`           | the [Malta Gaming Authority](https://www.mga.org.mt/mgalicenseeregister/) licensee register | |
| `nct`           | the [National Clinical Trials](https://clinicaltrials.gov/ct2/resources/download#DownloadAllData) database | Marcel Wieting's [Code Review post](https://codereview.stackexchange.com/questions/239521/performance-read-large-amount-of-xmls-and-load-into-single-csv) |
| `transfermarkt` | the [transfermarkt.com](https://www.transfermarkt.com/wettbewerbe/europa) football database | Marcel Wieting's [LinkedIn post](https://www.linkedin.com/pulse/web-scraping-relative-age-effect-professional-football-marcel-wieting/?trackingId=d8UqaacWy%2FaNdTYFhh4MsQ%3D%3D) |

## Installation

```bash
git clone https://github.com/rhalbersma/scrape.git
cd scrape
python3 -m venv .env
source .env/bin/activate
pip install --upgrade pip setuptools wheel
pip install -e .
```

## Notes

For each module, the `examples` directory contains a script that can be run in order to download the relevant data and, in some cases, to do some exploratory data analysis. The 'weapons of choice' for the actual web scraping are the Python packages [requests](https://requests.readthedocs.io/en/master/) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). The actual data is being handled through [Pandas](https://pandas.pydata.org/). For visualisation, we employ [plotnine](https://plotnine.readthedocs.io/en/stable/) (a Python implementation of the Grammar of Graphics).

Please note that some scripts can take a long time (upwards of an hour) to run and store several gigabytes on disk. Such long-running computations are being monitored through a [tqdm](https://github.com/tqdm/tqdm) progress bar.

Please note that the `scrape` package tries to be a good netizen by using a thin wrapper `etiget()` around `requests.get()` that by default uses a crawl delay of two seconds in between every request. Please don't override this without reading a corresponding website's `robots.txt`.

## Acknowledgements

Special thanks to Marcel Wieting and Wessel Oomens for exchange of ideas.

## License

Copyright Rein Halbersma 2020.  
Distributed under the [Boost Software License, Version 1.0](http://www.boost.org/users/license.html).  
(See accompanying file LICENSE_1_0.txt or copy at [http://www.boost.org/LICENSE_1_0.txt](http://www.boost.org/LICENSE_1_0.txt))
