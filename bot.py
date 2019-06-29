# Pyrium (Discord Hack Week) - 

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import os
import pickle
import sys
import traceback
import re
import aiohttp

bot = commands.Bot(command_prefix='py.')

bot.remove_command('help')

bot.load_extension("cogs.fun")

@bot.event
async def on_ready():
    print ("Pyrium is ready and running.")
    print ("My Username currently is: " + bot.user.name)
    game = discord.Game("Pyrium | py.help")
    await bot.change_presence(status=discord.Status.dnd, activity=game)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban (ctx, member:discord.User=None, reason =None):
    if member == None :                                
        embed=discord.Embed(title="Incorrect Usage", description='''**Command:** py.ban
**Information:** User being naughty? Hit them with the ban!
**Usage:** py.ban <mention user or ID> <reason>
**Example:** ?py.ban Insane#0002 I stole your cookies.'''.format(member, ctx.message.author), color=0xff00f6)
        await ctx.channel.send(embed=embed)
        
    if  member == ctx.message.author:
        embed=discord.Embed(title="Action Failed!", description=":x: **You can't ban yourself!**".format(member, ctx.message.author), color=0xff00f6)
        await ctx.channel.send(embed=embed)
        return
    if reason == None:
        reason = "You have been banished by the mighty hammer"
    message = f"Peekaboo, you have been wiped out the server from **{ctx.guild.name}** for: {reason}."
    await member.send(message)
    await ctx.guild.ban(member)
    embed=discord.Embed(title="**Accomplished Your Request.**", description=f'''**Done!**

**{member}** Has been wiped out of the server. Thor made his decision.'''.format(member, ctx.message.author), color=0xace5ee)
    await ctx.channel.send(embed=embed)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick (ctx, member:discord.User=None, reason =None):
    if member == None :                                
        embed=discord.Embed(title="Incorrect Usage", description='''**Command:** py.kick
**Information:** Want a soft ice-cream kick? Give them one!
**Usage:** py.kick <mention user or ID> <reason>
**Example:** py.kick Insane#0002 I stole your cookies.'''.format(member, ctx.message.author), color=0xff00f6)
        await ctx.channel.send(embed=embed)
        
    if  member == ctx.message.author:
        embed=discord.Embed(title="Action Failed!", description=":x: **You can't kick yourself!**".format(member, ctx.message.author), color=0xff00f6)
        await ctx.channel.send(embed=embed)
        return
    if reason == None:
        reason = "You have been executed temporarily!"
    message = f"Peekaboo, you have been snapped temporarily (kicked) from the server from **{ctx.guild.name}** for: {reason}."
    await member.send(message)
    await ctx.guild.ban(member)
    embed=discord.Embed(title="**Accomplished Your Request.**", description=f'''**Done!**

**{member}** Has been snapped by Thanos! Avengers, Rescue him!'''.format(member, ctx.message.author), color=0xace5ee)
    await ctx.channel.send(embed=embed)

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h":3600, "s":1, "m":60, "d":86400}

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k]*float(v)
            except KeyError:
                raise commands.BadArgument("{} is an invalid time-key! h/m/s/d are valid!".format(k))
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time

@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member:discord.Member, *, time:TimeConverter = None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)
    await ctx.send(("Muted {} for {}s" if time else "Muted {}").format(member, time))
    return
    if time:
        await asyncio.sleep(time)
        await member.remove_roles(role)

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed=discord.Embed(title="Incorrect Usage", description='''**Command:** py.mute
**Information:** Send someone to the quiet corner, enjoy the total silence.
**Usage:** py.mute <mention user or ID> <time> <reason>
**Example:** py.mute Insane#0002 30m Spamming.''')
        await ctx.channel.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member:discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(role)
    await ctx.send(("Unmuted {}.").format(member))

@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed=discord.Embed(title="Incorrect Usage", description='''**Command:** py.unmute
**Information:** Forgive the quite-cornered user.
**Usage:** py.unmute <mention user or ID> 
**Example:** py.unmute Insane#0002 false mute.''')
        await ctx.channel.send(embed=embed)

@bot.command()
async def ball(ctx):
   await ctx.channel.send(random.choice(["It is certain. :8ball:",
                                         "It is decidedly so. :8ball:",               
                                         "Without a doubt. :8ball:",
                                         "Yes, definitely. :8ball:",
                                         "You may rely on it. :8ball:",
                                         "As I see it, yes. :8ball:",
                                         "Most likely. :8ball:",
                                         "Outlook good. :8ball:",
                                         "Yes. :8ball:",
                                         "Signs point to yes. :8ball:",
                                         "Reply hazy, try again. :8ball:",
                                         "Ask again later. :8ball:",
                                         "Better not tell you now. :8ball:",
                                         "Cannot predict now. :8ball:",
                                         "Concentrate and ask again. :8ball:",
                                         "Don't count on it. :8ball:",
                                         "My reply is no. :8ball:",
                                         "My sources say no. :8ball:",
                                         "Outlook not so good. :8ball:",
                                         "Very doubtful. :8ball:"]))

@bot.command()
async def coinflip(ctx):
    await ctx.channel.send(random.choice(["Heads!","Tails!"]))

@bot.command()
async def choose(ctx, *choices: str):
    await ctx.send(random.choice(choices))

@choose.error
async def choose_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.channel.send(":warning: Please input your choices and try again!")
        
@bot.command()
async def dadjoke(ctx):
    await ctx.channel.send(random.choice(["What do you call a mac ‘n’ cheese that gets all up in your face? Too close for comfort food!",
                                          "What concert costs just 45 cents? 50 Cent featuring Nickelback!",
                                          "Why did the scarecrow win an award? Because he was outstanding in his field!",
                                          "What do sprinters eat before a race? Nothing, they fast!",
                                          "Whys couldn’t the bicycle stand up by itself? It was two tired!",
                                          "Did you hear about the guy who invented Lifesavers?  They say he made a mint!",
                                          "Why do you never see elephants hiding in trees? Because they’re so good at it!",
                                          "How does a penguin build its house? Igloos it together!",
                                          "Why did the old man fall in the well? Because he couldn’t see that well!",
                                          "Why don’t skeletons ever go trick or treating? Because they have no body to go with!",
                                          "What do you call a factory that sells passable products? A satisfactory!",
                                          "Why did the invisible man turn down the job offer? He couldn’t see himself doing it!",
                                          "Want to hear a joke about construction? I’m still working on it!",
                                          "Funny dad jokes you can tell in one line.",
                                          "Dad and son laughing on a park bench, dad jokes",
                                          "I like telling Dad jokes. Sometimes he laughs!",
                                          "To whoever stole my copy of Microsoft Office, I will find you. You have my Word!"]))

@bot.command(pass_context=True)
async def serverinfo(ctx):
    embed = discord.Embed(name="{}'s info".format(ctx.message.guild.name), color=0x00ffff)
    embed.set_author(name="Server Information")
    embed.add_field(name="Name", value=ctx.message.guild.name, inline=True)
    embed.add_field(name='Owner', value=ctx.message.guild.owner, inline=False)
    embed.add_field(name="Server ID", value=ctx.message.guild.id, inline=True)
    embed.add_field(name="Roles", value=len(ctx.message.guild.roles), inline=True)
    embed.add_field(name="Member Count", value=len(ctx.message.guild.members))
    embed.add_field(name="Verification Level", value=len(ctx.message.guild.verification_level))
    embed.add_field(name="Amount of Boosts", value=ctx.message.guild.premium_subscription_count)
    embed.set_thumbnail(url=ctx.message.guild.icon_url)
    embed.set_footer(text=f"Requested By: {ctx.message.author}", icon_url=ctx.author.avatar_url)
    await ctx.channel.send(embed=embed)

@bot.command(pass_context=True)
async def boostinfo(ctx):
    embed = discord.Embed(name="{}'s info".format(ctx.message.guild.name), color=0xffff00)
    embed.set_author(name=f"Nitro Boosting Status for: {ctx.message.guild.name}")
    embed.add_field(name="Boost Amount", value=ctx.message.guild.premium_subscription_count)
    embed.add_field(name="Boost / Server Level", value=ctx.message.guild.premium_tier)
    embed.set_thumbnail(url="https://discordemoji.com/assets/emoji/7485_server_boost.png")
    embed.set_footer(text=f"Requested By: {ctx.message.author}", icon_url=ctx.author.avatar_url)
    await ctx.channel.send(embed=embed)

@bot.command()
async def botinfo(ctx):
    embed = discord.Embed(name="Bot Info", color=0x7289da)
    embed.set_author(name="Pyrium | Bot Info")
    embed.add_field(name="Bot Version", value="n/a", inline=True)
    embed.add_field(name="Owner(s)", value="Insane#0002, Dragonic#0001", inline=True)
    embed.add_field(name="discord.py version", value="v1.2.2", inline=True)
    embed.add_field(name="Prefix", value="py.", inline=True)
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1135619777060167680/Arbl-pB2_400x400.png")
    embed.set_footer(text="Made with discord.py | Submission for Discord Hack Week", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1024px-Python-logo-notext.svg.png")
    await ctx.channel.send(embed=embed)

@bot.command()
async def help(ctx):
    embed=discord.Embed(title='''Category » Fun
━━━━━━━━━━''', color=0xff8000)
    embed.set_author(name='''Pyrium | Help Menu
━━━━━━━━━━''')
    embed.add_field(name="py.battle » Battle a user with a gadget for win or loss!", value="usage: py.battle <mention user or id> <gadget>", inline=False)
    embed.add_field(name="py.dice » role a dice. simple.", value="usage: py.dice", inline=False)
    embed.add_field(name="py.dm » type a message, get it from Pyrium.", value="usage: py.dm <message>", inline=False)
    embed.add_field(name="py.lenny » ( ͡° ͜ʖ ͡° )", value="( ͡° ͜ʖ ͡° )", inline=False)
    embed.add_field(name="py.quote » Quote a message.", value="usage: py.quote <messageid>", inline=True)
    embed.add_field(name="py.reverse » Reverse a message.", value="usage: py.reverse <message>", inline=False)
    embed.add_field(name="py.say » say something. easy.", value="usage: py.say <message>", inline=False)
    embed.add_field(name="py.tomorse » Be a secret spy, and encode a message into morse code with this command!", value="usage: py.tomorse <message>", inline=True)
    embed.add_field(name="py.frommorse » Ready to decode your message? Here you go.", value="usage: py.frommorse <message>", inline=True)
    embed.add_field(name="py.trigger » You mad? Match your Profile Pic with your mood and make it triggered with this command.", value="usage: py.trigger <mention user or id> or py.trigger", inline=True)
    embed.add_field(name="py.ball » Ask the Bot's 8Ball, and observe.", value="usage: py.ball <question>", inline=True)
    embed.add_field(name="py.coinflip » Heads or Tails? Let the bot flip a coin, and find out!", value="usage: py.coinflip", inline=True)
    embed.add_field(name="py.choose » Cant decide? Let the bot do it for you.", value="usage: py.choose <option1> <option2>", inline=True)
    embed.add_field(name="py.dadjoke » Oh. Dad jokes.. You get it.", value='''usage: py.dadjoke
                    ━━━━━━━━━━''', inline=True)
    embed.add_field(name="Catergory » Moderation", value="━━━━━━━━━━", inline=False)
    embed.add_field(name="py.ban » Let Thor's mighty hammer take action. Ban someone from the server.", value="usage: py.ban <mention user or id> <reason>", inline=True)
    embed.add_field(name="py.kick » Thanos Snap them out. Kick someone from the server. They can return when The Avengers fix everything.", value="usage: py.kick <mention user or id> <reason>", inline=True)
    embed.add_field(name="py.mute » Send someone to the quiet corner, mute them.", value="usage: py.mute <mention user or id> <time> <reason>", inline=True)
    embed.add_field(name="py.unmute » Forgive the user in the quiet corner, unmute them.", value='''usage: py.unmute <mention user or id>
━━━━━━━━━━''', inline=True)
    embed.add_field(name="Catergory » Utils", value="━━━━━━━━━━", inline=False)
    embed.add_field(name="py.botinfo » Gives information about the bot.", value="usage: py.botinfo", inline=True)
    embed.add_field(name="py.serverinfo » Gives information about the server.", value="usage: py.serverinfo", inline=True)
    embed.add_field(name="py.boostinfo » Gives information about the server boost status.", value="usage: py.boostinfo", inline=True)
    await ctx.channel.send(embed=embed)

bot.run("TOKEN")
