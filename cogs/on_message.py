import discord, re
from discord.ext import commands

from modules.insta import Instagram
from modules.fb import Facebook
from modules.tiktok import Tiktok


def parseUrl(url : str) -> (discord.File, str):
        
        file : discord.File = None
        msg : str = ""

        insta = r"https?:\/\/(www\.)?instagram.*"
        fb = r"https?:\/\/(www\.|m\.)?facebook.*"
        tiktok = r"https?:\/\/(www\.|vt\.)?tiktok.*"

        rsInsta = re.search(insta, url)
        rsFb = re.search(fb, url)
        rsTiktok = re.search(tiktok, url)

        if rsInsta:
            file = Instagram.insta(url)
        elif rsFb:
            file, msg = Facebook.facebook(url)
        elif rsTiktok:
            file = Tiktok.tiktok(url)

        return file, msg

class OnMessage(commands.Cog):
    def __init__(self, bot : discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        
        urlPattern = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)'
        try:
            baseUrl = re.search(urlPattern, message.content).group(0)
        except:
            baseUrl = ""
            pass
        
        files, msg = parseUrl(baseUrl)
            
        if any([files, msg]):
            await message.reply(files=files, content=msg, mention_author = False)
            return
        
def setup(bot : discord.Bot) -> None:
    bot.add_cog(OnMessage(bot))
