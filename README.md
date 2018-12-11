# nhl_analysis
## Python package to use to analyze the NHL's play by play data:
I built this package as a way to analyze the data provided by the National Hockey League through their data api service. 

This package was built on code developed [here](https://github.com/josh314/nhl) and refactored to work directly with play-by-play data havested from the NHL API. To get the data I used [Harry Shomer's Hockey-Scraper](https://github.com/HarryShomer/Hockey-Scraper). After you have the csv downloaded, you can run it through the clean.py script on the command line. The output of that script can then be read in and put through the `transform()` function and you will get a complete statistical breakdown of the season by team by game(this will take a minute to run). If you would like to construct your own dataframe, you can leverage the event_filter, and aggregation modules on the clean csv. 

The data folder included in this repo has data harvested from the 2013-2014 season - all games up to 11/30/2018. Each season is in its own csv and can be run through the command line as `python clean.py filename` 

I added an example script to show usage of the `transform()` and `team_goals` functions from the tranform and aggregate modules respectivly. the script takes a minute to run but it shows how the data returns. It should be noted that I used the unlceaned data so the teams were not all formated by the standard NHL three letter code, to ensure you can search by that code run the csv through the clean script first. 
