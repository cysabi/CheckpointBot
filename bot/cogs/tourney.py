"""Tourney cog."""

import random

import discord
from discord.ext import commands

from bot import utils, google


class Tourney(commands.Cog):
    """All of the commands that assist with the Checkpoint In-House Tournaments."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["canned"])
    async def whatis(self, ctx, prefix=None, image: bool = False):
        """Send a canned response."""
        if prefix:
            try:
                name, response, image_link = google.connector.whatis.get(prefix.lower())
            except TypeError:
                await ctx.send(self.invalid_whatis(prefix))
            else:
                embed = utils.Embed(title=f"What Is... {name.capitalize()}?", description=response)
                if image:
                    embed.set_image(url=image_link)
                await ctx.send(embed=embed)
        else:
            embed = utils.Embed(title="What Is...")
            embed.add_field(
                name="Options:",
                value=utils.Embed.list(google.connector.whatis.options()))
            await ctx.send(embed=embed)

    def invalid_whatis(self, prefix):
        """Send a random error message when the prefix doesn't exist."""
        return random.choice([
            f"WHAT IS {prefix.upper()}??",
            "doesn't exist",
            "under rules?",
            "it's a social construct",
            "your parent/guardian",
            "gay gay homosexual gay",
            "\*poof*",
            "???",
            "¯\_(ツ)_/¯",
            "dark matter",
            "a collection of subatomic particles",
            "an empty void",
            "probably mostly hydrogen",
            "the information has been lost to a black hole",
            "it's in elon musk's spaceship",
            f"{prefix.lower()[:int(len(prefix)/2)]} with no {prefix.lower()[int(len(prefix)/2):]}",
            "in it's natural habitat",
            "a reminent of a simpler time",
            "a harsh reminder of the truely cruel society we live in",
            "ask my cousin",
            "it was inside your heart all along",
            f"have you ever asked 'how is {prefix}?'",
            "look up",
            "trust me, i wish i knew",
            "your future d&d character",
            "you leave them out in the sun too long and they get all brown and stuff",
            "you're joking right?",
        ])


def setup(bot):
    bot.add_cog(Tourney(bot))
