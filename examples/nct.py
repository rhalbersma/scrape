#          Copyright Rein Halbersma 2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

# An independent re-implementation of Marcel Wieting's code review post
# https://codereview.stackexchange.com/questions/239521/performance-read-large-amount-of-xmls-and-load-into-single-csv

import os

import pandas as pd
from tqdm import tqdm

import scrape.nct as nct

# https://clinicaltrials.gov/ct2/resources/download#DownloadAllData
url = 'https://clinicaltrials.gov/AllPublicXML.zip'
file = url.split('/')[-1]
path = file.split('.')[0]

# Please note the rather large size of these files!
nct.download_data(url, file)    # 1.6 Gb on disk
nct.unzip_data(file, path)      # 8.5 Gb on disk

xml_files = [
    os.path.join(dirpath, file)
    for dirpath, _, filenames in os.walk(path)
    for file in filenames
    if file.endswith('.xml')
]

df = pd.concat((
    nct.parse_xml(f)
    for f in tqdm(xml_files)
))

df.info()               #  3.0 Gb in memory
# df.to_csv('nct.csv')  # 12.0 Gb on disk
