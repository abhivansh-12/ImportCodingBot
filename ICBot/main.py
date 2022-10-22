from pyrogram import Client
from dotenv import load_dotenv
import os

#----------------------------
bottoken = os.getenv("BOT_TOKEN")
apiid = 8
apihash = "7245de8e747a0d6fbe11f7cc14fcc0bb"
plugins = dict(root="addons")
app = Client("ICBot", api_id = apiid, api_hash = apihash, plugins = plugins, bot_token = bottoken)
#----------------------------

app.run()
