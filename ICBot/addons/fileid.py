from pyrogram import Client, filters
import os

'''===========EDITABLES==========='''

preFix = "/"
cmds = ["fid", F"fid{os.getenv('BOT_UNAME')}"]
HELP = F"""Reply to a message containing a file or media
{preFix if preFix else os.getenv('MASTER_PREFIX', '/')}{cmds[0]} - get the file_id specific to this bot means it can only be recognized by this bot"""

'''-------------------------------'''


command = lambda cmd: filters.command(cmd, prefixes = preFix if preFix else os.getenv('MASTER_PREFIX', '/'))
fileTypes = ["animation", "audio", "photo", "video", "document", "sticker"]

@Client.on_message(command(cmds))
async def fileid(_, msg):
  if msg.reply_to_message:
    obj = msg.reply_to_message
    for x in fileTypes:
      if eval(F"obj.{x}"): await msg.reply(f"{x}".capitalize()+" ID: `"+ eval(f"obj.{x}.file_id")+"`", quote = 1)
  else: return await msg.reply(F"Usage:\n`{HELP}`", quote = 1)
