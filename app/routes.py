from flask import render_template, request
from app import app
import os
import glob


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    UUID = request.args.get("uid") #"FCB89A"
    caps_img_dir = 'app/static/caps_img/'
    
    #check for new user folders and add their UID to the autocomplete list 
    UID_LIST = [ name for name in os.listdir(caps_img_dir) if os.path.isdir(os.path.join(caps_img_dir, name)) ]
    
    pan_img = glob.glob(caps_img_dir + UUID + "/"+ "*.png")[0].split('/')[-1]

    
    AUD = "000.mp3"
    with open(f"{caps_img_dir}{UUID}/{UUID}.txt", "r") as txtfile:
        AUD = f"{txtfile.read()}.mp3"
        print(AUD)
        
    
    
    # print(UID_LIST)
    
    return render_template('index.html', user=UUID, panorama = pan_img, audio=AUD, uids = UID_LIST)