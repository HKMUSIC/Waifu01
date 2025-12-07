# TEAMZYRO/main.py
import asyncio
import importlib
from TEAMZYRO import *
from TEAMZYRO.modules import ALL_MODULES
import inspect
import traceback


async def safe_call(func):
    """Runs send_start_message safely whether async or sync."""
    try:
        result = func()
        if inspect.isawaitable(result):
            await result
    except Exception:
        print("\n--- send_start_message ERROR ---")
        traceback.print_exc()


async def start_bot():
    # ---------------- Load all modules ----------------
    for module_name in ALL_MODULES:
        importlib.import_module(f"TEAMZYRO.modules.{module_name}")

    LOGGER("TEAMZYRO.modules").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚𝐛𝐲🥳...")

    # ---------------- Start Pyrogram ----------------
    try:
        await ZYRO.start()
        LOGGER("TEAMZYRO").info("Pyrogram (ZYRO) started.")
    except Exception as e:
        LOGGER("TEAMZYRO").error(f"Pyrogram start failed: {e}")
        traceback.print_exc()

    # ---------------- Start PTB ----------------
    try:
        await application.initialize()
        await application.start()
        LOGGER("TEAMZYRO").info("PTB Application started.")

        await application.updater.start_polling(drop_pending_updates=True)
        LOGGER("TEAMZYRO").info("PTB Polling started.")
    except Exception as e:
        LOGGER("TEAMZYRO").error(f"PTB start failed: {e}")
        traceback.print_exc()

    # ---------------- send_start_message (safe) ----------------
    await safe_call(send_start_message)

    LOGGER("TEAMZYRO").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎MADE BY GOJOXNETWORK☠︎︎\n╚═════ஜ۩۞۩ஜ════╝"
    )

    # Keep running forever
    await asyncio.Event().wait()


def main():
    asyncio.run(start_bot())


if __name__ == "__main__":
    main()
