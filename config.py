import firebase_admin
from firebase_admin import credentials,firestore

def config():
    # ตั้งค่า Firebase Admin SDK
    cred = credentials.Certificate("./backtesting-ab7f5-firebase-adminsdk-chrms-036c5c7334.json")
    firebase_admin.initialize_app(cred)


    # เริ่มต้นการใช้งาน Firestore
    db = firestore.client()
    return db