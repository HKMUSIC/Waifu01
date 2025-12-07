# TEAMZYRO/main.py
import asyncio
import importlib
from TEAMZYRO import *
from TEAMZYRO.modules import ALL_MODULES


async def start_bot():
    # Load modules
    for module_name in ALL_MODULES:
        importlib.import_module(f"TEAMZYRO.modules.{module_name}")

    LOGGER("TEAMZYRO.modules").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚𝐛𝐲🥳...")

    # Start Pyrogram
    await ZYRO.start()
    LOGGER("TEAMZYRO").info("Pyrogram (ZYRO) started.")

    # Start PTB
    await application.initialize()
    await application.start()
    await application.updater.start_polling(drop_pending_updates=True)
    LOGGER("TEAMZYRO").info("PTB Polling started.")

    # ---------------------------
    # NO send_start_message here
    # ---------------------------

    LOGGER("TEAMZYRO").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎MADE BY GOJOXNETWORK☠︎︎\n╚═════ஜ۩۞۩ஜ════╝"
    )

    await asyncio.Event().wait()


def main():
    asyncio.run(start_bot())


if __name__ == "__main__":
    main()
