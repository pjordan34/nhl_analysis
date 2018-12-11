import pandas as pd
from aggregate import team_goals
from transform import transform

pbp = pd.read_csv('data/nhl_pbp20172018.csv')

# note that you can use the "uncleaned pbp files in this code,
# you just will not be able to index on the the standard three-letter abbreviations for all teams
print(team_goals(pbp))


pbp = transform(pbp)

print(pbp.head())