# run flask app 
from app import app

# a class which checks for new data on the jetson
from new_data_grabber import DataGrabber
data_grabber = DataGrabber()

from music_picker import MusicPicker
music_picker = MusicPicker()

# check for new data on the jetson
print("loading...")
new_users = data_grabber.check_remote_data()
print(f"New users added: {new_users}")
if len(new_users) > 0:
    for user in new_users:
        print(f"Converting userID {user} data to music")
        music_picker.data_to_music(user)
