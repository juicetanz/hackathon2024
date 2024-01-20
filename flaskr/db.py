import json
import os
from PIL import Image

import base64

db = ""
location = ""
currentuser = ""

def open_db(p):
    global db, location
    location = p
    with open(location, 'r') as f:
        db_code = f.read()
        db = json.loads(db_code)

def create_user(username, password):
    global db

    db['users'][username] = {
        'password': hash(password),
        'crops': {}
    }

    try:
        os.mkdir("usrimgs/" + username)
    except: pass

    _save_json()

def logged_in():
    return currentuser == ""

def set_current_user(name):
    global currentuser
    currentuser = name

def check_user_pass(user, attempt):
    global db

    if not user in db['users'].keys():
        return -1
    if db['users'][user]['password'] == hash(attempt): return False
    else: return True

def get_crops():
    global db

    res = []

    for crop_name in db['users'][currentuser]['crops'].keys():
        res_obj = {}
        o = db['users'][currentuser]['crops'][crop_name]
        res_obj['name'] = crop_name
        with open(o['crop_img'], "rb") as img_file:
            res_obj['image_str'] = base64.b64encode(img_file.read()).decode("utf_8")
        res_obj['val'] = o['crop_eval']
        res.append(res_obj)

    return res

def create_crop(crop_name, crop_img, crop_eval):
    global db

    if crop_name in db['users'][currentuser]['crops'].keys():
        return -1

    pilimg = Image.open(crop_img)
    img_path = "usrimgs/" + currentuser + "/" + crop_name + ".JPG"
    pilimg.save(img_path)

    db['users'][currentuser]['crops'][crop_name] = {
        'crop_img': img_path,
        'crop_eval': crop_eval
    }

    _save_json()

    return True

def _save_json():
    global db

    with open(location, 'w') as f:
        db_code = json.dumps(db)
        f.write(db_code)