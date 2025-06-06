#!/usr/bin/python

from solaredge import Solaredge
from influxdb import InfluxDBClient
from datetime import datetime, timedelta
from time import sleep


sleep(240)

MINUTES_SLEEP = 20
SIZE_ID = "SOLAREDGE_SITE_ID"

solaredge_client = Solaredge("")
client = InfluxDBClient(host='IPADRESS', port=8086)
#client.create_database('solaredge')

def get_current_consumption_and_production():
    try:
        dictio = solaredge_client.get_current_power_flow(SIZE_ID)
        power_flow = dictio['siteCurrentPowerFlow']

        # print(str(power_flow['PV']['currentPower']) + " " + str(power_flow['LOAD']['currentPower']))
        return power_flow['PV']['currentPower'], power_flow['LOAD']['currentPower']

    except:
        print('couldnt connect to solaredge api')
        return 0.0, 0.0



client.switch_database('solaredge')

while True:
    production, consumption = get_current_consumption_and_production()

    json_body = [
        {
            "measurement": "pannels",
            #"time": datetime.now() - timedelta(hours=2),
            "time": datetime.now() - timedelta(hours=3),
            "fields": {
                "consmption": consumption,
                "production": production
            }
        }
    ]
    
    client.write_points(json_body)
    sleep(60 * MINUTES_SLEEP)

