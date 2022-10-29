from pyrogram import Client, filters
import os
import json

'''===========EDITABLES==========='''

preFix = "/"
cmds = ["size", F"size{os.getenv('BOT_UNAME')}"]
HELP = F"""Reply to a message containing a file of any type
{preFix if preFix else os.getenv('MASTER_PREFIX', '/')}{cmds[0]} - get the file size"""

'''-------------------------------'''


command = lambda cmd: filters.command(cmd, prefixes = preFix if preFix else os.getenv('MASTER_PREFIX', '/'))

def convert_bytes(num):
  for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
    if num < 1024.0:
      return F"{num:3.1f} {x}"
    num /= 1024.0

fileTypes = ["animation", "audio", "photo", "video", "document", "sticker"]
def get_bytes(msg):
  typ = None
  for x in fileTypes:
    if x in msg:
      typ = x
      break
  return msg[typ]['file_size'] if typ else typ

@Client.on_message(command(cmds))
async def filesize(_, msg):
  if msg.reply_to_message:
    rep = await msg.reply("Processing...", quote = 1)
    origMsg = msg.reply_to_message
    msgS = str(origMsg)
    msgD = json.loads(msgS)
    try: await rep.edit(f"File Size: {convert_bytes(get_bytes(msgD))}")
    except: await rep.edit("`ERROR: No file found in the message!`")
  else: return await msg.reply(F"Usage:\n`{HELP}`", quote = 1)
