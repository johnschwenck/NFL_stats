# %%
import sys
import os
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from urllib import request
import requests
import zipfile, io
from pathlib import Path
from datetime import datetime
import glob
import math



# %%
# List of all team abbreviations per Pro Football Reference
def team_info():
    team_info = {
        'ari' : {
            "common": "ARI", 
            "full": "Arizona Cardinals", 
            "last": "Cardinals", 
            "first": "Arizona", 
            "PFR_key": "crd",
            "conf":'NFC',
            "div":'West'
        },

        'atl' : { 
            "common": "ATL",
            "full": "Atlanta Falcons",
            "last": "Falcons",
            "first": "Atlanta",
            "PFR_key": "atl",
            "conf":'NFC',
            "div":'South'
        },

        'bal' : {
            "common": "BAL",
            "full": "Baltimore Ravens",
            "last": "Ravens",
            "first": "Baltimore",
            "PFR_key": "rav",
            "conf":'AFC',
            "div":'North'
        },

        'buf' : {
            "common": "BUF",
            "full": "Buffalo Bills",
            "last": "Bills",
            "first": "Buffalo",
            "PFR_key": "buf",
            "conf":'AFC',
            "div":'East'
        },

        'car' : {
            "common": "CAR",
            "full": "Carolina Panthers",
            "last": "Panthers",
            "first": "Carolina",
            "PFR_key": "car",
            "conf":'NFC',
            "div":'South'
        },

        'chi' : {
            "common": "CHI",
            "full": "Chicago Bears",
            "last": "Bears",
            "first": "Chicago",
            "PFR_key": "chi",
            "conf":'NFC',
            "div":'North'
        },

        'cin' : {
            "common": "CIN",
            "full": "Cincinnati Bengals",
            "last": "Bengals",
            "first": "Cincinnati",
            "PFR_key": "cin",
            "conf":'AFC',
            "div":'North'
        },

        'cle' : {
            "common": "CLE",
            "full": "Cleveland Browns",
            "last": "Browns",
            "first": "Cleveland",
            "PFR_key": "cle",
            "conf":'AFC',
            "div":'North'
        },

        'dal' : {
            "common": "DAL",
            "full": "Dallas Cowboys",
            "last": "Cowboys",
            "first": "Dallas",
            "PFR_key": "dal",
            "conf":'NFC',
            "div":'East'
        },

        'den' : {
            "common": "DEN",
            "full": "Denver Broncos",
            "last": "Broncos",
            "first": "Denver",
            "PFR_key": "den",
            "conf":'AFC',
            "div":'West'
        },

        'det' : {
            "common": "DET",
            "full": "Detroit Lions",
            "last": "Lions",
            "first": "Detroit",
            "PFR_key": "det",
            "conf":'NFC',
            "div":'North'
        },

        'gbp' : {
            "common": "GB",
            "full": "Green Bay Packers",
            "last": "Packers",
            "first": "Green Bay",
            "PFR_key": "gnb",
            "conf":'NFC',
            "div":'North'
        },

        'hou' : {
            "common": "HOU",
            "full": "Houston Texans",
            "last": "Texans",
            "first": "Houston",
            "PFR_key": "htx",
            "conf":'AFC',
            "div":'South'
        },

        'ind' : {
            "common": "IND",
            "full": "Indianapolis Colts",
            "last": "Colts",
            "first": "Indianapolis",
            "PFR_key": "clt",
            "conf":'AFC',
            "div":'South'
        },

        'jax' : {
            "common": "JAX",
            "full": "Jacksonville Jaguars",
            "last": "Jaguars",
            "first": "Jacksonville",
            "PFR_key": "jax",
            "conf":'AFC',
            "div":'South'
        },

        'kcc' : {
            "common": "KCC",
            "full": "Kansas City Chiefs",
            "last": "Chiefs",
            "first": "Kansas City",
            "PFR_key": "kan",
            "conf":'AFC',
            "div":'West'
        },

        'lac' : {
            "common": "LAC",
            "full": "Los Angeles Chargers",
            "last": "Chargers",
            "first": "Los Angeles",
            "PFR_key": "sdg",
            "conf":'AFC',
            "div":'West'
        },

        'lar' : {
            "common": "LAR",
            "full": "Los Angeles Rams",
            "last": "Rams",
            "first": "Los Angeles",
            "PFR_key": "ram",
            "conf":'NFC',
            "div":'West'
        },

        'mia' : {
            "common": "MIA",
            "full": "Miami Dolphins",
            "last": "Dolphins",
            "first": "Miami",
            "PFR_key": "mia",
            "conf":'AFC',
            "div":'East'
        },

        'vik' : {
            "common": "MIN",
            "full": "Minnesota Vikings",
            "last": "Vikings",
            "first": "Minnesota",
            "PFR_key": "min",
            "conf":'NFC',
            "div":'North'
        },

        'nep' : {
            "common": "NE",
            "full": "New England Patriots",
            "last": "Patriots",
            "first": "New England",
            "PFR_key": "nwe",
            "conf":'AFC',
            "div":'East'
        },

        'nos' : {
            "common": "NO",
            "full": "New Orleans Saints",
            "last": "Saints",
            "first": "New Orleans",
            "PFR_key": "nor",
            "conf":'NFC',
            "div":'South'
        },

        'nyg' : {
            "common": "NYG",
            "full": "New York Giants",
            "last": "Giants",
            "first": "New York",
            "PFR_key": "nyg",
            "conf":'NFC',
            "div":'East'
        },

        'nyj' : {
            "common": "NYJ",
            "full": "New York Jets",
            "last": "Jets",
            "first": "New York",
            "PFR_key": "nyj",
            "conf":'AFC',
            "div":'East'
        },

        'oak' : {
            "common": "OAK",
            "full": "Oakland Raiders",
            "last": "Raiders",
            "first": "Oakland",
            "PFR_key": "rai",
            "conf":'AFC',
            "div":'West'
        },

        'phi' : {
            "common": ["PHI","PHL"],
            "full": "Philadelphia Eagles",
            "last": "Eagles",
            "first": "Philadelphia",
            "PFR_key": "phi",
            "conf":'NFC',
            "div":'East'
        },

        'pit' : {
            "common": "PIT",
            "full": "Pittsburgh Steelers",
            "last": "Steelers",
            "first": "Pittsburgh",
            "PFR_key": "pit",
            "conf":'AFC',
            "div":'North'
        },

        'sf' : {
            "common": "SF",
            "full": "San Francisco 49ers",
            "last": "49ers",
            "first": "San Francisco",
            "PFR_key": "sfo",
            "conf":'NFC',
            "div":'West'
        },

        'sea' : {
            "common": "SEA",
            "full": "Seattle Seahawks",
            "last": "Seahawks",
            "first": "Seattle",
            "PFR_key": "sea",
            "conf":'NFC',
            "div":'West'
        },

        'tbb' : {
            "common": "TBB",
            "full": "Tampa Bay Buccaneers",
            "last": "Buccaneers",
            "first": "Tampa Bay",
            "PFR_key": "tam",
            "conf":'NFC',
            "div":'South'
        },

        'ten' : {
            "common": "TEN",
            "full": "Tennessee Titans",
            "last": "Titans",
            "first": "Tennessee",
            "PFR_key": "oti",
            "conf":'AFC',
            "div":'South'
        },

        'was' : {
            "common": "WAS",
            "full": "Washington Redskins",
            "last": "Redskins",
            "first": "Washington",
            "PFR_key": "was",
            "conf":'NFC',
            "div":'East'
        }
    }

    return team_info



# %%

# Example of how to iterate through the above dictionary:
tmp = team_info() # assign function to an object
print( tmp.keys() ) # show all keys of dictionary
print( list(tmp.keys()) ) # puts all keys into an iterable list
print( list(tmp.keys())[0] ) # extracts first element of the list 
print( tmp[list(tmp.keys())[0]] ) # if we want to locate information for a specific key, we include the above line as the key for the original tmp dictionary
print( tmp[list(tmp.keys())[0]]['PFR_key'] ) # we can then extract specific information for that key (team)

for item in range(len(list(tmp))):
    print( tmp[list(tmp.keys())[item]]['PFR_key'] ) # lists all of the Pro Football Reference HTML team references
# i.e. https://www.pro-football-reference.com/teams/was/



# %%
# Scrape Injuries
def injuries():
    URL = 'https://www.pro-football-reference.com/players/injuries.htm'
    resp = request.urlopen(URL)
    soup = BeautifulSoup(resp, 'html.parser')

    injuries = []

    # Player
    row = soup.find_all('th')
    for rows in row:
        injuries.append(rows.get_text())
    injuries = pd.DataFrame(injuries)
    injuries.columns = injuries.iloc[0]
    injuries = injuries.iloc[6:,]
    injuries = injuries.reset_index(drop=True)

    # Injury Report
    append_report = []
    row = soup.find_all('td')
    for rows in row:
        append_report.append(rows.get_text())
    append_report = np.reshape(append_report, (int(len(append_report)/5),5))
    append_report = pd.DataFrame(append_report)
    append_report = append_report.reset_index(drop=True)

    injuries = pd.concat([injuries,append_report], axis=1)#.reset_index(drop=True, inplace=True)
    injuries.columns = ['Player','Team','Pos','Type of Injury','Status','Details']
   
    return injuries

# testinj = injuries()
 #testinj.loc[testinj['Team'] == 'NYG'] # see all injuries for a given team
# Alternatively: testinj[testinj['Team']=='NYG']

# %%
# Scrape Transactions
def NFL_transactions():

    #month = 

    URL = 'https://www.pro-football-reference.com/years/2020/08_transactions.htm'
    resp = request.urlopen(URL)
    soup = BeautifulSoup(resp, 'html.parser')
    
    trans = []
    rows = soup.find_all('p')
    for lines in rows:
        trans.append(lines.get_text())
    return trans



# %%
# 2020 Season Schedule
def schedule(teamname = None):
    
    URL = 'https://www.pro-football-reference.com/years/2020/games.htm'
    resp = request.urlopen(URL)
    soup = BeautifulSoup(resp, 'html.parser')

    sched = []
    row = soup.find_all('td')
    for rows in row:
        sched.append(rows.get_text())
    sched = pd.DataFrame(np.reshape(sched, (int(len(sched)/8),8)))

    week = []
    row = soup.find_all('th')
    for rows in row:
        week.append(rows.get_text())
    header = week[0:9]
    week = pd.DataFrame(week)[-pd.DataFrame(week).isin(header)].dropna().reset_index(drop=True)

    sched = pd.concat([week, sched], axis = 1)
    sched.columns = ['Week', 'Day', 'Date', 'Away', 'Away_Pts', '@', 'Home', 'Home_Pts', 'Time']
    sched.set_index('Week', drop=False)

    sched = sched[~sched['Week'].isin(['Pre0','Pre1', 'Pre2', 'Pre3', 'Pre4'])] # Remove Preseason games
    sched = sched.reset_index(drop=True)

    if teamname is not None:
            try:
                if teamname.upper() == team_info()[teamname]['common']:
                    lookup_team = team_info()[teamname]['full']
                    sched = sched[(sched['Home'] == lookup_team) | (sched['Away'] == lookup_team)]
                    sched['Opp'] = np.where(sched.Away == team_info()[teamname]['full'], sched.Home,sched.Away)
            except:
                print("Invalid team abbreviation. Input does not exist. Please try again.")
                teamname = input("Team Abbreviation:")
                lookup_team = team_info()[teamname.lower()]['full']
                sched = sched[(sched['Home'] == lookup_team) | (sched['Away'] == lookup_team)]
                sched['Opp'] = np.where(sched.Away == team_info()[teamname]['full'], sched.Home,sched.Away)
    
    return sched

#test = schedule()
#test = schedule('nyg')


# %%
# Team Stats
def team_stats(team = None, year = None):
    team_dict = team_info()
    if team is None:
        team = input('Enter 3 letter abbreviation for team (i.e. "was" for Washington)')
        team = str(team_dict[team]['PFR_key'])
    else:
        #team_info = team_info()
        team = str(team_dict[team]['PFR_key'])

    if year is None:
        year = 2019
    
    # Add team stats to dictionary:
    team_URL = 'https://www.pro-football-reference.com/teams/' + team + '/' + str(year) + '.htm'
    teamstats = pd.read_html(team_URL)
    teamstats_dict = {}
    for j in range(len(teamstats)):
        teamstats_dict["stats_{0}".format(j)] = pd.DataFrame(teamstats[j])






    # Add Roster information to dictionary:
    #roster_URL = 'https://www.pro-football-reference.com/teams/' + team + '/' + str(year) + '_roster.htm'
    #roster = pd.read_html(roster_URL)
    #roster = pd.DataFrame(roster[0])
    #roster['Pos Type'] = x # Fix this
    
    #teamstats_dict['roster'] = roster




    def depth_chart(teamname = None):
        # Depth Chart
        depth_URL = 'https://www.espn.com/nfl/team/depth/_/name/' + teamname
        depth = pd.read_html(depth_URL)
        depth[0].columns = ['Pos']

        depth[0].loc[len(depth[0])+1] = 0
        depth[0] = depth[0].shift(periods = 1)
        depth[0] = depth[0].replace(np.nan, "QB")
        off_depth = pd.concat([depth[0].reset_index(drop = True),depth[1]], axis = 1)

        depth[2].loc[len(depth[2])+1] = 0
        depth[2] = depth[2].shift(periods = 1)
        depth[2] = depth[2].replace(np.nan, "LDE")
        def_depth = pd.concat([depth[2].reset_index(drop = True),depth[3]], axis = 1)

        depth[4].loc[len(depth[4])+1] = 0
        depth[4] = depth[4].shift(periods = 1)
        depth[4] = depth[4].replace(np.nan, "PK")
        st_depth = pd.concat([depth[4].reset_index(drop = True),depth[5]], axis = 1)

        return [off_depth, def_depth, st_depth]
    
    depth_chart = depth_chart(team)

    # For reference in dictionary:
    # stats_0: Team Stats & Rankings
    # stats_1: Schedule & Game Results
    # stats_2: Team Conversions
    # roster: Team Roster
    

    return [teamstats_dict, depth_chart]

# tmp = team_stats()
# tmp['roster'] # display roster
# tmp['stats_0'] # Team Stats & Rankings

# %%

"""     # Advanced Stats
    adv_URL = 'https://www.pro-football-reference.com/teams/' + team + '/' + str(year) + '_advanced.htm'
    advstats = pd.read_html(team_URL)
    advstats_dict = {}
    pd.read_html('//*[@id="advanced_defense"]/tbody/tr[1]')

    import lxml.html as LH
    url = 'https://www.espn.com/nfl/stats/player/_/view/defense/table/defensiveInterceptions/sort/interceptions/dir/desc'
    r = requests.get(url)
    root = LH.fromstring(r.content)
    
    for table in root.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "Table2__title--remove-capitalization", " " ))]'):
        header = [text(th) for th in table.xpath('//th')]        # 1
        data = [[text(td) for td in tr.xpath('td')]  
                for tr in table.xpath('//tr')]                   # 2
        data = [row for row in data if len(row)==len(header)]    # 3 
        data = pd.DataFrame(data, columns=header)                # 4
        print(data)  """

# %%
pd.read_html('https://www.pro-football-reference.com/teams/nyg/2019_roster.htm')
# %%
import nflgame
nflgame.one(2011,17,"NE", "BUF")
# %%
