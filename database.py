import os
# PYMONGO_TOKEN IS YOUR PYMONGO ACCOUNT PASSWORD.
link = 'mongodb+srv://YOUR USERNAME:'+str(os.environ['PYMONGO_TOKEN'])+'@cluster0-9droo.mongodb.net/test?retryWrites=true&w=majority'