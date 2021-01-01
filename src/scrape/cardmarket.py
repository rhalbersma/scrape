#          Copyright Rein Halbersma 2020-2021.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import re

import bs4
import lxml
import pandas as pd
from tqdm import tqdm
from typing import Optional, Tuple

from scrape.etiget import etiget

cardmarket_url='https://www.cardmarket.com/en/'

def parse_row(row: bs4.element.Tag) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str], Optional[int], Optional[str]]:
    try:
        Title = row.find('span', class_='expansionIcon')['data-original-title']
    except:
        Title = None
    try:
        Name = (row
            .find('div', class_='row no-gutters')
            .find('a')
            .text
        )
    except:
        Name = None
    try:
        Rarity = (row
            .find('div', class_=re.compile(r'.*col-rarity.*'))
            .find('span', class_='icon')
        )['data-original-title']
    except:
        Rarity = None
    try:
        Number = (row
            .find('div', class_='col-number d-none d-md-flex text-nowrap')
            .find_all('span')[-1]
            .text
        )
    except:
        Number = None
    try:
        Available = int(row
            .find('div', class_='col-availability px-2')
            .find('span')
            .text
        )
    except:
        Available = None
    try:
        From = (row
            .find('div', class_='col-price pr-sm-2')
            .text
        )
    except:
        From = None
    return Title, Name, Rarity, Number, Available, From

def parse_table(table: bs4.element.ResultSet) -> pd.DataFrame:
    return pd.DataFrame(
        data = [
            parse_row(row)
            for row in table.find_all('div', id=re.compile(r'^productRow\d+'))
        ],
        columns = [
            'Title', 'Name', 'Rarity', 'Number', 'Available', 'From'
        ]
    )

def fetch_page(page: str) -> pd.DataFrame:
    response = etiget(page)
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.content, 'lxml')
    table = soup.select('body > main > section > div.table.table-striped > div.table-body')[0]
    return parse_table(table)

def fetch_query(query: str) -> pd.DataFrame:
    response = etiget(query)
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.content, 'lxml')
    try:
        hits = int(soup
            .select('body > main > section > div.row.my-3.align-items-center > div.col-auto.d-none.d-md-block')[0]
            .text
            .split(' Hits')[0]
        )
        per_page = 30
        pages = (hits + per_page - 1) // per_page
        return pd.concat([
            fetch_page(query + f'&site={page + 1}')
            for page in tqdm(range(pages))
        ]).reset_index(drop=True)
    except Exception as e:
        print(e)
        return pd.DataFrame()

def search_products(game='Magic', idCategory='All', idExpansion='All', idRarity='All',
                    searchString=None, exactMatch=None, onlyAvailable=None, onlyCardmarket=None) -> pd.DataFrame:
    input_searchString   = '' if searchString   is None else f'&searchString={searchString}'
    check_exactMatch     = '' if exactMatch     is None else f'&exactMatch={exactMatch}'
    check_onlyAvailable  = '' if onlyAvailable  is None else f'&onlyAvailable={onlyAvailable}'
    check_onlyCardmarket = '' if onlyCardmarket is None else f'&onlyCardmarket={onlyCardmarket}'
    query = cardmarket_url + game + f'/Products/Search?idCategory={idCategory}&idExpansion={idExpansion}&idRarity={idRarity}{input_searchString}{check_exactMatch}{check_onlyAvailable}{check_onlyCardmarket}'
    return fetch_query(query)
