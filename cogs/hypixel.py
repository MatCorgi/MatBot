from discord.ext import commands
import discord
import asyncio
import aiohttp
import json
import datetime

class Hypixel:
    def __init__(self, bot):
        self.bot = bot

    cmduses = 0
    usemin = datetime.datetime.now().minute
    apikey = "hypixelapikeydonotsteal"

    @commands.command()
    async def bwstats(self,ctx,*,name):

        if datetime.datetime.now().minute == self.usemin and self.cmduses > 70:
            await ctx.send("Hypixel commands were used 70 times last minute! Please wait a bit before using this command again")
            return
        self.usemin = datetime.datetime.now().minute
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.hypixel.net/player?key='+self.apikey+'&name='+name) as r:
                js = await r.json()
                self.cmduses += 1
        if js["player"] != None:
            try:
                lo = js["player"]["stats"]["Bedwars"]
            except KeyError:
                await ctx.send("No bedwars stats found for that player.")
                return
            embed = discord.Embed(title=name+"'s Hypixel Bedwars stats", colour=int("ff7575", 16))
            embed.set_thumbnail(url="https://minotar.net/helm/{}/64.png".format(name))

            ach = js["player"]["achievements"]
            bwstar = str(ach["bedwars_level"])
            embed.add_field(name="Bedwars Level", value=bwstar+"\N{WHITE MEDIUM STAR}", inline=False)

            wins = str(ach["bedwars_wins"])
            winstreak = str(js["player"]["stats"]["Bedwars"]["winstreak"])
            embed.add_field(name="Wins", value=wins+" Total wins\nCurrent winstreak : "+winstreak, inline=True)

            try: kills = str(js["player"]["stats"]["Bedwars"]["kills_bedwars"])
            except KeyError: kills = "0"
            try: fkills = str(js["player"]["stats"]["Bedwars"]["final_kills_bedwars"])
            except KeyError: fkills = "0"
            tkills = str(int(kills) + int(fkills))
            embed.add_field(name=tkills+" Total kills", value=kills+" Kills\n"+fkills+" Final kills", inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Player not found.")

def setup(bot):
    bot.add_cog(Hypixel(bot))
