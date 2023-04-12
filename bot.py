from pyrogram import *
import vars
import os
import sys
from time import time, strftime, gmtime
import time
import asyncio
from tu import humanbytes, progress_for_pyrogram, check_is_streamable, get_video_duration,  take_ss, TimeFormatter, get_width_height
from os import path as os_path

BLACKLISTED_EXTENSIONS = (".sex")

tony = Client(name="My Tony", api_id=vars.api_id, api_hash=vars.api_hash, bot_token=vars.bot_token)

@tony.on_message(filters.command('start') & filters.private)
def start(client, message):
    message.reply_text(text="welcome to Toon Encodes shell bot")
    print("Welcome to Toon Encodes bot")

@tony.on_message(filters.command('help') & filters.private)
def help(client, message):
    if help:
       message.reply_text(text="This Bot Is For @ToonEncodes Owner/Admin.")
    else:
       message.reply_text(text="No helps")

async def run_comman_d(command_list):
    process = await asyncio.create_subprocess_shell(
        command_list,
        # stdout ni access cheyadaniki pipe kavalli ra subprocess.pipe
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # idi kavalli zumka 
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    return e_response, t_response

@tony.on_message(filters.command('shell') & filters.private)
async def tg_s_Handler(client, message):
    cmd = message.text.split(' ', 1)
    sts = await message.reply_text("Excuting...")
    if len(cmd) == 1:
        return await sts.edit('**Send a command**')
    cmd = cmd[1]
    for check in cmd.split(" "):
        if check.upper().endswith(BLACKLISTED_EXTENSIONS):
            return await sts.edit("you can't execute this cmd, because you gey")
    reply = ''
    stderr, stdout = await run_comman_d(cmd)
    newstdout = ""
    for line in stdout.split("\n"):
        if not line.upper().endswith(BLACKLISTED_EXTENSIONS):
            newstdout += line + "\n"
    if len(newstdout) != 0:
        reply += f"<b>Stdout</b>\n<code>{newstdout}</code>\n"
    if len(stderr) != 0:
        reply += f"<b>Stderr</b>\n<code>{stderr}</code>\n"
    if len(reply) > 3000:
        with open('output.txt', 'w') as file:
            file.write(reply)
        with open('output.txt', 'rb') as doc:
            await message.reply_document(
                document=doc,
                caption=f"`{cmd}`")
            await sts.delete()
    elif len(reply) != 0:
        await sts.edit(reply)
    else:
        await sts.edit('Executed')

@tony.on_message(filters.command("tgup") & filters.private)
async def tg_up(client, message):
    sts_msg = await message.reply_text("Checking")
    try:
        input_str = message.text.split(" ", 1)[1]
    except:
        await message.reply_text("send along with file path")
        await sts_msg.delete()
        return
    await tg_up(input_str, message, sts_msg, False)

def tg_up(input_str, message, sts_msg, drm=True):
    if not os_path.exists(input_str):
        sts_msg.delete()
        message.reply_text(f"{input_str} File Is Not There In Path")
        return
    current_time = time.time()
    if os_path.exists(str(message.from_user.id) + ".jpg"):
        thumb = str(message.from_user.id) + ".jpg"
    else:
        thumb = None
    file_name = os_path.basename(input_str)
 
    if check_is_streamable(file_name):
        try:
            duration = get_video_duration(input_str)
        except:
            duration = None

    if thumb is None:
        thumb = take_ss(input_str)
        sent_msg = tony.send_video(chat_id=message.chat.id,
                                video=input_str,
                                  thumb=thumb,
                                  caption=f"<code>{filename}</code>",
                                  progress=progress_for_pyrogram,
                                  progress_args=("Uploading",
                                                 sts_msg,
                                                 current_time,

file_name))

                        
print("well starting up")
print("Bot started..")

tony.run()
