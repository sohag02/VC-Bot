from vcbot.plugins import *
from vcbot import app, player, group_call
from pyrogram import idle
import importlib
import sys
from pathlib import Path
import glob



def load_plugins(plugin_name):
    path = Path(f"vcbot/plugins/{plugin_name}.py")
    name = "vcbot.plugins.{}".format(plugin_name)
    spec = importlib.util.spec_from_file_location(name, path)
    load = importlib.util.module_from_spec(spec)
    #load.logger = logging.getLogger(plugin_name)
    spec.loader.exec_module(load)
    sys.modules["vcbot.plugins." + plugin_name] = load


path = "vcbot/plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        load_plugins(plugin_name.replace(".py", ""))




async def run_bot():
    await app.start()
    print("Bot started")
    await player.start()
    print("Userbot started")
    await idle()

#group_call.run()
app.loop.run_until_complete(run_bot())