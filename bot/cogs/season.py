"""Season cog."""

from datetime import datetime

import discord
from discord.ext import commands

from bot import utils


class Season(commands.Cog):
    """All of the commands that assist with verification seasons."""

    def __init__(self, bot):
        self.bot = bot
        self.rank_roles = {
            "Under S": 0x1AB46A,
            "S Rank": 0x6A1EC1,
            "Low S+": 0xCD2D7E,
            "High S+": 0xED580B,
            "Low X": 0xDB7821,
        }

    @commands.has_role("Baristas")
    @commands.group(invoke_without_command=True, aliases=["verify", "verification"])
    async def season(self, ctx):
        """Command group for managing verification seasons."""
        await ctx.invoke(self.list)

    @commands.has_role("Baristas")
    @commands.command(aliases=["list", "view"])
    async def roles(self, ctx):
        """List all of the current verification season roles."""
        rank_roles = await self.get_rank_roles(ctx)

        await ctx.send(embed=utils.Embed(
            title="Current season roles:",
            description=utils.Embed.list(role.mention for role in rank_roles)
        ))

    @commands.has_role("Baristas")
    @commands.command(aliases=["start", "open", "create"])
    async def new(self, ctx, season: str, delete: bool = False):
        """Create new roles for a new season.

        `season` - The season name, if it's the name of a season (such as "winter"), it will be converted to an emoji.
            Otherwise, the name will be used directly.
        `delete` - Whether the old season roles should be deleted, defaults to `no`.
        """
        if delete:
            await ctx.invoke(self.end)

        async with ctx.typing():
            verified = await self.get_verified_role(ctx)
            rank_roles = []
            for rank, color in self.rank_roles.items():
                season_name = {
                    "spring": "🌱",
                    "summer": "🌻",
                    "fall": "🍂",
                    "autumn": "🍂",
                    "winter": "❄️",
                }.get(season.lower(), season)
                name = f"{rank} ({season_name} '{str(datetime.now().year)[2:]})"
                rank_roles.append(await ctx.guild.create_role(
                    name=name,
                    color=color,
                    reason="Creating new season roles"
                ))
                await rank_roles[-1].edit(position=verified.position)

        await ctx.send(embed=utils.Embed(
            title="Created new season roles!",
            description=utils.Embed.list([role.mention for role in rank_roles])
        ))

    @commands.has_role("Baristas")
    @commands.command(aliases=["close", "delete"])
    async def end(self, ctx):
        """Delete the old season roles."""
        async with ctx.typing():
            rank_roles = await self.get_rank_roles(ctx)
            for role in rank_roles:
                await role.delete(reason="Deleting old season roles")

        await ctx.send(embed=utils.Embed(
            title="Deleted old season roles!",
            description=utils.Embed.list([role.name for role in rank_roles])
        ))

    @commands.has_role("Baristas")
    @commands.command()
    async def prune(self, ctx):
        """Prune the Verified role members.

        This will remove the Verified role from anyone who doesn't currently have a rank role.
        """
        async with ctx.typing():
            pruned = 0
            verified = await self.get_verified_role(ctx)
            rank_roles = await self.get_rank_roles(ctx)
            for member in verified.members:
                if not any(role in member.roles for role in rank_roles):
                    await member.remove_roles(verified, reason="Pruning the Verified role members.")
                    pruned += 1

        await ctx.send(embed=utils.Embed(
            title="Pruned the Verified role members!",
            description=f"Pruned Members: `{str(pruned)}`"
        ))

    async def get_verified_role(self, ctx):
        """Utility method to get the verified role."""
        return discord.utils.get(ctx.guild.roles, name="Verified")

    async def get_rank_roles(self, ctx):
        """Utility method to get the current season's rank roles."""
        get_role = lambda n: next(iter(filter(lambda role: role.name.startswith(n), ctx.guild.roles)))
        return [get_role(f"{r} (") for r in self.rank_roles.values()]


def setup(bot):
    bot.add_cog(Season(bot))
