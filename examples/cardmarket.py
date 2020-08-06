#          Copyright Rein Halbersma 2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import scrape.cardmarket as cm

df = cm.parse_query(cm.product_query(searchString='Forest'))

# df.to_cvs('magic_forest.csv')
