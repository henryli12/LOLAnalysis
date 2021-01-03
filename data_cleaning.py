# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 13:33:42 2021

@author: Henry
"""

import pandas as pd

def calculate_kda(row):
    if row['deaths'] == 0:
        return row['kills'] + row['assists']
    else:
        return (row['kills'] + row['assists']) / row['deaths']

def calculate_per_min(col, row):
    result = row[col] / row['gameDuration'] * 60
    return round(result, 2)

if __name__ == "__main__":
    filename = "players_data.csv"
    outFilename = "cleaned_players_data.csv"
    # columns that that not needed
    columns_to_drop = ['participantId', 'item0', 'item1', 'item2', 'item3', 'item4', 'item5', 
                       'item6', 'unrealKills', 'largestCriticalStrike', 'combatPlayerScore',
                       'objectivePlayerScore', 'totalPlayerScore', 'totalScoreRank',
                       'playerScore0', 'playerScore1', 'playerScore2', 'playerScore3',
                       'playerScore4', 'playerScore5', 'playerScore6', 'playerScore7',
                       'playerScore8', 'playerScore9', 'perk0', 'perk0Var1', 'perk0Var2',
                       'perk0Var3', 'perk1', 'perk1Var1', 'perk1Var2', 'perk1Var3',
                       'perk2', 'perk2Var1', 'perk2Var2', 'perk2Var3', 'perk3', 'perk3Var1',
                       'perk3Var2', 'perk3Var3', 'perk4', 'perk4Var1', 'perk4Var2',
                       'perk4Var3', 'perk5', 'perk5Var1', 'perk5Var2', 'perk5Var3', 'longestTimeSpentLiving',
                       'trueDamageDealtToChampions', 'trueDamageTaken', 'gameMode', 'killingSprees',
                       'sightWardsBoughtInGame']
    # columns to calculate per minute
    calc_per_min = ['totalDamageDealt', 'magicDamageDealt', 'physicalDamageDealt',
       'trueDamageDealt', 'totalDamageDealtToChampions',
       'magicDamageDealtToChampions', 'physicalDamageDealtToChampions', 'totalHeal',
       'totalUnitsHealed', 'damageSelfMitigated', 'damageDealtToObjectives',
       'damageDealtToTurrets', 'totalDamageTaken', 'magicalDamageTaken', 'physicalDamageTaken',
       'goldEarned', 'goldSpent', 'totalMinionsKilled', 'neutralMinionsKilled',
       'neutralMinionsKilledTeamJungle', 'neutralMinionsKilledEnemyJungle']
    
    df = pd.read_csv(filepath_or_buffer=filename, index_col=0)
    # Get rid of data not wanted
    df = df[df['gameMode'] == 'CLASSIC']
    df = df.drop(columns=columns_to_drop, axis=1)
    # Convert all null values to None
    df = df.where(pd.notnull(df), 'N/A')

    # Calculate kda
    df['kda'] = df.apply(lambda row: calculate_kda(row), axis=1)
    # Calculate stats per min
    for col in calc_per_min:
        temp = f"{col}_per_min"
        df[temp] = df.apply(lambda row: calculate_per_min(col, row), axis=1)
    df = df.drop(columns=calc_per_min, axis = 1)
    df.to_csv(outFilename, mode = 'w+')