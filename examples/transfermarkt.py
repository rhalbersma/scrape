#          Copyright Rein Halbersma 2020.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

# An independent re-implementation of Marcel Wieting's LinkedIn post
# https://www.linkedin.com/pulse/web-scraping-relative-age-effect-professional-football-marcel-wieting/?trackingId=d8UqaacWy%2FaNdTYFhh4MsQ%3D%3D

import calendar

import numpy as np
import pandas as pd
import plotnine as p9
from tqdm import tqdm

import scrape.transfermarkt as tm

print('Fetching leauge URLs from the top 50 EU leagues:')
eu_league_urls = list(filter(lambda link: link.endswith('1'), [
    tm.extract_league_link(league)
    for page in tqdm(range(1, 5))
    for league in tm.fetch_eu_leagues(page)
]))

print('Fetching club URLs from all leagues:')
eu_club_urls = [
    tm.extract_club_link(club)
    for league in tqdm(eu_league_urls)
    for club in tm.fetch_clubs(league)
]

print('Fetching player data from all clubs:')
eu_player_data = pd.concat([
    # Normally, we would extract player data from the team table with pd.read_html().
    # However, some cells contain nested HTML tables which would not have been handled gracefully.
    # Instead, we use our own extract_player_data() on each player individually.
    pd.DataFrame(
        data=[
            tm.extract_player_data(player)
            for player in tm.fetch_players(club)
        ],
        columns=[
            'number', 'name', 'position', 'birth_date', 'market_value'
        ]
    ).assign(squad = club.split('/')[1])
    for club in tqdm(eu_club_urls)
])

df = (eu_player_data
    .reset_index(drop=True)
    .replace({'number': {'-': np.nan}})
    .astype(dtype={'number': float})
    .astype(dtype={'number': 'Int64'})
    .assign(birth_date = lambda x: pd.to_datetime(x.birth_date.str.split('(').str[0].replace('- ', ''), errors='coerce'))
    .dropna(subset=['birth_date'])
    .assign(dayofyear = lambda x: x.birth_date.dt.dayofyear.astype(int))
    .assign(month = lambda x: x.birth_date.dt.month.astype(int))
    .assign(month_abbr = lambda x: x.apply(lambda y: calendar.month_abbr[y.month], axis=1))
    .assign(weight = lambda x: 1.0 / x.birth_date.dt.days_in_month)
    .assign(market_value = lambda x: x.market_value.str.normalize('NFKD').str.replace(' ', '').replace('-', np.nan).str.replace('Th.', 'k'))
    .assign(multiplier = lambda x: x.market_value.str[-1].replace('m', 1.).replace('k', .001))
    .assign(market_value = lambda x: x.market_value.str[1:-1].replace('', np.nan).astype(float) * x.multiplier)
    .drop(columns=['multiplier'])
)
df.info()

# Total players, per month (unweighted by length of month)
data = (df
    .groupby(['month', 'month_abbr'])
    .agg(players = ('month', 'count'))
    .reset_index()
)
(p9.ggplot(data, p9.aes('month', 'players'))
    + p9.geom_point()
    + p9.stat_smooth(method='lm')
    + p9.scale_x_continuous(breaks=data.month, labels=data.month_abbr)
)

# Players per day, per month (weighted by length of month)
data = (df
    .groupby(['month', 'month_abbr'])
    .agg(players_per_day = ('weight', 'sum'))
    .reset_index()
)
(p9.ggplot(data, p9.aes('month', 'players_per_day'))
    + p9.geom_point()
    + p9.stat_smooth(method='lm')
    + p9.scale_x_continuous(breaks=data.month, labels=data.month_abbr)
)

# Total players, per day
data= (df
    .groupby('dayofyear')
    .agg(players = ('dayofyear', 'count'))
    .reset_index()
)
(p9.ggplot(data, p9.aes('dayofyear', 'players'))
    + p9.geom_point()
    + p9.stat_smooth(method='lm')
)
