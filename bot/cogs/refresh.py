"""Refresh cog."""

from discord.ext import commands, tasks

from bot import google


class Refresh(commands.Cog, command_attrs={"hidden": True}):
    """All the miscellaneous commands."""

    def __init__(self, bot):
        self.bot = bot
        self.refresh_loop.start()

    @staticmethod
    async def run_refresh():
        """Reload all the data on the worksheets."""
        await google.connector.whatis.refresh()

    @commands.command()
    async def refresh(self, ctx):
        """Refresh data for Info and Tourney."""
        with ctx.typing():
            await self.run_refresh()
        await ctx.send("♻ **Refreshed!**")

    @tasks.loop(hours=1)
    async def refresh_loop(self):
        """Loop that refreshes worksheets."""
        await self.run_refresh()


def setup(bot):
    bot.add_cog(Refresh(bot))
