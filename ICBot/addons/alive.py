from pyrogram import Client, filters


'''===========EDITABLES==========='''

preFix = "?"
cmds = ["alive"]
HELP = F"{preFix}{cmds[0]} - Replies if the bot is alive"

'''-------------------------------'''


command = lambda cmd: filters.command(cmd, prefixes = preFix)

@Client.on_message(command(cmds))
async def alive(_, msg):
  await msg.reply("Alive af!", quote = 1)