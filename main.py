from flask import Flask
from threading import Thread
from bot import *
app = Flask(__name__)

@app.route('/')
def home():
    return 'If you are seeing this, the bot is online!'

def run():
	app.run(host='0.0.0.0',port=8080)

def keep_alive():
    print('Running server...')
    t = Thread(target=run)
    t.start()
    Username601()

if __name__=='__main__': keep_alive()