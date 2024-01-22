import discord
from colored import fg, bg, attr
from discord.ext import commands

import os




class OnReady(commands.Cog):
    def __init__(self, bot : discord.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{fg(119)}{attr("bold")}Logging as {self.bot.user}!{attr(0)}')
        print(f'{fg(69)}List of servers the bot is in: {attr(0)}')

        for guild in self.bot.guilds:
            print(fg(6),f'-{guild.name} {fg(117)}(ID: {guild.id}){attr(0)}',attr(0))

        await self.bot.register_commands()

        
def setup(bot: discord.Bot) -> None:
    bot.add_cog(OnReady(bot))