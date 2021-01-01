from flask import *
from os import listdir, getenv
from json import dumps
from random import choice
from requests import get
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from database import DB

class Website:
  def __init__(self, name):
    self.site = Flask(name)
    self.db = DB(getenv("DBLK"))
    self.ratelimiter = Limiter(
      self.site,
      key_func=get_remote_address,
      default_limits=["3 per second"]
    )
    self.page = self.site.route
    self.commands = dumps(get("https://raw.githubusercontent.com/vierofernando/username601/master/assets/json/commands.json").json())
    self.template_files = listdir('./templates')
    self.credits = """<style>
    body {
      font-family: monospace;
    }
    </style>
    """+open('./templates/credits.txt', 'r').read().replace('\n', '<br>')
    self.on_error = self.site.errorhandler
    self.raw_index_template = open('./templates/index.html', 'r').read().replace('\n', '').replace('COMMANDS_LIST', f'`{self.commands}`')

  def render_index_template(self):
    try:
      data = self.db.get_data()
      return self.raw_index_template.replace('SERVER_COUNT', str(data['guild_count'])).replace('USERS_COUNT', str(data['users_count'])).replace('UPTIME', f'"{data["last_update"]}"').replace('ECONOMIES', str(data["economy_length"])).replace('DASHBOARDS', str(data["dashboard_length"])).replace('${CHANGELOG}', dumps(data['changelog']))
    except Exception as e:
      print("ERROR: "+str(e))
      return self.raw_index_template.replace('SERVER_COUNT', '0').replace('USERS_COUNT', '0').replace('UPTIME', '??? time')
      
  def check_template(self, filename):
    return (not ((filename not in self.template_files) or (filename.lower().endswith('.html'))))
  
  def start(self, host='0.0.0.0', port=8080):
    self.site.run(host=host, port=port)