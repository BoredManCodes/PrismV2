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
)
from naff.models.discord import color


class MemberManagement(Extension):
    print("Member management extension loaded")

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
