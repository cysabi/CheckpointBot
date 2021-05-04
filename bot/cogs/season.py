"""Season cog."""

from collections import namedtuple
from datetime import datetime

import discord
from discord.ext import commands

from bot import utils


class Season(commands.Cog):
    """All of the commands that assist with verification seasons."""

    def __init__(self, bot):
        self.bot = bot
        self.SeasonRole = namedtuple('SeasonRole', ['name', 'mention', 'delete'])
        self.rank_roles = {
            "Under S": 0x1AB46A,
            "S Rank": 0x0199B8,
            "Low S+": 0xCD2D7E,
            "High S+": 0xED580B,
            "Low X": 0xDB7821,
        }

    @commands.has_role("Baristas")
    @commands.group(invoke_without_command=True, aliases=["verify", "verification"])
    async def season(self, ctx):
        """Command group for managing verification seasons."""
        await ctx.invoke(self.roles)

    @commands.has_role("Baristas")
    @season.command(aliases=["list", "view"])
    async def roles(self, ctx):
        """List all of the current verification season roles."""
        rank_roles = await self.get_rank_roles(ctx)

        await ctx.send(embed=utils.Embed(
            title="Current season roles:",
            description=utils.Embed.list(role.mention for role in rank_roles)
        ))

    @commands.has_role("Baristas")
    @season.command(aliases=["start", "open", "create"])
    async def new(self, ctx, name: str, delete: bool = False):
        """Create new roles for a new season.

        `season` - The season name, if it's the name of an actual season (such as "winter"), it will be converted to an emoji.
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
                }.get(name.lower(), name)
                role_name = f"{rank} ({season_name} '{str(datetime.now().year)[2:]})"
                rank_roles.append(await ctx.guild.create_role(
                    name=role_name,
                    color=color,
                    reason="Creating new season roles"
                ))
            await ctx.guild.edit_role_positions({
                role: verified.position for role in rank_roles
            })

        await ctx.send(embed=utils.Embed(
            title="✅ Created new season roles!",
            description=utils.Embed.list([role.mention for role in rank_roles])
        ))

    @commands.has_role("Baristas")
    @season.command(aliases=["close", "delete"])
    async def end(self, ctx):
        """Delete the old season roles."""
        async with ctx.typing():
            rank_roles = await self.get_rank_roles(ctx)
            for role in rank_roles:
                await role.delete(reason="Deleting old season roles")

        await ctx.send(embed=utils.Embed(
            title="🗑️ Deleted old season roles!",
            description=utils.Embed.list([role.name for role in rank_roles])
        ))

    @commands.has_role("Baristas")
    @season.command()
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
            title="✂️ Pruned the Verified role members!",
            description=f"Pruned Members: `{str(pruned)}`"
        ))

    async def get_verified_role(self, ctx):
        """Utility method to get the verified role."""
        return discord.utils.get(ctx.guild.roles, name="Verified")

    async def get_rank_roles(self, ctx):
        """Utility method to get the current season's rank roles."""
        return [self._get_rank_role(ctx, f"{r} (") for r in self.rank_roles.keys()]

    def _get_rank_role(self, ctx, name):
        """Utility function to get a rank role."""
        try:
            return next(iter(filter(lambda role: role.name.startswith(name), ctx.guild.roles)))
        except StopIteration:
            async def _(*a, **k): pass
            return self.SeasonRole('None', '`None`', _)


def setup(bot):
    bot.add_cog(Season(bot))
