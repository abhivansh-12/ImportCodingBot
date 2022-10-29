from pyrogram import Client, enums
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent
from addons.gangsta import gangstafy


'''===========EDITABLES==========='''

queries = ["gangsta", "uf"] # Append any more inline query prefixes here

'''-------------------------------'''


@Client.on_inline_query()
async def inlineQHandler(_, queryObj):
  query = queryObj.query
  if not query: return
  results=[]

  # gangsta
  if query.split()[0]==queries[0]:
    oText = query.split(maxsplit=1)[1]
    gText = gangstafy(oText)
    results.append(
      InlineQueryResultArticle(
        title=gText,
        input_message_content=InputTextMessageContent(gText, parse_mode=enums.ParseMode.DISABLED)
      )
    )

  # uf
  if query.split()[0]==queries[1]:
    text = query.split(maxsplit=1)[1]
    disablePrev=text.endswith("~")
    if disablePrev:text=text[:-1]
    results.append(
      InlineQueryResultArticle(
        title="Send unformatted text",
        input_message_content=InputTextMessageContent(text, parse_mode=enums.ParseMode.DISABLED, disable_web_page_preview=disablePrev)
      )
    )

  # new_query
  # if query.split()[0]==queries[Index_Of_Your_Query]:
  #   results.append(Results_of_the_query)

  await queryObj.answer(results, cache_time=1)
