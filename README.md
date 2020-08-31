# Educational Exercises in Web Scraping

[![Language](https://img.shields.io/badge/language-Python-blue.svg)](https://www.python.org/)
[![Standard](https://img.shields.io/badge/Python-3.8-blue.svg)](https://en.wikipedia.org/wiki/History_of_Python)
[![License](https://img.shields.io/badge/license-Boost-blue.svg)](https://opensource.org/licenses/BSL-1.0)
[![Lines of Code](https://tokei.rs/b1/github/rhalbersma/scrape?category=code)](https://github.com/rhalbersma/scrape)

## Overview

The `scrape` package consists of four modules of (hopefully!) educational programming exercises that I used to sharpen my Python web scraping skills.

| Module          | Topic | References |
| :-------------- | :---- | :--------- |
| `cardmarket`    | the [cardmarket.com](https://www.cardmarket.com/en/Magic/Products/Search) market place for Magic: The Gathering | |
| `mga`           | the [Malta Gaming Authority](https://www.mga.org.mt/mgalicenseeregister/) licensee register | |
| `nct`           | the [National Clinical Trials](https://clinicaltrials.gov/ct2/resources/download#DownloadAllData) database | Marcel Wieting's [Code Review post](https://codereview.stackexchange.com/questions/239521/performance-read-large-amount-of-xmls-and-load-into-single-csv) |
| `transfermarkt` | the [transfermarkt.com](https://www.transfermarkt.com/wettbewerbe/europa) football database | Marcel Wieting's [LinkedIn post](https://www.linkedin.com/pulse/web-scraping-relative-age-effect-professional-football-marcel-wieting/?trackingId=d8UqaacWy%2FaNdTYFhh4MsQ%3D%3D) |

## Installation

```bash
git clone https://github.com/rhalbersma/scrape
cd scrape
python3 -m venv .env
source .env/bin/activate
pip install --upgrade pip setuptools wheel
pip install -e .
```

## Notes

For each module, the `examples` directory contains a script that can be run in order to download the relevant data and, in some cases, to do some exploratory data analysis. The 'weapons of choice' for the actual web scraping are the Python packages [requests](https://requests.readthedocs.io/en/master/) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). The actual data is being handled through [Pandas](https://pandas.pydata.org/). For visualisation, we employ [plotnine](https://plotnine.readthedocs.io/en/stable/) (a Python implementation of the Grammar of Graphics), stored inside a [Jupyter](https://jupyter.org/) notebook.

Please note that some scripts can take a long time (upwards of an hour) to run and store several gigabytes on disk. Such long-running computations are being monitored through a [tqdm](https://github.com/tqdm/tqdm) progress bar.

Please note that the `scrape` package tries to be a good netizen by using a thin wrapper `etiget()` around `requests.get()` that by default uses a crawl delay of two seconds in between every request. Please don't override this without reading a corresponding website's `robots.txt`.

## Guide

The `nct` module is the easiest way to get started. This code involves downloading a single `.zip` file, unpacking the contents on disk and parsing a large number of XML files and combining them into a `DataFrame`. The challenge here is to do so efficiently, since the downloaded content consumes several gigabytes of disk space. A suboptimal approach will quickly exhaust the memory of even a high end machine.

The `cardmarket` module is a typical webscraping exercise where tabled data from several web pages are being downloaded and brought together into a single `DataFrame`. The tabled data is *just* not structured enough (is it ever?) to be consumed directly through `pandas.read_html()`, so each individual row has to be separately extracted.

The `transfermarkt` module goes a step beyond this by unraveling several levels of aggregation: from the continent, via the league, to finally the club level. This website also requires a handwritten parser for the tabled data. The resulting data is tidied up to be able make scatterplots (shown in a Jupyter notebook that is stored in the `examples` subdirectory).

The `mga` module contains the most complicated code. We use the `ast` Python module to parse a JavaScript array of web menu options directly into a Python list for further processing. This website has multiple levels of indirection that cross-link each other. Downloading the data is straightforward, but substantial domain knowledge is required to combine the downloaded data into a meaningful set of tidied `DataFrame`s.

## Status

This repository is **inactive**. There are currently no plans to resume activity. Nevertheless, bug reports (websites change over time!) are welcome.

## Acknowledgements

Special thanks to Marcel Wieting and Wessel Oomens for exchange of ideas.

## License

Copyright Rein Halbersma 2020.  
Distributed under the [Boost Software License, Version 1.0](http://www.boost.org/users/license.html).  
(See accompanying file LICENSE_1_0.txt or copy at [http://www.boost.org/LICENSE_1_0.txt](http://www.boost.org/LICENSE_1_0.txt))
