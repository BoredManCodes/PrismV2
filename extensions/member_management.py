from naff import (
    Extension,
    Permissions,
    Embed,
    utils,
    Color,
    InteractionContext,
    slash_option,
    slash_command,
    OptionTypes,
    Member,
    listen
)
from naff.models.discord import color
from naff.api.events import MemberUpdate


class MemberManagement(Extension):
    print("Member management extension loaded")
    
    @listen()
    async def on_member_update(self, event: MemberUpdate):
        if (
                event.before.guild.id == 858547359804555264
                and event.before.display_name != event.after.display_name
        ):
            embed = Embed(title=f"Changed Name")
            embed.add_field(name="User", value=event.before.mention)
            embed.add_field(name="Before", value=event.before.display_name)
            embed.add_field(name="After", value=event.after.display_name)
            embed.set_thumbnail(url=event.before.avatar.as_url())
            channel = self.bot.get_channel(897765157940396052)
            await channel.send(embed=embed)
        
                
    @slash_command(
        name="whitelist",
        description="Add a user to the whitelist",
        dm_permission=False,
        default_member_permissions=Permissions.KICK_MEMBERS,
    )
    @slash_option(
        name="user",
        description="the user you wish to whitelist",
        required=True,
        opt_type=OptionTypes.USER,
    )
    async def whitelist(self, ctx: InteractionContext, member: Member):
        role = utils.get(member.guild.roles, name="Whitelisted")
        await member.add_role(role)
        message = f"Added {member.mention} to the whitelist"
        embed = Embed(description=message, color=color.BrandColors.BLURPLE)
        embed.set_footer(
            text=f"Whitelisted by {ctx.author.display_name}",
            icon_url=ctx.author.avatar.as_url(),
        )
        embed.set_author(name="📋 User added to whitelist")
        await ctx.send(embed=embed)


def setup(bot):
    MemberManagement(bot)
