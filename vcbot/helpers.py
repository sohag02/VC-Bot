import ffmpeg
import pafy
from pyrogram.types import Message
import wget
import os
import asyncio


def transcode(filename: str):
    out_file = f"{filename}.raw"
    a= ffmpeg.input(filename).output(
        f"{filename}.raw",
        format="s16le",
        acodec="pcm_s16le",
        ac=2,
        ar="48k",
        loglevel="error",
    ).overwrite_output().run_async()
    #os.remove(filename)
    return out_file


def show_progress(message : Message):
    pass
  

def download_song(url, message : Message, thumnail = True, service="youtube"):

    def progress_pyro(current, total, width=80):
        progress_msg = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
        asyncio.ensure_future(message.edit(progress_msg))
        #asyncio.sleep(1)

    video = pafy.new(url)

    title = video.title
    thum = video.thumb
    length = video.duration

    if thumnail == True:
        thum_path = wget.download(thum, f"songs/{title}.jpg", bar=progress_pyro)
    else:
        thum_path = None

    audio = video.getbestaudio()
    path = wget.download(audio.url, out = f"songs/{title}.mp3")
    caption = f"Tittle : {title}\nlength : {length}"

    return path, thum_path, title, length, caption


def download_and_transcode(url, message : Message):
    path, thum, title, length, caption = download_song(url, message,thumnail=False)
    raw_file = transcode(path)
    return raw_file, title, length

async def run_async(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, func, *args, **kwargs)