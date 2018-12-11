# nhl_analysis
Python package to use to analyze the NHL's play by play data
This package was built on code developed [here](https://github.com/josh314/nhl) and refactored to work directly with play-by-play data havested from the NHL API. To get the data I used [Harry Shomer's Hockey-Scraper](https://github.com/HarryShomer/Hockey-Scraper) once you have the csv downloaded, you can run it through the clean.py script on the command line. The output of that script can then be read in and put through the `transform()` function and you will get a complete statistical breakdown of the season by team by game(this will take a minute to run). If you would like to construct your own dataframe, you can leverage the event_filter, and aggregation modules on the clean csv. 

The data folder included in this repo has data harvested from the 2013-2014 season - all games up to 11/30/2018. Each season is in its own csv and can be run through the command line as `python clean.py filename` 
