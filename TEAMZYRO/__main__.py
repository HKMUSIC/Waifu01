# TEAMZYRO/__main__.py
from TEAMZYRO import *
import importlib
import logging
from TEAMZYRO.modules import ALL_MODULES
import asyncio
import inspect
import traceback

# ---------- safe wrapper for startup message ----------
async def safe_call(func, *args, **kwargs):
    """
    Call func which may be sync or async. Never raise (logs exceptions).
    """
    try:
        result = func(*args, **kwargs)
        if inspect.isawaitable(result):
            try:
                await result
            except Exception as e:
                print("[Startup - awaited func error]", e)
                traceback.print_exc()
        else:
            # sync call returned fine
            pass
    except Exception as e:
        print("[Startup - call raised]", e)
        traceback.print_exc()

# ---------- main startup ----------
async def start_all():
    # 1) load modules
    for module_name in ALL_MODULES:
        importlib.import_module("TEAMZYRO.modules." + module_name)
    LOGGER("TEAMZYRO.modules").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚𝐛𝐲🥳...")

    # 2) start pyrogram (ZYRO)
    try:
        await ZYRO.start()
        LOGGER("TEAMZYRO").info("ZYRO (Pyrogram) started.")
    except Exception as e:
        LOGGER("TEAMZYRO").error(f"Failed to start ZYRO: {e}")
        traceback.print_exc()

    # 3) run send_start_message safely (handles sync/async)
    await safe_call send_start_message()

    # 4) initialize & start python-telegram-bot (application) in same loop
    try:
        await application.initialize()
        await application.start()
        LOGGER("TEAMZYRO").info("PTB application initialized & started.")
        # start polling (async)
        await application.updater.start_polling(drop_pending_updates=True)
        LOGGER("TEAMZYRO").info("PTB polling started.")
    except Exception as e:
        LOGGER("TEAMZYRO").error(f"Failed to start PTB application: {e}")
        traceback.print_exc()

    # 5) keep the process alive
    await asyncio.Event().wait()


def main():
    asyncio.run(start_all())


if __name__ == "__main__":
    main()
