import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("map-of-paintings-firebase-adminsdk-3u6rf-7ad6ed0251.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://map-of-paintings-default-rtdb.europe-west1.firebasedatabase.app"
})

ref = db.reference(path="/")
print(ref)

def get_artist():
    pass

def get_institution():
    pass

def get_paintings_for_artist():
    pass