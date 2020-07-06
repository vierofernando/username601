from pymongo import MongoClient
import os

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