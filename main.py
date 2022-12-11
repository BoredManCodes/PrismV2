from naff import Client, Intents, listen
from dotenv import load_dotenv
import os

bot = Client(
    intents=Intents.DEFAULT
    | Intents.GUILD_MEMBERS
    | Intents.PRIVILEGED
    | Intents.ALL
    | Intents.MESSAGES,
    delete_unused_application_cmds=True,
)
load_dotenv()


@listen()
async def on_ready():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


bot.load_extension("extensions.member_join_and_leave")
bot.load_extension("extensions.member_management")
bot.load_extension("extensions.utilities")
bot.load_extension("extensions.message_events")
bot.start(os.getenv("DISCORD_TOKEN"))
