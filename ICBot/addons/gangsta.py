from pyrogram import Client, filters, enums
import os
import re
import bs4
import requests


'''===========EDITABLES==========='''

preFix = ""
cmds = ["gangsta", F"gangsta{os.getenv('BOT_UNAME')}"]
HELP = F"""{preFix if preFix else os.getenv('MASTER_PREFIX', '/')}{cmds[0]} Your text - gangstafy yo' text dawwggg

Inline Usage:
{os.getenv('BOT_UNAME')} {cmds[0]} Your text"""

'''-------------------------------'''


command = lambda cmd: filters.command(cmd, prefixes = preFix if preFix else os.getenv('MASTER_PREFIX', '/'))

def gangstafy(input_text):
  # https://github.com/SouravJohar/gangsta/blob/master/gizoogle.py
  params = {"translatetext": input_text}
  target_url = "http://www.gizoogle.net/textilizer.php"
  resp = requests.post(target_url, data=params)
  # the html returned is in poor form normally.
  soup_input = re.sub("/name=translatetext[^>]*>/", 'name="translatetext" >', resp.text)
  soup = bs4.BeautifulSoup(soup_input, "lxml")
  giz = soup.find_all(text=True)
  giz_text = giz[37].strip("\r\n")  # Hacky, but consistent.
  return giz_text

@Client.on_message(command(cmds))
async def gangsta(_, msg):
  if len(msg.text.split()) > 1:
    origText = msg.text.partition(msg.text.split()[0])[-1].strip()
    return await msg.reply(gangstafy(origText), quote = 1, parse_mode = enums.ParseMode.DISABLED)
  else: return await msg.reply(F"Usage:\n`{HELP}`", quote = 1)

# Inline method defined in inlineQHandler.py
