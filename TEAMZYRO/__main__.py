from TEAMZYRO import *
import importlib
import logging
from TEAMZYRO.modules import ALL_MODULES
from pyrogram import idle
import asyncio


# ---- LOAD ALL MODULES ----
def load_modules():
    for module_name in ALL_MODULES:
        importlib.import_module("TEAMZYRO.modules." + module_name)
    LOGGER("TEAMZYRO.modules").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚𝐛𝐲🥳...")


# ---- START BOT (PYROGRAM) ----
async def start_bot():
    load_modules()

    await ZYRO.start()
    LOGGER("TEAMZYRO").info("Bot started successfully!")

    await idle()               # keeps bot alive
    await ZYRO.stop()


if __name__ == "__main__":
    asyncio.run(start_bot())
