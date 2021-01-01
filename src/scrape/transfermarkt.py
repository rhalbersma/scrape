#          Copyright Rein Halbersma 2020-2021.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

# Re-implementing Marcel Wieting's LinkedIn post
# https://www.linkedin.com/pulse/web-scraping-relative-age-effect-professional-football-marcel-wieting/?trackingId=d8UqaacWy%2FaNdTYFhh4MsQ%3D%3D

import re

import bs4
import lxml
from typing import Optional, Tuple

from scrape.etiget import etiget

transfermarkt_url = 'https://www.transfermarkt.com'
eu_leagues = '/wettbewerbe/europa'

def fetch_eu_leagues(page: str) -> bs4.element.ResultSet:
    response = etiget(transfermarkt_url + eu_leagues + f'?page={page}')
    assert response.status_code == 200
    return (bs4
        .BeautifulSoup(response.content, 'lxml')
        .find('div', class_='responsive-table')
        .find('tbody')
        .find_all('tr', class_=re.compile('odd|even'))
    )

def extract_league_link(league: bs4.element.Tag) -> str:
    return (league
        .find_all('td')[2]
        .find('a')
        .get('href')
    )

def fetch_clubs(league: str) -> bs4.element.ResultSet:
    response = etiget(transfermarkt_url + league)
    assert response.status_code == 200
    return (bs4
        .BeautifulSoup(response.content, 'lxml')
        .find('div', class_='responsive-table')
        .find('tbody')
        .find_all('tr', class_=re.compile('odd|even'))
    )

def extract_club_link(club: bs4.element.Tag) -> str:
    return (club
        .find('td')
        .find('a')
        .get('href')
    )

def fetch_players(club: str) -> bs4.element.ResultSet:
    response = etiget(transfermarkt_url + club)
    try:
        soup = bs4.BeautifulSoup(response.content, 'lxml')
        try:
            return (soup
                .find('div', class_='responsive-table')
                .find('tbody')
                .find_all('tr', class_=re.compile('odd|even'))
            )
        except Exception as e:
            print(f'{e}: empty squad for club == {club}')
            return []
    except:
        print(f'Error {response.status_code}: not finding club == {club}')
        return []

def extract_player_data(player: bs4.element.Tag) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]]:
    try:
        number = (player
            .find('div', class_='rn_nummer')
            .text
        )
    except:
        number = None
    try:
        name = (player
            .find('td', itemprop='athlete')
            .text
        )
    except:
        name = None
    try:
        position = (player
            .find('td', class_='posrela')
            .find_all('tr')[1]
            .find('td')
            .text
        )
    except:
        position = None
    try:
        birth_date = (player
            .find_all('td', recursive=False)[3]
            .text
        )
    except:
        birth_date = None
    try:
        market_value = (player
            .find('td', class_='rechts hauptlink')
            .text
        )
    except:
        market_value = None
    return number, name, position, birth_date, market_value
