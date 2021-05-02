"""Holds the custom Bot subclass."""

import random
import logging

import asyncio
import discord
from discord.ext import commands, tasks

from bot import utils


class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.help_command = utils.HelpCommand()

    async def on_ready(self):
        logging.info("Logged in as: %s", self.user.name)
        self.update_presence.start()

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=utils.Embed(
                title="Error: **Missing Required Argument**",
                description=f"You can use `{ctx.prefix}help` for help."))
        elif isinstance(error, (commands.CommandNotFound, commands.MissingRole)):
            return
        else:
            logging.error(error)
            raise error

    @tasks.loop(minutes=1)
    async def update_presence(self):
        """Loop to update the bot presence by selecting one of the strings at random."""
        await self.change_presence(activity=discord.Game(random.choice([
            "!help to get started",
            "Signup for the Checkpoint In-House!",
            "Powered by Radia!",
            "Sponsored by shellenforf institute",
            "Twitter: @Checkpoint1SPL",
            # People-specific
            "Icon by @MochaSplats!",
            "I kid you not Star, she turns herself into a sucklet",
            "Helpdesk needs you Mocha",
            #"Vin",
            #"Lily",
            #"yoru",
            #"robyn",
            #"Knight",
            #"Vicvillon",
        ])))
