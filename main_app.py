# python3 -m flask run
# http://localhost:5000/?uid=000000 (replace 000000 with and existing UID)

import threading
import time

# run flask app 
from app import app

# a class which checks for new data on the jetson
from new_data_grabber import DataGrabber
data_grabber = DataGrabber()

from music_picker import MusicPicker
music_picker = MusicPicker()

def jetscope_data_grabber(delay = 120):        
    while True:
        # check for new data on the jetson
        print("Checking for new data on the JetScope...")
        new_users = data_grabber.check_remote_data()

        if len(new_users) > 0:
            for user in new_users:
                print(f"Converting userID {user} data to music")
                music_picker.data_to_music(user)    
            print(f"New users added: {new_users}")
        
        else:
            print("No new data on the JetScope")
        
        time.sleep(delay)

# check for new data on the jetson every X seconds
data_grab = threading.Thread(target=jetscope_data_grabber, args=(180,))
data_grab.start()
