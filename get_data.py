# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 14:01:36 2020

@author: Jens Ringsholm
"""

from Get_token import get_token, get_telemetry_from_EV


###########  get token

JWT_token = get_token()

############## Choose Entity view from name

entityViewName = "Emotional Support - final\t\t\t"


# get telemetry and store in dataframe

df = get_telemetry_from_EV(entityViewName, JWT_token)


# save dataframe as pkl file

df.to_pickle('data/lol.pkl')
