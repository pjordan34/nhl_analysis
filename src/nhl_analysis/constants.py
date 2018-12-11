
################### Player id ################################

# A placeholder value indicating no player, e.g. to indicate
# pulled goalie
NOPLAYER = 'xxxxxxxNA'

########################### GCODE ##############################

# Each game of a season is assigned a unique 'Game_Id' number. The
# regular season games are between 20000 & 30000 and playoff games
# are over 30000

SEASON_START = 20000
PLAYOFFS_START = 30000
 
#################################################################

######################## Player columns #########################

# Use these arrays to grab all the columns for the home or away
# team in the pbp event data. They include include spots for a 6th
# attacker if the goalie is pulled. Note that at least one of the
# columns in each array will be NaN for every event because of this.


HOME_PLAYERS = ['homePlayer1','homePlayer2','homePlayer3','homePlayer4','homePlayer5','homePlayer6','Home_Goalie']
AWAY_PLAYERS = ['awayPlayer1','awayPlayer2','awayPlayer3','awayPlayer4','awayPlayer5','awayPlayer6','Away_Goalie']

# Same as above but without the goalies. 
HOME_SKATERS = ['homePlayer1','homePlayer2','homePlayer3','homePlayer4','homePlayer5','homePlayer6']
AWAY_SKATERS = ['awayPlayer1','awayPlayer2','awayPlayer3','awayPlayer4','awayPlayer5','awayPlayer6']