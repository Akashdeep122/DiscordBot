import discord
from discord.ext import commands
from replit import db
import os
import pyowm
import requests
import json
import datetime
import random
from Rumble import randomchooser
import time
import Rumble
from keep_alive import keep_alive
import asyncio
from PIL import Image
from io import BytesIO
from PIL import ImageOps
from PIL import ImageEnhance
import Warnings

intents = discord.Intents.default()
intents.members = True


def makeembed(title, description):
	embed = discord.Embed(title=title,
	                      description=description,
	                      colour=discord.Colour.random())
	embed.set_footer(
	    text='Dank Island ',
	    icon_url=
	    'https://cdn.discordapp.com/icons/821575403855544370/a_85c6630c72154018ecc7740c58411dea.gif?size=128'
	)
	embed.timestamp = datetime.datetime.utcnow()
	return embed


def convert(time):
	pos = ["s", "m", "h", "d"]
	time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}
	unit = time[-1]

	if unit not in pos:
		return -1
	try:
		val = int(time[:-1])
	except:
		return -2

	return val * time_dict[unit]

def get_prefix(cleint, message):
  with open("prefixes.json") as f:
    prefixes = json.load(f)

	#default_prefix = "di "
  try:
    return prefixes[str(message.guild.id)]
  except AttributeError:
    print("")


client = discord.Client()
client = commands.Bot(command_prefix=get_prefix)
client.remove_command('help')

@client.command()
async def dmremind(ctx,val:str,*,val1:str=None):
  def check(m):
    if m.author == ctx.author and isinstance(m.channel, discord.DMChannel):
      return m.author == ctx.author
  if "@" in ctx.message.content:
        msg = ctx.message.content.replace("@","")
        msg = msg + " (Ive got kicked for pinging no pings then)"
        print(msg)
        if "&" in msg:
          return      
  timest = convert(val)
  if timest == -1:
    await ctx.author.send("You didnt write a proper unit (s/m/h/d)")
    return
  elif timest == -2:
    await ctx.author.send("You didnt write a number before the unit")
    return
  if timest < 5:
    await ctx.author.send("Please dont try to make me Spam")
    return
  await ctx.send(f"Alright ill remind you in {val} about {val1} in your dms")
  while True:
    await asyncio.sleep(timest)
    await ctx.author.send(f"{ctx.author.mention}, im reminding you about {val1}")
    try:
      while True:
        msg = await client.wait_for('message', timeout=float(timest), check=check)
        msg.content = msg.content.upper()
        print(msg.content)
        if msg.content == "CANCEL":
          await ctx.send("Ok Cancelled")
          return
    except:
      continue


def get_quote():
	response = requests.get("https://zenquotes.io/api/random")
	json_data = json.loads(response.text)
	quote = json_data[0]['q'] + " -" + json_data[0]['a']
	return (quote)


client.http.api = "https://discord.com/api"


def randomchooser(Names, message, random_function_selector):
	valuerecv = random.choice(random_function_selector)(Names, message)
	return valuerecv


@client.command(aliases=["partnership"])
async def partner(ctx):
	answers = []

	def check(m):
		if m.author == ctx.author and isinstance(m.channel, discord.DMChannel):
			return m.author == ctx.author

	title = "Dank island Partnerships"
	description = "Please Check your Dm For The Partnership, make sure to have dms unlocked else it wont work"
	await ctx.send(embed=makeembed(title, description))
	questions = [
	    "Please tell which kind of partnership you want. [Heist|Server]",
	    "Please Tell The Name of The Server",
	    "Please Tell The Id Of the server",
	    "Please tell which ping are you offering",
	    "Tell me the exact number of role containing members and make suree to subtract non - partnership ping",
	    "Please tell anything extra you want like a special channel etc etc"
	]
	x = 0
	for i in questions:
		embed = discord.Embed(title="Partnership With Dank Island",
		                      description=f"{i}",
		                      colour=discord.Colour.random())
		embed.set_footer(
		    text='Dank Island , Type "cancel" to cancel the partnership',
		    icon_url=
		    'https://cdn.discordapp.com/icons/821575403855544370/a_85c6630c72154018ecc7740c58411dea.gif?size=128'
		)

		await ctx.author.send(embed=embed)
		try:
			msg = await client.wait_for('message', timeout=60.0, check=check)
		except:
			await ctx.author.send(
			    makeembed(
			        "Partnership Failed",
			        "Please dont take that long for your answer, be quicker next time"
			    ))
			return
		else:
			msg.content = msg.content.lower()
			if msg.content == "cancel":
				await ctx.author.send(
				    "Ok Cancelling partnership, you can still re-apply")
				return
			answers.append(msg.content)

	await ctx.author.send("Do you want to submit?")
	try:
		msg = await client.wait_for('message', timeout=60.0, check=check)
	except:
		await ctx.author.send(
		    "Please dont take that long for your answer, be quicker next time")
		return
	else:
		if msg.content == "no":
			await ctx.author.send("Ok Cancelling partnership")
			return
		elif msg.content == "yes":
			await ctx.author.send(
			    "K fine i submitted your answers, a partnership manager will be there with you shortly to confirm the partnership"
			)
		else:
			await ctx.author.send("Ive still sent your partnership")

	embed = discord.Embed(title=f"Partnership Request",
	                      description=f"{answers[1]} Wants to partner with us",
	                      colour=ctx.author.colour)
	embed.add_field(name="Type of Partnership",
	                value=f"{answers[0]}",
	                inline=True)
	embed.add_field(name="Server Id", value=f"{answers[2]}", inline=True)
	embed.add_field(name="Ping The Offer and Strength",
	                value=f"{answers[3]} , {answers[4]}",
	                inline=False)
	embed.add_field(name="Extra Requirements",
	                value=f"{answers[5]}",
	                inline=False)
	chnl = client.get_channel(846328679193116712)

	await chnl.send(embed=embed)
	await chnl.send(
	    f"Please DM {ctx.author.mention} To Complete The Partnership")
	await chnl.send("<@&830735932885303296>")


@client.event
async def on_ready():
	print(f"Connected succesfully as {client.user}")


@client.command(aliases=['guessthenumber'])
async def gtn(ctx, value: int = 1, value2: int = 100):
	number = random.randint(value, value2)
	await ctx.send(f'i Just have chosen a number from {value} and {value2}')
	user = await client.fetch_user(f'{ctx.author.id}')
	embed = makeembed("The Secret Number",
	                  f"Hey The Number is {number} DONT TELL ANYONE")
	await discord.DMChannel.send(user, embed=embed)
	#await ctx.send('Event Managers Please unlock After my Next Statement')
	await asyncio.sleep(3)
	await ctx.send('Everythings Done go Start')
	a = time.time()
	b = 0
	while (b < 400):
		b = time.time() - a
		#me = await client.get_user_info(f'{ctx.author.id}')
		#await client.send(ctx.author,f"Hey The Number is {number} DONT TELL ANYONE")
		response = await client.wait_for('message')
		if response.content == ";end":
			await ctx.send("Ended The Match")
			return
		try:
			guess = int(response.content)
		except:
			#await ctx.channel.send('BREH you have to type a Number Dud')
			guess = None
		if guess == number:
			embed = makeembed(
			    "Someone Guessed the Number",
			    f"<@{response.author.id}> guessed it right , Well Done")
			await response.reply(embed=embed)
			return
    
	await ctx.send("Man you took so long to think lel , Now try again")


def getwinner(userid, something):
	try:
		w = random.choice(userid)
	except IndexError:
		#await ctx.send('F No one entered')
		something = "NOBODY"
		return something

	return w


mygaw = []


@client.command(aliases=['giveawaystart'])
@commands.has_role('Giveaway Manager')
async def gstart(ctx,
                 minutes: str,
                 channel: discord.TextChannel,
                 member: int = 1,
                 *,
                 prize: str = "ask the hoster"):
	something = ""
  
	#if channel == None:
	#channel = ctx.channel
	title = f"**{prize}**"
	description = f"**React with 🎉 to Enter!\nHosted by: {ctx.author.mention}**"
	myembed = discord.Embed(title=title,
	                        description=description,
	                        colour=ctx.author.color)
	myembed.set_footer(
	    text=f'{member} winner(s) • Dank Island ',
	    icon_url=
	    'https://cdn.discordapp.com/icons/821575403855544370/a_85c6630c72154018ecc7740c58411dea.gif?size=128'
	)
	myembed.timestamp = datetime.datetime.utcnow()

	timeval = convert(minutes)
	if timeval == -1:
		await ctx.send("You didnt write a proper unit (s/m/h/d)")
	elif timeval == -2:
		await ctx.send("You didnt write a number before the unit")

	#end = datetime.datetime.utcnow() + datetime.timedelta(seconds = minutes*60)

	myembed.add_field(name="ends in:", value=f"{minutes}")
	try:
		msg1 = await channel.send("🎉🎉**GIVEAWAY**🎉🎉")
		msg = await channel.send(embed=myembed)
	except:
		await channel.send("I DONT HAVE THE REQUIRED PERMS")
		return
	await msg.add_reaction("🎉")

	await asyncio.sleep(timeval)
	#await client.run_background_task()
	#await client.process_commands(ctx)

	#else:
	#role = "<@&"+role+">"

	msgid = await ctx.channel.fetch_message(msg.id)
	userid = await msgid.reactions[0].users().flatten()
	#reaction = await msgid.reactions[0].users()
	#print(userid)
	#print(reaction)
	#for x in userid[1:]:
	#if role in x.roles:
	#await msgid.remove_reaction("🎉",x)
	#users = await msgid.
	#something = []
	userid.pop((userid.index(client.user)))
	mlist = []
	for x in range(member):
		something = getwinner(userid, something)
		try:
			mlist.append(something.mention)
		except:
			mlist.append("None")

	#if winner == client.user:
	res = str(mlist)[1:-1].replace("'", "")

	await ctx.send(f'The winner is {res}')

	title = f"{prize}"
	description = f"{res} won the giveaway"
	myembed = makeembed(title, description)
	await msg1.edit(content="🎉🎉**GIVEAWAY ENDED**🎉🎉")
	await msg.edit(embed=myembed)


@client.command()
#@commands.has_permissions(kick_members=True)
async def reroll(ctx, channel: discord.TextChannel, id_: int, winner: int = 1):
	something = ""

	try:
		new_msg = await channel.fetch_message(id_)
	except:
		await ctx.send(
		    "The ID that was entered was incorrect, make sure you have entered the correct giveaway message ID."
		)
	userid = await new_msg.reactions[0].users().flatten()
	userid.pop(userid.index(client.user))

	mlist = []
	for x in range(winner):
		something = getwinner(userid, something)
		mlist.append(something.mention)

	#if winner == client.user:
	res = str(mlist)[1:-1].replace("'", "")

	await ctx.send(f'The winner is {res}')

	await channel.send(
	    f"Congratulations the new winner is: {winner.mention} for the giveaway rerolled!"
	)


@client.command(aliases=['purge'])
@commands.has_guild_permissions(manage_messages=True)
async def clear(ctx, amount: int = None):
	if amount == None:
		await ctx.send('Pls tell me a number')
		return
	await ctx.channel.purge(limit=amount + 1)
	message = await ctx.send(f"purged {amount} messages")
	time.sleep(2)
	await message.delete()


@client.command()
async def hack(ctx, member: discord.Member):
	value = 1
	title = '** Hack Start **'
	description = f'Hacking in progress \n **{value}% done**'
	howgaystart = makeembed(title, description)
	msg = await ctx.send(embed=howgaystart)
	while value < 100:
		value = value + 11
		title = '** Hack Start **'
		description = f'Hacking in progress \n **{value}% done**'
		howgaystart = makeembed(title, description)
		await msg.edit(embed=howgaystart)
	messages = ["DuckDuck36", "HelloIMyourmom", "Pizzatasty", "BrehBruh"]
	title = '** Hack Ended **'
	description = f'**Username {member.name}** \n **Id : {member.id}\n password : {random.choice(messages)}**'
	howgaystart = makeembed(title, description)
	await msg.edit(embed=howgaystart)


@client.command()
async def meme(ctx):
	r = requests.get("https://memes.blademaker.tv/api?lang=en")
	res = r.json()
	title = res["title"]
	ups = res["ups"]
	downs = res["downs"]
	sub = res["subreddit"]

	m = discord.Embed(title=f"{title}\nsubreddit: {sub}")
	m.set_image(url=res["image"])
	m.set_footer(text=f"👍: {ups} 👎: {downs}")
	await ctx.send(embed=m)


@client.command(aliases=["gay", "gaymachine"])
async def howgay(ctx, *, amount: str = None):
	if amount == None:
		value = ctx.author.name
	else:
		value = amount
	howgayvalue = random.randint(1, 100)
	title = '** Gay Machine **'
	description = f'{value} is **{howgayvalue}%** gay'
	howgaystart = makeembed(title, description)
	await ctx.send(embed=howgaystart)


@client.command(aliases=["roll", "rn"])
async def randomnumber(ctx, amount: int = None, amount1: int = None):
	if amount == None:
		amount = 1
	if amount1 == None:
		amount1 = 100

	howgayvalue = random.randint(amount, amount1)
	title = '**randomnumber Machine **'
	description = f'Your randomnumber is **{howgayvalue}**'
	howgaystart = makeembed(title, description)
	await ctx.send(embed=howgaystart)


@client.command(aliases=['makemehappy'])
async def inspire(ctx):
	quote = get_quote()
	title = f"**Inspiring Words**"
	description = f'{quote}'
	howgaystart = makeembed(title, description)
	await ctx.send(embed=howgaystart)
	pass


@client.group(invoke_without_command=True)
async def help(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)
		em = discord.Embed(
		    title="Help",
		    description=
		    f"Use {prefixes[str(ctx.guild.id)]}help <command> for more information on the command.",
		    color=ctx.author.color)
		em.add_field(
		    name="<:ban_hammer:869070330222743592> Utility",
		    value=
		    "```ping,prefix,giveawaystart,partner,eventlock,eventunlock,snipe,dmremind```",
		    inline=False)
		em.add_field(
		    name="💸 Donations",
		    value=
		    "```view,adddono,removedono,makenew```",
		    inline=False)
		em.add_field(
		    name="<:Popcorn:868511638435811331> Fun",
		    value=
		    "```howgay,inspire,meme,temprature,coinflip,meaning,battle,guessthenumber,hack,fastestwordfirst```",
		    inline=False)

		em.add_field(name="<:Nukes:869093984117616671> Moderation",
		             value="```purge,lottery,demote,promote```",
		             inline=False)
		em.set_footer(
		    text='Dank Island ',
		    icon_url=
		    'https://cdn.discordapp.com/icons/821575403855544370/a_85c6630c72154018ecc7740c58411dea.gif?size=128'
		)
		em.add_field(
		    name="🖼️ image",
		    value=
		    "```map,clap,negative,roblox,wanted,delete,simp,notanymore,slap,brighten,darken```",
		    inline=False)
		em.timestamp = datetime.datetime.utcnow()
		await ctx.send(embed=em)


@help.command(aliases=['gtn'])
async def guessthenumber(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)

	title = "**Dank island Help**"
	em = makeembed(title, "")
	em.add_field(
	    name="guessthenumber",
	    value=
	    f"```{prefixes[str(ctx.guild.id)]}guessthenumber <startnumber: Optional  else 1> <endnumber else 100>```",
	    inline=False)
	em.add_field(
	    name="aliases",
	    value=
	    f"```{prefixes[str(ctx.guild.id)]}gtn <startnumber: Optional  else 1> <endnumber else 100>```",
	    inline=False)
	em.add_field(name="description",
	             value="Guess the number game",
	             inline=False)
	em.add_field(name="Developer", value="```Akashdeep#9572```", inline=True)
	await ctx.send(embed=em)


@help.command(aliases=['lighten'])
async def brighten(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)

	title = "**Dank island Help**"
	em = makeembed(title, "")
	em.add_field(
	    name="brighten",
	    value=
	    f"```{prefixes[str(ctx.guild.id)]}brighten <Member: Optional> <brightness level : 1-9 , else 5 >```",
	    inline=False)
	em.add_field(
	    name="aliases",
	    value=
	    f"```{prefixes[str(ctx.guild.id)]}lighten <Member: Optional> <brightness level : 1-9 , else 5 >```",
	    inline=False)
	em.add_field(name="description",
	             value="lightens your image the level you specify else 5",
	             inline=False)
	em.add_field(name="Developer", value="```Akashdeep#9572```", inline=True)


@help.command()
async def darken(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)

	title = "**Dank island Help**"
	em = makeembed(title, "")
	em.add_field(
	    name="darken",
	    value=
	    f"```{prefixes[str(ctx.guild.id)]}darken <Member: Optional> <brightness level : 1-9 , else 5 >```",
	    inline=False)
	#em.add_field(name="aliases", value=f"```{prefixes[str(ctx.guild.id)]}lighten <Member: Optional> <brightness level : 1-9 , else 5 >```",inline = False)
	em.add_field(name="description",
	             value="darkens your image the level you specify else 5",
	             inline=False)
	em.add_field(name="Developer", value="```Akashdeep#9572```", inline=True)


@help.command(aliases=['trash'])
async def notanymore(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)

	title = "**Dank island Help**"
	em = makeembed(title, "")
	em.add_field(
	    name="notanymore",
	    value=
	    f"```{prefixes[str(ctx.guild.id)]}notanymore <Member: Optional>```",
	    inline=False)
	em.add_field(
	    name="aliases",
	    value=f"```{prefixes[str(ctx.guild.id)]}trash <Member: Optional>```",
	    inline=False)
	em.add_field(name="description",
	             value="A Funny meme , go try it yourself",
	             inline=False)
	em.add_field(name="Developer", value="```Akashdeep#9572```", inline=True)
	await ctx.send(embed=em)


@help.command(aliases=['simpcard'])
async def simp(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)

	title = "**Dank island Help**"
	em = makeembed(title, "")
	em.add_field(
	    name="simp",
	    value=f"```{prefixes[str(ctx.guild.id)]}simp <Member: Optional>```",
	    inline=False)
	em.add_field(
	    name="aliases",
	    value=f"```{prefixes[str(ctx.guild.id)]}simpcard <Member: Optional>```",
	    inline=False)
	em.add_field(name="description",
	             value="Just shows The Member's pfp in a simpcard",
	             inline=False)
	em.add_field(name="Developer", value="```Akashdeep#9572```", inline=True)
	await ctx.send(embed=em)


@help.command()
async def delete(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)

	title = "**Dank island Help**"
	em = makeembed(title, "")
	em.add_field(
	    name="delete",
	    value=f"```{prefixes[str(ctx.guild.id)]}wanted <Member: Optional>```",
	    inline=False)
	#em.add_field(name="aliases", value=f"```{prefixes[str(ctx.guild.id)]}trash <Member: Optional>```",inline = False)
	em.add_field(name="description",
	             value="WILL DELETE YOUR PFP (joking bro try it yourself)",
	             inline=False)
	em.add_field(name="Developer", value="```Akashdeep#9572```", inline=True)
	await ctx.send(embed=em)


@help.command()
async def wanted(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)

	title = "**Dank island Help**"
	em = makeembed(title, "")
	em.add_field(
	    name="wanted",
	    value=f"```{prefixes[str(ctx.guild.id)]}wanted <Member: Optional>```",
	    inline=False)
	#em.add_field(name="aliases", value=f"```{prefixes[str(ctx.guild.id)]}wanted <Member: Optional>```",inline = False)
	em.add_field(name="description",
	             value="Just shows The Member's pfp in a wanted Template",
	             inline=False)
	em.add_field(name="Developer", value="```Akashdeep#9572```", inline=True)
	await ctx.send(embed=em)


@help.command()
async def roblox(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)

	title = "**Dank island Help**"
	em = makeembed(title, "")
	em.add_field(
	    name="roblox",
	    value=f"```{prefixes[str(ctx.guild.id)]}roblox <Member: Optional>```",
	    inline=False)
	#em.add_field(name="aliases", value=f"```{prefixes[str(ctx.guild.id)]}invert <Member: Optional>```",inline = False)
	em.add_field(
	    name="description",
	    value=
	    "Makes The member's pfp a Roblox Chatacter, if it not mentioned , then it will make yours",
	    inline=False)
	em.add_field(name="Developer", value="```Akashdeep#9572```", inline=True)
	await ctx.send(embed=em)


@help.command(aliases=['makemehappy'])
async def inspire(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)

	title = "**Dank island Help**"
	em = makeembed(title, "")
	em.add_field(name="inspire",
	             value=f"```{prefixes[str(ctx.guild.id)]}inspire```",
	             inline=False)
	em.add_field(name="aliases",
	             value=f"```{prefixes[str(ctx.guild.id)]}makemehappy```",
	             inline=False)
	em.add_field(name="description",
	             value="Just a random inspirational quote",
	             inline=False)
	em.add_field(name="Developer", value="```Akashdeep#9572```", inline=True)
	await ctx.send(embed=em)


@help.command(aliases=['inverted'])
async def negative(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)

	title = "**Dank island Help**"
	em = makeembed(title, "")
	em.add_field(
	    name="negative",
	    value=f"```{prefixes[str(ctx.guild.id)]}negative <Member: Optional>```",
	    inline=False)
	em.add_field(
	    name="aliases",
	    value=f"```{prefixes[str(ctx.guild.id)]}invert <Member: Optional>```",
	    inline=False)
	em.add_field(
	    name="description",
	    value="will invert your pfp, if member not given , it will inver yours",
	    inline=False)
	em.add_field(name="Developer", value="```Akashdeep#9572```", inline=True)
	await ctx.send(embed=em)


@help.command(aliases=['makemap'])
async def map(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)

	title = "**Dank island Help**"
	em = makeembed(title, "")
	em.add_field(name="map",
	             value=f"```{prefixes[str(ctx.guild.id)]}map```",
	             inline=False)
	em.add_field(name="aliases",
	             value=f"```{prefixes[str(ctx.guild.id)]}makemap```",
	             inline=False)
	em.add_field(name="description", value="Shows a world map", inline=False)
	em.add_field(name="Developer", value="```Akashdeep#9572```", inline=True)
	await ctx.send(embed=em)


@help.command(aliases=['applause'])
async def clap(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)

	title = "**Dank island Help**"
	em = makeembed(title, "")
	em.add_field(name="map",
	             value=f"```{prefixes[str(ctx.guild.id)]}clap```",
	             inline=False)
	em.add_field(name="aliases",
	             value=f"```{prefixes[str(ctx.guild.id)]}applause```",
	             inline=False)
	em.add_field(name="description", value="Shows a random clap", inline=False)
	em.add_field(name="Developer", value="```Akashdeep#9572```", inline=True)
	await ctx.send(embed=em)


@help.command(aliases=['spank'])
async def slap(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)

	title = "**Dank island Help**"
	em = makeembed(title, "")
	em.add_field(
	    name="map",
	    value=f"```{prefixes[str(ctx.guild.id)]}slap <Member: required>```",
	    inline=False)
	em.add_field(
	    name="aliases",
	    value=f"```{prefixes[str(ctx.guild.id)]}spank <Member: required>```",
	    inline=False)
	em.add_field(name="description",
	             value="Slaps the member you mentioned, else returns a error",
	             inline=False)
	em.add_field(name="Developer", value="```Akashdeep#9572```", inline=True)
	await ctx.send(embed=em)


@help.command()
async def hack(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)

	title = "**Dank island Help**"
	em = makeembed(title, "")
	em.add_field(
	    name="hack",
	    value=f"```{prefixes[str(ctx.guild.id)]}hack <user (required)>```",
	    inline=False)
	#em.add_field(name="aliases", value=f"```{prefixes[str(ctx.guild.id)]}gawping <message(optional)>```",inline = False)
	em.add_field(name="description",
	             value="Just a fun Command , you better try it out",
	             inline=False)
	em.add_field(name="Developer", value="```Akashdeep#9572```", inline=True)

	#await ctx.send(embed=em)
	await ctx.send(embed=em)


@help.command(aliases=['weather'])
async def temprature(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)
	em = makeembed("**Dank island Help**", "")

	em.add_field(
	    name="temprature",
	    value=
	    f"```{prefixes[str(ctx.guild.id)]}temprature <Celsius or Farheinheit> <place>```",
	    inline=False)
	em.add_field(
	    name="aliases",
	    value=
	    f"```{prefixes[str(ctx.guild.id)]}temprature <Celsius or Farheinheit> <place>```",
	    inline=False)
	em.add_field(name="description",
	             value="Tells you a weather of a place",
	             inline=False)
	em.add_field(name="Developer", value="```Akashdeep#9572```", inline=True)

	#await ctx.send(embed=em)
	await ctx.send(embed=em)


@help.command(aliases=['flip'])
async def coinflip(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)
	em = makeembed(title="**Dank island Help**", description="")
	em.add_field(name="coinflip",
	             value=f"```{prefixes[str(ctx.guild.id)]}coinflip```",
	             inline=False)
	em.add_field(name="flip",
	             value=f"```{prefixes[str(ctx.guild.id)]}flip```",
	             inline=False)
	em.add_field(name="description",
	             value="Shows a random funny meme when command is pressed",
	             inline=False)
	em.add_field(name="Developer", value="```Akashdeep#9572```", inline=True)
	#await ctx.send(embed=em)
	await ctx.send(embed=em)


@help.command()
async def meme(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)
	em = makeembed(title="**Dank island Help**", description="")
	em.add_field(name="meme",
	             value=f"```{prefixes[str(ctx.guild.id)]}meme```",
	             inline=False)
	#em.add_field(name="aliases", value=f"```{prefixes[str(ctx.guild.id)]}gawping <message(optional)>```",inline = False)
	em.add_field(name="description",
	             value="Shows a random funny meme when command is pressed",
	             inline=False)
	em.add_field(name="Developer", value="```Akashdeep#9572```", inline=True)
	#await ctx.send(embed=em)
	await ctx.send(embed=em)


@help.command(aliases=['gawping'])
async def ping(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)
	em = makeembed(title="**Dank island Help**", description="")

	em.add_field(
	    name="command",
	    value=f"```{prefixes[str(ctx.guild.id)]}ping <message(optional)>```",
	    inline=False)
	em.add_field(
	    name="aliases",
	    value=f"```{prefixes[str(ctx.guild.id)]}gawping <message(optional)>```",
	    inline=False)
	em.add_field(
	    name="description",
	    value=
	    "pings gawping , if message added : it writes the message below else Types somethin funny",
	    inline=False)
	em.add_field(name="Developer", value="```Akashdeep#9572```", inline=True)
	#await ctx.send(embed=em)
	await ctx.send(embed=em)


@help.command(aliases=['gstart'])
async def giveawaystart(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)
	em = makeembed(title="**Dank island Help**", description="")

	em.add_field(
	    name="command",
	    value=
	    f"```{prefixes[str(ctx.guild.id)]}giveawaystart <time (example: 2s)><channel><message(optional)>```",
	    inline=False)
	em.add_field(
	    name="aliases",
	    value=
	    f"```{prefixes[str(ctx.guild.id)]}gstart <time (example: 2s)><channel><message(optional)>```",
	    inline=False)
	em.add_field(
	    name="description",
	    value=
	    "pings gawping , if message added : it writes the message below else Types somethin funny",
	    inline=False)
	em.add_field(name="Developer", value="```Akashdeep#9572```", inline=True)
	#await ctx.send(embed=em)
	await ctx.send(embed=em)


@help.command()
async def prefix(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)
	em = makeembed(title="**Dank island Help**", description="")
	em.add_field(
	    name="command",
	    value=
	    f"```{prefixes[str(ctx.guild.id)]}prefix <newprefix(optional)> <Space : True/False (default False)>```",
	    inline=False)
	em.add_field(
	    name="description",
	    value="If value given : changes Prefix else Tells your current prefix",
	    inline=False)
	#em.add_field(name="aliases", value=f"```{prefixes[str(ctx.guild.id)]}gawping <message(optional)>```",inline = False)
	em.add_field(name="Developer", value="```Akashdeep#9572```", inline=True)
	#await ctx.send(embed=em)
	await ctx.send(embed=em)


@help.command()
async def battle(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)
	em = makeembed(title="**Dank island Help**", description="")
	em.add_field(
	    name="command",
	    value=
	    f"```{prefixes[str(ctx.guild.id)]}battle <value : see subcommands section>```",
	    inline=False)
	em.add_field(name="description",
	             value="a fun game of battle royale",
	             inline=False)
	em.add_field(
	    name="subcommands",
	    value=
	    f"```start: starts a match\njoin: Joins a match which is already started\nbot: Set ups a match with 5 bots (cant be changed)\nleave: leaves a match```",
	    inline=False)
	em.add_field(name="Developer", value="```Akashdeep#9572```", inline=True)
	#await ctx.send(embed=em)
	await ctx.send(embed=em)


@help.command(aliases=['clear'])
async def purge(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)
	em = makeembed(title="**Dank island Help**", description="")
	em.add_field(
	    name="command",
	    value=f"```{prefixes[str(ctx.guild.id)]}purge <number(required)>```",
	    inline=False)
	em.add_field(
	    name="aliases",
	    value=f"```{prefixes[str(ctx.guild.id)]}clear <number(required)>```",
	    inline=False)
	em.add_field(
	    name="description",
	    value=
	    "purges a number of messages , returns a error if you dont mention, also you require manage messages permission",
	    inline=False)
	em.add_field(name="Developer", value="```Akashdeep#9572```", inline=True)

	#await ctx.send(embed=em)
	await ctx.send(embed=em)


@help.command(aliases=['fwf'])
async def fastestwordfirst(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)
	em = makeembed(title="**Dank island Help**", description="")
	em.add_field(name="command",
	             value=f"```{prefixes[str(ctx.guild.id)]}fastestwordfirst```",
	             inline=False)
	em.add_field(name="aliases",
	             value=f"```{prefixes[str(ctx.guild.id)]}fwf```",
	             inline=False)
	em.add_field(name="description",
	             value="Fastest word first game , go play with your friends",
	             inline=False)
	em.add_field(name="Developer", value="```Akashdeep#9572```", inline=True)

	#await ctx.send(embed=em)
	await ctx.send(embed=em)


@help.command(aliases=['dict', 'dictionary'])
async def meaning(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)
	em = makeembed(title="**Dank island Help**", description="")

	em.add_field(
	    name="command",
	    value=f"```{prefixes[str(ctx.guild.id)]}meaning <word (required)>```",
	    inline=False)
	em.add_field(
	    name="aliases",
	    value=
	    f"```{prefixes[str(ctx.guild.id)]}dict <word (required)>```\n```{prefixes[str(ctx.guild.id)]}dictionary <word (required)>``` ",
	    inline=False)
	em.add_field(
	    name="description",
	    value=
	    "Tells meaning of a word or group of words, returns a check again if word isnt found or Pls tell a word if you didnt enter a word",
	    inline=False)
	em.add_field(name="Developer", value="```Akashdeep#9572```", inline=True)

	#await ctx.send(embed=em)
	await ctx.send(embed=em)


@help.command(aliases=['rn', 'roll'])
async def randomnumber(ctx):
	with open("prefixes.json") as f:
		prefixes = json.load(f)
	em = makeembed(title="**Dank island Help**", description="")

	em.add_field(
	    name="command",
	    value=
	    f"```{prefixes[str(ctx.guild.id)]}rn <startnumber (optional else:1)> <endnumber (optional else:100)>```",
	    inline=False)
	em.add_field(
	    name="aliases",
	    value=
	    f"```{prefixes[str(ctx.guild.id)]}randomnumber <startnumber (optional else:1)> <endnumber (optional else:100)>```\n```{prefixes[str(ctx.guild.id)]}roll <startnumber (optional else:1)> <endnumber (optional else:100)>``` ",
	    inline=False)
	em.add_field(
	    name="description",
	    value=
	    "Gives you a randomnumber , and can change the start and the end values if mentioned",
	    inline=False)
	em.add_field(name="developer", value="```Akashdeep#9572```", inline=True)

	#await ctx.send(embed=em)
	await ctx.send(embed=em)


@client.command(aliases=['gawping'])
async def ping(ctx, message: str = "Just Trying to be quiet"):
	gawchannel = [
	    839483172671455243, 839887476960264233, 839483172671455243,
	    839482877225992263, 847389751527211038
	]
	if ctx.message.channel.id in gawchannel:
		await ctx.send("<@&821578275381706812>")
		giveaway = makeembed(
		    title=
		    '**<:tada:865900512988758046>Dank island Giveaways<:tada:865900512988758046>**',
		    description=f'**Host** - {ctx.author.name}\n **message** {message}'
		)
		await ctx.send(embed=giveaway)
		pass
	else:
		await ctx.send("breh this is not the correct channel")


@client.command()
async def vote(ctx):
	emoji = ctx.guild.emojis(ctx.guild.emojis, name='arrow11')
	emoji1 = ctx.guild.emojis(ctx.guild.emojis, name='heart-1')
	#await ctx.send("<@&821578275381706812>")
	giveaway = makeembed(
	    title=f'**<:heart-1:{str(emoji)}>Support us by voting**',
	    description=
	    'Vote Here - [Top.gg](https://top.gg/servers/821575403855544370/vote)')
	giveaway.add_field(
	    name='<:heart-1:853281699609837588>__voter Perks__',
	    value=
	    "<:arrow11:855071214161756250>Role, the <&@856044490346594324> \n <:arrow11:855071214161756250> Access to <#839848405677244416> \n <:arrow11:855071214161756250> You help us grow, which allows us to hold larger heists, giveaways, and other events.",
	    inline=False)
	giveaway.add_field(
	    name="<:heart-1:853281699609837588> Other Benefits:",
	    value=
	    "<:arrow11:855071214161756250> Top Voter in <#856056648723857439> will get amazing prizes \n <:arrow11:855071214161756250> Noumnenon Giveaway Bypass for a week \n <:arrow11:855071214161756250> Top Voter Role",
	    inline=False)
	await ctx.send(embed=giveaway)
	pass


@client.command(aliases=['temperature'])
async def weather(ctx, value: str = "C", *, place: str = None):
	if value == None:
		await ctx.send("Breh Add Both Degree Type and Place ")
		return
	value = value.lower()
	owm = pyowm.OWM('7d27569e239a09981a5e17fde3e348ac')
	mgr = owm.weather_manager()
	print(mgr.weather_at_place(place))
	try:
		observation = mgr.weather_at_place(place)
	except:
		await ctx.send('we couldnt find the place , try again ')
	w = observation.weather
	print(w)
	wind = w.wind()
	speed = wind['speed']
	humidity = w.humidity
	temperature = w.temp

	if value.startswith("c"):
		maxtemp = round(temperature['temp_max'] - 273.15)
		mintemp = round(temperature['temp_min'] - 273.15)
		crtemp = round(temperature['temp'] - 273.15)
		feelslike = round(temperature['feels_like'] - 273.15)
		kind = "C"
	elif value.startswith("f"):
		kind = "F"
		maxtemp = round((temperature['temp_max'] - 273.15) * 9 / 5 + 32)
		mintemp = round((temperature['temp_min'] - 273.15) * 9 / 5 + 32)
		crtemp = round((temperature['temp'] - 273.15) * 9 / 5 + 32)
		feelslike = round((temperature['feels_like'] - 273.15) * 9 / 5 + 32)
	information = w.detailed_status
	howgaystart = makeembed(title=f'** Weather Today for {place} **',
	                        description=f'**{information}**')
	howgaystart.add_field(name='Degree Type', value=f'{kind}', inline=True)
	howgaystart.add_field(name='Humidity', value=f'{humidity}%', inline=True)
	howgaystart.add_field(
	    name='Temprature',
	    value=f'Right Now {crtemp}°, Max:{maxtemp}°, Min{mintemp}°',
	    inline=False)
	howgaystart.add_field(name='Wind Speed', value=f'{speed}mph', inline=True)
	howgaystart.add_field(name='Feels Like',
	                      value=f'{feelslike}°',
	                      inline=True)
	await ctx.send(embed=howgaystart)
	pass


@client.command(aliases=['coinflip'])
async def flip(ctx):
	flip = ["Heads", "Tails"]
	value = random.choice(flip)
	howgaystart = makeembed(title=f"**{ctx.author.name}'s coin Flipped to :**",
	                        description=f'{value}')
	await ctx.send(embed=howgaystart)
	pass


@client.command(aliases=['makemap'])
async def map(ctx):
	#mymap = folium.Map(location=[180, 90],tiles='Stamen Terrain')
	#mymap.save('Map.html')
	#await ctx.send('Download this file and open it in a browser')
	await ctx.send(file=discord.File('world-map.gif'))
	await ctx.message.delete()


@client.command()
async def wanted(ctx, Member: discord.Member = None):
	if Member == None:
		Member = ctx.author

	wanted = Image.open("wanted.jpg")
	asset = Member.avatar_url_as(size=128)
	data = BytesIO(await asset.read())
	pfp = Image.open(data)
	pfp = pfp.resize((253, 256))
	wanted.paste(pfp, (100, 200))
	wanted.save("profile.jpg")
	await ctx.send(file=discord.File("profile.jpg"))
	os.remove("profile.jpg")
	await ctx.message.delete()


@client.command(aliases=['simpcard'])
async def simp(ctx, Member: discord.Member = None):
	if Member == None:
		Member = ctx.author

	card = Image.open("card.png")
	asset = Member.avatar_url_as(size=128)
	data = BytesIO(await asset.read())
	pfp = Image.open(data)
	pfp = pfp.resize((389, 600))
	card.paste(pfp, (85, 100))
	card.save("profile.png")
	await ctx.send(file=discord.File("profile.png"))
	os.remove("profile.png")
	await ctx.message.delete()


@client.command(aliases=['lighten'])
async def brighten(ctx, Num: int = 5, Member: discord.Member = None):
	if Member == None:
		Member = ctx.author
	if Num > 9:
		await ctx.send('Please give a number Less than 9')
	Num = Num / 10
	asset = Member.avatar_url_as(size=128)
	data = BytesIO(await asset.read())
	pfp = Image.open(data)
	enhancer = ImageEnhance.Brightness(pfp)
	factor = 1 + Num  #darkens the image
	im_output = enhancer.enhance(factor)
	im_output.save('profile.png')
	await ctx.send(file=discord.File("profile.png"))
	os.remove("profile.png")
	await ctx.message.delete()


@client.command()
async def darken(ctx,Num: int = 5,Member: discord.Member = None):
	if Member == None:
		Member = ctx.author
	if Num > 9:
		await ctx.send('Please give a number Less than 9')
	Num = Num / 10
	asset = Member.avatar_url_as(size=128)
	data = BytesIO(await asset.read())
	pfp = Image.open(data)
	enhancer = ImageEnhance.Brightness(pfp)
	factor = 1 - Num  #darkens the image
	im_output = enhancer.enhance(factor)
	im_output.save('profile.png')
	await ctx.send(file=discord.File("profile.png"))
	os.remove("profile.png")
	await ctx.message.delete()


@client.command()
async def delete(ctx, Member: discord.Member = None):
	if Member == None:
		Member = ctx.author

	card = Image.open("delete.png")
	asset = Member.avatar_url_as(size=128)
	data = BytesIO(await asset.read())
	pfp = Image.open(data)
	pfp = pfp.resize((196, 196))
	card.paste(pfp, (120, 135))
	card.save("profile.png")
	await ctx.send(file=discord.File("profile.png"))
	os.remove("profile.png")
	await ctx.message.delete()


@client.command(aliases=['notanymore'])
async def trash(ctx, Member: discord.Member = None):
	if Member == None:
		Member = ctx.author

	card = Image.open("notanymore.jpg")
	asset = Member.avatar_url_as(size=128)
	data = BytesIO(await asset.read())
	pfp = Image.open(data)
	pfp = pfp.resize((521, 521))
	card.paste(pfp, (121, 122))
	card.save("profile.jpg")
	await ctx.send(file=discord.File("profile.jpg"))
	os.remove("profile.jpg")
	await ctx.message.delete()


@client.command(aliases=['negative'])
async def invert(ctx, Member: discord.Member = None):
	if Member == None:
		Member = ctx.author

	asset = Member.avatar_url_as(size=1024)
	data = BytesIO(await asset.read())
	pfp = Image.open(data)
	pfp = ImageOps.invert(pfp)
	pfp.save("profile.png")
	await ctx.send(file=discord.File("profile.png"))
	os.remove("profile.png")
	await ctx.message.delete()


@client.command()
async def roblox(ctx, Member: discord.Member = None):
	if Member == None:
		Member = ctx.author

	roblox = Image.open("roblox.jpg")
	asset = Member.avatar_url_as(size=128)
	data = BytesIO(await asset.read())
	pfp = Image.open(data)
	#pfp = ImageOps.invert(pfp)
	pfp = pfp.resize((64, 64))
	roblox.paste(pfp, (63, 8))
	#wanted.save("profile.jpg")
	roblox.save("profile.jpg")
	await ctx.send(file=discord.File("profile.jpg"))
	os.remove("profile.jpg")
	await ctx.message.delete()


@client.command(aliases=['spank'])
async def slap(ctx, Member1: discord.Member = None):
	#if Member == None:
	#Member1 = Member
	Member = ctx.author

	if Member1 == None:
		await ctx.send('Who are you even slapping?')
		return

	roblox = Image.open("unnamed.jpg")
	asset = Member.avatar_url_as(size=128)
	data = BytesIO(await asset.read())
	pfp = Image.open(data)
	#pfp = ImageOps.invert(pfp)
	pfp = pfp.resize((134, 134))
	roblox.paste(pfp, (161, 1))
	#wanted.save("profile.jpg")
	asset1 = Member1.avatar_url_as(size=128)
	data1 = BytesIO(await asset1.read())
	pfp1 = Image.open(data1)
	pfp = pfp.resize((95, 95))
	roblox.paste(pfp1, (316, 123))
	roblox.save("profile.jpg")
	await ctx.send(file=discord.File("profile.jpg"))
	os.remove("profile.jpg")
	await ctx.message.delete()


	#mymap = folium.Map(location=[180, 90],tiles='Stamen Terrain')
	#mymap.save('Map.html')
	#await ctx.send('Download this file and open it in a browser')
	#await ctx.send(file=discord.File('world-map.gif'))
	#flip = ["Heads","Tails"]
@client.command(aliases=['applause'])
async def clap(ctx):
	mylist = [
	    'https://media.tenor.com/images/af3285a51b9ae2fbe2a574169ac8610c/tenor.png',
	    'https://media1.tenor.com/images/479b108bb4cca32cf38cf23acf83b408/tenor.gif?itemid=15979248',
	    'https://media1.tenor.com/images/63813addcbb166e5e70e741d7f6625b9/tenor.gif?itemid=17643070',
	    'https://tenor.com/view/oscars-standing-ovation-clap-clapping-applause-gif-5089552'
	]

	await ctx.send(random.choice(mylist))
	await ctx.message.delete()
	#os.delete('Map.html')"""


"""@client.command(aliases=['raid'])
async def nuke(ctx):
    mnumber = 1
    nukeembed = discord.Embed(
      title='** Nuke The Server **',
      description=f'{ctx.author.name} wants to nuke this Server',
      colour=discord.Colour.random())
    nukeembed.set_footer(text = 'Dank Island ',icon_url='https://cdn.discordapp.com/icons/821575403855544370/a_85c6630c72154018ecc7740c58411dea.gif?size=128')
    nukeembed.timestamp = datetime.datetime.utcnow()
    mymsg = await ctx.send(embed=nukeembed)
    pass
    while mnumber<=100:
      nukeembed = discord.Embed(
        title='** Nuke The Server **',
        description=f'Nuke {mnumber}% completed',
        colour=discord.Colour.random())
      nukeembed.set_footer(text = 'Dank Island ',icon_url='https://cdn.discordapp.com/icons/821575403855544370/a_85c6630c72154018ecc7740c58411dea.gif?size=128')
      nukeembed.timestamp = datetime.datetime.utcnow()
      await mymsg.edit(embed = nukeembed)
      mnumber += 9
     
    nukeend = discord.Embed(
      title='** Nuked The Server **',
      description=f'**{ctx.author.name} tried to Nuke this server**\n Nuke Failed \n Stupid You TRYNA RAID THIS SERVER , Youre Muted',
      colour=discord.Colour.random())

    nukeend.set_footer(text = 'Dank Island ',icon_url='https://cdn.discordapp.com/icons/821575403855544370/a_85c6630c72154018ecc7740c58411dea.gif?size=128')
    nukeend.timestamp = datetime.datetime.utcnow()
    member = ctx.author
    var = discord.utils.get(ctx.guild.roles, name = "Muted")
    await member.add_roles(var)
    await mymsg.edit(embed=nukeend)"""

@client.event
async def on_guild_join(guild):
	with open("prefixes.json") as f:
		prefixes = json.load(f)

	#default_prefix = "di "
	prefixes[str(guild.id)] = "di "

	with open('prefixes.json', 'w') as f:
		json.dump(prefixes, f, indent=2)

@client.event
async def on_guild_remove(guild):
	with open("prefixes.json") as f:
		prefixes = json.load(f)

	#default_prefix = "di "
	del prefixes[str(guild.id)]

	with open('prefixes.json', 'w') as f:
		json.dump(prefixes, f, indent=2)


@client.command()
@commands.has_guild_permissions(administrator=True)
async def prefix(ctx, prefix: str = None, Space: bool = False):

	with open("prefixes.json") as f:
		prefixes = json.load(f)

	if prefix == None:
		currentprefix = prefixes[str(ctx.guild.id)]
		await ctx.send(f"The current prefix is {currentprefix}")
		return

	if Space == False:
		prefix = prefix
	else:
		prefix = prefix + " "

	#default_prefix = "di "
	oldprefix = prefixes[str(ctx.guild.id)]
	prefixes[str(ctx.guild.id)] = prefix

	with open('prefixes.json', 'w') as f:
		json.dump(prefixes, f, indent=2)
	howgaystart = makeembed(
	    title=f"**Prefix Change**",
	    description=
	    f'The Prefix got changed from {oldprefix} to {prefix}\n \n Ordered by {ctx.author.name}'
	)
	await ctx.send(embed=howgaystart)
	pass


#@client.command(aliases='heist')
#async def scan(ctx):

@client.command()
async def battlebot(ctx,value:int=5):
  if value > 10:
    await ctx.send("DONT Try FLOOD THE BOT LIKE THAT NOOB")
    return
  Names = {}
  def check(m):
    if m.channel == ctx.channel:
      return m.channel == ctx.channel

  dead = []
  json.dump(dead, open('Dead.json', 'w'))
  json.dump(Names, open('Names.json', 'w'))
  prefixes = json.load(open('prefixes.json','r'))
  emoji = '<:PepeYes:868059827111358506>'
  await ctx.message.add_reaction(emoji)
  await ctx.send(
			    f"A Match has started , Quickly type ```{prefixes[str(ctx.guild.id)]}battlejoin``` within 30 seconds")
  for i in range(1,value+1):
    num = str(i)
    Name = "Bot"+num
    Names[Name] = 50
  a = time.time()
  b = 0
  while (b <= 30):
    b = time.time() - a
    response = await client.wait_for('message',check=check)
    if response.content == prefixes[str(ctx.guild.id)]+"battlejoin":
      Name = response.author.name
      Names[Name] = 50
      await response.add_reaction('<:PepeOk:868375254093938728>')
      json.dump(Names, open('Names.json', 'w'))

    if response.content == 'leave':
      if response.author.name in list(Names):
        del Names[ctx.author.name]
      else:
        await ctx.send(
				    'AHHHH man , how can you even leave when you havent even joined'
				)
    
    json.dump(Names, open('Names.json', 'w'))

  hello = makeembed(
			    title="**Players**",
			    description=
			    f"If you just got a react like <:PepeOk:868375254093938728> then you are in "
		)
  await ctx.send(embed=hello)
  functions = [
			    Rumble.kill,Rumble.kill,Rumble.kill,Rumble.kill, Rumble.killyourself,Rumble.killyourself,Rumble.killyourself, Rumble.revive, Rumble.calm, Rumble.calm]
  mlist = [discord.Colour.green(), discord.Colour.red()]
  randomclr = random.choice(mlist)
  while len(list(Names)) > 1:
        time.sleep(5)
        val = randomchooser(Names, ctx, functions)
        if len(list(Names)) >= 1:
          val2 = randomchooser(Names, ctx, functions)
        else:
          val2 = "Looks like a winner is to be announced"
        if val == None:
          val = "<:872114295238967306:sorry> Someone Killed someone but The System Could'nt retrive it"
        if val2 == None:
          val2 = "<:872114295238967306:sorry> Someone Killed someone but The System Could'nt retrive it"
        hello = makeembed(title="**Match in Progress**",
				                  description=f"**{val}\n {val2}**")
        await ctx.send(embed=hello)
    
  hi = makeembed(
			    title="**Match Ended**",
			    description=f"**{Names} won and With these much bullets**")
  await ctx.send(embed=hi)
  Names = {}
  dead = []
  json.dump(dead, open('Dead.json', 'w'))
  json.dump(Names, open('Names.json', 'w'))

@client.command()
async def battlestart(ctx):
  Names = {}
  def check(m):
    if m.channel == ctx.channel:
      return m.channel == ctx.channel

  dead = []
  json.dump(dead, open('Dead.json', 'w'))
  json.dump(Names, open('Names.json', 'w'))
  prefixes = json.load(open('prefixes.json','r'))
  emoji = '<:PepeYes:868059827111358506>'
  await ctx.message.add_reaction(emoji)
  await ctx.send(
			    f"A Match has started , Quickly type ```{prefixes[str(ctx.guild.id)]}battlejoin``` within 30 seconds")
  a = time.time()
  b = 0
  while (b <= 30):
    b = time.time() - a
    try:
      response = await client.wait_for('message',check=check,timeout=30)
    except:
      continue
    if response.content == prefixes[str(ctx.guild.id)]+"battlejoin":
      Name = response.author.name
      Names[Name] = 50
      await response.add_reaction('<:PepeOk:868375254093938728>')
      json.dump(Names, open('Names.json', 'w'))

    if response.content == 'leave':
      if response.author.name in list(Names):
        del Names[ctx.author.name]
      else:
        await ctx.send(
				    'AHHHH man , how can you even leave when you havent even joined'
				)
    json.dump(Names, open('Names.json', 'w'))

  hello = makeembed(
			    title="**Players**",
			    description=
			    f"If you just got a react like <:PepeOk:868375254093938728> then you are in "
		)
  await ctx.send(embed=hello)
  functions = [
			    Rumble.kill,Rumble.kill,Rumble.kill,Rumble.kill, Rumble.killyourself,Rumble.killyourself,Rumble.killyourself, Rumble.revive, Rumble.calm, Rumble.calm]
  mlist = [discord.Colour.green(), discord.Colour.red()]
  randomclr = random.choice(mlist)
  while len(list(Names)) > 1:
        time.sleep(5)
        val = randomchooser(Names, ctx, functions)
        if len(list(Names)) >= 1:
          val2 = randomchooser(Names, ctx, functions)
        else:
          val2 = "Looks like a winner is to be announced"
        if val == None:
          val = "<:872114295238967306:sorry:> Someone Killed someone but The System Could'nt retrive it"
        if val2 == None:
          val2 = "<:872114295238967306:sorry:> Someone Killed someone but The System Could'nt retrive it"
        hello = makeembed(title="**Match in Progress**",
				                  description=f"**{val}\n {val2}**")
        await ctx.send(embed=hello)
    
  hi = makeembed(
			    title="**Match Ended**",
			    description=f"**{Names} won and With these much bullets**")
  await ctx.send(embed=hi)
  Names = {}
  dead = []
  json.dump(dead, open('Dead.json', 'w'))
  json.dump(Names, open('Names.json', 'w'))
  

  

@client.event
async def on_message(message):
  if message.content.startswith("imagine "):
    try:
      msg = message.content.split('imagine', 1)[1]
      print(msg)
      if "@" in msg:
        msg = msg.replace("@","")
        msg = msg + " (Ive got kicked for pinging no pings then)"
        print(msg)
        if "&" in msg:
          return      
      await message.channel.send(f"i cant even imagine{msg}, bro")
    except:
      await message.channel.send("Breh what are you ebven imagining")
  if message.content.startswith("no u"):
    await message.channel.send("no you")
  
  else:
    await client.process_commands(message)
    """
		msg = message.content
    try:
			depends = msg.split(f'{prefixes[str(message.guild.id)]}battle ',1)[1]
		except IndexError:
			await message.channel.send('Breh Tell if you wanna join or not?')
			return

		msg = message.content
		if depends == 'start':
			global Names
			Names = {}
			global Dead
			dead = []
			with open('Names.json', 'w') as f:
				json.dump(dead, f)
			with open('Names.json', 'w') as f:
				json.dump(Names, f)
			global truefalse
			truefalse = True
			emoji = '<:PepeYes:868059827111358506>'
			await message.add_reaction(emoji)
			await message.channel.send(
			    f"A Match has started , Quickly type ```{prefixes[str(message.guild.id)]}battle join``` within 30 seconds"
			)
			a = time.time()
			b = 0
			while (b < 30):
				b = time.time() - a
				with open('Names.json', 'r') as f:
					Names = json.load(f)
			print(list(Names.keys()))
			#killed = kill(message,Names,Dead)
			hello = makeembed(
			    title="**Players**",
			    description=
			    f"If you just got a react like <:PepeOk:868375254093938728> then you are in "
			)
			await message.channel.send(embed=hello)
			pass
			functions = [
			    Rumble.kill, Rumble.killyourself, Rumble.revive, Rumble.calm
			]  #puttraps
			mlist = [discord.Colour.green(), discord.Colour.red()]
			randomclr = random.choice(mlist)
			while len(list(Names)) > 1:
				time.sleep(5)
				val = randomchooser(Names, message, functions)
				if len(list(Names)) >= 1:
					val2 = randomchooser(Names, message, functions)
				else:
					val2 = "Looks like a winner is to be announced"
				if val == None:
					val = "<:872114295238967306:sorry> Someone Killed someone but The System Could'nt retrive it"
				if val2 == None:
					val2 = "<:872114295238967306:sorry> Someone Killed someone but The System Could'nt retrive it"
				hello = makeembed(title="**Match in Progress**",
				                  description=f"**{val}\n {val2}**")
				await message.channel.send(embed=hello)
				pass
			hi = makeembed(
			    title="**Match Ended**",
			    description=f"**{Names} won and With these much bullets**")
			await message.channel.send(embed=hi)
			Names = {}
			dead = []
			with open('Dead.json', 'w') as f:
				json.dump(dead, f)
			with open('Names.json', 'w') as f:
				json.dump(Names, f)
				pass
		if depends == 'bot':
			#global Names
			Names = {}
			#global Dead
			dead = []
			with open('Dead.json', 'w') as f:
				json.dump(dead, f)
			with open('Names.json', 'w') as f:
				json.dump(Names, f)
			#global truefalse
			truefalse = True
			emoji = '<:PepeYes:868059827111358506>'
			await message.add_reaction(emoji)
			await message.channel.send(
			    f"A Match has started , Quickly type```{prefixes[str(message.guild.id)]} battle join``` within 30 seconds"
			)
			a = time.time()
			b = 0
			await message.channel.send("quickly setting a match with 5 bots")
			while (b < 30):
				b = time.time() - a
				with open('Names.json', 'r') as f:
					Names = json.load(f)
					Names["Bot1"] = 50
					Names["Bot2"] = 50
					Names["Bot3"] = 50
					Names["Bot4"] = 50
					Names["Bot5"] = 50

			print(list(Names.keys()))
			#killed = kill(message,Names,Dead)
			hello = makeembed(title="**Players**",
			                  description=f"The Match is starting")
			await message.channel.send(embed=hello)
			pass
			functions = [
			    Rumble.kill, Rumble.killyourself, Rumble.revive, Rumble.calm,
			    Rumble.calm, Rumble.kill, Rumble.kill, Rumble.killyourself,
			    Rumble.calm, Rumble.kill
			]  #puttraps
			while len(list(Names)) > 1:
				time.sleep(5)
				val = randomchooser(Names, message, functions)
				if len(list(Names)) >= 2:
					val2 = randomchooser(Names, message, functions)
				elif len(list(Names)) == 1:
					val2 = "Looks like a winner is to be announced"
				if val == None:
					val = "<:872114295238967306:sorry> Someone Killed someone but The System Could'nt retrive it"
				if val2 == None:
					val2 = "<:872114295238967306:sorry> Someone Killed someone but The System Could'nt retrive it"
				hello = makeembed(title="**Match in Progress**",
				                  description=f"**{val}\n {val2}**")
				await message.channel.send(embed=hello)
			hi = makeembed(
			    title="**Match Ended**",
			    description=f"**{Names} won and With these much bullets**")
			await message.channel.send(embed=hi)
			Names = {}
			dead = []
			with open('Dead.json', 'w') as f:
				json.dump(dead, f)
			with open('Names.json', 'w') as f:
				json.dump(Names, f)
			pass

		if depends == 'join':
			#if truefalse == False:
			#await message.channel.send('Ye Dum or what ? How Can you join a Match when it isnt even started \n type ```di battle start``` to start')
			#else:
			Name = message.author.name
			Names[Name] = 50
			await message.add_reaction('<:PepeOk:868375254093938728>')
			with open('Names.json', 'w') as f:
				print(Names)
				json.dump(Names, f)

		if depends == 'leave':
			if message.author.name in list(Names):
				del Names[message.author.name]
			else:
				await message.channel.send(
				    'AHHHH man , how can you even leave when you havent even joined'
				)
	await client.process_commands(message)

	#await client.edit_role(server='547874634978789398', role='' ,colour=0x008000)
	#value =  random.choice(flip)
	howgaystart = discord.Embed(
    title=f"**Role Changed**",
    description=f'The role Colour has been Changed',
    colour=discord.Colour.random())
  howgaystart.set_footer(text = 'Dank Island ',icon_url='https://cdn.discordapp.com/icons/821575403855544370/a_85c6630c72154018ecc7740c58411dea.gif?size=128')
  howgaystart.timestamp = datetime.datetime.utcnow()
  await ctx.send(embed=howgaystart)
  pass"""


@client.command(aliases=["dict", 'meaning'])
async def dictionary(ctx, *, message: str = None):
	if message == None:
		await ctx.send('Please Tell me a word also')
		return
	value = message.lower()
	data = json.load(open("data.json"))
	if value in data:
		meaning = data[value]
		#item = meaning[0:]
		howgaystart = makeembed(title='** Dank Island Dictionary **',
		                        description=''.join(meaning))
		await ctx.send(embed=howgaystart)
		pass
	elif value not in data:
		await ctx.send('wait sir this word Isnt in dictionary')


def makeword(data):
	number = random.choice(list(data))
	return number
	#elif word == Medium:


@client.command(aliases=['fastestwordfirst'])
async def fwf(ctx):
	data = json.load(open("data.json"))
	myword = makeword(data)

	#number = random.choice(data.keys())
	#if number
	embed = makeembed("A random word has been chosen", "starting in 3")
	msg = await ctx.send(embed=embed)
	await asyncio.sleep(1)
	embed = makeembed("A random word has been chosen", "starting in 2")
	await msg.edit(embed=embed)
	await asyncio.sleep(1)
	embed = makeembed("A random word has been chosen", "starting in 1")
	await msg.edit(embed=embed)

	#await ctx.send('Event Managers Please unlock After my Next Statement')
	await asyncio.sleep(1)
	await ctx.send(f'Everythings Done go Start, The Word is : \n {myword}')
	a = time.time()
	b = 0
	while (b < 400):
		b = time.time() - a
		#me = await client.get_user_info(f'{ctx.author.id}')
		#await client.send(ctx.author,f"Hey The Number is {number} DONT TELL ANYONE")
		response = await client.wait_for('message')
		try:
			guess = response.content
		except:
			#await ctx.channel.send('BREH you have to type a Number Dud')
			guess = None
		if guess == myword:
			break

	embed = makeembed(
	    "Someone Wrote The Word",
	    f"<@{response.author.id}> wrote it fast and right , Well Done")
	await response.reply(embed=embed)


def addnum(member):
	member = member.name
	with open("lotto.json") as f:
		lotto = json.load(f)
	lotto.append(member)
	with open("lotto.json", 'w') as f:
		json.dump(lotto, f)


def removenum(member):
	#member = member.name
	with open("lotto.json") as f:
		lotto = json.load(f)
	lotto.remove(member)
	with open("lotto.json", 'w') as f:
		json.dump(lotto, f)


@client.command(aliases=['lottery', 'l'])
@commands.has_role('Admin')
async def lotto(ctx, x: str, Member: discord.Member = None, value: int = None):
	if x == "add":
		if value == None:
			await ctx.send("breh tell me how many tickets to add")
			return
		with open("lotto.json") as f:
			lotto = json.load(f)
		for _ in range(value):
			addnum(Member)
		await ctx.send(f"Successfully added {value} tickets to that user")
	if x == "remove":
		if value == None:
			await ctx.send("breh tell me how many tickets to add")
			return
		print(value)
		print(Member)
		for _ in range(value):
			removenum(Member.name)
		await ctx.send(f"Succesfuly remove {value} tickets from that user")
	if x == "showmember":
		with open("lotto.json") as f:
			lotto = json.load(f)
		a = lotto.count(Member.name)
		await ctx.send(
		    f"The Number of tickets for this user {Member.name} are {a}")
	if x == "winner":
		with open("lotto.json") as f:
			lotto = json.load(f)
		answer = random.choice(lotto)
		embed = makeembed("The Winner is to be Announced",
		                  f"The winner is ||{answer}|| Congratulations 🎉🎉🎉")
		await ctx.send(embed=embed)
	if x == "show":
		with open("lotto.json") as f:
			lotto = json.load(f)
		something = set(list(lotto))
		for s in something:
			await ctx.send(embed=makeembed("Dank Island lottery",f"{s} has {lotto.count(s)} tickets"))
	if x == "clear":
		lotto = []
		with open("lotto.json", 'w') as f:
			json.dump(lotto, f)
		await ctx.send("Cleared the lottery")


@client.command(aliases=["lockdown"])
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel: discord.TextChannel = None):
	if channel == None:
		channel = ctx.channel
	overwrite = channel.overwrites_for(ctx.guild.default_role)
	overwrite.send_messages = False
	await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
	await ctx.send('Channel locked.')


@client.command(aliases=["unlockdown"])
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel: discord.TextChannel = None):
	if channel == None:
		channel = ctx.message.channel
	overwrite = channel.overwrites_for(ctx.guild.default_role)
	overwrite.send_messages = True
	await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
	await ctx.send('Channel unlocked.')


@client.command(aliases=["eventlock", "eventlockdown"])
@commands.has_role('Event Manager')
async def elock(ctx, channel: discord.TextChannel = None):
	if channel == None:
		channel = ctx.channel
	channels = [839482755062693959, 853283944232386560]
	if channel.id not in channels:
		await ctx.send(
		    "Bro its not a events Channel , you Arent a Head Moderator or Above to manage all channels"
		)
		return
	overwrite = channel.overwrites_for(ctx.guild.default_role)
	overwrite.send_messages = False
	await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
	await ctx.send('Channel locked.')


@client.command(aliases=["eventunlock", "eventunlockdown"])
@commands.has_role('Event Manager')
async def eunlock(ctx, channel: discord.TextChannel = None):
	if channel == None:
		channel = ctx.message.channel
	channels = [839482755062693959, 853283944232386560]
	if channel.id not in channels:
		await ctx.send(
		    "Bro its not a events Channel , you Arent a Head Moderator or Above to manage all channels"
		)
		return
	overwrite = channel.overwrites_for(ctx.guild.default_role)
	overwrite.send_messages = True
	await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
	await ctx.send('Channel unlocked.')


@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(error)
		await ctx.message.delete()
	elif isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(
		    "You have Used this Command IncorrectlyType The help of this Command and Write the Arguments required Properly"
		)
		await ctx.message.delete()
	#elif isinstance(error,commands.CommandInvokeError):
	#print(error)
	#await ctx.send("You have Used this Command Incorrectly Type The help of this Command and Write the Arguments required Properly")
	#await ctx.message.delete()
	elif isinstance(error, commands.MissingRole):
		await ctx.send(error)
		await ctx.message.delete()
	elif isinstance(error, commands.ChannelNotFound):
		await ctx.send(error)
		await ctx.message.delete()

	else:
		print(error)
		raise error


snipe_message_content = []
snipe_message_author = []
#url = []

@client.event
async def on_message_delete(message):
    snipe_message_content.append(message.content) 
    snipe_message_author.append(message.author) 

    await asyncio.sleep(60)


@client.command()
async def snipe(ctx,value:int=1):
    if snipe_message_content==[]:
        await ctx.send("Theres nothing to snipe.")
    else:
        value = value-value-value
        print(snipe_message_content,snipe_message_author)

        myvalue = snipe_message_content[value]
        myvalue2 = snipe_message_author[value]

        embed = makeembed(title="",description=f"{myvalue}")
        #embed.set_footer(text=f"Asked by {message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)
        embed.set_author(name= f"{myvalue2.name}#{myvalue2.discriminator}",icon_url=myvalue2.avatar_url)
        await ctx.send(embed=embed)
        return
def rules(value):
  rules.title = {"1":"**__Respect Others__**","2":"**__No Inappropriate Language__**","3":"**__No Pornographic and Gore__**","4":"**__No Spamming__**","5":"**__Keep The Use of Channels for Their Purposes__**","6":"**__No Impersonation__**","7":"__**No Scamming**__","11":"**__Asking for Promos__**","69":"Sample Gae","8":"**__No Begging__**","9":"__**No Advertising**__","10":"__**Mentions**__"}
  rules.rules = {"1":"Treat others the way you wanted to be treated. Discrimination, racism, feminism, stereotyping, and other forms of disrespect will not be tolerated.","2":"Using of profane language is allowed but must be kept at minimum and it should not point at someone. Throwing profanity and insulting words against someone will not be tolerated and might result to harsh punishment.","3":"This is a SFW server. Pornographic or anything that contains violence is not allowed.","4":"Spamming or anything that is considered repetitive is not strictly allowed. Do not disrupt chat.","5":"Do not use channels for anything but their intended purposes.","6":"Whoever it may be, impersonation is strictly not allowed. Impersonating someone within the server may result to punishment.","7":"Scamming or attempting to scam is strictly prohibited.","11":"Asking for promos may get staff demoted , So Staff Shouldn't ask for promos","69":"Akash is best staff ngl","8":"Do not beg for anything! Not dank memer coins, not nitros, not roles. ","9":"Do not advertise anything within the server or in other members' DMs unless you are given the permission to do so.","10":"Do not mention users without a good reason and do not ping any of the staffs more than once for a question or concerns. If you have any concern, go to <#839487324920348673>"}
  hi = makeembed(rules.title[value],rules.rules[value])
  return hi
@client.command()
async def rule(ctx,value:int=0):
  if value == 0 or value > 69:
    await ctx.send("Thats not a valid rule")
    return

  await ctx.message.delete()
  embed = rules(str(value))
  embed.set_author(name= "Dank Island Rules",icon_url="https://cdn.discordapp.com/icons/821575403855544370/a_85c6630c72154018ecc7740c58411dea.gif?size=128")
  await ctx.send(embed=embed)
def rolelist(ctx,member):
  EM=discord.utils.get(ctx.guild.roles,name=("Event Manager"))
  GM=discord.utils.get(ctx.guild.roles,name=("Giveaway Manager"))
  TM=discord.utils.get(ctx.guild.roles,name=("Trial Mod"))
  M=discord.utils.get(ctx.guild.roles,name=("Moderator"))
  HM=discord.utils.get(ctx.guild.roles,name=("Head Moderator"))
  TA=discord.utils.get(ctx.guild.roles,name=("Trial Admin"))
  A=discord.utils.get(ctx.guild.roles,name=("Admin"))
  if member.top_role < EM:
    return EM
  if member.top_role < GM:
    return GM
  elif member.top_role < TM:
    return TM
  elif member.top_role < M:
    return M
  elif member.top_role < HM:
    return HM
  elif member.top_role < TA:
    return TA
  elif member.top_role < A:
    return A
  else:
    return -1

@client.command(aliases=["promo"])
@commands.has_permissions(administrator=True)
async def promote(ctx,member:discord.Member=None):
  if member ==  None:
    await ctx.send("You can't promote yourself , that will be cheating :)")
    return
  role = rolelist(ctx,member)
  if role == -1:
    await ctx.send("The user is Above Admin or has higher higharchy")
    return
  await member.add_roles(role)
  print(role)
  embed = makeembed("Promotion!!!",f"{member.mention} got promoted to {role.mention}")
  await ctx.send(embed=embed)

def rolemeh(ctx,member):
  EM=discord.utils.get(ctx.guild.roles,name=("Event Manager"))
  GM=discord.utils.get(ctx.guild.roles,name=("Giveaway Manager"))
  TM=discord.utils.get(ctx.guild.roles,name=("Trial Mod"))
  M=discord.utils.get(ctx.guild.roles,name=("Moderator"))
  HM=discord.utils.get(ctx.guild.roles,name=("Head Moderator"))
  TA=discord.utils.get(ctx.guild.roles,name=("Trial Admin"))
  A=discord.utils.get(ctx.guild.roles,name=("Admin"))
  HA=discord.utils.get(ctx.guild.roles,name=("Head Admin"))
  if member.top_role > HA:
    return -1

  if A in member.roles:
    return A
  elif TA in member.roles:
    return TA
  elif HM in member.roles:
    return HM
  elif M in member.roles:
    return M
  elif TM in member.roles:
    return TM
  elif GM in member.roles:
    return GM
  elif EM in member.roles:
    return EM
  else:
    return -2
  

  

@client.command(aliases=["demo"])
@commands.has_permissions(administrator=True)
async def demote(ctx,member:discord.Member=None):
  if member ==  None:
    await ctx.send("You can't demote yourself , why you even waana do it :)")
    return
  role = rolemeh(ctx,member)
  if role == -1:
    await ctx.send("The user is Above Admin or has higher higharchy, i cant demote")
    return
  if role == -2:
    await ctx.send("That user even doesnt have event Manager How can you demote him")
    return
  await member.remove_roles(role)
  embed = makeembed("Demotion!!!",f"{member.mention} got demoted from {role.mention} :( So Sad.")
  await ctx.send(embed=embed)


@client.command()
async def view(ctx,member : discord.Member = None):
  if member == None:
    await ctx.send("Please Mention a Member")
  value = Warnings.view(member.id,member.name)
  if value == -1:
    await ctx.send("The Member Has Not Donated or His Dono isnt Mentioned")
    return
  else:
    for x in value:
      if x[0] == member.id:
        y=x
        break
      else:
        continue
    value = y[2]
    embed = makeembed("View Member Donations!!!",
	                      f"This Person Has Donated {value} dmc in Dank Island")
    embed.set_footer(
      text=f'{member.name}\'s Donations',
	    icon_url=
	    f'{member.avatar_url}'
	    )
    await ctx.send(embed=embed)

def seperate(amt):
  try:
    allval = int(amt[:-2])
  except:
    return -2
  val = amt[-1]
  val = int(val)
  amt = allval * 10**val
  
  print(amt)
  return amt



@client.command(aliases = ['adono'])
async def adddono(ctx,member : discord.Member = None,amt:str=None):
  if member == None:
    await ctx.send("Please Mention a Member")
    return
  if amt == None:
    await ctx.send("Please Mention a Amount As well")
    return
  if "e" in amt:
    amt = seperate(amt)
    if amt == -2:
      await ctx.send("Please mention a valid Number")
      return
  else:
    try:
      amt = int(amt)
    except:
      await ctx.send("Send a Number Please")
      return
  print(member.id)
  value = Warnings.add(int(member.id),member.name,amt)
  if value == -1:
      await ctx.send("The User Has not been defined Please define the member using the makenew cmd")
      return
  oldvalue = value[0]
  newvalue = value[1]
  amount = value[2]

  embed = makeembed("Member Donated!!!!",
	                      f"{member.name} Has Donated {amount}\n Old donations : {oldvalue} \n Updated Donations : {newvalue}")
  embed.set_footer(
      text=f'{member.name}\'s Donations',
	    icon_url=
	    f'{member.avatar_url}'
	    )
  await ctx.send(embed=embed)

@client.command(aliases=['remdono','rdono'])
async def removedono(ctx,member : discord.Member = None,amt:str=None):
  if member == None:
    await ctx.send("Please Mention a Member")
    return
  if amt == None:
    await ctx.send("Please Mention a Amount As well")
    return
  if "e" in amt:
    amt = seperate(amt)
    if amt == -2:
      await ctx.send("Please mention a valid Number")
      return
  else:
    try:
      amt = int(amt)
    except:
      await ctx.send("Send a Number Please")
      return
  print(member.id)
  value = Warnings.remove(int(member.id),member.name,amt)
  if value == -1:
      await ctx.send("The User Has not been defined Please define the member using the makenew cmd")
      return
  if value == -2:
      await ctx.send("This remove will turn his donations in negative, i cant do it")
      return
  oldvalue = value[0]
  newvalue = value[1]
  amount = value[2]

  embed = makeembed("Member Donation Remove!!!!",
	                      f"{member.name}'s donations got removed by {amount}\n Old donations : {oldvalue} \n Updated Donations : {newvalue}")
  embed.set_footer(
      text=f'{member.name}\'s Donations',
	    icon_url=
	    f'{member.avatar_url}'
	    )
  await ctx.send(embed=embed)

@client.command()
async def makenew(ctx,member : discord.Member = None,amount : str=None):
  if member == None:
    await ctx.send("Please mention a Member")
  if amount == None:
    amount = 0.0
  if "e" in amount:
    amount = seperate(amount)
  value = Warnings.insert(member.id,member.name,amount)
  if value == -1:
    await ctx.send("The Member Already Exists")
    return
  await ctx.send("The Member is Created Successfully")




keep_alive()
client.run(os.environ['TOKEN'])
