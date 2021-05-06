from random import choice
from discord.ext.commands import Cog
from discord.ext.commands import command

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @command(name="hello", aliases=["hi", "hey"], hidden=True)  #+hello +hi +hey
    async def say_hello(self, ctx):
        await ctx.send(f"{choice(('Hello','Hey','Hi'))} {ctx.author.mention}!")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")

def setup(bot):
    bot.add_cog(Fun(bot))
    