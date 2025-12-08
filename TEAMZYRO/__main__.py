import asyncio
import importlib
from TEAMZYRO import ZYRO, application, LOGGER
from TEAMZYRO.modules import ALL_MODULES


OWNER_ID = 7553434931
LOG_CHAT = -1002792716047


async def send_start_message():
    """
    Sends start messages AFTER both bots have started.
    """
    try:
        await ZYRO.send_message(
            OWNER_ID,
            "✅ **Bot Started Successfully!**\nAll systems are running smoothly."
        )

        await ZYRO.send_message(
            LOG_CHAT,
            "🚀 **TEAMZYRO Bot Started!**\nAll modules loaded without errors."
        )

        LOGGER("TEAMZYRO").info("Start messages sent successfully.")

    except Exception as e:
        LOGGER("TEAMZYRO").error(f"Error in send_start_message: {e}")


async def start_all():
    """
    Loads modules, starts Pyrogram & PTB in async-safe way.
    """

    # Load all modules
    for module_name in ALL_MODULES:
        importlib.import_module("TEAMZYRO.modules." + module_name)

    LOGGER("TEAMZYRO.modules").info("🔥 All Features Loaded Successfully!")

    # Start Pyrogram bot
    await ZYRO.start()

    # Start PTB (async safe)
    asyncio.create_task(application.run_polling(drop_pending_updates=True))

    # Send start messages
    await send_start_message()

    LOGGER("TEAMZYRO").info(
        "╔═════ஜ۩۞۩ஜ════╗\n"
        "  ☠︎︎ MADE BY GOJOXNETWORK ☠︎︎\n"
        "╚═════ஜ۩۞۩ஜ════╝"
    )


def main():
    asyncio.run(start_all())


if __name__ == "__main__":
    main()
