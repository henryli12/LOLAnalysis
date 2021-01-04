# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 13:33:42 2021

@author: Henry
"""

import pandas as pd
import json

def calculate_kda(row):
    if row['deaths'] == 0:
        return row['kills'] + row['assists']
    else:
        return round((row['kills'] + row['assists']) / row['deaths'], 2)

def calculate_per_min(col, row):
    result = row[col] / row['gameDuration'] * 60
    return round(result, 2)

def get_lane(row):
    lane = row['lane']
    role = row['role']
    if lane == "BOTTOM" and role == "DUO_CARRY":
        return "ADC"
    elif lane == "BOTTOM" and role == "DUO_SUPPORT":
        return "SUPPORT"
    elif lane == "BOTTOM":
        return "BOTTOM"
    elif lane == "JUNGLE":
        return "JUNGLE"
    elif lane == "TOP":
        return "TOP"
    elif lane == "MIDDLE":
        return "MIDDLE"
    else:
        return "MISSING"

if __name__ == "__main__":
    filename = "data/players_data.csv"
    champFile = "json/id_to_champion.json"
    sumFile = "json/id_to_summoner.json"
    outFilename = "data/cleaned_players_data.csv"
    with open(champFile, encoding="utf8") as f:
        champion = json.load(f)
    with open(sumFile, encoding="utf8") as f:
        summoner = json.load(f)
    needed_cols = ['win', 'kills', 'deaths', 'assists', 'largestKillingSpree',
                   'largestMultiKill', 'doubleKills', 'tripleKills', 'quadraKills',
                   'pentaKills', 'visionScore', 'timeCCingOthers', 'turretKills',
                   'inhibitorKills', 'totalTimeCrowdControlDealt', 'champLevel',
                   'visionWardsBoughtInGame', 'wardsPlaced', 'wardsKilled',
                   'firstBloodKill', 'firstBloodAssist', 'firstTowerKill',
                   'firstTowerAssist', 'firstInhibitorKill', 'firstInhibitorAssist',
                   'gameDuration', 'tier', 'division'] 
    # columns to calculate per minute
    calc_per_min = ['totalDamageDealt', 'magicDamageDealt', 'physicalDamageDealt',
       'trueDamageDealt', 'totalDamageDealtToChampions',
       'magicDamageDealtToChampions', 'physicalDamageDealtToChampions', 'totalHeal',
       'totalUnitsHealed', 'damageSelfMitigated', 'damageDealtToObjectives',
       'damageDealtToTurrets', 'totalDamageTaken', 'magicalDamageTaken', 'physicalDamageTaken',
       'goldEarned', 'goldSpent', 'totalMinionsKilled', 'neutralMinionsKilled',
       'neutralMinionsKilledTeamJungle', 'neutralMinionsKilledEnemyJungle']

    
    df = pd.read_csv(filepath_or_buffer=filename, index_col=0)
    # Keep data only for classic game mode
    df = df[df['gameMode'] == 'CLASSIC']
    # Convert all null values to False
    df = df.where(pd.notnull(df), False)
    
    out_df = df[needed_cols].copy()
    # Calculate kda, stats per min, and get lane
    out_df['champion'] = df['champion'].apply(lambda x: champion[str(x)])
    out_df['spell1'] = df['spell1'].apply(lambda x: summoner[str(x)])
    out_df['spell2'] = df['spell2'].apply(lambda x: summoner[str(x)])
    out_df['kda'] = df.apply(lambda row: calculate_kda(row), axis=1)
    for col in calc_per_min:
        temp = f"{col}_per_min"
        out_df[temp] = df.apply(lambda row: calculate_per_min(col, row), axis=1)
    out_df['lane'] = df.apply(lambda row: get_lane(row), axis=1)
    
    out_df.to_csv(outFilename, mode = 'w+')