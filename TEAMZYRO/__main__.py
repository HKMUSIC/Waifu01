import asyncio
import importlib
from TEAMZYRO import *
from TEAMZYRO.modules import ALL_MODULES
import logging


async def start_all():
    # Load modules
    for module_name in ALL_MODULES:
        importlib.import_module("TEAMZYRO.modules." + module_name)

    LOGGER("TEAMZYRO.modules").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 🥳")

    # Start Pyrogram
    await ZYRO.start()

    # Start python-telegram-bot in async mode
    await application.initialize()
    await application.start()
    await application.updater.start_polling(drop_pending_updates=True)

    # Send start message
    await send_start_message()

    LOGGER("TEAMZYRO").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎MADE BY GOJOXNETWORK☠︎︎\n╚═════ஜ۩۞۩ஜ════╝"
    )

    # Keep the bot running forever
    await asyncio.Event().wait()


def main():
    asyncio.run(start_all())


if __name__ == "__main__":
    main()
