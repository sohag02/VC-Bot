import ffmpeg
import pafy
from pyrogram.raw.types import InputGroupCall
# from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.phone import EditGroupCallTitle
import wget
import asyncio
from vcbot import player, group_call


async def change_vc_title(title: str):
    # peer = await player.resolve_peer(Config.CHAT_ID)
    # chat = await player.send(GetFullChannel(channel=peer))
    call = InputGroupCall(id=group_call.group_call.id, access_hash=group_call.group_call.access_hash)
    data = EditGroupCallTitle(call=call, title=title)
    
    await player.send(data)


def transcode(filename: str):
    out_file = f"{filename}.raw"
    a= ffmpeg.input(filename).output(
        f"{filename}.raw",
        format="s16le",
        acodec="pcm_s16le",
        ac=2,
        ar="48k",
        loglevel="error",
    ).overwrite_output().run()
    #os.remove(filename)
    return out_file
  

def download_song(url, thumnail = True, service="youtube"):

    # def progress_pyro(current, total, width=80):
    #     progress_msg = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
    #     asyncio.ensure_future(message.edit(progress_msg))
    #     #asyncio.sleep(1)

    video = pafy.new(url)

    title = video.title
    thum = video.thumb
    length = video.duration

    if thumnail == True:
        thum_path = wget.download(thum, f"songs/{title}.jpg")
    else:
        thum_path = None

    audio = video.getbestaudio()
    path = wget.download(audio.url, out = f"songs/{title}.mp3")
    caption = f"Tittle : {title}\nlength : {length}"

    return path, thum_path, title, length, caption


def download_and_transcode(url):
    path, thum, title, length, caption = download_song(url, thumnail=False)
    raw_file = transcode(path)
    return raw_file, title, length

async def run_async(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, func, *args, **kwargs)