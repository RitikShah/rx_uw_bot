import discord
import logging
import asyncio
import re
import tk
from random import randint
from discord.ext import commands

print('Y for Debug')
if input() == 'Y':
	meetup_channel = 400567035249033217
	meetup_mention = '<@&489719429224071168>'
else:
	meetup_channel = 362691852274630657
	meetup_mention = '<@&487120797190848534>'

logging.basicConfig(level="INFO")

bot = commands.Bot(command_prefix="?", description="Rx has the best bot let that be heard.")
setattr(bot, "logger", logging.getLogger("log"))
url_pattern = '(https?:\\/\\/(?:www\\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\\.[^\\s]{2,}|www\\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\\.[^\\s]{2,}|https?:\\/\\/(?:www\\.|(?!www))[a-zA-Z0-9]\\.[^\\s]{2,}|www\\.[a-zA-Z0-9]\\.[^\\s]{2,})'

event_list = []
#meetup_channel = 400567035249033217
#meetup_channel = 362691852274630657

rx_uw_bot_id = 489158438086115328

def check_meetup_channel(ctx):
	return ctx.message.channel.id == meetup_channel

x_emojis = ['❎', '❌', '✖️']
check_emojis = ['☑️', '✔️', '✅']

@bot.event
async def on_ready():
	print("\nRX UW Bot is Online!\n")

@bot.event
async def on_reaction_add(reaction, user):
	for event in event_list:
		if event[0].id == reaction.message.id:
			if str(reaction.emoji) in x_emojis and user == event[1]:
				event_list.remove(event)
				await reaction.message.channel.send("❎ Event Deleted!", delete_after=5.0)
				await event[0].delete()
			elif str(reaction.emoji) in check_emojis and user == event[1]:
				event_list.remove(event)
				await reaction.message.channel.send("✅ Event Unpinned!", delete_after=5.0)
				await event[0].unpin()

'''
@bot.event
async def on_guild_channel_pins_update(channel, last_pin):
	message_pins = await channel.pins()
	for event in event_list:
		for pin in message_pins:
			if event[0].id == pin.id:
				event_list.remove(event)
'''

@bot.event
async def on_message_delete(message):
	if message.author.id == rx_uw_bot_id:
		for event in event_list:
			if event[0].id == message.id:
				event_list.remove(event)

@bot.command()
@commands.cooldown(rate=20,per=10,type=commands.BucketType.user)
async def hello(ctx):
	rint = randint(0,1000)
	if rint > 999:
		message = await ctx.send("Honestly, if you see this message, you are amazing. This message has a 0.1% chance of showing. \nYou, {}, are a motherfucking God\n\nDo screenshot this. \n~ Rx".format(ctx.author))
	elif rint > 990:
		message = await ctx.send("Wow, hit the lottery today {}, cause you just hit a 1% lottery!".format(ctx.author))
	elif rint > 900:
		message = await ctx.send("Good day, my good sir, {}".format(ctx.author))
	elif rint > 500:
		message = await ctx.send("Hello?")
	else:
		message = await ctx.send("Hello world!")

@bot.command()
@commands.cooldown(rate=3,per=120,type=commands.BucketType.user)
@commands.check(check_meetup_channel)
@commands.has_any_role('meetup', 'Mods', 'Admins')
async def meetup(ctx):
	event = {}
	bot_messages = []

	def check(msg):
		return msg.author == ctx.author and msg.channel.id == meetup_channel

	def is_url(url):
		prog = re.compile(url_pattern)
		return prog.search(url)

	try:
		bot_messages.append(await ctx.send("What is the title of this meetup?", delete_after=60.0))
		msg = await bot.wait_for('message', timeout=60.0, check=check)
		event['title'] = msg 

		bot_messages.append(await ctx.send("When and Where (Ex: Tommorow 3 @ Starbucks)", delete_after=60.0))
		msg = await bot.wait_for('message', timeout=60.0, check=check)
		event['when_where'] = msg 

		bot_messages.append(await ctx.send("What is the period of time (Ex: 12:30)?", delete_after=60.0))
		msg = await bot.wait_for('message', timeout=60.0, check=check)
		event['time'] = msg 

		bot_messages.append(await ctx.send("Is this casual or structured?", delete_after=60.0))
		msg = await bot.wait_for('message', timeout=60.0, check=check)
		event['type'] = msg 

		bot_messages.append(await ctx.send("What are we doing?", delete_after=60.0))
		msg = await bot.wait_for('message', timeout=60.0, check=check)
		event['activity'] = msg 

		bot_messages.append(await ctx.send("What is the cost range?", delete_after=60.0))
		msg = await bot.wait_for('message', timeout=60.0, check=check)
		event['cost'] = msg 

		bot_messages.append(await ctx.send("Write a small description about this meetup.", delete_after=60.0))
		msg = await bot.wait_for('message', timeout=60.0, check=check)
		event['description'] = msg 

		bot_messages.append(await ctx.send("Paste a link to Google Maps or anything else (Optional, put a non-url to skip).", delete_after=60.0))
		msg = await bot.wait_for('message', timeout=60.0, check=check)
		event['location'] = msg
		
	except asyncio.TimeoutError:
		await ctx.send(":thumbsdown:, Your request timed out", delete_after=15.0)

		for key, msg in event.items():
			await msg.delete()

	else:
		if is_url(event['location'].content) is not None:
			embed = discord.Embed(title=event['title'].content, url=event['location'].content, description=event['when_where'].content, color=0x00baa6)
		else:
			embed = discord.Embed(title=event['title'].content, description=event['when_where'].content, color=0x00baa6)
		embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
		embed.add_field(name='Type', value=event['type'].content, inline=True)
		embed.add_field(name='Time', value=event['time'].content, inline=True)
		embed.add_field(name='Activity', value=event['activity'].content, inline=True)
		embed.add_field(name='Cost', value=event['cost'].content, inline=True)
		embed.set_footer(text=event['description'].content)
		
		# meetup role: <@&487120797190848534>
		embed_msg = await ctx.send('A new {} has appeared!'.format(meetup_mention), embed=embed)
		await embed_msg.pin()
		await embed_msg.add_reaction('👍')
		await embed_msg.add_reaction('👀')
		await embed_msg.add_reaction('👎')

		event_list.append((embed_msg, ctx.author))

		await ctx.send("👍 Meetup successfully created! Add any X emoji to the message to delete the event. Add any check emoji to unpin the event.", delete_after=10.0)

		for key, msg in event.items():
			await msg.delete()

		for msg in bot_messages:
			await msg.delete()

		await ctx.message.delete()

bot.run(tk.token())
