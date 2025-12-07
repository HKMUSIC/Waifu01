from TEAMZYRO import *
import importlib
import logging
from TEAMZYRO.modules import ALL_MODULES
from pyrogram import idle
import asyncio


def main() -> None:
    for module_name in ALL_MODULES:
        imported_module = importlib.import_module("TEAMZYRO.modules." + module_name)
    LOGGER("TEAMZYRO.modules").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚𝐛𝐲🥳...")


async def main():
    await ZYRO.start()
    print("Bot started!")
    await idle()   # keeps event loop alive safely

asyncio.run(main())

    application.run_polling(drop_pending_updates=True)
    send_start_message()
    LOGGER("TEAMZYRO").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎MADE BY GOJOXNETWORK☠︎︎\n╚═════ஜ۩۞۩ஜ════╝"
    )

if __name__ == "__main__":
    main()
    
    
