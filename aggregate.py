"""
Functions to perform aggregation on the cleaned WAR-On-Ice data. 
"""
import event_filter as evfilter
import pandas as pd


def team_record(pbp, team, filter_fn=None):  # TODO
    if (filter_fn == 'home'):
        filter_fn = evfilter.by_home_team(pbp, team)
    elif (filter_fn == 'away'):
        filter_fn = evfilter.by_away_team(pbp, team)
    else:
        filter_fn = evfilter.by_team(pbp, team)




#################################################################


############### Skaters Aggregation #############################

def players_goals(pbp):
    goal = evfilter.goals(pbp)
    players_goals = goal.groupby('p1_name').size()
    players_goals.index.name = 'player'
    return players_goals



def corsi_for(pbp):
    shot = evfilter.shot_attempts(pbp)
    corsi_for = shot.groupby('Ev_Team').size()
    corsi_for.index.name = 'Ev_Team'
    return corsi_for


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


def skaters_total_scoring(pbp):  #TODO
    pass

#################################################################
################# Team Aggregation ##############################

def team_goals_by_game(pbp):
    goal = evfilter.goals(pbp)
    team_goals_by_game = goal.groupby('Ev_Team').size()
    team_goals_by_game.index.name = 'Ev_Team'
    return team_goals_by_game

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

def team_saves(pbp):#TODD
    sog = team_shot_attempts(pbp)
    pass


#################################################################

############### Goalies Aggregation #############################

def _goalie_index(pbp):
    # dropna() removes nan from empty net situations
    def uniq_col(x): return set(pbp[x].dropna().unique())

    goalies = sorted(list(uniq_col('Away_Goalie').union(uniq_col('Home_Goalie'))))
    return pd.Index(goalies)


def goalies_games_played(pbp):  #TODO
    games = pbp['Game_Id'].unique()
    for game in games:
        pass


def goalie_records(pbp, goalie_index=None):  #TODO
    "Aggregate goalie win/loss record over input pbp. Returns data frame with total wins/losses, and home & away win/losses. A win/loss is recorded only if the goalie is on the ice for the game-winning-goal. A list or index of goalies can be input if already calculated; otherwise computed on the fly from pbp."
    g = evfilter.game_winning_goals(pbp)
    wins = {t: g[g['Ev_Team'] == g[t + 'team']] for t in ['home', 'away']}
    records = {
        'home_wins': wins['home'].groupby('Home_Goalie').size(),
        'home_losses': wins['away'].groupby('Home_Goalie').size(),
        'away_wins': wins['away'].groupby('Away_Goalie').size(),
        'away_losses': wins['home'].groupby('Away_Goalie').size(),
    }
    index = goalie_index if goalie_index is not None else _goalie_index(pbp)
    res = pd.DataFrame(index=index, data=records).fillna(0)
    res.insert(0, 'losses', res['home_losses'] + res['away_losses'])
    res.insert(0, 'wins', res['home_wins'] + res['away_wins'])
    return res


def goalies_games_started(pbp, goalie_index=None):
    "Aggregate goalie starts over input pbp. A list or index of goalies can be input if already calculated; otherwise computed on the fly from pbp. Returns data frame with columns: (starts,home_starts,away_starts)."
    index = goalie_index if goalie_index is not None else _goalie_index(pbp)
    res = pd.DataFrame(index=index)
    games = pbp.groupby('Game_Id').head(1)
    res.insert(len(res.columns), 'home_starts', games['Home_Goalie'].value_counts())
    res.insert(len(res.columns), 'away_starts', games['Away_Goalie'].value_counts())
    res.fillna(0, inplace=True)
    res.insert(0, 'starts', res['home_starts'] + res['away_starts'])
    return res


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




# def goalie_stats(pbp,player):#need to fix this
# stats = None
# return stats
