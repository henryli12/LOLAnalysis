# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 20:13:47 2021

@author: Henry
"""

from riotwatcher import LolWatcher, ApiError
import pandas as pd
import numpy as np
import time
import os

# Add data of one game to a list of all data
def add_to_data(tier, division, match_data, index, all_data):
    for i in range(len(match_data['participants'])):
        player = match_data['participants'][i]
        name = match_data['participantIdentities'][i]['player']['summonerName']
        temp_dict = player['stats'].copy()
        temp_dict['lane'] = player['timeline']['lane']
        temp_dict['role'] = player['timeline']['role']
        temp_dict['champion'] = player['championId']
        temp_dict['spell1'] = player['spell1Id']
        temp_dict['spell2'] = player['spell2Id']
        temp_dict['gameDuration'] = match_data['gameDuration']
        temp_dict['tier'] = tier
        temp_dict['division'] = division
        temp_dict['gameMode'] = match_data['gameMode']
        all_data.append(temp_dict)
        index.append(name)

# Use riot api to get x random summoner names from certain tier
def select_players(tier, division, amount):
    players = watcher.league.entries(region, queue, tier, division)
    chosen_indices = np.random.choice(len(players), amount)
    chosen_names = [players[i]['summonerName'] for i in chosen_indices]
    return chosen_names

# select_players for challenger, grandmaster, and master tier
def select_high_players(tier, amount):
    players = None
    if tier == "CHALLENGER":
        players = watcher.league.challenger_by_queue(region, queue)
    elif tier == "GRANDMASTER":
        players = watcher.league.grandmaster_by_queue(region, queue)
    elif tier == "MASTER":
        players = watcher.league.masters_by_queue(region, queue)
    else:
        return
    chosen_indices = np.random.choice(len(players), amount)
    chosen_names = [players['entries'][i]['summonerName'] for i in chosen_indices]
    return chosen_names

# Get the matches for all the summoners in the list and add needed data to all_data
def get_matches(players, index, all_data):
    matches_list = list()
    for player in players:
        try:
            player = player.replace(" ", "")
            begin_index = np.random.randint(20)
            summoner = watcher.summoner.by_name(region, player)
            matches = watcher.match.matchlist_by_account(
                region=region, encrypted_account_id=summoner['accountId'], 
                begin_index=begin_index,end_index=begin_index+1)
            match = watcher.match.by_id(region, int(matches['matches'][0]['gameId']))
            matches_list.append(match)
        except ApiError as err:
            print(err)
            continue            
    for match in matches_list:
        add_to_data(tier, division, match, index, all_data)      

if __name__ == "__main__":
    api_key = os.environ.get('RIOT_API_KEY')
    watcher = LolWatcher(api_key)
    region = 'na1'
    division_list = ['I', "II", "III", "IV"]
    tier_list = ['DIAMOND', 'PLATINUM', 'GOLD', 'SILVER', 'BRONZE', 'IRON']
    high_tier_list = ['CHALLENGER', 'GRANDMASTER', 'MASTER']
    queue = 'RANKED_SOLO_5x5'
    game_per_division = 5
    filename = "players_data.csv"
    index = list()
    all_data = list()
    start = time.time()
    try:
        for tier in tier_list:
            for division in division_list:
                print(f"{tier} {division}")
                players = select_players(tier, division, game_per_division)
                get_matches(players, index, all_data)
        for tier in high_tier_list:
            print(f"{tier}")
            players = select_high_players(tier, game_per_division)
            get_matches(players, index, all_data)
    except Exception as err:
        print(err)
    matches_df = pd.DataFrame(all_data, index=index)
    try:
        temp = pd.read_csv(filepath_or_buffer=filename, index_col=0)
        cols_format = temp.columns
        matches = matches_df[cols_format]
        matches_df.to_csv(filename, mode='a+', header=False)
    except Exception:
        matches_df.to_csv(filename, mode = 'a+')
    print(time.time() - start)