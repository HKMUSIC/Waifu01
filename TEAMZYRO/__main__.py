from TEAMZYRO import *
import importlib
import logging
from TEAMZYRO.modules import ALL_MODULES
from pyrogram import idle
import asyncio


# -------------------------------------------------
# LOAD ALL MODULES
# -------------------------------------------------
def load_modules():
    for module_name in ALL_MODULES:
        importlib.import_module("TEAMZYRO.modules." + module_name)
    LOGGER("TEAMZYRO.modules").info("All Modules Loaded Successfully.")


# -------------------------------------------------
# ASYNC MAIN FUNCTION
# -------------------------------------------------
async def start_bot():
    load_modules()

    await ZYRO.start()
    print("Bot Started Successfully!")

    LOGGER("TEAMZYRO").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎MADE BY GOJOXNETWORK☠︎︎\n╚═════ஜ۩۞۩ஜ════╝"
    )

    await idle()   # keep bot running


# -------------------------------------------------
# RUN ASYNCIO LOOP
# -------------------------------------------------
if __name__ == "__main__":
    asyncio.run(start_bot())
