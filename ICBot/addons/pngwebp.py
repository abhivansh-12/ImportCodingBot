from pyrogram import Client, filters, enums
import os
from PIL import Image


'''===========EDITABLES==========='''

preFix = "/"
cmds = ["png", F"png{os.getenv('BOT_UNAME')}", "webp", F"webp{os.getenv('BOT_UNAME')}"]
HELP = F"""Reply to a message containing an image
{preFix if preFix else os.getenv('MASTER_PREFIX', '/')}{cmds[0]} - converts the image to a PNG file
{preFix if preFix else os.getenv('MASTER_PREFIX', '/')}{cmds[2]} - converts the image to a WEBP file"""

'''-------------------------------'''


command = lambda cmd: filters.command(cmd, prefixes = preFix if preFix else os.getenv('MASTER_PREFIX', '/'))

def delfiles(files_to_del: list):
  for x in files_to_del:
    if os.path.exists(x):
      os.remove(x)

@Client.on_message(command(cmds))
async def pngwebp(app, msg):
  if msg.reply_to_message:
    origMsg = msg.reply_to_message

    # File names
    global dl
    if msg.text.split()[0][1:] in cmds[0:2]:
      imgExtension = "png"
    if msg.text.split()[0][1:] in cmds[2:4]:
      imgExtension = "webp"
    fname = F"{imgExtension}{msg.chat.id}{msg.id}"
    convertedImg = F"{fname}.{imgExtension}"
    
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
        dl = await app.download_media(origMsg, file_name=fname)
        if dl:
          await rep.edit('`Upload successfull!\nConverting...\nPlease be patient, your file will be sent after conversion!`')
  
          # Convert to PNG/WEBP
          img = Image.open(dl).convert("RGBA")
          img.save(convertedImg, imgExtension)
          await rep.edit("`Conversion successfull!\nSending the file...`")
  
          # Send converted file and perform cleanup
          if imgExtension=="webp":
            await msg.reply_sticker(sticker = convertedImg, quote = 1)
          else:
            await msg.reply_photo(photo = convertedImg, quote = 1)
          await msg.reply_document(document = convertedImg, quote = 1, force_document = 1)
          await rep.delete()
          delfiles([dl if dl else "", convertedImg])
          
        else: return await rep.edit('`ERROR: Failed to upload the file!\nYou might retry!`')
      
      except Exception as e:
        delfiles([dl if dl else "", convertedImg])
        return await rep.edit(F"ERROR:\n`{e}`")

    else: return await msg.reply('`ERROR: No image found in the message!`', quote = 1)
  else: return await msg.reply(F"Usage:\n`{HELP}`", quote = 1)
