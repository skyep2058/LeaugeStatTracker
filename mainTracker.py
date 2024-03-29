LuckyFin
#1835

Luckyfin — Today at 1:52 AM
new code 8/23/21 at 1:52am MST
from riotwatcher import LolWatcher, ApiError
import pandas as pd
import pprint
import json


Expand
message.txt
7 KB
﻿
from riotwatcher import LolWatcher, ApiError
import pandas as pd
import pprint
import json


# Dependencies to identify me/API key
lol_watcher = LolWatcher('RGAPI-08ea6e49-e687-4925-abd5-341c32fdff78')                      # RIOT API KEY
my_region = 'na1'                                                                           # Define Region
me = lol_watcher.summoner.by_name(my_region, 'LuckyFin')                                    # Throw error if name is wrong
my_matches = lol_watcher.match.matchlist_by_account(my_region, me['accountId'])             # Limit is 100, can index more
static_champ_list = lol_watcher.data_dragon.champions(game_version, False, 'en_US')         # Latest game version


# Throw Errors
try:
    response = lol_watcher.summoner.by_name(my_region, 'LuckyFin')
except ApiError as err:
    if err.response.status_code == 429:                                                 # Throw for rate limiting error
        print('We should retry in {} seconds.'.format(err.headers['Retry-After']))
        print('this retry-after is handled by default by the RiotWatcher library')
        print('future requests wait until the retry-after time passes')
    elif err.response.status_code == 404:                                               # Throw for not finding summoner error
        print('Summoner with that ridiculous name not found.')
    else:
        raise


# Get match info API's
match0 = my_matches['matches'][0]                                       # Most recent match
match_detail0 = lol_watcher.match.by_id(my_region, match0['gameId'])    # Details of the match
gameDuration = match_detail0['gameDuration']                            # Declare and define the game duration (seconds)
gameMode = match_detail0['gameMode']
queueId = match_detail0['queueId']


# Variables
grid = []                                                               # Declare a list for our dataframe
statDict = {}                                                           # Declare a dictionary of statistics
participantId = ""
summonerName = ""


# Find the Summoner name
for identity in match_detail0['participantIdentities']:
    if "LuckyFin" in identity['player']['summonerName']:
        participantId = identity['participantId']
        summonerName = identity['player']['summonerName']
    else:
        pass


# Add the stats of the player to the dataframe
for player in match_detail0['participants']:
    if player['participantId'] == participantId:
        statDict['Player'] = summonerName
        championId = player['championId']
        statDict['Champion'] = championId

        statDict['Queue Type'] = queueId
        statDict['Game Mode'] = gameMode
        statDict['Win/Lost'] = player['stats']['win']
        if statDict['Win/Lost'] == True:
            statDict['Win/Lost'] = 'Win'
        else:
            statDict['Win/Lost'] = 'Lost'
        statDict['Kills'] = player['stats']['kills']
        statDict['Deaths'] = player['stats']['deaths']
        statDict['Assists'] = player['stats']['assists']
        if statDict['Deaths'] == 0:
            statDict['KDA'] = (player['stats']['kills'] + player['stats']['assists']) / 1
        else:
            statDict['KDA'] = (player['stats']['kills'] + player['stats']['assists']) / player['stats']['deaths']
        statDict['Avg CS/Min'] = (player['stats']['totalMinionsKilled'] / (gameDuration / 60))
        statDict['Vision Score'] = player['stats']['visionScore']
        statDict['Wards Placed'] = ((player['stats']['visionWardsBoughtInGame']) + (player['stats']['sightWardsBoughtInGame']))
        grid.append(statDict)
    else:
        pass
df = pd.DataFrame(grid)


# This will make a dictionary of the champions and their number
champ_dict = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    champ_dict[row['key']] = row['id']
    #print(dict_of_values['id'])                                 # This will print out the Champion names
    #print(dict_of_values['key'])                                # This will print out the champion ID number
    #print(champ_dict[row['key']])                               # This will display the names of the champions
#print(champ_dict)                                               # This will print the dictionary


# This will change the champion numbers to actual names in the Dataframe.
for row in grid:
    row['Champion'] = champ_dict[str(row['Champion'])]
df = pd.DataFrame(grid)


# This json file contains the league game ID's and their descriptions
# Get the json file from:   https://static.developer.riotgames.com/docs/lol/queues.json


#f = open('/Users/luckyfin/Desktop/queues.json')                     # Open on skyes mac
f = open('C:/Users/Peterson/Desktop/queues.json')                           # Open on skyes PC
queueId_dict = {}
data = json.load(f)


# This converts the queueId to the Queue Description in the json file
for key in data:
    # print(key['queueId'])                               # This will print the ID's of each game (a int)
    # print(key['description'])                           # This will print the game selection (a str)
    for row in grid:
        if row['Queue Type'] == key['queueId']:
            row['Queue Type'] = key['description']
        else:
            pass
df = pd.DataFrame(grid)


# Print what we have in our dataframe to see the outcome!
pprint.pp(df)


# Lastly, pretty print the files and write to an EXCEL sheet
#df.to_csv('/Users/luckyfin/PycharmProjects/LeagueStatTracker.csv')         # FOR MAC
df.to_csv('C:/Users/Peterson/Desktop/LeagueStatTracker.csv')                # FOR PC
f.close()














            # OTHER STUFF




# We will need this to determine rank
# This call will return my ranked stats in Flex and Solo queue, total overall games played, and some special ID's
# my_ranked_stats = lol_watcher.league.by_summoner(my_region, me['id'])
# print(my_ranked_stats)





# seasonId = match_detail0['seasonId']
# gameType = match_detail0['gameType']
# I ALSO WANT GAME DURATION, SEASON NUMBER, PLATFORM (NA/EU), GAMEMODE (URF/RANKED SOLO)
# I ALSO WANT TO CENTER EVERYTHING IN THE DATAFRAME AND IF POSSIBLE ADJUST FONT ON TITLES
# not a huge deal though because we can create a tool that queries that data and then does these changes
