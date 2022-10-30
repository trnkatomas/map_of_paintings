import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


def init_the_db():
    cred = credentials.Certificate("map-of-paintings-firebase-adminsdk-3u6rf-7ad6ed0251.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://map-of-paintings-default-rtdb.europe-west1.firebasedatabase.app"
    })

    ref = db.reference(path="/")
    print(ref)

def get_artist(artist: str):
    ref = db.reference(f"/artists/{artist}")
    return ref.get()

def get_institution(institution: str):
    ref = db.reference(f"/institutions/{institution}")
    return ref.get()

def get_paintings_for_artist(artist: str):
    ref = db.reference("paintings").order_by_child("artist").start_at(f"{artist}").end_at(f"{artist}")
    return ref.get()

def get_all_the_paintings_for_institution(institution: str):
    ref = db.reference("paintings").order_by_child("institution").start_at(f"{institution}").end_at(f"{institution}")
    return ref.get()