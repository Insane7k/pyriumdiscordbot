import asyncio
import cat
import os
import hashlib

from discord.ext import commands
from utils.tools import *
from utils.unicode import *
from utils.fun.lists import *
from utils import imagetools
from PIL import Image

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, message:str):
        """Make the bot say whatever you want it to say"""
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send(strip_global_mentions(message, ctx))

    @say.error
    async def say_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'message':
                await ctx.send(":warning: Please give me a message to say!")
    
    @commands.command()
    async def lenny(self, ctx):
        """<Insert lenny face here>"""
        await ctx.send(lenny)

    @commands.command()
    async def dm(self, ctx, *, message:str):
        await ctx.author.send(message)
        await ctx.send(Language.get("fun.plzmsgme", ctx))

    @dm.error
    async def dm_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'message':
                await ctx.send(":warning: Please give me a message to say!")
                
    @commands.command()
    async def quote(self, ctx, id:int):
        try:
            message = await ctx.channel.fetch_message(id)
        except discord.errors.NotFound:
            await ctx.send(Language.get("bot.no_message_found", ctx).format(id))
            return
        embed = make_message_embed(message.author, message.author.color, message.content, formatUser=True)
        timestamp = message.created_at
        if message.edited_at:
            timestamp = message.edited_at
        embed.timestamp = timestamp
        await ctx.send(embed=embed)

    @commands.command()
    async def trigger(self, ctx, *, member:discord.Member=None):
        await ctx.channel.trigger_typing()
        if member is None:
            member = ctx.author
        download_file(get_avatar(member, animate=False), "data/trigger.png")
        avatar = Image.open("data/trigger.png")
        triggered = imagetools.rescale(Image.open("assets/imgs/pillow/triggered.jpg"), avatar.size)
        position = 0, avatar.getbbox()[3] - triggered.getbbox()[3]
        avatar.paste(triggered, position)
        avatar.save("data/trigger.png")
        await ctx.send(file=discord.File("data/trigger.png"))

    @commands.command()
    async def reverse(self, ctx, *, msg:str):
        await ctx.send(msg[::-1])

    @reverse.error
    async def reverse_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'msg':
                await ctx.send(":warning: Please give me a word/word(s) to reverse!")

    @commands.command()
    async def tomorse(self, ctx, *, msg:str):
        encoded_message = ""
        for char in list(msg.upper()):
            encoded_message += encode_morse[char] + " "
        await ctx.send(encoded_message)

    @tomorse.error
    async def tomorse_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'msg':
                await ctx.send(":warning: Please give me a word/word(s) to encode to morse code!")

    @commands.command()
    async def frommorse(self, ctx, *, msg:str):
        decoded_message = ""
        for char in msg.split():
            if char == " ":
                continue
            decoded_message += decode_morse[char]
        await ctx.send(decoded_message)

    @frommorse.error
    async def frommorse_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'msg':
                await ctx.send(":warning: Please give me a morse code word/word(s) to decode to normal!")

    @commands.command()
    async def dice(self, ctx):
        await ctx.send("You rolled a {}!".format(random.randint(1, 6)))

    @commands.command()
    async def battle(self, ctx, user:str=None, *, weapon:str=None):
        if user is None or user.lower() == ctx.author.mention or user == ctx.author.name.lower() or ctx.guild is not None and ctx.author.nick is not None and user == ctx.author.nick.lower():
            await ctx.send("{} decided to battle themselves, but they ended up Resting In Peace.".format(ctx.author.mention))
            return
        if weapon is None:
            await ctx.send("{0} tried to battle empty handed but {1} knocked them out with Nunchucks!".format(ctx.author.mention, user))
            return
        await ctx.send("**OOF!** {} used the **{}** on **{}** {}".format(ctx.author.mention, weapon, user, random.choice(fight_results).replace("%user%", user).replace("%attacker%", ctx.author.mention)))

def setup(bot):
    bot.add_cog(Fun(bot))
