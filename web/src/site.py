from flask import *
from os import listdir, getenv
from json import loads
from random import choice
from requests import get
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

class Website:
  def __init__(self, name):
    self.site = Flask(name)
    self.ratelimiter = Limiter(
      self.site,
      key_func=get_remote_address,
      default_limits=["3 per second"]
    )
    self.page = self.site.route
    self.commands = get("https://raw.githubusercontent.com/vierofernando/username601/master/assets/json/commands.json").json()
    self.template_files = listdir('./templates')
    self.credits = """<style>
    body {
      font-family: monospace;
    }
    </style>
    """+open('./templates/credits.txt', 'r').read().replace('\n', '<br>')
    self.on_error = self.site.errorhandler
    self.redirects = {
      "support": "https://discord.com/invite/HhAPkD8/",
      "invite": "https://discord.com/oauth2/authorize?client_id=696973408000409626&permissions=8&scope=bot",
      "vote": "https://top.gg/bot/696973408000409626/vote",
      "github": "https://github.com/vierofernando/username601",
      "api": "https://useless-api.vierofernando.repl.co/docs"
    }
    self.raw_command_template = open('./templates/commands.html', 'r').read().replace('\n', '').replace("`%CATEGORIES%`", str([
        list(i.keys())[0] for i in self.commands
    ])).replace("%COMMANDS%", str(self.commands).replace("'", '"'))
    self.raw_index_template = open('./templates/index.html', 'r').read().replace('\n', '')
    self.title_messages = loads(open("./src/site_description.json", "r").read())
  
  def render_index_template(self):
    try:
      msg = choice(self.title_messages)
      data = get('https://useless-api.vierofernando.repl.co/get_bot_stats', headers={"superdupersecretkey": getenv("CHKDB")}).json()
      return self.raw_index_template.replace(
        "'flex'>",
        "'flex'>Serving <b>{}</b> discord servers with <b>{}</b> users as of <b>{} ago</b>".format(
          data['guild_count'], data['user_count'], data['last_updated']
        )
      ).replace("{{FLEX}}", msg).replace("{{TITLE}}", msg if ('<a' not in msg) else "601 the bot")
    except Exception as e:
      print("ERROR: "+str(e))
      return self.raw_index_template.replace(
        "'flex'>",
        "'flex'>Serving <b>{}</b> discord servers with <b>{}</b> users as of <b>{} ago</b>".format(
          "???", "???", "some time "
        )
      )

  def redirect(self, key):
    return f"<script>window.location.href = '{self.redirects[key]}';</script>"

  def check_template(self, filename):
    if (filename not in self.template_files) or (filename.lower().endswith('.html')):
      return False
    return True
  
  def start(self, host='0.0.0.0', port=8080):
    self.site.run(host=host, port=port)