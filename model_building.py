# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 19:40:32 2021

@author: Henry
"""

import pandas as pd
import numpy as np
import time

if __name__ == "__main__":
    filename = 'data/cleaned_players_data.csv'
    df = pd.read_csv(filepath_or_buffer=filename, index_col=0)
    
    df_model = df[['win', 'visionScore', 'turretKills',
                'inhibitorKills', 'wardsPlaced', 'wardsKilled',
                'kda', 'totalDamageDealt_per_min', 'totalDamageDealtToChampions_per_min',
                'damageSelfMitigated_per_min', 'damageDealtToObjectives_per_min',
                'totalDamageTaken_per_min', 'goldEarned_per_min',
                'goldSpent_per_min', 'totalMinionsKilled_per_min',
                'neutralMinionsKilled_per_min']]
    df_dum = pd.get_dummies(df_model)
    
    from sklearn.model_selection import train_test_split
    
    x = df_dum.drop('win', axis=1)
    y = df_dum['win'].values
        
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
    
    from sklearn.linear_model import LinearRegression, LogisticRegression, Lasso
    from sklearn.model_selection import cross_val_score
    
    linreg = LinearRegression()
    linreg.fit(x_train, y_train)
    print('linear regression--------------------------------------')
    print(linreg.predict(x_test[:5]))
    print(np.mean(cross_val_score(linreg, x_train, y_train, cv= 3)))
    
    logreg = LogisticRegression(random_state=0, max_iter=10000)
    logreg.fit(x_train, y_train)
    print("logistic regression------------------------------------")
    print(logreg.predict_proba(x_test[:5])[:,1])
    print(np.mean(cross_val_score(logreg, x_train, y_train, cv= 3)))

    from sklearn.ensemble import RandomForestRegressor
    rf = RandomForestRegressor(random_state=0)
    rf.fit(x_train, y_train)
    print('random forest------------------------------------------')
    print(rf.predict(x_test[:5]))
    print(np.mean(cross_val_score(rf,x_train,y_train, cv= 3)))