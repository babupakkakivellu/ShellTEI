import asyncio
import time
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import os
from PIL import Image
from subprocess import run as srun


AUDIO_SUFFIXES = ("MP3", "M4A", "M4B", "FLAC", "WAV", "AIF", "OGG", "AAC", "DTS", "MID", "AMR", "MKA")
VIDEO_SUFFIXES = ("M4V", "MP4", "MOV", "FLV", "WMV", "3GP", "MPG", "WEBM", "MKV", "AVI")

def check_is_streamable(file_path:str) -> bool:
    return file_path.upper().endswith(VIDEO_SUFFIXES)

async def get_width_height(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("width") and metadata.has("height"):
      return metadata.get("width"), metadata.get("height")
    else:
      return 1280, 720

async def take_ss(video_file):
    des_dir = 'Thumbnails'
    if not os.path.exists(des_dir):
        os.mkdir(des_dir)
    des_dir = os.path.join(des_dir, f"{time.time()}.jpg")
    duration = await get_video_duration(video_file)
    if duration == 0:
        duration = 3
    duration = duration // 2
    status = await downloadaudiocli(["ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", str(duration),
                   "-i", video_file, "-frames:v", "1", des_dir])
    if not os.path.lexists(des_dir):
        return None
    with Image.open(des_dir) as img:
        img.convert("RGB").save(des_dir, "JPEG")
    return des_dir

async def downloadaudiocli(command_to_exec):
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE, )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    print("Download error:", e_response)
    return e_response, t_response

async def progress_for_pyrogram(
    current,
    total,
    ud_type,
    message,
    start,
    file_name
):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        # if round(current / total * 100, 0) % 5 == 0:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        comp = "▪️"
        ncomp = "▫️"
        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)
        pr = ""
        try:
            percentage=int(percentage)
        except:
            percentage = 0
        for i in range(1,11):
            if i <= int(percentage/10):
                pr += comp
            else:
                pr += ncomp
        progress = "{}: {}%\n[{}]\n".format(
            ud_type,
            round(percentage, 2),
            pr)

        tmp = progress + "{0} of {1}\nSpeed: {2}/sec\nETA: {3}\nfilename: `{4}`".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            # elapsed_time if elapsed_time != '' else "0 s",
            estimated_total_time if estimated_total_time != '' else "0 s",
            file_name
        )
        try:
            await message.edit(text=tmp)
        except Exception as e:
            pass


async def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T', 5: 'P', 6: 'E', 7: 'Z', 8: 'Y'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'

async def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]

async def get_video_duration(input_file):
    metadata = extractMetadata(createParser(input_file))
    total_duration = 0
    if metadata.has("duration"):
        total_duration = metadata.get("duration").seconds
    return total_duration
