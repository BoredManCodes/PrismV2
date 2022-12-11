from naff import Extension, Embed, listen, utils, Task, IntervalTrigger
from naff.api.events import MemberAdd, Ready, MemberRemove
from naff.models.discord import color
import random
import time
import datetime

class MemberJoinAndLeave(Extension):
    print("Member join and leave extension loaded")

    @listen()
    async def on_member_remove(self, event: MemberRemove):
        if (
            event.member.guild.id == 858547359804555264
        ):  # Only detect if the user left the Prism guild
            if event.member.bot:
                return
            else:
                messages = [
                    f"Goodbye {event.member.display_name}",
                    f"It appears {event.member.display_name} has left",
                    f"{event.member.display_name} has disappeared :(",
                    f"We wish {event.member.display_name} well in their travels",
                    f"Toodles {event.member.display_name}!",
                    f"{event.member.display_name} found love elsewhere :(",
                    f"{event.member.display_name} left\nSee you later alligator",
                    f"{event.member.display_name} left\nBye Felicia",
                    f"{event.member.display_name} left\nSo long, and thanks for all the fish!",
                    f"{event.member.display_name} left\nGoodbye, Vietnam! That’s right, I’m history, I’m outta here",
                ]
                general = self.bot.get_channel(858547359804555267)
                await general.send(random.choice(messages))
                channel = self.bot.get_channel(897765157940396052)
                title = f"{event.member.display_name} left the server"
                embed = Embed(title=title, color=color.BrandColors.RED)
                embed.set_footer(
                    text=f"Discord name: {event.member.display_name}\nDiscord ID: {event.member.id}",
                    icon_url=event.member.avatar.as_url(),
                )
                date_format = "%a, %d %b %Y %I:%M %p"
                embed.set_author(
                    name=str(event.member), icon_url=event.member.avatar.as_url()
                )
                embed.set_thumbnail(url=event.member.avatar.as_url())
                embed.add_field(
                    name="Joined Server",
                    value=event.member.joined_at.strftime(date_format),
                    inline=False,
                )
                embed.add_field(
                    name="Joined Discord",
                    value=event.member.created_at.strftime(date_format),
                    inline=False,
                )
                embed.set_footer(text="ID: " + str(event.member.id))
                await channel.send(embed=embed)

    @listen()
    async def on_member_add(self, event: MemberAdd):
        if (
            event.member.guild.id == 858547359804555264
        ):  # Only detect if the user joined the Prism guild
            if event.member.bot:  # Bloody bots
                return
            else:
                if time.time() - event.member.created_at.timestamp() < 2592000:
                    # Send a message to the mods
                    mod_log = self.bot.get_channel(897765157940396052)
                    title = f"{event.member.display_name} is potentially suspicious"
                    embed = Embed(title=title, color=color.BrandColors.RED)
                    embed.set_footer(
                        text=f"Discord name: {event.member.display_name}\nDiscord ID: {event.member.id}",
                        icon_url=event.member.avatar.as_url(),
                    )
                    date_format = "%a, %d %b %Y %I:%M %p"
                    embed.set_thumbnail(
                        url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Warning.svg/1200px-Warning.svg.png"
                    )
                    embed.add_field(
                        name="Joined Discord",
                        value=event.member.created_at.strftime(date_format),
                        inline=False,
                    )
                    await mod_log.send(embed=embed)
                else:
                    # Send a message to the mods
                    mod_log = self.bot.get_channel(897765157940396052)
                    title = f"{event.member.display_name} joined the server"
                    embed = Embed(title=title, color=color.BrandColors.GREEN)
                    embed.set_footer(
                        text=f"Discord name: {event.member.display_name}\nDiscord ID: {event.member.id}",
                        icon_url=event.member.avatar.as_url(),
                    )
                    date_format = "%a, %d %b %Y %I:%M %p"
                    embed.add_field(
                        name="Joined Discord",
                        value=event.member.created_at.strftime(date_format),
                        inline=False,
                    )
                    embed.set_thumbnail(url=event.member.avatar.as_url())
                    await mod_log.send(embed=embed)
                # Give the user the New Member role
                role = utils.get(event.member.guild.roles, name="New Member")
                await event.member.add_role(role)
                # Send the welcome banner
                channel = self.bot.get_channel(858547359804555267)
                messages = [
                    f"Welcome {event.member.display_name}",
                    f"Hi {event.member.display_name}!",
                    f"{event.member.display_name} joined us",
                    f"{event.member.display_name} is *one of us*",
                    f"Hoi {event.member.display_name}",
                    f"{event.member.display_name} is here!",
                    f"Welcome to the party {event.member.display_name}",
                    f"Hey `@everyone` {event.member.display_name} joined Prism",
                ]
                await channel.send(
                    f"{random.choice(messages)}\nIf you need anything from staff or simply have questions, ping a <@&858547638719086613>"
                )
        # elif event.member.guild.id == 861018927752151071:

    @Task.create(IntervalTrigger(hours=2))
    async def prismian_upgrade_check(self):
        print("Checking for Prismian upgrades")
        guild = self.bot.get_guild(858547359804555264)
        for member in guild.members:
            prismian_role = utils.get(guild.roles, name="Prismian")
            new_role = utils.get(guild.roles, name="New Member")
            general = self.bot.get_channel(858547359804555267)
            if prismian_role not in member.roles and new_role in member.roles:
                duration = datetime.datetime.now(tz=datetime.timezone.utc) - member.joined_at
                hours, remainder = divmod(int(duration.total_seconds()), 3600)
                days, hours = divmod(hours, 24)
                if days >= 14:
                    mod_log = self.bot.get_channel(897765157940396052)
                    await mod_log.send(
                        f"{member.display_name} has been a new member for {days} days and upgraded to Prismian today!"
                    )
                    await member.remove_role(new_role)
                    await member.add_role(prismian_role)
                    await general.send(
                        "https://cdn.discordapp.com/attachments/861289278374150164/934758089075355708/party-popper-joypixels.gif"
                    )
                    await general.send(
                        f"{member.mention} congrats on upgrading from New Member to Prismian today!"
                    )
                    print(f"{member.display_name} has been upgraded to Prismian")
        print("Done checking for Prismian upgrades")

    @listen()
    async def on_ready(self):
        print("Started prismian upgrade loop")
        try:
            await self.prismian_upgrade_check.start()
        except TypeError:
            print("Error? What error? I see nothing wrong here...")
            pass

def setup(bot):
    MemberJoinAndLeave(bot)
