from TEAMZYRO import *
import importlib
import logging
import asyncio
from TEAMZYRO.modules import ALL_MODULES


async def start_all():
    # Load all modules
    for module_name in ALL_MODULES:
        importlib.import_module("TEAMZYRO.modules." + module_name)

    LOGGER("TEAMZYRO.modules").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 🥳")

    # Start Pyrogram first
    await ZYRO.start()
    LOGGER("TEAMZYRO").info("Pyrogram started ✔")

    # ------- PTB 20+ Async Mode -------
    await application.initialize()   # NO LOOP START/STOP
    await application.start()        # Safe start
    await application.updater.start_polling()  # Safe polling WITHOUT touching event-loop
    LOGGER("TEAMZYRO").info("PTB polling started ✔")

    # Start message
    try:
        await send_start_message()
    except Exception as e:
        LOGGER("TEAMZYRO").warning(f"Start message error: {e}")

    LOGGER("TEAMZYRO").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎MADE BY GOJOXNETWORK☠︎︎\n╚═════ஜ۩۞۩ஜ════╝"
    )

    # Keep bot alive
    await asyncio.Event().wait()


def main():
    asyncio.run(start_all())


if __name__ == "__main__":
    main()
