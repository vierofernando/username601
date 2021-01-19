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
        self.cache = None
        self.last_usage = time()

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
        if self.cache and ((time() - self.last_usage) <= 61):
            return self.cache

        data = self.db.find_one({"h": True})
        stats = data["stats"].split(":")
        self.cache = {
            "guild_count": stats[0],
            "users_count": stats[1],
            "economy_length": stats[2],
            "dashboard_length": stats[3],
            "last_update": self.strfsecond(time() - float(stats[4])),
            "changelog": data["changelog"],
            "commands_run": data["commands_run"],
            "online": data["online"],
            "down_times": data["down_times"]
        }
        self.last_usage = time()
        return self.cache