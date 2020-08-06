#          Copyright Rein Halbersma 2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

# An independent re-implementation of Marcel Wieting's LinkedIn post
# https://www.linkedin.com/pulse/web-scraping-relative-age-effect-professional-football-marcel-wieting/?trackingId=d8UqaacWy%2FaNdTYFhh4MsQ%3D%3D

import re

import bs4
import lxml
import pandas as pd

from scrape.etiget import etiget

transfermarkt = 'https://www.transfermarkt.com'
eu_leagues = '/wettbewerbe/europa'

def fetch_eu_leagues(page):
    response = etiget(transfermarkt + eu_leagues + f'?page={page}')
    assert response.status_code == 200
    return (bs4
        .BeautifulSoup(response.content, 'lxml')
        .find('div', {'class', 'responsive-table'})
        .find('tbody')
        .find_all('tr', {'class', re.compile('odd|even')})
    )

def extract_league_link(league):
    return (league
        .find_all('td')[2]
        .find('a')
        .get('href')
    )

def fetch_clubs(league):
    response = etiget(transfermarkt + league)
    assert response.status_code == 200
    return (bs4
        .BeautifulSoup(response.content, 'lxml')
        .find('div', {'class', 'responsive-table'})
        .find('tbody')
        .find_all('tr', {'class', re.compile('odd|even')})
    )

def extract_club_link(club):
    return (club
        .find('td')
        .find('a')
        .get('href')
    )

def fetch_players(club):
    response = etiget(transfermarkt + club)
    try:
        soup = bs4.BeautifulSoup(response.content, 'lxml')
        try:
            return (soup
                .find('div', {'class', 'responsive-table'})
                .find('tbody')
                .find_all('tr', {'class', re.compile('odd|even')})
            )
        except Exception as e:
            print(f'{e}: empty squad for club == {club}')
            return []
    except:
        print(f'Error {response.status_code}: not finding club == {club}')
        return []

def extract_player_data(player):
    return tuple(
        cell.text
        for cell in player.find_all('td', recursive=False)
    )
