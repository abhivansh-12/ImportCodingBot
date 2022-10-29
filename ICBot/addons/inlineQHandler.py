from pyrogram import Client, enums
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent
from addons.gangsta import gangstafy


'''===========EDITABLES==========='''

queries = ["gangsta"]

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
  
  await queryObj.answer(results, cache_time=1)
