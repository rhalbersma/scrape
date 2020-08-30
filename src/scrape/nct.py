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

from scrape.etiget import etiget

def download_data(url, file):
    response = etiget(url, stream=True)
    assert response.status_code == 200
    with open(file, 'wb') as dst:
        for chunk in response.iter_content(chunk_size=4096):
            dst.write(chunk)

def unzip_data(file, path):
    with zipfile.ZipFile(file) as src:
        src.extractall(path)

def parse_xml(file):
    # The XML files are named NCTyyyyxxxx, this extracts the 8 yyyyxxxx digits
    id = int(os.path.splitext(os.path.basename(file))[0][-8:])
    tree = etree.parse(file)
    return pd.DataFrame(
        data=[
            (id, tree.getpath(elem), elem.text)
            for elem in tree.iter()
        ],
        columns=['id', 'key', 'value']
    )
