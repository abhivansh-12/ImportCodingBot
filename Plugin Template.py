# All the imports on top, just for the sake of convention, not mandatory
from pyrogram import Client, filters
from dotenv import load_dotenv
import os


load_dotenv()
'''===========EDITABLES==========='''

preFix = "?" # Change this character for a custom command prefix, leave empty to use the master prefix defined in .env, the fallback prefix is  TG's default "/" prefix
cmds = ["mycmd", F"mycmd{os.getenv('BOT_UNAME')}"] # Change the command list accordingly
HELP = F"{preFix if preFix else os.getenv('MASTER_PREFIX', '/')}{cmds[0]} - Short info about mycommand" # Provide brief and meaningful help information about what the command is for

'''-------------------------------'''


command = lambda cmd: filters.command(cmd, prefixes = preFix if preFix else os.getenv('MASTER_PREFIX', '/'))

@Client.on_message(command(cmds))
async def FunctionName_SameAs_FileName(app, msg): # The function name will be myFunc if the file name is myFunc.py, not necessarily but try to stick to this convention
  # Function Body
