from pyrogram import Client, filters
from dotenv import load_dotenv
import os


load_dotenv()
'''===========EDITABLES==========='''

preFix = "?"
cmds = ["alive"]
HELP = F"{preFix if preFix else os.getenv('MASTER_PREFIX', '/')}{cmds[0]} - Replies if the bot is alive"

'''-------------------------------'''


command = lambda cmd: filters.command(cmd, prefixes = preFix if preFix else os.getenv('MASTER_PREFIX', '/'))

@Client.on_message(command(cmds))
async def alive(_, msg):
  await msg.reply("Alive af!", quote = 1)