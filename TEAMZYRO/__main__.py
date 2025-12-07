from TEAMZYRO import *
import importlib
import logging
from TEAMZYRO.modules import ALL_MODULES
import asyncio


async def safe_send_start_message():
    """Start message ko crash-free banata hai."""
    try:
        await send_start_message()
    except Exception as e:
        print(f"[Start Message Error] {e}")


async def start_all():
    # 1. Load all modules
    for module_name in ALL_MODULES:
        importlib.import_module("TEAMZYRO.modules." + module_name)

    LOGGER("TEAMZYRO.modules").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚𝐛𝐲🥳...")

    # 2. Start Pyrogram (no crash)
    await ZYRO.start()

    # 3. Send start message safely
    await safe_send_start_message()

    # 4. Start python-telegram-bot safely (NO threading, NO executor)
    await application.initialize()
    await application.start()
    await application.updater.start_polling(drop_pending_updates=True)

    # 5. Keep bot running forever
    await asyncio.Event().wait()


def main():
    asyncio.run(start_all())


if __name__ == "__main__":
    main()
