import pickle

user_name = ""

def set_user_name(name):
    global user_name
    user_name = name
    save_user_name()

def get_user_name():
    global user_name
    return user_name

def save_user_name():
    with open("user_data.pkl", "wb") as f:
        pickle.dump(user_name, f)

def load_user_name():
    global user_name
    try:
        with open("user_data.pkl", "rb") as f:
            user_name = pickle.load(f)
    except FileNotFoundError:
        user_name = ""
