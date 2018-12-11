"""
Functions to perform aggregation on the cleaned WAR-On-Ice data. 
"""
import hockey_analysis.event_filter as evfilter
import pandas as pd


#################################################################
############### Skaters Aggregation #############################

def players_goals(pbp):
    goal = evfilter.goals(pbp)
    players_goals = goal.groupby('p1_name').size()
    players_goals.index.name = 'player'
    return players_goals

def players_assists(pbp):
    goal = evfilter.goals(pbp)
    players_assists = pd.melt(goal[['p2_name', 'p3_name']]).dropna().groupby('value').size()
    players_assists.index.name = 'player'
    return players_assists


def players_points(pbp):
    goal = players_goals(pbp)
    assists = players_assists(pbp)
    players_points = goal.add(assists, fill_value=0)
    players_points.index.name = 'player'
    return players_points


#################################################################
################# Team Aggregation ##############################

def team_goals(pbp):
    goal = evfilter.goals(pbp)
    team_goals = goal.groupby('Ev_Team').size()
    team_goals.index.name = 'Ev_Team'
    return team_goals

def team_hits(pbp):
    hit = evfilter.hits(pbp)
    team_hits = hit.groupby('Ev_Team').size()
    team_hits.index.name = 'Ev_Team'
    return team_hits

def team_blocks_against(pbp):
    block = evfilter.blocked_shots(pbp)
    team_blocks = block.groupby('Ev_Team').size()
    team_blocks.index.name = 'Ev_Team'
    return team_blocks

def team_SOG(pbp):
    shot = evfilter.shots(pbp)
    team_SOG = shot.groupby('Ev_Team').size()
    team_SOG.index.name = 'Ev_Team'
    return team_SOG

def team_shot_attempts(pbp):
    shot = evfilter.shot_attempts(pbp)
    team_shot_attempts = shot.groupby('Ev_Team').size()
    team_shot_attempts.index.name = 'Ev_Team'
    return team_shot_attempts

def team_shot_attempts_against(pbp):
    shot = evfilter.shot_attempts(pbp)
    if pbp['Ev_Team'] == pbp['Home_Team']:
        team_shot_attempts_against = shot.groupby('Away_Team').size()
        team_shot_attempts_against.index.name = 'Away_Team'
    else:
        team_shot_attempts_against = shot.groupby('Home_Team').size()
        team_shot_attempts_against.index.name = 'Home_Team'
    return team_shot_attempts


#################################################################

############### Goalies Aggregation #############################

def _goalie_index(pbp):
    # dropna() removes nan from empty net situations
    def uniq_col(x): return set(pbp[x].dropna().unique())
    goalies = sorted(list(uniq_col('Away_Goalie').union(uniq_col('Home_Goalie'))))
    return pd.Index(goalies)

def goals_against(pbp):
    "Aggregate goals against for individual goalies over the input set of pbp. Returns a series indexed by goalie text_id."
    goal = evfilter.goals(pbp)
    goalies = pd.Series(data=goal['Home_Goalie'], index=goal.index)
    goalies[goal['Ev_Team'] == goal['Home_Team']] = goal['Away_Goalie']
    return goalies.dropna().value_counts().sort_index()


def goalie_saves(pbp):
    "Aggregate saves for individual goalies over the input set of pbp. Returns a series indexed by goalie text_id."
    saved_shots = evfilter.saves(pbp)
    goalie = pd.Series(data=saved_shots['Home_Goalie'], index=saved_shots.index)
    goalie[saved_shots['Ev_Team'] == saved_shots['Home_Team']] = saved_shots['Away_Goalie']
    return goalie.dropna().value_counts().sort_index()




