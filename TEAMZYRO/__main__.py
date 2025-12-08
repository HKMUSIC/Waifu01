from TEAMZYRO import *
import importlib
import logging
import asyncio
from TEAMZYRO.modules import ALL_MODULES


async def start_all():
    # Load modules
    for module_name in ALL_MODULES:
        importlib.import_module("TEAMZYRO.modules." + module_name)

    LOGGER("TEAMZYRO.modules").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 🥳")

    await ZYRO.start()  # Pyrogram async start

    asyncio.create_task(application.run_polling(drop_pending_updates=True))

    await send_start_message()   # PROPER await
    LOGGER("TEAMZYRO").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎MADE BY GOJOXNETWORK☠︎︎\n╚═════ஜ۩۞۩ஜ════╝"
    )


def main():
    asyncio.run(start_all())


if __name__ == "__main__":
    main()
