#          Copyright Rein Halbersma 2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

from .cardmarket import parse_query, product_query
from .etiget import etiget
from .mga import fetch_menus, fetch_register, eval_companies, fetch_linked_companies, fetch_providers_and_urls
from .nct import download_data, unzip_data, parse_xml
from .transfermarkt import fetch_eu_leagues, extract_league_link, fetch_clubs, extract_club_link, fetch_players, extract_player_data
