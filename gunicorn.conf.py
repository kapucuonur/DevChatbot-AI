import os

bind = "0.0.0.0:" + os.environ.get("PORT", "5000")
workers = 10 # or however many workers you want.