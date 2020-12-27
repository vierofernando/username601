from pymongo import MongoClient
from time import time

class DB:
    def __init__(self, url, database_name="username601", collection_name="config"):
        self.db = MongoClient(url)[database_name][collection_name]
        self._time = {
            31536000: "year",
            2592000: "month",
            86400: "day",
            3600: "hour",
            60: "minute"
        }

    def strfsecond(self, seconds):
        seconds = int(seconds)
        result = None
        
        if seconds < 60:
            return f"{seconds} second" + ("" if (seconds == 1) else "s")
        
        for key in self._time.keys():
            if seconds >= key:
                seconds = round(seconds / key)
                return f"{seconds} {self._time[key]}" + ("" if seconds == 1 else "s")
        
        seconds = round(seconds / 31536000)
        return f"{seconds} year" + ("" if seconds == 1 else "s")
    
    def get_data(self):
        data = self.db.find_one({"h": True})["stats"].split(":")
        return {
            "guild_count": data[0],
            "users_count": data[1],
            "economy_length": data[2],
            "dashboard_length": data[3],
            "last_update": self.strfsecond(time() - float(data[4]))
        }