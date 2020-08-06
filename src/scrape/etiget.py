#          Copyright Rein Halbersma 2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import time

import requests

def etiget(url, crawl_delay=2, headers={'User-agent': 'Custom'}, **kwargs):
    """
    Wrap requests.get to conform to webscraping etiquette.
    """
    time.sleep(crawl_delay)
    return requests.get(url, headers=headers, **kwargs)
