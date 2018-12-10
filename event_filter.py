"""
Functions for subsetting/filtering the cleaned NHL Play by Play data. I leverged hockey_scraper to get data from the NHL API.
"""

import pandas as pd
import numpy as np
import constants as const


# event_filter notebook
def by_season(pbp, season):
    "Returns pbp from a given season. Season codes take the form '20142015'."
    return pbp[pbp['season'] == season]


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

def shooting_percentage(pbp):#TODO
    goal = goals(pbp)
    shot = shots(pbp)
    shot_percentage = goal/shot
    return shot_percentage

def record(pbp):
    Win = []
    Loss = []
    Tie = []
    if pbp['Home_Score'] > pbp['Away_Score']:
        Win.append(pbp['Home_Team'])
        Loss.append(pbp['Away_Team'])
    elif pbp['Home_Score'] < pbp['Away_Score']:
        Win.append(pbp['Away_Team'])
        Loss.append(pbp['Home_Team'])
    else:
        Tie.append(pbp['Home_Team'])
        Tie.append(pbp['Away_Team'])

    return Win, Loss, Tie

def losses(pbp):
    Losses = []
    if pbp['Home_Score'] > pbp['Away_Score']:
        Losses.append(pbp['Away_Team'])
    else:
        Losses.append((pbp['Home_Team']))
    return Losses

def tie(pbp):
    Ties = []
    if pbp['Home_Score'] == pbp['Away_Score']:
        Ties.append(pbp['Home_Team'])
        Ties.append(pbp['Away_Team'])
    return Ties



def game_winning_goals(pbp):  #TODO
    "Returns subset of the input pbp which represent game winning goals. Note that the input must include all non-shootout goals in a game for the output to be reliable."
    goal = remove_shootouts(pbp[pbp['Event'] == 'GOAL'])
    games = goal.groupby('Game_Id')

    def _find_gwg(game_goals):  # Returns empty df if a tie
        def _max_score(team):  # team = 'home' or 'away'
            score = game_goals[team + '_score'].max()
            if (game_goals.tail(1)['Ev_Team'].values[0] == game_goals[team + 'team'].values[0]):
                score += 1  # score entries don't include the goal just scored
            return score

        winner, loser = 'home', 'away'
        if _max_score('away') > _max_score('home'):
            winner, loser = 'away', 'home'
        winner_goals = game_goals[game_goals['Ev_Team'] == game_goals[winner + 'team']]
        return winner_goals[winner_goals[winner + '.score'] + 1 > _max_score(loser)].head(1)

    gwg = games.apply(_find_gwg)
    gwg.index = gwg.index.levels[1]  # removes the redundant gcode indexing layer
    return gwg



#################### Defensive events ##############################

def blocked_shots(pbp):
    return pbp[pbp['Event'] == 'BLOCK']


#################### Goalie events ###################################

def saves(pbp):

    return pbp[pbp['Event'] == 'SHOT']
