#          Copyright Rein Halbersma 2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import numpy as np
import pandas as pd
from tqdm import tqdm

import scrape.mga as mga

print('Fetching all 4 menu options:')
licensees, statuses, services, urls = mga.fetch_menus()

print('Fetching register information:')
register_empty = (mga.fetch_register()
    .drop_duplicates()
    .assign(CompanySeal = lambda x: x.CompanySeal.str.split('=').str[-1])
    .replace('', np.nan)
    .sort_values('CompanyName')
    .reset_index(drop=True)
)

print('Fetching register information from all licensees:')
register_licensees = (pd
    .concat([
        mga.fetch_register(Licensee=licensee.CompanyName)
        for _, licensee in tqdm(licensees.iterrows(), total=licensees.shape[0])
    ])
    .drop_duplicates()
    .assign(CompanySeal = lambda x: x.CompanySeal.str.split('=').str[-1])
    .replace('', np.nan)
    .sort_values('CompanyName')
    .reset_index(drop=True)
)

print('Fetching register information from all gaming service types:')
register_services = (pd
    .concat([
        mga.fetch_register(Class=service.GamingService)
        for _, service in tqdm(services.iterrows(), total=services.shape[0])
    ])
    .drop_duplicates()
    .assign(CompanySeal = lambda x: x.CompanySeal.str.split('=').str[-1])
    .replace('', np.nan)
    .sort_values('CompanyName')
    .reset_index(drop=True)
)

print('Fetching register information from all status types:')
register_statuses = (pd
    .concat([
        mga.fetch_register(Status=status.Status)
        for _, status in tqdm(statuses.iterrows(), total=statuses.shape[0])
    ])
    .drop_duplicates()
    .assign(CompanySeal = lambda x: x.CompanySeal.str.split('=').str[-1])
    .replace('', np.nan)
    .sort_values('CompanyName')
    .reset_index(drop=True)
)

print('Fetching register information from all URLs:')
register_urls = (pd
    .concat([
        mga.fetch_register(URL=url.URL)
        for _, url in tqdm(urls.iterrows(), total=urls.shape[0])
    ])
    .drop_duplicates()
    .assign(CompanySeal = lambda x: x.CompanySeal.str.split('=').str[-1])
    .replace('', np.nan)
    .sort_values('CompanyName')
    .reset_index(drop=True)
)

# Combine all unique entries in the register versions found so far.
register = (pd
    .concat([
        register_empty,
        register_licensees,
        register_statuses,
        register_services,
        register_urls
    ])
    .drop_duplicates()
    .sort_values('CompanyName')
    .reset_index(drop=True)
)
companies = mga.eval_companies(register)

print('Fetching linked companies from all companies:')
linked_companies = (pd
    .concat([
        mga.fetch_linked_companies(company)
        for _, company in tqdm(companies.iterrows(), total=companies.shape[0])
    ])
    .merge(
        companies,
        how='outer',
        left_on='LinkedSeal',
        right_on='CompanySeal',
        suffixes=('', '_y'),
        indicator=True
    )
    .rename(columns={'_merge': 'LinkType'})
    # If the linked company was not present in the MGA Licensee Register, it is a daughter company.
    .replace({'LinkType': {
        'left_only': 'daughter'
    }})
    .assign(LinkType = lambda x: np.where(
        x.LinkType == 'daughter',
        x.LinkType,
        # If the linked company is not a daughter company, it is either the parent company or a partner.
        # A parent company has the same seal as the linked company, otherwise it is a partner.
        np.where(
            x.CompanySeal == x.LinkedSeal,
            'parent',
            'partner'
        )
    ))
    .drop(columns={'CompanyName_y', 'CompanySeal_y'})
    .sort_values(['CompanyName', 'LinkedName'])
    .reset_index(drop=True)
)

df = linked_companies.drop_duplicates(subset='LinkedSeal')
linked_providers, linked_urls = tuple(
    pd.concat(list(t), sort=False).drop_duplicates().reset_index(drop=True)
    # The loop over fetch_providers_and_urls returns a list of pairs of DataFrames.
    # The zip(*) operation transposes this into a pair of lists of DataFrames.
    for t in zip(*[
        mga.fetch_providers_and_urls(company)
        for _, company in tqdm(df.iterrows(), total=df.shape[0])
    ])
)

# register.to_csv('register.csv', index=False, sep=';')
# linked_companies.to_csv('linked_companies.csv', index=False, sep=';')
# linked_providers.to_csv('linked_providers.csv', index=False, sep=';')
# linked_urls.to_csv('linked_urls.csv', index=False, sep=';')
