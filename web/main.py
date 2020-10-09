from flask import *
from src.site import Website
from threading import Thread
from os.path import abspath
web = Website("username601's webshite")

@web.on_error(404)
def not_found(err):
  return render_template("404.html")

@web.page('/github')
def github():
  return web.redirect('github')

@web.page('/api')
def api():
  return web.redirect('api')

@web.page('/vote')
def vote():
  return web.redirect('vote')

@web.page('/invite')
def invite():
  return web.redirect('invite')

@web.page('/support')
def support():
  return web.redirect('support')

@web.page('/commands')
def commands():
  return render_template("commands.html")

@web.page('/')
def home():
  return render_template("index.html")

@web.page('/credits')
def credits():
  return web.credits

@web.page('/raw/<file>')
def get_raw(file: str):
  if web.check_template(file):
    return send_from_directory('templates', file)
  abort(404)

def run():
  web.start()

def main():
  t = Thread(target=run)
  t.start()

if __name__ == "__main__": main()