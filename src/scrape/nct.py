#          Copyright Rein Halbersma 2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

# Re-implementing Marcel Wieting's code review post
# https://codereview.stackexchange.com/questions/239521/performance-read-large-amount-of-xmls-and-load-into-single-csv

import os
import zipfile

from lxml import etree
import pandas as pd
from tqdm import tqdm

from scrape.etiget import etiget

def download_data(url: str, file: str, chunk_size=1024*1024) -> None:
    response = etiget(url, stream=True)
    assert response.status_code == 200
    content_length = int(response.headers['Content-Length'])
    num_chunks = (content_length + chunk_size - 1) // chunk_size
    with open(file, 'wb') as dst:
        for chunk in tqdm(response.iter_content(chunk_size=chunk_size), total=num_chunks):
            dst.write(chunk)

def unzip_data(file: str, path: str) -> None:
    with zipfile.ZipFile(file) as src:
        src.extractall(path)

def parse_xml(file: str) -> pd.DataFrame:
    # The XML files are named NCTyyyyxxxx, this extracts the last 8 yyyyxxxx digits
    id = int(os.path.splitext(os.path.basename(file))[0][-8:])
    tree = etree.parse(file)
    return pd.DataFrame(
        data=[
            (id, tree.getpath(elem), elem.text)
            for elem in tree.iter()
        ],
        columns=['id', 'key', 'value']
    )
