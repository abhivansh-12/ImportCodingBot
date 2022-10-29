from pyrogram import Client, filters, enums
import os
from PIL import Image


'''===========EDITABLES==========='''

preFix = "/"
cmds = ["fliph", F"fliph{os.getenv('BOT_UNAME')}", "flipv", F"flipv{os.getenv('BOT_UNAME')}"]
HELP = F"""Reply to a message containing an image
{preFix if preFix else os.getenv('MASTER_PREFIX', '/')}{cmds[0]} - flips image horizontally
{preFix if preFix else os.getenv('MASTER_PREFIX', '/')}{cmds[2]} - flips image vertically"""

'''-------------------------------'''


command = lambda cmd: filters.command(cmd, prefixes = preFix if preFix else os.getenv('MASTER_PREFIX', '/'))

def delfiles(files_to_del: list):
  for x in files_to_del:
    if os.path.exists(x):
      os.remove(x)

@Client.on_message(command(cmds))
async def imgflip(app, msg):
  if msg.reply_to_message:
    origMsg = msg.reply_to_message

    # File names
    dl, fname = "", ""
    
    if origMsg.photo or origMsg.sticker or origMsg.document:
      # Handle non-image document files
      if origMsg.document and (not origMsg.document.mime_type.startswith("image/")):
        return await msg.reply('`ERROR: No image found in the message!`', quote = 1)
      # Handle animated/video stickers
      if origMsg.sticker and (origMsg.sticker.is_animated or origMsg.sticker.is_video):
        return await msg.reply('`ERROR: Animated/Video stickers can\'t be processed!`', quote = 1)

      await msg.reply_chat_action(enums.ChatAction.UPLOAD_PHOTO)
      rep = await msg.reply('`Uploading the image...\nPlease wait, you\'ll be notified after the upload!`', quote = 1)
      try:
        dl = await app.download_media(origMsg)
        if dl:
          await rep.edit('`Upload successfull!\nFlipping...\nPlease be patient, your file will be sent after processing!`')
  
          # Flip the image
          img = Image.open(dl)
          extension = img.format.lower()
          if msg.text.split()[0][1:] in cmds[0:2]:
            fname = F"FlipH{msg.chat.id}{msg.id}.{extension}"
            flipped = img.transpose(Image.FLIP_LEFT_RIGHT)
          if msg.text.split()[0][1:] in cmds[2:4]:
            fname = F"FlipV{msg.chat.id}{msg.id}.{extension}"
            flipped = img.transpose(Image.FLIP_TOP_BOTTOM)
          flipped.save(fname, extension)
          await rep.edit("`Flipped the image successfully!\nSending the file...`")
  
          # Send flipped file and perform cleanup
          if origMsg.sticker:
            await msg.reply_sticker(sticker = fname, quote = 1)
          elif origMsg.photo:
            await msg.reply_photo(photo = fname, quote = 1 )
          else:
            await msg.reply_document(document = fname, quote = 1)
          await rep.delete()
          delfiles([dl, fname])
        else: return await rep.edit('`ERROR: Failed to upload the file!\nYou might retry!`')
      
      except Exception as e:
        delfiles([dl, fname])
        return await rep.edit(F"ERROR:\n`{e}`")

    else: return await msg.reply('`ERROR: No image found in the message!`', quote = 1)
  else: return await msg.reply(F"Usage:\n`{HELP}`", quote = 1)
