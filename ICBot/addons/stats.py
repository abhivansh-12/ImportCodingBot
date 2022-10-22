from pyrogram import Client, filters


'''===========EDITABLES==========='''

preFix = "/" # Change this for a custom command prefix
cmds = ["serverstats"]
HELP = F"{preFix}{cmds[0]} - displays basic server stats"

'''-------------------------------'''


command = lambda cmd: filters.command(cmd, prefixes = preFix)

SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
def readable_file_size(size_in_bytes) -> str:
    if size_in_bytes is None:
        return '0B'
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f'{round(size_in_bytes, 2)}{SIZE_UNITS[index]}'
    except IndexError:
        return 'File too large'


@Client.on_message(command(cmds))
async def stats(_, msg):
  import shutil, psutil
  total, used, free = shutil.disk_usage('.')
  total = readable_file_size(total)
  used = readable_file_size(used)
  free = readable_file_size(free)
  sent = readable_file_size(psutil.net_io_counters().bytes_sent)
  recv = readable_file_size(psutil.net_io_counters().bytes_recv)
  cpuUsage = psutil.cpu_percent(interval=0.5)
  memory = psutil.virtual_memory().percent
  disk = psutil.disk_usage('/').percent
  stats = F"Total Disk Space: `{total}`\nUsed: `{used}`\nFree: `{free}`\n\nUpload: `{sent}`\nDownload: `{recv}`\n\nCPU: `{cpuUsage}%` | RAM: `{memory}%` | DISK: `{disk}%`"
  await msg.reply(stats, quote = 1)