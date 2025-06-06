import os
import sys
import pyinotify
import soco
from time import sleep
from mail_sender import send_mail_with_photo
import json
import os 
import requests


class SmartHomeNotify:
    def __init__(self):
        def get_home_dir():
            return  os.path.expanduser("~")
        
        self.home_dir = get_home_dir()

        def read_configuration():
            with open(f"{self.home_dir}/alarm_configuration.json", "r") as file:
                return json.load(file)

        configuration = read_configuration()

        self.host = configuration['host']
        self.addresses = configuration['mail_addresses']
        self.alarm_sounds = configuration['alarm_sounds']

    def is_alarm_enabled(self):
        response = requests.get("http://localhost:5000/get_state")
        return response.status_code == 200 and response.json().get("state") == "on"
    
    
    def check_alarm_level(self):
        with open(f"{self.home_dir}/alarm_level") as f:
            return f.read().strip().split('=')[1]

    def play_alarm(self, seconds):
        alarm_level = self.check_alarm_level()
        mp3_file = f"http://{self.host}:8002/{self.alarm_sounds[alarm_level]}"

        try:
            speakers = soco.discover()
            for speaker in speakers:
                if speaker.is_coordinator:
                    speaker.play_uri(mp3_file)
                    # sleep(seconds)
                    # speaker.stop()
        except Exception as e:
            print(e)

class EventHandler(pyinotify.ProcessEvent):
    
    def process_IN_CREATE(self, event):
        file_path = os.path.join(event.path, event.name)
        print(file_path)
        smart_home_notifier = SmartHomeNotify()

        if smart_home_notifier.is_alarm_enabled():
            smart_home_notifier.play_alarm(4)
            for address in smart_home_notifier.addresses:
                send_mail_with_photo(file_path, address)
       
def main(directory):

    if not os.path.isdir(directory):
        print(f"{directory} is not a valid directory.")
        sys.exit(1)
    
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_CREATE
    handler = EventHandler()
    notifier = pyinotify.Notifier(wm, handler)

    wdd = wm.add_watch(directory, mask, rec=True)

    notifier.loop()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python inotify_directory.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.exists(directory):
        print("Directory does not exist.")
        sys.exit(1)

    main(directory)


