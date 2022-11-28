from naff import (
    Extension,
    Embed,
    slash_command,
    InteractionContext,
    Member,
    slash_option,
    OptionTypes,
)
from naff.models.discord import color
import time
from dotenv import load_dotenv
import json
from millify import prettify
import os
import aiohttp
import datetime
import dateutil.relativedelta
import inflect


class Utilities(Extension):
    print("Utilities extension loaded")
    load_dotenv()

    @slash_command(name="ping", description="Check the bot's ping")
    async def ping(self, ctx: InteractionContext):
        start_time = time.perf_counter()
        ping_discord = round((self.bot.latency * 1000), 2)

        mes = await ctx.send(
            f"Pong!\n`{ping_discord}` ms from Discord.\nCalculating personal ping..."
        )

        end_time = time.perf_counter()
        ping_personal = round(((end_time - start_time) * 1000), 2)

        await ctx.edit(
            message=mes,
            content=(
                f"Pong!\n`{ping_discord}` ms from Discord.\n`{ping_personal}` ms"
                " personally."
            ),
        )

    @slash_command(name="game-stats", description="Check a player's game stats")
    @slash_option(
        name="user",
        description="The user you would like to check",
        opt_type=OptionTypes.USER,
    )
    async def game_stats(self, ctx: InteractionContext, user: Member = None):
        p = inflect.engine()
        if user is None:
            user = ctx.guild.get_member(ctx.author.id)
        IP = os.getenv("GAME_IP")
        url = f"http://{IP}/players/{user.display_name}"
        headers = {"secret": os.getenv("SECRET")}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as resp:
                content = await resp.text()
        if resp.status != 200:
            await ctx.send("Couldn't contact server")
            return
        stats = json.loads(content)
        try:
            if stats["error"]:
                return
        except:
            # Game time

            ts = int(str(datetime.datetime.now().timestamp()).split(".")[0])
            game_time = ts - int(stats["time"])
            dt1 = datetime.datetime.fromtimestamp(game_time)
            dt2 = datetime.datetime.fromtimestamp(ts)
            rd = dateutil.relativedelta.relativedelta(dt2, dt1)
            game_time = ""
            if rd.years != 0:
                game_time += f'{rd.years} {p.plural("year", rd.years)}, '
            if rd.months != 0:
                game_time += f'{rd.months} {p.plural("month", rd.months)}, '
            if rd.days != 0:
                game_time += f'{rd.days} {p.plural("day", rd.days)}, '
            if rd.hours != 0:
                game_time += f'{rd.hours} {p.plural("hour", rd.hours)}, '
            if rd.minutes != 0:
                game_time += f'{rd.minutes} {p.plural("minute", rd.minutes)}, '
            if rd.seconds != 0:
                game_time += f'{rd.seconds} {p.plural("second", rd.seconds)}'
            death_time = ts - int(stats["death"])
            dt1 = datetime.datetime.fromtimestamp(death_time)
            dt2 = datetime.datetime.fromtimestamp(ts)
            rd = dateutil.relativedelta.relativedelta(dt2, dt1)
            death_time = ""
            if rd.years != 0:
                death_time += f'{rd.years} {p.plural("year", rd.years)}, '
            if rd.months != 0:
                death_time += f'{rd.months} {p.plural("month", rd.months)}, '
            if rd.days != 0:
                death_time += f'{rd.days} {p.plural("day", rd.days)}, '
            if rd.hours != 0:
                death_time += f'{rd.hours} {p.plural("hour", rd.hours)}, '
            if rd.minutes != 0:
                death_time += f'{rd.minutes} {p.plural("minute", rd.minutes)}, '
            if rd.seconds != 0:
                death_time += f'{rd.seconds} {p.plural("second", rd.seconds)}'

            if stats["online"]:
                embed = Embed(
                    color=color.BrandColors.GREEN,
                    title=f"{user.display_name}'s current game stats",
                )
                last_online = "Now"
            else:
                embed = Embed(
                    color=color.BrandColors.RED,
                    title=f"{user.display_name}'s cached game stats",
                )
                last_online = f"<t:{str(stats['lastJoined'])[:-3]}:R>"
            embed.add_field(name="Time spent in game:", value=game_time, inline=True)
            embed.add_field(
                name="Time since last death:", value=death_time, inline=True
            )
            embed.add_field(name="Kills:", value=prettify(stats["kills"]), inline=True)
            embed.add_field(
                name="Deaths:", value=prettify(stats["deaths"]), inline=True
            )
            embed.add_field(
                name="XP level:", value=prettify(stats["level"]), inline=True
            )
            embed.add_field(name="Health:", value=stats["health"][:4], inline=True)
            embed.add_field(name="Hunger:", value=stats["food"][:4], inline=True)
            embed.add_field(
                name="Times jumped:", value=prettify(stats["jumps"]), inline=True
            )
            embed.add_field(name="World:", value=stats["world"], inline=True)
            # staff stuffs
            if ctx.channel.parent_id == 861041901921632276:
                embed.add_field(
                    name="IP:",
                    value=f"[{stats['address']}](https://iplocation.io/ip/{stats['address']} \"Click for more info\")",
                    inline=True,
                )
                embed.add_field(
                    name="UUID",
                    value=f"[{stats['uuid']}](https://namemc.com/profile/{stats['username']} \"Click for more info\")",
                    inline=True,
                )
                embed.add_field(
                    name="Gamemode:", value=stats["gamemode"].lower(), inline=True
                )
                embed.add_field(name="Bed location:", value=stats["bed"], inline=True)
                location = stats["location"].split(",")
                embed.add_field(
                    name="Their location:",
                    value=f"{location[0].split('.')[0]},{location[1].split('.')[0]},{location[2].split('.')[0]}",
                    inline=True,
                )
            embed.add_field(name="Last online:", value=last_online, inline=True)

            embed.set_thumbnail(
                url=f"https://heads.discordsrv.com/head.png?name={user.display_name}&overlay"
            )
            await ctx.send(embed=embed)


def setup(bot):
    Utilities(bot)
