from naff import Task, IntervalTrigger, Extension, listen
from naff.api.events import MessageCreate
import re
import json

class MessageEvents(Extension):
    print("Message Events extension loaded")
    
    @listen()
    async def on_message_create(self, event = MessageCreate):
        # Auto reacts
        if "plugin" in event.message.content.lower():
            await event.message.add_reaction("<:cranky:870165423272886282>")
        if "bored" in event.message.content.lower():
            await event.message.add_reaction("<:koala:1051462428208152687>")
        if "koala" in event.message.content.lower():
            await event.message.add_reaction("<:koala:1051462428208152687>")
        if "mod" in event.message.content.lower():
            await event.message.add_reaction("<:cranky:870165423272886282>")
        if "orenge" in event.message.content.lower():
            await event.message.add_reaction("<:orenge_sad:1051462245596528670>")
        if "vanilla" in event.message.content.lower():
            await event.message.add_reaction("🍦")
        if "rat" in event.message.content.lower():
            await event.message.add_reaction("🐀")
    
def setup(bot):
    MessageEvents(bot)
