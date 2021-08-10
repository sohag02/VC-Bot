from vcbot import app, group_call, is_admin, vcstatus
from pyrogram import filters
from pyrogram.types import Message
from helpers import run_async, download_and_transcode, transcode, change_vc_title
from .music_control import playlist
from youtubesearchpython import VideosSearch
import signal
from .radio import FFMPEG_PROCESSES




@app.on_message(filters.regex("^/play"))
@is_admin()
async def play(client, message : Message):
    if vcstatus["call"] == "radio":
        group_call.stop_playout()
        process = FFMPEG_PROCESSES.get(message.chat.id)

        if process:
            process.send_signal(signal.SIGTERM)
        await message.reply("Radio Stoped!")

    # if vcstatus["call"] == "not started":
    #     await group_call.start(Config.CHAT_ID)
        
    if message.reply_to_message:
        service = "telegram"
    else:
        service = "youtube"
    if service == "youtube":
        msg = await message.reply("Searching...")
        try:
            link = message.text.replace("/play", "")
        except:
            await message.edit("Provide a valid url or song name to play or reply to a file")
            return

        if "www.youtube.com" in link:
            await msg.edit("Downloading...")
            file, title, length = await run_async(download_and_transcode, link)
            if len(playlist) > 0:
                playlist.append(file)
                print(file)
            elif len(playlist) == 0:
                playlist.append(file)
                group_call.input_filename = file
                print("playing : ", group_call.input_filename)

            pos = playlist.index(file)
            await msg.delete()
            await message.reply(f"Added to playlist at no. {pos + 1}!")
            print("\n" + file)
        else:
            src = VideosSearch(link, limit=1)
            await msg.edit("Downloading...")
            u = "https://www.youtube.com/watch?v=" + src.result()['result'][0]['id']
            file, title, length = await run_async(download_and_transcode, u)
            if len(playlist) > 0:
                playlist.append(file)
                print(file)
            elif len(playlist) == 0:
                playlist.append(file)
                group_call.input_filename = file
                print("\nplaying : ", file)
                
            pos = playlist.index(file)
            await msg.delete()
            await message.reply(f"Added to playlist at no. {pos + 1}!")
            print("\n" + file)

    else:
        msg = await message.reply("Downloading...")
        path = message.reply_to_message.download("song.mp3")

        file = run_async(transcode, path)
        if len(playlist) > 0:
                playlist.append(file)
                print(file)
        elif len(playlist) == 0:
            playlist.append(file)
            group_call.input_filename = file
            print("\nplaying : ", file)
                
        pos = playlist.index(file)
        await msg.edit(f"Added to playlist at no. {pos + 1}!")
        print("\n" + file)
    ta = group_call.input_filename.replace("songs/", "")
    tb = ta.replace(".mp3.raw", "")
    await change_vc_title(tb)
    