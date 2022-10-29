from pyrogram import Client, filters, enums
import os
from PIL import Image
import imghdr


'''===========EDITABLES==========='''

preFix = "/"
cmds = ["stickerize", F"stickerize{os.getenv('BOT_UNAME')}"]
HELP = F"""Reply to a message containing an image
{preFix if preFix else os.getenv('MASTER_PREFIX', '/')}{cmds[0]} - converts the image to a telegram sticker"""

# {preFix if preFix else os.getenv('MASTER_PREFIX', '/')}{cmds[0]} any_text_here - converts the image to a telegram sticker resulting in a 512x512 square canvas"""

'''-------------------------------'''


command = lambda cmd: filters.command(cmd, prefixes = preFix if preFix else os.getenv('MASTER_PREFIX', '/'))

def delfiles(files_to_del: list):
  for x in files_to_del:
    if os.path.exists(x):
      os.remove(x)

def PNG_ResizeKeepTransparency(img, ResizedFile, new_width=512, new_height=512, resample="ANTIALIAS"):
  img = img.convert("RGBA")
  img.load()
  bands = img.split()
  resample = Image.ANTIALIAS
  bands = [b.resize((new_width, new_height), resample) for b in bands]
  img = Image.merge('RGBA', bands)
  img.save(ResizedFile)

def make_square(im, min_size=512, fill_color=(0, 0, 0, 0)):
  x, y = im.size
  size = max(min_size, x, y)
  new_im = Image.new('RGBA', (size, size), fill_color)
  new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
  return new_im

@Client.on_message(command(cmds))
async def stickerize(app, msg):
  if msg.reply_to_message:
    origMsg = msg.reply_to_message

    # File names
    fname = F"Stickerize{msg.chat.id}{msg.id}"
    global dl
    pngImg = F"{fname}.png" # PNG File
    resizedImg = F"{fname}_resized.png"
    stickerizedImg = F"{fname}.webp"
    filesToDel = [pngImg, resizedImg, stickerizedImg]
    
    if origMsg.photo or origMsg.document:
      # Handle non-image document files
      if origMsg.document and (not origMsg.document.mime_type.startswith("image/")):
          return await msg.reply('`ERROR: No image found in the message!`', quote = 1)

      await msg.reply_chat_action(enums.ChatAction.UPLOAD_PHOTO)
      rep = await msg.reply('`Uploading the image...\nPlease wait, you\'ll be notified after the upload!`', quote = 1)
      try:
        dl = await app.download_media(origMsg, file_name=fname)
        if dl:
          await rep.edit('`Upload successfull!\nConverting to sticker...\nPlease be patient, your file will be sent after conversion!`')
  
          # Determine and calculate required image details
          img = Image.open(dl)  # orig img obj
          ratio = min(512/float(img.size[0]), 512/float(img.size[1]))
          wsize = int(round(float(img.size[0]) * float(ratio)))
          hsize = int(round(float(img.size[1]) * float(ratio)))
  
          # Convert to PNG if not already
          # This conversion is performed in order to be able to open the image in RGBA mode later
          if imghdr.what(dl)!="png":
            img = img.convert("RGB")
            img.save(pngImg, "png")
            img = Image.open(pngImg)
  
          if len(msg.text.split())>1:
            img = make_square(img)
            PNG_ResizeKeepTransparency(img, resizedImg)
          else:
            PNG_ResizeKeepTransparency(img, resizedImg, wsize, hsize)
  
          # Convert to sticker
          img = Image.open(resizedImg).convert("RGBA")
          img.save(stickerizedImg, "webp")  # Sticker file
          await rep.edit("`Conversion successfull!\nSending the file...`")
  
          # Send sticker and perform cleanup
          await msg.reply_sticker(sticker = stickerizedImg, quote = 1)
          await rep.delete()
          filesToDel+=[dl if dl else ""]
          delfiles(filesToDel)
          
        else: return await rep.edit('`ERROR: Failed to upload the file!\nYou might retry!`')
      
      except Exception as e:
        filesToDel+=[dl if dl else ""]
        delfiles(filesToDel)
        return await rep.edit(F"ERROR:\n`{e}`")
        
    else: return await msg.reply('`ERROR: No image found in the message!`', quote = 1)
  else: return await msg.reply(F"Usage:\n`{HELP}`", quote = 1)
