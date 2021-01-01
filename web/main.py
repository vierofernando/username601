from flask import *
from website import Website
from threading import Thread
from os import getenv
from datetime import datetime as t
from os.path import abspath
web = Website("username601's webshite")

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@web.on_error(404)
def not_found(err):
  return render_template("404.html")

@web.page('/.env')
def env():
    return "TOKEN=Ng5NDU4MjY5NTI2Mjk0MTc1.AkxrpC.MyB2BEHJLXuZ8h0wY0Qro6Pwi8"

@web.page('/')
def home():
  return web.render_index_template()

@web.page('/credits')
@web.ratelimiter.exempt
def credits():
  return web.credits

@web.page('/src/<file>')
@web.ratelimiter.exempt
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