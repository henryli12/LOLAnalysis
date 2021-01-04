# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 20:42:04 2021

@author: Henry
"""

import json

if __name__ == "__main__":
    with open('json/champion.json', encoding="utf8") as f:
        data = json.load(f)
    champions = dict()
    for champ in data['data']:
        champions[data['data'][champ]['key']] = champ
    with open('json/id_to_champion.json', 'w') as f:
        json.dump(champions, f)
    
    with open('json/summoner.json', encoding="utf8") as f:
        data = json.load(f)
    summoners = dict()
    for summoner in data['data']:
        summoners[data['data'][summoner]['key']] = data['data'][summoner]['name']
    summoners['0'] = 'None'
    with open('json/id_to_summoner.json', 'w') as f:
        json.dump(summoners, f)