from discord.ext import commands
import discord
import asyncio
from PIL import Image, ImageDraw, ImageColor, ImageFont
import random
import io
from functools import partial
import aiohttp

class ImageStuff:
    def __init__(self,bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
    async def get_avatar(self, user) -> bytes:
        avatar_url = user.avatar_url_as(format="png")

        async with self.session.get(avatar_url) as response:
            avatar_bytes = await response.read()

        return avatar_bytes

    @staticmethod
    def tenprintpil() -> io.BytesIO:
        l = Image.new('RGB', (500,500), (255,255,255))
        n = 10
        div = l.width/n
        d = ImageDraw.Draw(l)
        for y in range(n):
            for x in range(n):
                r = random.randint(0,1)
                if r == 0:
                    d.line((div*x,y*div,div*x+div,y*div+div),fill="#000000",width=2)
                else:
                    d.line((div*x+div,y*div,div*x,y*div+div),fill="#000000",width=2)
        imgobject = io.BytesIO()
        l.save(imgobject,format='PNG')
        imgobject.seek(0)
        return imgobject
    
    @commands.command()
    async def tenprint(self,ctx):
        """maze like structure (not a maze)"""
        async with ctx.typing():
            p = partial(self.tenprintpil)
            img = await self.bot.loop.run_in_executor(None, p)
            await ctx.send(file=discord.File(img, 'tenprint.png'))

    @staticmethod
    def dhl_textpil(ttext,btext) -> io.BytesIO:
        white = (255,255,255)
        imgm = Image.open('stuff/dhl.png').convert('RGBA')
        txtsize = 100
        fnt = ImageFont.truetype('stuff/maybe.otf', txtsize)
        d = ImageDraw.Draw(imgm)
        center = lambda x: (1024 - d.textsize(x, fnt)[0]) / 2
        if center(ttext) > 10:
            d.text((center(ttext),100), ttext, font=fnt, fill=white)
        else:
            while center(ttext) < 10:
                txtsize -= 20
                fnt = ImageFont.truetype('stuff/maybe.otf', txtsize)
                center = lambda x: (1024 - d.textsize(x, fnt)[0]) / 2
            d.text((center(ttext),100), ttext, font=fnt, fill=white)
        txtsize = 100
        fnt = ImageFont.truetype('stuff/maybe.otf', txtsize)
        if center(btext) > 10:
            d.text((center(btext),869), btext, font=fnt, fill=white)
        else:
            while center(btext) < 10:
                txtsize -= 20
                fnt = ImageFont.truetype('stuff/maybe.otf', txtsize)
                center = lambda x: (1024 - d.textsize(x, fnt)[0]) / 2
            d.text((center(btext),869), btext, font=fnt, fill=white) 
        imgobject = io.BytesIO()
        imgm.save(imgobject,format='PNG')
        imgobject.seek(0)
        return imgobject

    @commands.command()
    async def dhl_text(self, ctx, ttext, btext):
        """dhlgay lol
        Usage: mb!dhl_text "top text" "bottom text"
        Example: mb!dhl_text "your" "mom"
        mb!dhl_text no "space bar"
        """
        async with ctx.typing():
            p = partial(self.dhl_textpil,ttext,btext)
            img = await self.bot.loop.run_in_executor(None, p)
            
            await ctx.send(file=discord.File(img, 'dhl_gay.png'))

    @staticmethod
    def nicehackspil(avatar,name,color,msg) -> io.BytesIO:
        l = Image.new('RGB', (219,64), (54,57,62))
        av = Image.open(io.BytesIO(avatar))
        av = av.resize((36,36),resample=Image.BILINEAR)
        m = Image.new("L", av.size, 0)
        ImageDraw.Draw(m).ellipse((0,0)+av.size,fill=155)
        av.putalpha(m)
        d = ImageDraw.Draw(l)
        txtf = ImageFont.truetype("stuff/Whitney-Book.otf", 15)
        namef = ImageFont.truetype("stuff/Whitney-Book.otf", 16)
        timef = ImageFont.truetype("stuff/Whitney-Book.otf", 10)

        widttht = d.textsize(msg,txtf)[0]+68+5
        space = d.textsize(name,namef)[0]+68+4
        today = d.textsize("Today at 6:30 PM",timef)[0]+space+5
        if today > widttht:
            l = l.resize((today,64))
        else:
            l = l.resize((widttht,64))
        d = ImageDraw.Draw(l)
        d.text((68,34), msg, font=txtf, fill="#ffffff")
        d.text((68,10), name, font=namef, fill=color)
        d.text((space,16), "Today at 6:30 PM", font=timef, fill="#50555B")
        l.paste(av, (14,13),mask=m)
        tmp = io.BytesIO()
        l.save(tmp,format='PNG')
        tmp.seek(0)
        return tmp

    @commands.command()
    async def nicehacks(self,ctx,msg,uid=None):
        async with ctx.typing():
            if uid != None:
                m = ctx.message.guild.get_member(int(uid)) or self.bot.get_user(int(uid))
            else:
                m = ctx.author

            av = await self.get_avatar(m)

            if isinstance(m, discord.Member):
                c = m.colour.to_rgb()
                if m.colour == discord.Colour.default():
                    c = (255,255,255)
            else:
                c = (255,255,255)
            

            p = partial(self.nicehackspil,av,m.display_name,c,msg)
            img = await self.bot.loop.run_in_executor(None, p)
            await ctx.send(file=discord.File(img, 'notme.png'))
            
def setup(bot):
    bot.add_cog(ImageStuff(bot))
