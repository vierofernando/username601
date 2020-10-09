from flask import *
from os import listdir
from requests import get

class Website:
  def __init__(self, name):
    self.site = Flask(name)
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
  
  def redirect(self, key):
    return f"<script>window.location.href = '{self.redirects[key]}';</script>"

  def check_template(self, filename):
    if (filename not in self.template_files) or (filename.lower().endswith('.html')):
      return False
    return True
  
  def start(self, host='0.0.0.0', port=8080):
    self.site.run(host=host, port=port)