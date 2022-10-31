import os


'''===========EDITABLES==========='''

query = "uf"
HELP = F"""generates an unparsed/unformatted message from your text keeping all the characters intact

Inline Usage:
{os.getenv('BOT_UNAME')} {query} ~~Formatted~~ **text** __here__ ||Spoilers||
{os.getenv('BOT_UNAME')} {query} End the message with a 'tilde' symbol to disable web preview if your message contains any links like t.me/telegram ~"""

'''-------------------------------'''


# Inline method defined in inlineQHandler.py