from pymongo import MongoClient
import os
from sys import path
from datetime import datetime as t
from random import choice
import requests
try: from modules.username601 import lapsed_time_from_seconds
except: from .username601 import lapsed_time_from_seconds
database = MongoClient(os.getenv('DB_LINK'))['username601']

class Dashboard:
    def getData(guildid):
        try:
            data = database['dashboard'].find_one({'serverid': guildid})
            return data
        except: return None
    def exist(guildid):
        try:
            data = database['dashboard'].find_one({'serverid': int(guildid)})
            assert data is not None
            return True
        except:
            return False
    def add_guild(guildid, **kwargs):
        warns = [] if kwargs.get('warns')is None else kwargs.get('warns')
        database["dashboard"].insert_one({
            "serverid": guildid,
            "autorole": kwargs.get('autorole'),
            "welcome": kwargs.get('welcome'),
            "starboard": kwargs.get('starboard'),
            "star_requirements": kwargs.get('starreq'),
            "warns": warns,
            "dehoister": kwargs.get('dehoister') if kwargs.get('dehoister')is not None else False,
            "mute": kwargs.get('muterole'),
            "shop": [],
            "subscription": kwargs.get('sub')
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
    def get_subscribers():
        return [{
            'url': i['subscription'], 'serverid': int(i['serverid'])
        } for i in database['dashboard'].find() if i['subscription']is not None]
    def subscribe(url, guildid, reset=False):
        if reset:
            if Dashboard.exist(guildid):
                database['dashboard'].update_one({'serverid': guildid}, {'$set': {'subscription': None}})
            return
        if not Dashboard.exist(guildid):
            Dashboard.add_guild(guildid, sub=url); return
        database['dashboard'].update_one({'serverid': guildid}, {'$set': {'subscription': url}}); return
    def add_autorole(guildid):
        if not Dashboard.exist(guildid):
            return str(None)
        try:
            return str(database["dashboard"].find_one({"serverid": guildid})["autorole"])
        except:
            return str(None)
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
    def getStarboardChannel(guild, **kwargs):
        guildid = guild.id if (guildis not None) else int(kwargs.get('guildid'))
        if not Dashboard.exist(guildid): return None
        data = database['dashboard'].find_one({'serverid': guildid})
        try:
            return {
                'channelid': data['starboard'],
                'starlimit': data['star_requirements']
            }
        except: return None
    def sendStarboard(discord, message):
        embed = discord.Embed(title=f':star: {message.channel.name} | {message.author.name}#{message.author.discriminator}', description=message.content, color=discord.Colour.from_rgb(255, 255, 0), url=f'https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}')
        embed.set_footer(text='Click on the URL to jump to the message!')
        if len(message.attachments)>0: embed.set_image(url=message.attachments[0].url)
        return embed
    def setStarboardLimit(limit, guild):
        database['dashboard'].update_one({'serverid': guild.id}, {'$set': {'star_requirements': int(limit)}})
    def addStarboardChannel(channel, limit):
        if not Dashboard.exist(channel.guild.id):
            Dashboard.add_guild(channel.guild.id, starboard=channel.id, starreq=int(limit))
            return
        database['dashboard'].update_one({'serverid': channel.guild.id}, {'$set': {'starboard': channel.id, 'star_requirements': int(limit)}})
    def removeStarboardChannel(guild):
        if not Dashboard.exist(guild.id):
            Dashboard.add_guild(guild.id)
            return
        database['dashboard'].update_one({
            'serverid': guildid
        }, {'$set': {'starboard': None, 'star_requirements': None}})
    def databaseDeleteChannel(channel):
        try:
            data = database['dashboard'].find_one({'serverid': channel.guild.id})
            if datais None: return
        except: return
        if channel.id not in [data[i] for i in list(data.keys())]: return
        if data['welcome'] == channel.id:
            database['dashboard'].update_one({'serverid': channel.guild.id}, {'$set': {
                'welcome': None
            }})
            return
        elif data['starboard'] != channel.id: return
        database['dashboard'].update_one({'serverid': channel.guild.id}, {'$set': {
            'starboard': None, 'star_requirements': None
        }})
    def addWarn(user, moderator, reason):
        warn = f'{user.id}.{moderator.id}.{reason}'
        try:
            if not Dashboard.exist(moderator.guild.id):
                Dashboard.add_guild(moderator.guild.id, warns=warn)
                return True
            database['dashboard'].update_one({'serverid': moderator.guild.id}, {'$push': {'warns': warn}}) ; return True
        except Exception as e:
            print(e)
            return False
    def clearWarn(user):
        if not Dashboard.exist(user.guild.id): return False
        try:
            data = database['dashboard'].find_one({'serverid': user.guild.id})['warns']
            ids = [int(i.split('.')[0]) for i in data]
            if user.id not in ids: return False
            warns = [i for i in data if i.startswith(str(user.id))]
            for i in warns:
                database['dashboard'].update_one({'serverid': user.guild.id}, {'$pull': {'warns': i}})
            return True
        except: return False
    def getWarns(user):
        try:
            data, results = database['dashboard'].find_one({'serverid': user.guild.id})['warns'], []
            data = [i for i in data if i.startswith(str(user.id))]
            if len(data)==0: return None
            for i in data:
                results.append({
                    'moderator': int(i.split('.')[1].split('.')[0]),
                    'reason': i.split('.')[2]
                })
            return results
        except: return None
    def setDehoister(server, flip):
        if not Dashboard.exist(server.id):
            Dashboard.add_guild(server.id, dehoister=flip)
            return
        database['dashboard'].update_one({'serverid': server.id}, {'$set': {'dehoister': flip}})
    def getDehoister(serverid):
        if not Dashboard.exist(serverid): return False
        data = database['dashboard'].find_one({'serverid': serverid})
        if datais None: return False
        return data['dehoister']
    def getMuteRole(serverid):
        if not Dashboard.exist(serverid):
            Dashboard.add_guild(serverid)
            return None
        data = database['dashboard'].find_one({'serverid': serverid})
        if datais None: return None
        return data['mute']
    def editMuteRole(serverid, roleid):
        new = int(roleid) if roleidis not None else None
        database['dashboard'].update_one({'serverid': serverid}, {'$set': {
            'mute': new
        }})

class Economy:
    def get(userid):
        try:
            data = database['economy'].find_one({'userid': userid})
            return data
        except Exception as e:
            return None
    def getProfile(userid, guildMembersId):
        try:
            data = database['economy'].find_one({'userid': int(userid)})
            alldata = [i for i in database['economy'].find()]
            bal_global_list = sorted([i['bal'] for i in alldata])[::-1]
            bal_guild_list = sorted([i['bal'] for i in alldata if i['userid'] in guildMembersId])[::-1]
            time_join_list = sorted([i['joinDate'] for i in alldata])
            global_rank = str([i+1 for i in range(len(bal_global_list)) if bal_global_list[i]==data['bal']][0])
            after_bal = [i for i in bal_global_list[::-1] if i > data['bal']][0]
            return {
                'main': {
                    'rank': str([i+1 for i in range(len(bal_guild_list)) if bal_guild_list[i]==data['bal']][0]),
                    'global': str(global_rank),
                    'desc': data['desc'],
                    'wallet': str(data['bal']),
                    'bank': str(data['bankbal']),
                    'joined': str(t.fromtimestamp(data['joinDate']))[:-7],
                    'number': str([i+1 for i in range(len(time_join_list)) if time_join_list[i]==data['joinDate']][0])
                },
                'after': {
                    'bal': str(after_bal),
                    'delta': str(int(after_bal) - data['bal']),
                    'nextrank': str(int(global_rank) - 1)
                }
            }
        except:
            return {
                'main': {
                    'rank': str([i+1 for i in range(len(bal_guild_list)) if bal_guild_list[i]==data['bal']][0]),
                    'global': str(global_rank),
                    'desc': data['desc'],
                    'wallet': str(data['bal']),
                    'bank': str(data['bankbal']),
                    'joined': str(t.fromtimestamp(data['joinDate']))[:-7],
                    'number': str([i+1 for i in range(len(time_join_list)) if time_join_list[i]==data['joinDate']][0])
                },
                'after': None
            }
        
    def leaderboard(guildMembers):
        fetched, members = database['economy'].find(), [a.id for a in guildMembers]
        temp = ['{}|{}'.format(
            i['userid'], i['bal']
        ) for i in fetched if i['userid'] in members]
        return temp
    
    def setdesc(userid, newdesc):
        try:
            database['economy'].update_one({'userid': userid}, { '$set': { 'desc': str(newdesc) } })
        except:
            return 'error'
    def delete_data(userid):
        try:
            database['economy'].delete_one({"userid": userid})
            return True
        except:
            return False
    def deposit(userid, amount):
        database['economy'].update_one({'userid': int(userid)}, {
            '$inc': {
                'bal': -amount,
                'bankbal': amount
            }
        })
    def withdraw(userid, amount):
        database['economy'].update_one({'userid': int(userid)}, {
            '$inc': {
                'bal': amount,
                'bankbal': -amount
            }
        })
    def can_vote(userid):
        data = database['economy'].find_one({'userid': int(userid)})['lastDaily']
        if data==0:
            return {
                'bool': True,
                'time': None
            }
        elif (t.now().timestamp() - data) > 43200:
            return {
                'bool': True,
                'time': None
            }
        else:
            return {
                'bool': False,
                'time': lapsed_time_from_seconds(round((data+43200) - t.now().timestamp()))
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
                'bankbal': 0,
                'joinDate': t.now().timestamp(),
                'lastDaily': 0,
                'buyList': []
            })
            return 'done'
        except Exception as e:
            return e
    def addbal(userid, bal):
        try:
            database['economy'].update_one({'userid': userid}, { '$inc': { 'bal': bal } })
            return 'success'
        except Exception as e:
            return e
    def delbal(userid, bal):
        try:
            database['economy'].update_one({'userid': userid}, { '$inc': { 'bal': -bal } })
            return 'success'
        except Exception as e:
            return e
    
    def daily(userid):
        try:
            bal = choice([1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6001, 6969, 4200, 69420])
            database['economy'].update_one({'userid': userid}, { '$inc': {
                'bal': bal
            }})
            database['economy'].update_one({'userid': userid}, { '$set': {
                'lastDaily': t.now().timestamp()
            }})
            return bal
        except Exception as e:
            return e
    def getBuyList(author, raw=False):
        data = Economy.get(author.id)
        if datais None: return {'error': True, 'ctx': f'{author.name} has no profile'}
        elif len(data['buyList'])==0: return {'error': True, 'ctx': 'No buylist found'}
        if raw: return {'error': False, 'ctx': data['buyList']}
        return {'error': False, 'ctx': '\n'.join([str(i+1)+'. "'+' '.join(data['buyList'][i].split('.')[3:60])+'" (Price: '+str(data['buyList'][i].split('.')[2])+' :gem:)' for i in range(len(data['buyList']))])}
    def changedesc(userid, newdesc):
        try:
            data = database['economy'].find({'userid': userid})
            if len(data)==0 or datais None:
                return 'undefined'
            else:
                database['economy'].update_one({'userid': userid}, { '$set': { 'desc': str(newdesc) } })
                return 'success'
        except Exception as e:
            return 'e'

class Shop:
    def get_shop(server):
        if not Dashboard.exist(server.id):
            Dashboard.add_guild(server.id)
            return {'error': True, 'ctx': 'This server does not have any shops!'}
        data = database['dashboard'].find_one({'serverid': server.id})['shop']
        if len(data)==0:
            return {'error': True, 'ctx': 'This server does not have any shops!'}
        return {'error': False, 'ctx': [{
            'price': int(i.split('.')[0]),
            'name': ' '.join(i.split('.')[1:len(i)])
        } for i in data]}
    def delete_shop(server):
        if not Dashboard.exist(server.id):
            Dashboard.add_guild(server.id)
        database['dashboard'].update_one({'serverid': server.id}, {'$set': {'shop': []}})
    def add_value(name, price, server):
        data = Shop.get_shop(server)
        if not data['error']:
            if len(data['ctx'])>=20:
                return {'error': True, 'ctx': 'Bypassed the limit of 20 products!'}
        if not Dashboard.exist(server.id): Dashboard.add_guild(server.id)
        database['dashboard'].update_one({'serverid': server.id}, {'$push': {'shop': f'{price}.{name}'}})
        return {'error': False, 'ctx': 'Successfully added {} with the price of {} bobux'.format(
            name, price
        )}
    def remove_element(name, server):
        if not Dashboard.exist(server.id): Dashboard.add_guild(server.id)
        shop, product = database['dashboard'].find_one({'serverid': server.id})['shop'], None
        if len(shop)==0: return {'error': True, 'ctx': 'This server has no product left'}
        for i in shop:
            if name.lower() in i['name'].lower(): product = i; break
        if productis None: return {'error': True, 'ctx': 'Product not found'}
        database['dashboard'].update_one({'serverid': server.id}, {'$pull': {'shop': product['price']+'.'+product['name']}})
        return {'error': False, 'ctx': '{} deleted from shop'.format(product['name'])}
    def buy(name, user):
        element, server_shop, user_data = None, Shop.get_shop(user.guild), Economy.get(user.id)
        if server_shop['error']: return server_shop
        for i in server_shop['ctx']:
            if name.lower() in i['name'].lower(): element = i ; break
        if elementis None: return {'error': True, 'ctx': 'Error product not found'}
        elif user_datais None: return {'error': True, 'ctx': 'User does not have any profile'}
        elif user_data['bal'] < element['price']: return {'error': True, 'ctx': 'Money is less than the price.\nPlease have {} more bobux'.format(element['price']-user_data['bal'])}
        Economy.delbal(user.id, element['price'])
        if element['name'] not in [' '.join(i.split('.')[3:len(i.split('.'))]) for i in user_data['buyList']]:
            database['economy'].update_one({'userid': user.id}, {'$push': {'buyList': '{}.{}.{}.{}'.format(
                user.guild.id, round(t.now().timestamp()), element['price'], element['name']
            )}})
            buyList = Economy.getBuyList(user, raw=True)
            if len(buyList)>20:
                database['economy'].update_one({'userid': user.id}, {'$pull': {'buyList': buyList[0]}})
        return {'error': False, 'ctx': 'Successfully bought '+element['name']}

class selfDB:
    def ping():
        a = t.now().timestamp()
        temp = [i for i in database['dashboard'].find()]
        return round((t.now().timestamp()-a)*1000)
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