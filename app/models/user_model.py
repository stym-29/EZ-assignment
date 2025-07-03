from app import mongo

def find_user_by_email(email):
    return mongo.db.users.find_one({"email": email})

def insert_user(user_data):
    return mongo.db.users.insert_one(user_data)

def get_all_files():
    return list(mongo.db.fs.files.find({}))
