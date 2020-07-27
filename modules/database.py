from pymongo import MongoClient
import os
from sys import path
from datetime import datetime as t
from random import choice
import requests
path.append('/home/runner/hosting601/modules')
import username601 as myself
from username601 import *

database = MongoClient(os.getenv('DB_LINK'))['username601']

class Dashboard:
    def exist(guildid):
        data = database["dashboard"].find()
        if len([i for i in data if i["serverid"]==guildid])==0: return False
        return True
    def add_guild(guildid, **kwargs):
        database["dashboard"].insert_one({
            "serverid": guildid,
            "autorole": kwargs.get('autorole'),
            "welcome": kwargs.get('welcome')
        })
    def delete_data(guildid):
        if Dashboard.exist(guildid):
            database["dashboard"].delete_one({"serverid": guildid})
    def set_autorole(guildid, roleid):
        if not Dashboard.exist(guildid):
            Dashboard.add_guild(guildid, autorole=roleid)
        else:
            database["dashboard"].update_one({"serverid": guildid}, {"$set": {
                "autorole": roleid
            }})
    def add_autorole(guildid):
        if not Dashboard.exist(guildid):
            return str(None)
        return str(database["dashboard"].find_one({
            "serverid": guildid
        })["autorole"])
    def set_welcome(guildid, channelid):
        if not Dashboard.exist(guildid): Dashboard.add_guild(guildid, welcome=channelid)
        database["dashboard"].update_one({"serverid": guildid}, {"$set": {
            "welcome": channelid
        }})
    def send_welcome(member, discord):
        if not Dashboard.exist(member.guild.id): return None
        embed = discord.Embed(timestamp=t.now(), title=member.name, description="Welcome to *{}!*".format(member.guild.name), color=discord.Colour.green())
        embed.set_footer(text='ID: {}'.format(str(member.id)))
        embed.set_thumbnail(url=member.avatar_url)
        return embed
    def send_goodbye(member, discord):
        if not Dashboard.exist(member.guild.id): return None
        embed = discord.Embed(timestamp=t.now(), title=member.name, description="Left *{}*...".format(member.guild.name), color=discord.Colour.red())
        embed.set_footer(text='ID: {}'.format(str(member.id)))
        embed.set_thumbnail(url=member.avatar_url)
        return embed
    def get_welcome_channel(guildid):
        if not Dashboard.exist(guildid): return None
        try:
            data = database["dashboard"].find_one({"serverid": guildid})["welcome"]
            return int(data)
        except: return None
class Economy:
    def get(userid):
        try:
            data = database['economy'].find({'userid': userid})[0]
            return data
        except Exception as e:
            return None
    def leaderboard(guildMembers):
        fetched, total = database['economy'].find(), []
        for i in fetched:
            if i['userid'] in [a.id for a in guildMembers]:
                total.append(str(i['userid'])+'|'+str(i['bal']))
            else: continue
        return total
    
    def setdesc(userid, newdesc):
        try:
            database['economy'].update_one({'userid': userid}, { '$set': { 'desc': str(newdesc) } })
        except:
            return 'error'
    def vote(userid, bl):
        try:
            database['economy'].update_one({'userid': userid}, { '$set': { 'voted': bl } })
        except:
            return 'error'
    def delete_data(userid):
        try:
            database['economy'].delete_one({"userid": userid})
            return True
        except:
            return False

    def can_vote(userid):
        data = requests.get('https://api.ksoft.si/webhook/dbl/check?bot={}&user={}'.format(str(Config.id), str(userid)), headers={'authorization':'Bearer '+str(os.environ['KSOFT_TOKEN'])}).json()
        if data['voted']==False or Economy.get(userid)['voted']==False:
            return {
                'bool': True,
                'time': None
            }
        else:
            raw = data['data']['expiry'].replace('T', ' ')
            raw = [
                int(raw.split('-')[0]),
                int(raw.split('-')[1].split('-')[0]),
                int(raw.split('-')[2].split(' ')[0]),
                int(raw.split(' ')[1].split(':')[0]),
                int(raw.split(':')[1].split(':')[0]),
                int(raw.split(':')[2].split('.')[0])
            ]
            time = t(raw[0], raw[1], raw[2], raw[3], raw[4], raw[5])
            return {
                'bool': False,
                'time': myself.time_encode((time-t.now()).seconds)
            }
    
    def setbal(userid, newbal):
        if userid not in [i['userid'] for i in database['economy'].find()]:
            return 'user has no profile'
        else:
            try:
                database['economy'].update_one({'userid': userid}, { '$set': { 'bal': newbal } })
                return '200 OK'
            except Exception as e:
                return e

    def new(userid):
        try:
            database['economy'].insert_one({
                'userid': userid,
                'bal': 0,
                'desc': 'nothing here!',
                'voted': False
            })
            return 'done'
        except Exception as e:
            return e
    def addbal(userid, bal):
        try:
            old = database['economy'].find({'userid': userid})
            database['economy'].update_one({'userid': userid}, { '$set': { 'bal': old[0]['bal']+bal } })
            return 'success'
        except Exception as e:
            return e
    def delbal(userid, bal):
        try:
            old = database['economy'].find({'userid': userid})
            database['economy'].update_one({'userid': userid}, { '$set': { 'bal': old[0]['bal']-bal } })
            return 'success'
        except Exception as e:
            return e
    
    def daily(userid):
        try:
            bal = choice([500, 1000, 1500, 2000, 2500, 3000])
            old = database['economy'].find_one({'userid': userid})
            database['economy'].update_one({'userid': userid}, { '$set': {
                'bal': old['bal']+bal
            }})
            return bal
        except Exception as e:
            return e
    
    def changedesc(userid, newdesc):
        try:
            data = database['economy'].find({'userid': userid})
            if len(data)==0 or data==None:
                return 'undefined'
            else:
                database['economy'].update_one({'userid': userid}, { '$set': { 'desc': str(newdesc) } })
                return 'success'
        except Exception as e:
            return 'e'

class selfDB:
    def post_uptime():
        for i in database['config'].find():
            if 'uptime' in list(i.keys()):
                old_uptime = i['uptime'] ; break
        database['config'].update_one({'uptime': old_uptime}, { '$set': { 'uptime': t.now().timestamp() } })
    def get_uptime():
        for i in database['config'].find():
            if 'uptime' in list(i.keys()):
                uptime = i['uptime'] ; break
        time = str(t.now() - t.fromtimestamp(uptime))[:-7]
        return time+'|'+str(t.fromtimestamp(uptime))[:-7]
    def feedback_ban(userid, reason):
        for i in database['config'].find():
            if 'bans' in list(i.keys()):
                old_bans = i['bans'] ; break
        database['config'].update_one({'bans': old_bans}, { '$push': {'bans': str(userid)+'|'+str(reason)} })
    def feedback_unban(userid):
        try:
            for i in database['config'].find():
                if 'bans' in list(i.keys()):
                    for j in i['bans']:
                        if j.startswith(str(userid)): reason = j.split('|')[1] ; break
                    old_bans = i['bans'] ; break
            database['config'].update_one({'bans': old_bans}, { '$pull': {'bans': str(userid)+'|'+str(reason)} })
            return '200'
        except:
            return '404'
    def is_banned(user_id):
        banned, reason = False, None
        for i in database['config'].find():
            if 'bans' in list(i.keys()):
                for lists in i['bans']:
                    if user_id == int(lists.split('|')[0]):
                        banned, reason = True, lists.split('|')[1] ;break
                break
        if banned:
            return reason
        else:
            return False
