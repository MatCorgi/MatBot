import discord
from discord.ext import commands

# MysterialPy on github
# https://gist.github.com/MysterialPy/7822af90858ef65012ea500bcecf1612

class ErrorHandlerCog:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self,ctx,error):
        noperm = self.bot.get_emoji(321784861595664385)
        try:
            await ctx.message.add_reaction(noperm)
        except discord.errors.Forbidden:
            pass
        return

def setup(bot):
    bot.add_cog(ErrorHandlerCog(bot))
