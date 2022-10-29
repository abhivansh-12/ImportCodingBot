from pyrogram import Client, filters
from urllib.parse import urlparse
import os


'''===========EDITABLES==========='''

preFix = "/"
cmds = ["urlprev", F"urlprev{os.getenv('BOT_UNAME')}"]
HELP = F"""{preFix if preFix else os.getenv('MASTER_PREFIX', '/')}{cmds[0]} Your text ||| URL - generates a message from your text, with the preview of the provided URL embedding it in a leading space character resulting in a clean looking message"""

'''-------------------------------'''


command = lambda cmd: filters.command(cmd, prefixes = preFix if preFix else os.getenv('MASTER_PREFIX', '/'))

urlformat = "<a href='{}'> </a>{}"
def uri_validator(x):
  try:
      result = urlparse(x)
      return all([result.scheme, result.netloc, result.path])
  except:return 0

@Client.on_message(command(cmds))
async def urlprev(_, msg):
  if len(msg.text.split()) > 1:
    query = msg.text.partition(msg.text.split()[0])[-1].strip()
    if not query:
      return
    else:
      if len(query.split('|||'))==2:
        elements = [x.strip() for x in query.split('|||')]
        txt = elements[0]
        uri = elements[1]
        if uri_validator(uri):
          await msg.reply(urlformat.format(uri, txt))
      else: return await msg.reply(F"Usage:\n`{HELP}`", quote = 1)
  else: return await msg.reply(F"Usage:\n`{HELP}`", quote = 1)
