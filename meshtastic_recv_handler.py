import meshtastic
import meshtastic.serial_interface
import time
import meshtastic
from pubsub import pub
import soco
from time import sleep
from influxdb import InfluxDBClient
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)


MINUTES_SLEEP = 5

client = InfluxDBClient(host='$IPADDRESS', port=8086)
client.switch_database('meshtastic')

def onReceive(packet, interface):
    try:
        pac = packet['decoded']['telemetry']

        if pac.get('environmentMetrics'):
            logging.info(pac['environmentMetrics'])
            json_body = [{
                    "measurement": "traffic",
                    "time": datetime.now() - timedelta(hours=3),
                    # "time": datetime.now(),
                    "fields": {
                        "temperature": pac['environmentMetrics']['temperature']
                    }}]
            client.write_points(json_body)

        logging.debug('got regular packet')
        logging.debug(datetime.now() ) 


    except AttributeError as e:
        print("Attribute Error")
    except KeyError:
        print('KeyError')

        
def onConnection(interface, topic=pub.AUTO_TOPIC):
    logging.debug("connected!")

pub.subscribe(onReceive, "meshtastic.receive")
pub.subscribe(onConnection, "meshtastic.connection.established")


interface = meshtastic.serial_interface.SerialInterface()
while True:
    time.sleep(MINUTES_SLEEP * 60)
