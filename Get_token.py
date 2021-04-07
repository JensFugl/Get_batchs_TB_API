# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests
import json
import pandas as pd 
from datetime import datetime, timezone
import time


def get_token():
    '''
    Takes username and password and returns JWT token
    '''

    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    
    data = '{"username":"""WRITE_EMAIL""", "password":"""WRITE_PASSWORD"""}'
    response = requests.post('https://dash.zymoscope.com/api/auth/login', headers=headers, data=data)
    
    back = response.json()
    
    JWT_token = 'Bearer {}'.format(back['token'])
    
    return JWT_token



def get_EV_data(entityViewID, JWT_token):
    
    headers = {
        'Content-Type': 'application/json',
        'X-Authorization': JWT_token,
    }
    
    response = requests.get(
    'https://dash.zymoscope.com/api/entityView/{}'.format(entityViewID), headers=headers)
    #print(response.text)
    time1 = response.json()
    
    return time1

def get_EV_from_name(entityViewName, JWT_token):
    
    headers = {
        'Content-Type': 'application/json',
        'X-Authorization': JWT_token,
    }
    
    response = requests.get(
    'https://dash.zymoscope.com/api/tenant/entityViews?entityViewName={}'.format(entityViewName), headers=headers)
    
    #print(response.text)
    entityViewDeviceId = response.json()['entityId']['id']
    entityViewStartTime = response.json()['startTimeMs']
    entityViewEndTime = response.json()['endTimeMs']
    
    return entityViewDeviceId, entityViewStartTime, entityViewEndTime


def get_deviceId(deviceName, JWT_token):
    
    headers = {
        'Content-Type': 'application/json',
        'X-Authorization': JWT_token,
    }
    
    response = requests.get(
    'http://18.185.48.68/api/tenant/devices?deviceName={}'.format(deviceName), headers=headers)
    #print(response.text)
    deviceId = response.json()['id']['id']

    return deviceId


def get_telemetry_keys(deviceName, JWT_token):
    
    #deviceId = get_deviceId(deviceName, JWT_token)
    
    deviceId = deviceName
    
    headers = {
        'Content-Type': 'application/json',
        'X-Authorization': JWT_token,
    }    
    response = requests.get(
    'https://dash.zymoscope.com/api/plugins/telemetry/DEVICE/{}/keys/timeseries'.format(deviceId), headers=headers)
    
    text = response.json()
    
    return text



def get_telemetry_from_EV(entityViewName, JWT_token):

    deviceId, startTime, endTime = get_EV_from_name(entityViewName, JWT_token)

    keys = get_telemetry_keys(deviceId, JWT_token)
    
    keyjoin = ",".join(keys)

    headers = {
        'Content-Type': 'application/json',
        'X-Authorization': JWT_token,
    }
    
    if endTime == 0:
        endTime = round(time.time() * 1000)
    
    response = requests.get(
    'https://dash.zymoscope.com/api/plugins/telemetry/DEVICE/{}/values/timeseries?limit=200000&agg=NONE&useStrictDataTypes=false&keys={}&startTs={}&endTs={}'.format(deviceId, keyjoin, startTime, endTime), headers=headers)

    telemetry = response.json()
    
    df = convert_telemetry(telemetry, keys)
    
    return df



def convert_telemetry(telemetry, keys):

    df1 = pd.json_normalize(telemetry)
    
    ini = keys[1]
    
    df2 = pd.json_normalize(df1.loc[0][ini])
    
    df2 = df2.drop(columns = 'value')
    
    for key in keys:
        
        thing = pd.json_normalize(df1.loc[0][key])
        thing = thing.drop(columns ='ts')
        df2[key] = thing
    df2['DATE']=(pd.to_datetime(df2['ts'],unit='s'))    
    df2.index = df2['DATE']
    df2 = df2.drop(columns=['DATE', 'flowrate_max', 'temperature_sum', 'state', 'flowrate_min',
       'humidity_readings',  'temperature_max',
       'temperature_min', 'temperature_readings', 'humidity_sum',
        'pressure_max', 'flowrate_readings',
       'pressure_min', 'flowrate_sum',  'upload_frequency_sec',
       'humidity_max', 'device_mac', 'humidity_min', 'device_fw',
       'pressure_readings', 'pressure_sum'])
    df2['SG'] = df2['SG'].astype(float)    
    df2['ABV'] = df2['ABV'].astype(float)    
    df2['CO2L'] = df2['CO2L'].astype(float)    
    df2['flowrate_avg'] = df2['flowrate_avg'].astype(float)    
    df2['pressure_avg'] = df2['pressure_avg'].astype(float)    
    df2['temperature_avg'] = df2['temperature_avg'].astype(float)    
    df2['humidity_avg'] = df2['humidity_avg'].astype(float) 
    
    return df2


'''
def convert_telemetry(json_response, deviceName, JWT_token):

    text = json_response
    
    keys = json_response.keys()
    
    
    ABV = []
    SG = []
    v_sum = []
    epoch = []
    Vco2 = []
    avg = []
    count = []
    maxa = []
    mina = []
    suma = []
    

    for itm,i in enumerate(text['SG']):

        flow.append(float(text['avg'][itm]['value']))
        ABV.append(float(text['ABV'][itm]['value']))
        v_sum.append(float(text['sum'][itm]['value']))
        epoch.append(int(text['avg'][itm]['ts']))
        SG.append(float(text['SG'][itm]['value']))
        #rt.append(datetime.fromtimestamp(int(epoch[-1]), timezone.utc))
        
        import numpy as np
        data = (keys)
        keys = np.array(keys)
        df = pd.DataFrame(data, columns = keys)
        #df = df.set_index('epoch')


    return df

def get_telemetry(deviceName, time1, time2, JWT_token):


    entityId = get_deviceId(deviceName, JWT_token)
    
    keys = get_telemetry_keys(deviceName, JWT_token)
    
    keys = ",".join(keys)

    headers = {
        'Content-Type': 'application/json',
        'X-Authorization': JWT_token,
    }
    
    response = requests.get(
    'http://18.185.48.68/api/plugins/telemetry/DEVICE/{}/values/timeseries?limit=200000&agg=NONE&useStrictDataTypes=false&keys={}&startTs={}&endTs={}'.format(entityId, keys, time1, time2), headers=headers)

    text = response.json()

    return text





'''

def datetime_to_unix(time1, time2):
    
    stamp1 = time.strptime(time1, '%Y-%m-%d %H:%M:%S')
    stamp2 = time.strptime(time2, '%Y-%m-%d %H:%M:%S')
    
    epoch1 = int(time.mktime(stamp1)*1000)
    epoch2 = int(time.mktime(stamp2)*1000)

    return epoch1, epoch2
  

