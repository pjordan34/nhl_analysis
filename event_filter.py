"""
Functions for subsetting/filtering the cleaned NHL Play by Play data. I leverged hockey_scraper to get data from the NHL API.
"""

import pandas as pd
import numpy as np
import constants as const


############### By team ######################################

def by_home_team(pbp, team):
    "Returns pbp from homes games for `team` (use the standard 3-letter abbreviation for team names.)"
    return pbp[pbp['Home_Team'] == team]


def by_away_team(pbp, team):
    "Returns pbp from away games for `team` (use the standard 3-letter abbreviation for team names.)"
    return pbp[pbp['Away_Team'] == team]


def by_team(pbp, team):
    "Returns pbp from all games for `team` (use the standard 3-letter abbreviation for team names.)"
    home = by_home_team(pbp, team)
    away = by_away_team(pbp, team)
    return home.append(away).sort_values(by=['Game_Id'], axis=0)


def by_event_team(pbp, team):
    "Returns pbp where event team is `team` (use the standard 3-letter abbreviation for team names.)"
    return pbp[pbp['Ev_Team'] == team]


############### By players ######################################

def by_goalie(pbp, goalie):
    return pbp[(pbp['Home_Goalie'] == goalie) | (pbp['Away_Goalie'] == goalie)]


def by_home_goalie(pbp, goalie):
    return pbp[(pbp['Home_Goalie'] == goalie)]


def by_away_goalie(pbp, goalie):
    return pbp[(pbp['Away_Goalie'] == goalie)]


def by_skater(pbp, player):
    bool_vec = pd.Series(False, index=np.arange(len(pbp)))
    for position in (const.HOME_SKATERS + const.AWAY_SKATERS):
        bool_vec |= (pbp[position] == player)
    return pbp[bool_vec]


def by_home_skater(pbp, player):
    bool_vec = pd.Series(False, index=np.arange(len(pbp)))
    for position in const.HOME_PLAYERS:
        bool_vec |= (pbp[position] == player)
    return pbp[bool_vec]


def by_away_skater(pbp, player):
    bool_vec = pd.Series(False, index=np.arange(len(pbp)))
    for position in const.AWAY_SKATERS:
        bool_vec |= (pbp[position] == player)
    return pbp[bool_vec]


################### Period/Regulation/OT/Shootout ###########################

def period(pbp, period):
    "Return pbp from a given period of play."
    return pbp[pbp['Period'] == period]


def regulation(pbp):
    "Return pbp from regulation time, i.e. periods 1,2,3."
    return pbp[pbp['Period'] <= 3]


def overtime(pbp):
    "Return pbp from overtime, excluding shootouts."
    after_regulation = pbp[pbp['Period'] > 3]
    return remove_shootouts(after_regulation)


def shootouts(pbp):
    "Returns only shootout pbp."
    # Shootouts are period 5 of regular season games.
    return pbp[(pbp['Period'] == 5)
                  & (pbp['Game_Id'] <= const.PLAYOFFS_START)]


def remove_shootouts(pbp):
    "Removes all shootout pbp."
    # Shootouts are period 5 of regular season games.
    return pbp[(pbp['Period'] != 5)
                  | (pbp['Game_Id'] > const.PLAYOFFS_START)]


################## Man-advantage status #######################

def even_strength(pbp):
    "Return even-strength (5v5, 4v4, 3v3) pbp. "
    return pbp[pbp['Home_Players'] == pbp['Away_Players']]


def five_on_five(pbp):  # goalies count!
    return pbp[(pbp['Home_Players'] == 6) & (pbp['Away_Players'] == 6)]


def four_on_four(pbp):  # goalies count!
    return pbp[(pbp['Home_Players'] == 5) & (pbp['Away_Players'] == 5)]


def man_advantage(pbp):
    return pbp[pbp['Home_Players'] != pbp['Away_Players']]


def power_play(pbp, team):
    "Returns any power play pbp for specified team."
    return pbp[((pbp['Home_Team'] == team)
                   & (pbp['Home_Players'] > pbp['Away_Players']))
                  | ((pbp['Away_Team'] == team)
                     & (pbp['Away_Players'] > pbp['Home_Players']))]


def penalty_kill(pbp, team):
    "Returns any penalty_kill pbp for specified team."
    return pbp[((pbp['Home_Team'] == team)
                   & (pbp['Home_Players'] < pbp['Away_Players']))
                  | ((pbp['Away_Team'] == team)
                     & (pbp['Away_Players'] < pbp['Home_Players']))]


###################### Season status ##############################

def regular_season(pbp):
    "Return pbp from regular season games."
    return pbp[pbp['Game_Id'] <= const.PLAYOFFS_START]


def playoffs(pbp):
    "Return pbp from playoff games."
    return pbp[pbp['Game_Id'] > const.PLAYOFFS_START]


#################### Offensive events ##############################

def goals(pbp):
    return pbp[pbp['Event'] == 'GOAL']

def hits(pbp):
    return pbp[pbp['Event'] == 'HIT']


def shots(pbp):
    return pbp[(pbp['Event'] == 'SHOT') | (pbp['Event'] == 'GOAL')]


def shot_attempts(pbp):
    return pbp[(pbp['Event'] == 'SHOT') | (pbp['Event'] == 'GOAL')
                  | (pbp['Event'] == 'MISS') | (pbp['Event'] == 'BLOCK')]



#################### Defensive events ##############################

def blocked_shots(pbp):
    return pbp[pbp['Event'] == 'BLOCK']


#################### Goalie events ###################################

def saves(pbp):

    return pbp[pbp['Event'] == 'SHOT']
