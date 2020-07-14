from pymongo import MongoClient
import os
from sys import path
from datetime import datetime as t
from random import choice
path.append('/app/modules')
from username601 import time_encode

database = MongoClient(os.environ['DB_LINK'])['username601']

class Economy:
    def leaderboard(guildMembers):
        fetched, total = database["economy"].find(), []
        for i in fetched:
            if i["userid"] in [a.id for a in guildMembers]:
                total.append(str(i["userid"])+"|"+str(i["bal"]))
            else: continue
        return total
    
    def setdesc(userid, newdesc):
        try:
            database["economy"].update_one({"userid": userid}, { "$set": { "desc": str(newdesc) } })
        except:
            return 'error'
    
    def can_vote(userid):
        data = requests.get("https://api.ksoft.si/webhook/dbl/check?bot={}&user{}".format(str(Config.id), str(userid)), headers={"authorization":"Bearer "+str(os.environ['KSOFT_TOKEN'])}).json()
        if not data['voted']: 
            return {
                "bool": False,
                "time": None
            }
        else:
            return {
                "bool": False,
                "time": data['expiry'].split('T')[0]+' '+data['expiry'].split('T')[1][:-7]
            }
    
    def setbal(userid, newbal):
        if userid not in [i["userid"] for i in database["economy"].find()]:
            return 'user has no profile'
        else:
            try:
                database["economy"].update_one({"userid": userid}, { "$set": { "bal": newbal } })
                return '200 OK'
            except Exception as e:
                return e

    def new(userid):
        try:
            database["economy"].insert_one({
                "userid": userid,
                "bal": 0,
                "desc": "nothing here!"
            })
            return 'done'
        except Exception as e:
            return e
    def addbal(userid, bal):
        try:
            old = database["economy"].find({"userid": userid})
            database["economy"].update_one({"userid": userid}, { "$set": { "bal": old[0]['bal']+bal } })
            return 'success'
        except Exception as e:
            return e
    def delbal(userid, bal):
        try:
            old = database["economy"].find({"userid": userid})
            database["economy"].update_one({"userid": userid}, { "$set": { "bal": old[0]['bal']-bal } })
            return 'success'
        except Exception as e:
            return e
    
    def daily(userid):
        try:
            bal = choice([500, 1000, 1500, 2000, 2500, 3000])
            old = database["economy"].find_one({"userid": userid})
            database["economy"].update_one({"userid": userid}, { "$set": {
                "bal": old["bal"]+bal,
                "lastdaily": t.now().timestamp()
            }})
            return bal
        except Exception as e:
            return e
    
    def changedesc(userid, newdesc):
        try:
            data = database["economy"].find({"userid": userid})
            if len(data)==0 or data==None:
                return 'undefined'
            else:
                database["economy"].update_one({"userid": userid}, { "$set": { "desc": str(newdesc) } })
                return 'success'
        except Exception as e:
            return 'e'
    def get(userid):
        try:
            data = database["economy"].find({"userid": userid})[0]
            return data
        except Exception as e:
            return None

class selfDB:
    def post_uptime():
        for i in database["config"].find():
            if "uptime" in list(i.keys()):
                old_uptime = i["uptime"] ; break
        database["config"].update_one({"uptime": old_uptime}, { "$set": { "uptime": t.now().timestamp() } })
    def get_uptime():
        for i in database["config"].find():
            if "uptime" in list(i.keys()):
                uptime = i["uptime"] ; break
        time = str(t.now() - t.fromtimestamp(uptime))[:-7]
        return time+'|'+str(t.fromtimestamp(uptime))[:-7]
    def feedback_ban(userid, reason):
        for i in database["config"].find():
            if "bans" in list(i.keys()):
                old_bans = i["bans"] ; break
        database["config"].update_one({"bans": old_bans}, { "$push": {"bans": str(userid)+"|"+str(reason)} })
    def feedback_unban(userid):
        try:
            for i in database["config"].find():
                if "bans" in list(i.keys()):
                    for j in i["bans"]:
                        if j.startswith(str(userid)): reason = j.split('|')[1] ; break
                    old_bans = i["bans"] ; break
            database["config"].update_one({"bans": old_bans}, { "$pull": {"bans": str(userid)+"|"+str(reason)} })
            return '200'
        except:
            return '404'
    def is_banned(user_id):
        banned, reason = False, None
        for i in database["config"].find():
            if "bans" in list(i.keys()):
                for lists in i["bans"]:
                    if user_id == int(lists.split('|')[0]):
                        banned, reason = True, lists.split('|')[1] ;break
                break
        if banned:
            return reason
        else:
            return False