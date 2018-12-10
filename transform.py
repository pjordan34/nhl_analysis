import numpy as np
import pandas as pd


# Read in the csv after it has run through the clean script in a loop
def transform(pbp):
    """" feed transform a play by play dataframe, I would keep it to one season at a time, prior to putting the dataframe 
    in you can filter the dataframe by regular season/playoffs and eliminate shootouts if you want. this returns a new 
    dataframe with aggregated stats by game by team.
    """""
    # drop columns that are not needed for team aggrigations
    pbp.drop(['Description', 'Time_Elapsed',
                'Seconds_Elapsed', 'Strength', 'Ev_Zone', 'Type',
                'Home_Zone', 'p1_name', 'p1_ID', 'p2_name',
                'p2_ID', 'p3_name', 'p3_ID', 'awayPlayer1', 'awayPlayer1_id',
                'awayPlayer2', 'awayPlayer2_id', 'awayPlayer3', 'awayPlayer3_id',
                'awayPlayer4', 'awayPlayer4_id', 'awayPlayer5', 'awayPlayer5_id',
                'awayPlayer6', 'awayPlayer6_id', 'homePlayer1', 'homePlayer1_id',
                'homePlayer2', 'homePlayer2_id', 'homePlayer3', 'homePlayer3_id',
                'homePlayer4', 'homePlayer4_id', 'homePlayer5', 'homePlayer5_id',
                'homePlayer6', 'homePlayer6_id', 'Away_Players', 'Home_Players', 'Away_Goalie', 'Away_Goalie_Id',
                'Home_Goalie',
                'Home_Goalie_Id', 'xC', 'yC', 'Home_Coach', 'Away_Coach'], axis=1, inplace=True)
    # create filters to reduce the amount of rows you have to compute on.
    pbpShotAtt = pbp[pbp.Event.isin(['SHOT', 'GOAL', 'MISS', 'BLOCK'])]
    pbpMiss = pbp[pbp.Event.isin(['MISS'])]
    pbpSOG = pbp[pbp.Event.isin(['SHOT', 'GOAL'])]
    # This one will create a off row df from the others, so we will merge this back in last
    pbpGoal = pbp[pbp.Event.isin(['GOAL'])]
    pbpHit = pbp[pbp.Event.isin(['HIT'])]
    pbpBlock = pbp[pbp.Event.isin(['BLOCK'])]
    # set a MultiIndex to start your filtering
    pbp.set_index(['Game_Id', 'Ev_Team'], inplace=True)
    # Aggregations by game, and a concatonate at the end
    pbpShotAtt = (pbpShotAtt.groupby(['Game_Id', 'Ev_Team'])['Event'].size().reset_index())
    pbpShotAtt.rename(columns={'Event': 'Shot_Att'}, inplace=True)
    pbpSOG = (pbpSOG.groupby(['Game_Id', 'Ev_Team'])['Event'].size().reset_index())
    pbpSOG.rename(columns={'Event': 'SOG_for'}, inplace=True)
    pbpHit = (pbpHit.groupby(['Game_Id', 'Ev_Team'])['Event'].size().reset_index())
    pbpHit.rename(columns={'Event': 'Hits_for'}, inplace=True)
    pbpGoal = (pbpGoal.groupby(['Game_Id', 'Ev_Team'])['Event'].size().reset_index())
    pbpGoal.rename(columns={'Event': 'Goals_for'}, inplace=True)
    pbpblocks = (pbpBlock.groupby(['Game_Id', 'Ev_Team'])['Event'].size().reset_index())
    pbpblocks.rename(columns={'Event': 'Blocks_A'}, inplace=True)
    pbpMiss = (pbpMiss.groupby(['Game_Id', 'Ev_Team'])['Event'].size().reset_index())
    pbpMiss.rename(columns={'Event': 'Misses'}, inplace=True)
    pbpO = pd.concat(
        [regDfShotAtt, regDfMiss['Misses'], regDfSOG['SOG_for'], regDfHit['Hits_for'], regDfblocks['Blocks_A']], axis=1)
    # at this point we need the 'Against' metrics which are really the opposite of the calculations we have already made, so we make a loop to do that.
    # this is very repetiative and there may be a better way about it, but this is what I came up with
    games_list = list(pbpO.Game_Id.unique())

    pbpO['Blocks_for'] = 0
    j = 1
    for i in range(len(games_list)):
        pbpO['Blocks_for'][i * 2] = pbpO['Blocks_A'][i + j]
        pbpO['Blocks_for'][i + j] = pbpO['Blocks_A'][i * 2]
        j = j + 1

    pbpO['Shot_Att_A'] = 0
    j = 1
    for i in range(len(games_list)):
        pbpO['Shot_Att_A'][i * 2] = pbpO['Shot_Att'][i + j]
        pbpO['Shot_Att_A'][i + j] = pbpO['Shot_Att'][i * 2]
        j = j + 1

    pbpO['SOG_A'] = 0
    j = 1
    for i in range(len(games_list)):
        pbpO['SOG_A'][i * 2] = pbpO['SOG_for'][i + j]
        pbpO['SOG_A'][i + j] = pbpO['SOG_for'][i * 2]
        j = j + 1

    pbpO['Hits_A'] = 0
    j = 1
    for i in range(len(games_list)):
        pbpO['Hits_A'][i * 2] = pbpO['Hits_for'][i + j]
        pbpO['Hits_A'][i + j] = pbpO['Hits_for'][i * 2]
        j = j + 1

    # Now merge in the Goals_For column
    pbpcomplete = pbpO.merge(right=pbpGoal, left_on=['Game_Id', 'Ev_Team'], right_on=['Game_Id', 'Ev_Team'],
                                 how='left')
    # and fill in the NaN values with 0
    pbpcomplete.fillna(0, inplace=True)

    # one more loop to bring in Goals_A
    pbpcomplete['Goals_A'] = 0
    j = 1
    for i in range(len(games_list)):
        pbpcomplete['Goals_A'][i * 2] = pbpcomplete['Goals_for'][i + j]
        pbpcomplete['Goals_A'][i + j] = pbpcomplete['Goals_for'][i * 2]
        j = j + 1

    # now we can calculate Saves

    pbpcomplete['Saves'] = pbpcomplete['SOG_A'] - pbpcomplete['Goals_A']
    # add in stats and fancy stats
    pbpcomplete['Shot_Percentage_for'] = round((pbpcomplete['Goals_for'] / pbpcomplete['SOG_for']) * 100, 2)
    pbpcomplete['Fenwick_for'] = pbpcomplete['SOG_for'] + pbpcomplete['Misses']
    pbpcomplete['Corsi_for'] = pbpcomplete['Shot_Att']
    pbpcomplete['Corsi_A'] = pbpcomplete['Shot_Att_A']
    pbpcomplete['Fenwick_A'] = pbpcomplete['Shot_Att_A'] - pbpcomplete['Blocks_for']
    pbpcomplete['FSH%'] = round((pbpcomplete['Goals_for'] / pbpcomplete['Fenwick_for']) * 100, 2)
    pbpcomplete['Miss%'] = round((pbpcomplete['Misses'] / pbpcomplete['Fenwick_for']) * 100, 2)
    pbpcomplete['wshF'] = round(
        (pbpcomplete['Goals_for'] + (0.2 * (pbpcomplete['Corsi_for'] - pbpcomplete['Goals_for']))), 2)
    pbpcomplete['wshA'] = round(
        (pbpcomplete['Goals_A'] + (0.2 * (pbpcomplete['Corsi_A'] - pbpcomplete['Goals_A']))), 2)
    pbpcomplete['Goals_for%'] = round(
        (pbpcomplete['Goals_for'] / (pbpcomplete['Goals_for'] + pbpcomplete['Goals_A'])) * 100, 2)
    pbpcomplete['Fenwick_for%'] = round(
        (pbpcomplete['Fenwick_for'] / (pbpcomplete['Fenwick_for'] + pbpcomplete['Fenwick_A'])) * 100, 2)
    pbpcomplete['Corsi_for%'] = round(
        (pbpcomplete['Corsi_for'] / (pbpcomplete['Corsi_for'] + pbpcomplete['Corsi_A'])) * 100, 2)
    pbpcomplete['wshF%'] = round((pbpcomplete['wshF'] / (pbpcomplete['wshF'] + pbpcomplete['wshA'])) * 100, 2)
    pbpcomplete['Sv%'] = round((pbpcomplete['Saves'] / pbpcomplete['SOG_A']) * 100, 2)

    # and finally to calculate wins. I am going to count ties as a win for now since both teams get a standings point. if it negativly affects the model I'll adjust
    pbpcomplete['Win'] = np.where(np.logical_or(pbpcomplete['Goals_for'] > pbpcomplete['Goals_A'],
                                                  pbpcomplete['Goals_for'] == pbpcomplete['Goals_A']), 1, 0)
    return pbpcomplete
