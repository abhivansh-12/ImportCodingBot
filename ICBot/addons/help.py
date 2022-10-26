from pyrogram import Client, filters
from importlib import import_module

'''===========EDITABLES==========='''

preFix = "!"
cmds = ["help", "tasukette", "F1"]
HELP = F"{preFix}{cmds[0]} plugin_name - Displays the help info for the plugin"

'''-------------------------------'''


command = lambda cmd: filters.command(cmd, prefixes = preFix)

@Client.on_message(command(cmds))
async def help(_, msg):
  if len(msg.text.split()) == 1:
    return await msg.reply(F"Usage:\n`{HELP}`", quote = 1)
  if len(msg.text.split()) > 1:
    if msg.text.partition(msg.text.split()[0])[-1].strip().lower() in cmds:
      return await msg.reply(F"Usage:\n`{HELP}`", quote = 1)
    else:
      testCmd = msg.text.partition(msg.text.split()[0])[-1].strip().lower()
      try:
        mod = import_module(F"addons.{testCmd}")
        return await msg.reply(F"Usage:\n`{mod.HELP}`", quote = 1)
      except Exception as e:
        return await msg.reply(F"Error:\n`{e}`", quote = 1)
