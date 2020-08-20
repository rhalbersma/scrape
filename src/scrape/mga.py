#          Copyright Rein Halbersma 2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import ast
import re

import bs4
import lxml
import numpy as np
import pandas as pd

from scrape.etiget import etiget

register_url = 'https://mgalicenseeregister.mga.org.mt/'
verification_url = 'https://www.authorisation.mga.org.mt/verification.aspx'

def eval_option(soup, data_placeholder, colname):
    """
    Extract the option values for a menu into a Pandas DataFrame.
    """
    return pd.DataFrame(
        data=[
            option.text
            for option in (soup
                .find('select', {'data-placeholder': data_placeholder})
                .find_all('option')
            )
        ],
        columns=[colname]
    )

def fetch_menus():
    """
    Get the menus from the MGA Licensee Register.
    """
    response = etiget(register_url + 'index1.aspx')
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.content, 'lxml')
    return (
        eval_option(soup, 'Licensee Name', 'CompanyName'),
        eval_option(soup, 'Licence Status', 'Status'),
        eval_option(soup, 'Gaming Service', 'GamingService'),
        eval_option(soup, 'URL', 'URL')
    )

# The complete information per licensee that is provided.
licensee_columns = [
    'CompanyName',
    'LicenceNumber',
    'LicenceClass',
    'RegNumber',
    'CompanySeal',
    'Status',
    'TerminationDate',
    'Platform',
    'Address',
    'Telephone',
    'Email'
]

def eval_column(script, column):
    """
    Evaluate the JavaScript array for a column as a Python list.
    """
    return (ast
        .literal_eval((re
            .compile(rf'var vArray{re.escape(column)} = (\[.*\])')
            .search(script)
            .group(1)
        ))
    )

def fetch_register(Licensee='', Class='', Status='', URL=''):
    """
    The search form of the MGA Licensee Register.
    """
    response = etiget(register_url + f'Results1.aspx?Licencee={Licensee}&Class={Class}&Status={Status}&URL={URL}')
    try:
        soup = bs4.BeautifulSoup(response.content, 'lxml')
    except:
        print(f'Error {response.status_code}: {Licensee} - {Class} - {Status} - {URL}')
        return pd.DataFrame()
    try:
        script = (soup
            .find('script', src='list.min.js')
            .find_next_sibling('script')
            .string
        )
        N = len(eval_column(script, 'CompanyName'))
        cs = eval_column(script, 'CompanySeal')
        # Company seals are listed twice, but only the first half are used.
        assert cs[:N] == cs[N:]
        return (pd
            .DataFrame.from_dict({
                column: eval_column(script, column)[:N]
                for column in licensee_columns
            })
        )
    except Exception as e:
        print(f'{e}: {Licensee} - {Class} - {Status} - {URL}')
        return pd.DataFrame()

def eval_companies(register):
    """
    Extract the unique company names and seals from the MGA Licensee Register.
    """
    return (register
        .dropna(subset=['CompanySeal'])
        .loc[:, ['CompanyName', 'CompanySeal']]
        .drop_duplicates()
        .reset_index(drop=True)
    )

def fetch_linked_companies(company):
    """
    Get all indirectly linked companies.
    These are sometimes not directly returned from the menu options of the MGA Licensee Register.
    """
    response = etiget(verification_url + f'?company={company.CompanySeal}')
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.content, 'lxml')
    return (pd.DataFrame(
        data=[
            (company.CompanyName, company.CompanySeal, link.text,
                (link
                    .get('href')
                    .split('&company=')[-1]
                    .split('&details=')[0]
                )
            )
            for link in (soup
                .find('ul', class_='linked-companies-list')
                .find_all('a')
            )
        ],
        columns=[
            'CompanyName', 'CompanySeal', 'LinkedName', 'LinkedSeal'
        ]
    ))

def eval_game_type(company, row):
    """
    Extract all providers and their licence numbers for the game type table row.
    """
    content = row.find_all('td')[:-1]
    return pd.DataFrame(
        data=[(
                company.LinkedName,
                company.LinkedSeal,
                content[0].text,
                content[1].text,
                ' '.join(provider.split(' ')[:-1]),
                provider.split(' ')[-1]
            )
            for provider in [
                string.replace('\u2022 ', '')
                for string in (content[2]
                    .text
                    .lstrip('\r\n')
                    .rstrip(' \n')
                    .split(' \r\n')
                )
            ]
        ],
        columns=[
            'LinkedName',
            'LinkedSeal',
            'LicenceNumber',
            'LicenceClass',
            'ProviderName',
            'ProviderLicence'
        ]
    ) if content[2].text.count('\u2022') else pd.DataFrame()

def fetch_providers_and_urls(company):
    response = etiget(verification_url + f'?company={company.LinkedSeal}&details=1')
    try:
        soup = bs4.BeautifulSoup(response.content, 'lxml')
    except Exception as e:
        print(e)
        print(f'Error {response.status_code}: could not download company seal {company.LinkedSeal}')
        return pd.DataFrame(), pd.DataFrame()
    try:
        providers = pd.concat([
            eval_game_type(company, row)
            for row in (soup
                .find('table', id='mainPlaceHolder_coreContentPlaceHolder_mainContentPlaceHolder_sealContent_tblGameTypesTable')
                .find_all('tr')[1:]
            )
        ])
    except Exception as e:
        print(e)
        providers = pd.DataFrame()
    try:
        links = (soup
            .find('span', text='Website Urls')
            .find_parent('th')
            .find_next_sibling('td')
            .find_all('a')
        )
    except Exception as e:
        print(e)
        links = []
    URLs = pd.DataFrame(
        data=[
            (company.LinkedName, company.LinkedSeal, link.get('href'))
            for link in links
        ],
        columns=[
            'LinkedName', 'LinkedSeal', 'URL'
        ]
    )
    return providers, URLs
