# SmartHome
This is my private smart home monitoring and controlling various  smart hardware in my house.


These scripts run at the start of my raspberry pi, using the the ProcessCheckerApp binary (see aditional repo ProccessChecker)

explanation of each file:

inotify.py -> this is a python script using inotify monitoring a directory given as an argument. the script monitors a local FTP server whos input is comming from camera footages recognizing humans in my yard, once a new photo is being added it will send an email to all recepians and set an alarm (low/critical) depends on the configuration.

mail_sender -> a python script that read its configuration and send mail to all resepians from the configuration.

meshtastic_recv_handler.py -> a script subscribing to a meshtastic (open source communication protocol LoRa based) and fetting the sensor data (temperature and humidity) of my water heating boiler. once a new sample has arived it will write the new measuremnet into influxDB in order to seee it a a grfana dashboard.

solar_monitor_grafana.py -> a script using solaredge API inorder to get the production and cunsumption level of my solar system on the roof. once got that measurements -> write it to the INfluxDB. 




