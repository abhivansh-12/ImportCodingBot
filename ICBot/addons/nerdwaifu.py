from pyrogram import Client, filters, enums
from urllib.request import urlopen, urlretrieve
from pathlib import Path
import json
from dotenv import load_dotenv
import os
from deta import Deta


load_dotenv()
'''===========EDITABLES==========='''

preFix = "!"
cmds = ["nerdwaifu"]
HELP = F"""
{preFix if preFix else os.getenv('MASTER_PREFIX', '/')}{cmds[0]} - sends a random nerd waifu in the chat
{preFix if preFix else os.getenv('MASTER_PREFIX', '/')}{cmds[0]} set - sends and set a random waifu as the chat profile photo if the command was issued by an ADMIN/AUTH User"""

'''-------------------------------'''


deta = Deta(os.getenv("DETA_KEY"))
db = deta.Base("AuthUsers")

'''
AuthUsers Detabase Structure
{
  "key": "Authentic",
  "users": [
    userID1,
    userID2,
    userID3,....,userIDn  
  ]
}
'''
AUTHENTIC = db.get("Authentic").get("users")
command = lambda cmd: filters.command(cmd, prefixes = preFix if preFix else os.getenv('MASTER_PREFIX', '/'))
APIEndPoint = "https://znerdwaifuz.pythonanywhere.com/"

def delfiles(files_to_del: list):
  for x in files_to_del:
    if os.path.exists(x):
      os.remove(x)

@Client.on_message(command(cmds))
async def nerdwaifu(app, msg):
  rep = await msg.reply("Processing...", quote = 1)
  try:
    with urlopen(APIEndPoint) as response:
      waifu = json.loads(response.read()).get("waifu")
      url = waifu.get("file")
      file = urlretrieve(url, F"{os.getcwd()}/{Path(url).stem}{Path(url).suffix}")
      filePath = os.path.abspath(file[0])
      if len(msg.text.split()) > 1:
        if msg.text.partition(msg.text.split()[0])[-1].strip().lower() == "set":
          user = await app.get_chat_member(msg.chat.id, msg.from_user.id)
          if ((user.status in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]) or (msg.from_user.id in AUTHENTIC)):
            await app.set_chat_photo(msg.chat.id, photo = filePath)
      await msg.reply_photo(photo = filePath, quote = 1)
      await msg.reply_document(document = filePath, quote = 1)
      await rep.delete()
      delfiles([filePath])

  except Exception as e:
    await rep.edit(F"Error:\n`{e}`")
