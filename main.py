from flask import Flask
from threading import Thread
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["2 per second"],
)

@app.route('/')
def home():
    return 'If you are seeing this, the bot is online!'

def run():
	app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()