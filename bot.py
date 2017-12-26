import discord
from discord.ext import commands
import random
import base64
import hashlib
import json
import asyncio
import aiohttp
import datetime
import io
import sys
from PIL import Image, ImageDraw, ImageFont
import calendar
import re
import numpy as np
from mcstatus import MinecraftServer

#modules
sys.path.insert(0, "../modules")
import XORPython
import MatStuff

sys.path.pop(0)

#config file :P
with open('bot_config.json') as file:
    jsonf = json.load(file)
    gamename = jsonf['game']
    ownerid = jsonf['ownerid']
    desc = jsonf['desc']
    prefix = jsonf['prefix']
    token = jsonf['token']
    

bot = commands.Bot(command_prefix=prefix, description=desc, owner_id=int(ownerid), pm_help=None)

#useless variables
uses = 0
allemojis = bot.emojis
arrownames = ['fals', 'demun', 'harder', 'epic', 'wat', 'this', 'nou'
         'that', 'delet', 'hot', 'auto', 'hard', 'featur',
         'wher', 'tru', 'normal', 'pls', 'wy', 'cold', 'got',
         'saem', 'easy', 'sux', 'is', 'ret', 'when', 'kik', 'diki',
         'gey', 'insane', 'agre', 'sakujes', 'geeeeeey', 'omg']
allemojinames = [i.name for i in allemojis]
rainbowarrows = ''
for naem in arrownames:
    if naem in allemojinames:
        nmb = emnames.index(naem)
        a += str(emojis[nmb])



#events
@bot.event
async def on_ready():
    print('Logged in ass')
    print(bot.user.name)
    print(bot.user.id)
    gamename2 = gamename.replace('%numberofservers%', str(len(bot.guilds)))
    await bot.change_presence(game=discord.Game(name=gamename2))
    bot.load_extension("cogs.hypixel")
    bot.load_extension("cogs.image_stuff")
    bot.load_extension("cogs.error_handler")

@bot.event
async def on_message(message):
    global uses

    #sleep well to myself
    if 'going to sleep' in message.content and str(message.author.id) == '191233808601841665':
        await message.channel.send('good night mat i love you <3 <3')

    #reply to dm with same
    if not message.content.startswith("mb!") and type(message.channel) == discord.DMChannel and message.author.id != bot.user.id:
        await message.channel.send('same')
        return
        
    #mb!dhlcra only on dhl server
    if message.channel.id == 332292433750786058 and not message.content.startswith("mb!dhlcra"):
        return

    #disable bio command unless on dm
    if not type(message.channel) == discord.DMChannel and message.author.id == 323487397344051202:
        return

    #uses
    if message.content.startswith("mb!"):
        uses += 1
        print(uses)
    await bot.process_commands(message)
    

#custom check's


#--my commands

@bot.command(hidden=True)
@commands.is_owner()
async def statusc(ctx,*, string=None):
    if string is None:
        with open('bot_config.json') as file:
            jsonf = json.load(file)
            gamename = jsonf['game']
        await bot.change_presence(game=discord.Game(name=gamename.replace('%numberofservers%', str(len(bot.guilds)))))
    else:
        await bot.change_presence(game=discord.Game(name=string))

@bot.command(hidden=True)
@commands.is_owner()
async def sendemojis(ctx):
    emojis = bot.emojis
    msgs = []
    current = 0
    for i in range(len(emojis)):
        if len(msgs) < current + 1:
            msgs.append("")
        if len(msgs[current]) < 2000 and len(str(emojis[i - 1])) < 2000 - len(msgs[current]):
            msgs[current] += str(emojis[i - 1])
        else:
            msgs.append("")
            current += 1
            msgs[current] += str(emojis[i - 1])
    for msg in msgs:
        await ctx.send(msg)
            

@bot.command(hidden=True)
@commands.is_owner()
async def say(ctx, *, string: str):
    await ctx.send(string)

@bot.command(hidden=True)
@commands.is_owner()
async def scrolltext(ctx,*, string="text"):
    """dhl dhld hldmade thx"""
    string = "          "+string+"          "
    idk = 0
    msg = await ctx.send("`>|"+string[idk:idk+10]+"|<`")
    while idk+10 < len(string):
        idk += 1
        furry = "`>|{}|<`".format(string[idk:idk+10])
        await msg.edit(content=furry)
        await asyncio.sleep(0.9)
    await msg.add_reaction('\U00002705')
    #thx dhl <3

@bot.command(hidden=True)
@commands.is_owner()
async def sendmainchat(ctx,*,msg):
    c = bot.get_channel(267762647468998657)
    async with c.typing():
        asyncio.sleep(len(msg)*0.7)
        await c.send(msg)

@bot.command(hidden=True)
@commands.is_owner()
async def hiddencommands(ctx):
    c = bot.commands
    h = []
    for i in c:
        if i.hidden and i.name != "hiddencommands":
            h.append(i)
    f = "```"
    for i in h:
        f += "{0.name} {0.description}\n".format(i)
        
    f = f[:-1]
    f += "```"

    await ctx.send(f)

@bot.command(hidden=True)
@commands.is_owner()
async def botservers(ctx):
    g = bot.guilds
    h = []
    for i in g:
        h.append(i.name)
    f = "```"
    for i in h:
        f += i+"\n"
    f = f[:-1]
    f += "```"
    await ctx.send(f)

@bot.command(hidden=True)
@commands.is_owner()
async def memberlist(ctx):
    txt = open("gen/bot_memberlist.txt","w+",encoding="utf-8")
    f = ""
    for m in ctx.message.guild.members:
        f += m.display_name
        if m.nick != None:
            f += " - "+m.name
        f += " >> "+m.roles[len(m.roles)-1].name
        f += "\n"
    f = f[:-1]
    txt.write(f)
    txt.close()
    await ctx.send("done lol")

@bot.command(hidden=True)
@commands.is_owner()
async def rolelist(ctx):
    txt = open("gen/bot_rolelist.txt","w+",encoding="utf-8")
    rs = ""
    for r in ctx.message.guild.role_hierarchy:
        rs += "{0.name}\n".format(r)
    rs = rs[:-1]
    txt.write(rs)
    txt.close()
    await ctx.send("done")

@bot.command(hidden=True)
@commands.is_owner()
async def channellist(ctx):
    txt = open("gen/bot_channellist.txt","w+",encoding="utf-8")
    f = ""
    fnone = "No category ->\n"
    lastc = None
    for i in ctx.message.guild.text_channels:
        if i.category != None:
            if i.category.name != lastc:
                lastc = i.category.name
                f += "\n"+i.category.name+" ->\n"
            f += "#"+i.name+"\n"
        else:
            fnone += "#"+i.name+"\n"
    f = f[1:]
    f += "\n"+fnone[:-1]
    txt.write(f)
    txt.close()
    await ctx.send("done")

@bot.command(hidden=True)
@commands.is_owner()
async def deletemsg(ctx,mid):
    m = await ctx.get_message(int(mid))
    await m.delete()

@bot.command(hidden=True)
@commands.is_owner()
async def burn(ctx):
    await bot.change_presence(game=discord.Game(name="the world burn",type=3))

#--every1 commands
@bot.command()
async def embed(ctx,title,content,oolor):
    """Makes a embed message with the args given."""
    embed = discord.Embed(title=title, description=content, colour=int(color, 16))
    await ctx.send(embed=embed)

#enc command stuff
@bot.group()
async def enc(ctx):
    """Encodes/hash the given string."""
    if ctx.invoked_subcommand is None:
        await ctx.send('Command usage: **mb!enc <encoding/hash> <string to encode/hash>**')
@enc.command()
async def b64(ctx,*, string: str):
    """Encodes in Base64"""
    await ctx.send(base64.b64encode(bytes(string, 'utf-8')).decode('utf-8'))
@enc.command()
async def gjp(ctx,*, string: str):
    """Encodes in Geometry Jump Password"""
    await ctx.send(XORPython.encode(string, "37526"))
@enc.command()
async def md5(ctx,*, string: str):
    """Hashes the string in md5"""
    string = string.encode('utf-8')
    await ctx.send(hashlib.md5(string).hexdigest())
@enc.command()
async def sha1(ctx,*, string: str):
    """Hashes the string in sha1"""
    string = string.encode('utf-8')
    await ctx.send(hashlib.sha1(string).hexdigest())
@enc.command()
async def dog(ctx):
    """omg doggo bork lang (not accurate)"""
    borks = ["bork", "bark", "woof", "borky"]
    final = ""
    for i in range(random.randint(1,5)):
        final += " "+random.choice(borks)
    await ctx.send(final)
@enc.command()
async def noot(ctx,*,string):
    """Thanks to emptybox"""
    await ctx.send(MatStuff.nootencoder(string))
@enc.command()
async def xor(ctx,key,*,string):
    """Encodes in xor"""
    await ctx.send(XORPython.encode(string, key))

#dec command stuff
@bot.group()
async def dec(ctx):
    """Decodes the given string."""
    if ctx.invoked_subcommand is None:
        await ctx.send('Command usage: **mb!dec <encoding> <string to decode>**')
@dec.command()
async def b64(ctx,* , string: str):
    """Decodes in base64"""
    try:
        await ctx.send(base64.b64decode(bytes(string, 'utf-8')).decode('utf-8'))
    except Exception as e:
        pass
@dec.command()
async def gjp(ctx,* , string: str):
    """Decodes in Geometry Jump Password"""
    await ctx.send(XORPython.decode(string, '37526'))
@dec.command()
async def noot(ctx,*,string):
    """Thanks to emptybox"""
    await ctx.send(MatStuff.nootdecoder(string))
@dec.command()
async def xor(ctx,key,*,string):
    """Encodes in xor"""
    await ctx.send(XORPython.decode(string, key))

@bot.command()
async def ping(ctx):
    """Tests the bot latency"""
    await ctx.send(str(int(bot.latency*1000))+" seconds")

@bot.command()
async def spacefy(ctx,*, string: str):
    """a e s t h e t i c 'fy the given string."""
    await ctx.send(" ".join(string))

@bot.command()
async def invite(ctx):
    """Sends this bot invite link."""
    part1 = 'https://discordapp.com/oauth2/authorize?'
    part2 = 'client_id=317323392992935946&scope=bot&permissions=270400'
    await ctx.send(part1+part2)

@bot.command()
async def give(ctx, item='air', amount='1', mdata='0'):
    """Sends the minecraft item you specify."""
    if item == "gay":
        if amount == "69":
            await ctx.send("i present everyone with gay")
        else:
            await ctx.send("i present you with gay")
        return
    with open('bot_itemsid.json') as f:
        data = json.load(f)
    itemname = None
    if ctx.message.author.nick is None:
        player = ctx.message.author.name
    else:
        player = ctx.message.author.nick
    for i in data:
        if str(i['meta']) == str(mdata) and str(i['type']) == item or i['text_type'] == item and str(i['meta']) == str(mdata) or "minecraft:"+i['text_type'] == item and str(i['meta']) == str(mdata):
            itemname = str(i['name'])
            break
    if itemname != None:
        await ctx.send("Given [{}] x {} to {}".format(itemname, amount, player))
    else:
        await ctx.send("Invalid ID/Item.")

@bot.command()
async def joinedat(ctx):
    """Says when you joined the server"""
    a = ctx.message.author.joined_at
    await ctx.send("{0} {1.day} {1.year}".format(calendar.month_name[a.month], a))

@bot.command()
async def pfp(ctx,uid=None):
    """Gets a profile pic from id or from msg author"""
    if uid is None:
        await ctx.send(ctx.message.author.avatar_url_as(format="png"))
    else:
        m = bot.get_user(int(uid))
        await ctx.send(m.avatar_url_as(format="png"))

@bot.command()
async def serverpic(ctx):
    """Sends pic of server icon"""
    await ctx.send(ctx.message.guild.icon_url)

@bot.command()
async def mock(ctx,*,msg="ok guys"):
    """dOeS thIS To yOuR meSsaGE"""
    await ctx.send(MatStuff.uppLetters(msg))

@bot.command()
async def scramble(ctx,*,msg="ok guys"):
    """Scramble the given word"""
    await ctx.send(MatStuff.scrambleW(msg))

@bot.command()
async def arrows(ctx):
    """sends arrow rainbow wow"""
    global rainbowarrows
    await ctx.send(rainbowarrows)

@bot.command()
async def achievement(ctx,*,name):
    white = (255,255,255)
    imgm = Image.open('imgs/achievment.png').convert('RGBA')
    txtsize = 16
    fnt = ImageFont.truetype('../../Minecraftia.ttf', txtsize)
    d = ImageDraw.Draw(imgm)
    d.fontmode = "1"
    d.text((60,28), name, font=fnt, fill=white)
    imgobject = io.BytesIO()
    imgm.save(imgobject,format='PNG')
    imgobject.seek(0)
    await ctx.send(file=discord.File(imgobject, 'maincra.png'))
    
@bot.command()
async def dab(ctx):
    """dabs"""
    await ctx.send('<:autism:288129155013279748>')

@bot.command()
async def dhlcra(ctx):
    """sees dhlcra status"""
    dhlcra = MinecraftServer("dhlserverip", 25565)
    try:
        dhls = dhlcra.status()
    except:
        await ctx.send("Error connecting to dhlcra. (server down?)")
        return
    raw = dhls.raw
    embed = discord.Embed(title="DHL's minecraft server", colour=int("4bf442", 16))
    embed.set_thumbnail(url="https://i.imgur.com/XSEadDk.png")
    pc = "{}/{}".format(raw["players"]["online"],raw["players"]["max"])
    players = ""
    if raw["players"]["online"] > 0:
        for p in raw["players"]["sample"]:
            players += "- " + p["name"].replace("_","\_") + "\n"
        players = players[:-1]
    else:
        players = "No one online :("
    embed.add_field(name="Players online : "+pc, value=players, inline=False)
    
    embed.add_field(name="Server motd", value=raw["description"]["text"], inline=True)
    embed.add_field(name="Server version", value=raw["version"]["name"], inline=True)
    embed.add_field(name="World seed", value="-1265880969697154662", inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def createdat(ctx):
    """Says when you created your discord account"""
    a = ctx.message.author.created_at
    await ctx.send("{0} {1.day} {1.year}".format(calendar.month_name[a.month], a))

@bot.command(hidden=True)
async def strike(ctx,*,person):
    """lolo"""
    reasons = ["Bait","Loophole","Mod disrespect","Spam","Reasons not listed","Harassment","Public poll"]
    reason = random.choice(reasons)
    f = "Striked {} for: {}.".format(person,reason)
    await ctx.send(f)




bot.run(token)
