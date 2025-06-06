# SmartHome
This is my private smart home monitoring and controlling various  smart hardware in my house.


These scripts run at the start of my raspberry pi, using the the ProcessCheckerApp binary - that keep them alive at all cost (see additional repo ProcessChecker)

explanation of each file:

inotify.py -> this is a python script using inotify monitoring a directory given as an argument. The script monitors a local FTP server whose input is coming from camera footage recognizing humans in my yard. Once a new photo is being added it will send an email to all recipients and set an alarm (low/critical) depending on the configuration.

mail_sender -> a python script that reads its configuration and sends mail to all recipients from the configuration.

meshtastic_recv_handler.py -> a script subscribing to a meshtastic (open source communication protocol LoRa based) and getting the sensor data (temperature and humidity) of my water heating boiler. Once a new sample has arrived it will write the new measurement into influxDB in order to see it in a grafana dashboard.

solar_monitor_grafana.py -> a script using solaredge API in order to get the production and consumption level of my solar system on the roof. once got that measurement -> write it to the INfluxDB.

 




