#          Copyright Rein Halbersma 2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

# An independent re-implementation of Marcel Wieting's LinkedIn post
# https://www.linkedin.com/pulse/web-scraping-relative-age-effect-professional-football-marcel-wieting/?trackingId=d8UqaacWy%2FaNdTYFhh4MsQ%3D%3D

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from tqdm import tqdm

import scrape.transfermarkt as tm

print('Fetching leauge URLs from the top 50 EU leagues:')
eu_league_urls = list(filter(lambda link: link.endswith('1'), [
    tm.extract_league_link(league)
    for page in range(1, 5)
    for league in tm.fetch_eu_leagues(page)
]))

eu_league_ids = [
    url.split('/')[-1]
    for url in eu_league_urls
]

print('Fetching club URLs from all leagues:')
eu_club_urls = [
    tm.extract_club_link(club)
    for league in tqdm(eu_league_urls)
    for club in tm.fetch_clubs(league)
]

print('Fetching player data from all clubs:')
eu_player_data = pd.concat([
    # Normally, we would directly extract each team with pd.read_html().
    # However, some cells contain nested HTML tables which will not be handled gracefully.
    pd.DataFrame(data=[
        tm.extract_player_data(player)
        for player in tm.fetch_players(club)
    ]).assign(squad = club.split('/')[1])
    for club in tqdm(eu_club_urls)
])

df = eu_player_data.reset_index(drop=True)
df.columns = [ 'number', 'position', 'name', 'birth_date', 'empty', 'market_value', 'squad']
df = (df
    .replace({'number': {'-': np.nan}})
    .astype(dtype={'number': float})
    .astype(dtype={'number': 'Int64'})
    .assign(surname = lambda x: x.name.str.split(' ').str[-1])
    .assign(position = lambda x: x.apply(lambda y: y.position.split(y.surname)[-1], axis=1).str.normalize('NFKD'))
    .assign(birth_date = lambda x: pd.to_datetime(x.birth_date.str.split('(').str[0].replace('- ', ''), errors='coerce'))
    .assign(birth_month = lambda x: x.birth_date.dt.month)
    .assign(month_weight = lambda x: 1.0 / x.birth_date.dt.days_in_month)
    .assign(birth_dayofyear = lambda x: x.birth_date.dt.dayofyear)
    .assign(market_value = lambda x: x.market_value.str.normalize('NFKD').str.replace(' ', '').replace('-', np.nan))
    .assign(market_value = lambda x: x.market_value.str.replace('Th.', 'k'))
    .assign(multiplier = lambda x: x.market_value.str[-1].replace('m', 1.0).replace('k', .001))
    .assign(market_value = lambda x: x.market_value.str[1:-1].replace('', np.nan).astype(float) * x.multiplier)
    .drop(columns=['empty', 'surname', 'multiplier'])
)

# TODO: clean bad characters from "position" column, and solve Senegalese Centre-Back players named "Ba"

# Total players, per month
sns.regplot(y='players', x='birth_month', data=df.groupby('birth_month').agg(players = ('birth_month', 'count')).reset_index())
plt.show()

# Players per day, per month
sns.regplot(y='players_per_day', x='birth_month', data=df.groupby('birth_month').agg(players_per_day = ('month_weight', 'sum')).reset_index())
plt.show()

# Total players, per day
sns.regplot(y='players', x='birth_dayofyear', data=df.groupby('birth_dayofyear').agg(players = ('birth_date', 'count')).reset_index())
plt.show()

# Market value, per month
sns.regplot(y='market_value', x='birth_month', data=df.groupby('birth_month').agg(market_value = ('market_value', 'mean')).reset_index())
plt.show()

# Market value, per month
sns.boxplot(y='market_value', x='birth_month', data=df)
plt.ylim(0,3) # comment this line to see the huge variation of players worth more than EUR 3m
plt.show()

# df.to_csv('data/eu_player_data.csv')
