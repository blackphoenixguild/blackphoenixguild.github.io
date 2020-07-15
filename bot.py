import discord
from discord.ext import commands
import scraper
import random

client = commands.Bot(command_prefix = 'rb.')
client.remove_command('help')

@client.event
async def on_ready():
    print('STARTED')
    await client.change_presence(activity=discord.Game(name='ROTMG'))

@client.command()
async def search(ctx, *, searcher):
    embed = discord.Embed(title='Search results for: ' + searcher, color=random.randint(0, 0xffffff))
    result = scraper.get_pages_from_search(searcher)
    message = ''
    for page in result:
        embed.add_field(name='\u200b', value=page, inline=False)
    await ctx.send(embed=embed)

async def readinfo(ctx, url):
    res = scraper.get_wiki_page(url)
    stats = res[1]
    embed = discord.Embed(title=res[0], color=random.randint(0, 0xffffff))
    statmessage = ''
    for stat in stats:
        statmessage += stat + '\n'
    embed.add_field(name='description', value=res[2], inline=False)
    embed.add_field(name='stats', value=statmessage, inline=False)
    #embed.add_field(name='more info', value=res[3], inline=False)
    
    await ctx.send(embed=embed)

@client.command()
async def wikiurl(ctx, *, url):
    await readinfo(ctx, url)

@client.command()
async def wiki(ctx, *, name):
    await readinfo(ctx, 'https://www.realmeye.com/wiki/' + name.replace(" ", "-"))

@client.command()
async def help(ctx):
    embed = discord.Embed(title='very helpful help', color=random.randint(0, 0xffffff))
    embed.add_field(name='if you want actual help, use rb.help_', value='Stop begging and go play the game', inline=False)
    await ctx.send(embed=embed)

@client.command()
async def help_(ctx):
    embed = discord.Embed(title='very helpful help', color=random.randint(0, 0xffffff))
    embed.add_field(name='rb.search', value='Searches the wiki and provides the first 10 results from what you entered.', inline=False)
    embed.add_field(name='Example Usage', value='```rb.search dirk of cronus```', inline=False)
    embed.add_field(name='rb.wikiurl', value='Reads a wiki page based on the URL you provide.', inline=False)
    embed.add_field(name='Example Usage', value='```rb.wikiurl https://www.realmeye.com/wiki/doom-bow```', inline=False)
    embed.add_field(name='rb.wiki', value='Reads the wiki page of the item you enter.', inline=False)
    embed.add_field(name='Example Usage', value='```rb.wiki unstable anomaly```', inline=False)
    await ctx.send(embed=embed)


def guild_read_page():
    file = open('guild_board.txt', 'r')
    lines = file.readlines()
    new = []
    for line in lines:
        new.append(line.rsplit('\n')[0])
    lines = new
    output = []
    for i in range(0, len(lines), 2):
        output.append([lines[i], lines[i+1]])
    return output

def guild_write_page(arr):
    file = open('guild_board.txt', 'w')
    for notice in arr:
        file.write(notice[0])
        file.write('\n')
        file.write(str(notice[1]))
        file.write('\n')

@client.command()
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)

@client.command()
async def guild_add(ctx, *, message):
    guild_board = guild_read_page()
    guild_board.append([message, random.randint(1, 1000000)])
    guild_write_page(guild_board)
    embed = discord.Embed(title='Message added', color=0x00ff00)
    embed.add_field(name='\u200b', value=message, inline=False)
    await ctx.send(embed=embed)

@client.command()
async def board(ctx):
    guild_board = guild_read_page()
    embed = discord.Embed(title='Notices', color=random.randint(0, 0xffffff))
    for post in guild_board:
        embed.add_field(name=post[1], value=post[0], inline=False)
    await ctx.send(embed=embed)

@client.command()
async def guild_remove(ctx, id_):
    guild_board = guild_read_page()
    for i, notice in enumerate(guild_board):
        if str(notice[1]) == str(id_):
            guild_board.pop(i)
    guild_write_page(guild_board)

@client.command()
async def event(ctx, dungeon, datetime, section, *, info):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title='Guild Event', color=0x00ff00)
    embed.add_field(name='\u200b', value='Dungeon being Run: '+dungeon, inline=False)
    embed.add_field(name='\u200b', value='This event will be run '+datetime, inline=False)
    embed.add_field(name='\u200b', value='More information will be found in guild section '+section, inline=False)
    embed.add_field(name='\u200b', value=info, inline=False)
    embed.add_field(name='\u200b', value='React with :thumbsup: to confirm you can take part, or :thumbsdown: if you are unable. See you then!')
    sent = await ctx.send(embed=embed)
    await sent.add_reaction('\N{THUMBS UP SIGN}')
    await sent.add_reaction('\U0001F44E')
    await sent.pin()
    await ctx.channel.purge(limit=1)

@client.command()
async def react(ctx, id_):
    await ctx.channel.purge(limit=1)
    msg = await ctx.fetch_message(int(id_))
    await msg.add_reaction('\N{THUMBS UP SIGN}')
    await msg.add_reaction('\U0001F44E')

@client.command()
async def react2(ctx, id_):
    await ctx.channel.purge(limit=1)
    msg = await ctx.fetch_message(int(id_))
    await msg.add_reaction('\N{THUMBS UP SIGN}')

non = ['<@722099695702507620>']

@client.command()
async def giveaway(ctx):
    embed = discord.Embed(title='Giveaway', color=0x00ff00)
    members = ctx.guild.members
    rand = random.randint(1, 10000000)
    random.seed = rand
    winner = random.choice(members)
    while winner.mention in non:
        winner = random.choice(members)
    print(winner.mention)
    embed.add_field(name='\u200b', value='The winner is: '+winner.mention, inline=False)
    await ctx.send(embed=embed)

@client.command()
async def end_event(ctx, dungeon, turnout):
    target_channel = 723605953777500210
    target = client.get_channel(target_channel)
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title='Event concluded', color=0x00ff00)
    embed.add_field(name='dungeon ran', value=dungeon, inline=False)
    embed.add_field(name='number of participants', value=turnout, inline=False)
    await target.send(embed=embed)

'''    old = msgtwo.embeds[0]
    oldfield = old.fields[1]
    print(oldfield.value)
    old.set_field_at(1, name='pot', value=oldfield.value+'test', inline=False)
    await msgtwo.edit(embed=old)'''

@client.command()
async def initial(ctx):
    embed = discord.Embed(title='Giveaway Information', color=0x00ff00)
    embed.add_field(name='info', value='If you have any items or potions that you do not want, give them to one of the guild admins and they will store it for the next giveaway. Below this there will be a list of the current pot of the next giveaway. React to this message with :thumbsup: to enter.', inline=False)
    embed.add_field(name='pot', value='Items available:', inline=False)
    await ctx.send(embed=embed)

@client.command()
async def edit_pot(ctx, newitem):
    await ctx.channel.purge(limit=1)
    msgtwo = await ctx.fetch_message(724935634673860710)
    old = msgtwo.embeds[0]
    oldfield = old.fields[1]
    old.set_field_at(1, name='pot', value=oldfield.value+'\n'+newitem, inline=False)
    await msgtwo.edit(embed=old)

@client.command()
async def clear_pot(ctx):
    msgtwo = await ctx.fetch_message(724935634673860710)
    old = msgtwo.embeds[0]
    oldfield = old.fields[1]
    old.set_field_at(1, name='pot', value='Items available:', inline=False)
    await msgtwo.edit(embed=old)
    await ctx.channel.purge(limit=1)

@client.command()
async def realmeye(ctx, *, search_term):
    if scraper.get_realmeye_response(search_term) == None:
        embed = discord.Embed(title='Error', color=0xff0000)
        embed.add_field(name='\u200b', value='No Realmeye response found. Make sure you capitalise correctly.', inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='Realmeye response', color=0x00ff00)
        embed.add_field(name='results', value=scraper.get_realmeye_response(search_term), inline=False)
        await ctx.send(embed=embed)

@client.command()
async def profile(ctx, name):
    info = scraper.get_player_info(name)
    desc = scraper.get_player_description(name)
    if info == None:
        embed = discord.Embed(title='Error', color=0xff0000)
        embed.add_field(name='\u200b', value='No player profile found.', inline=False)
    else:
        embed = discord.Embed(title=name, color=0x00ff00)
        for i in range(0, len(info), 2):
            embed.add_field(name='\u200b', value=info[i]+': '+info[i+1], inline=False)
        if desc == None:
            embed.add_field(name='\u200b', value='This player has no description', inline=False)
        else:
            embed.add_field(name='Description:', value=desc, inline=False)
    await ctx.send(embed=embed)

@client.command()
async def reaction(ctx, id_):
    #await ctx.channel.purge(limit=1)
    guild = ctx.guild
    role = guild.get_role(722196007584137269)
    msg = await ctx.fetch_message(int(id_))
    react = msg.reactions
    for rea in react:
        if str(rea) == '\U0001f44d':
            print('up')
            users = await rea.users().flatten()
            for user in users:
                await ctx.send(user.mention)
                await user.add_roles(role)

@client.command()
async def give(ctx, msgid):
    message = await ctx.fetch_message(msgid)
    users = set([user for reaction in message.reactions for user in await reaction.users().flatten()])
    chosen = random.sample(users, 1)[0]
    while chosen.mention in non:
        chosen = random.sample(users, 1)[0]
    await ctx.send(chosen.mention)

@client.command()
async def give2(ctx, pers):
    await ctx.channel.purge(limit=1)
    person = client.get_user(int(pers))
    print(person.mention)
    await ctx.send(person.mention)
classes_ = [
    '<:wizard:727980630855647304>',
    '<:warrior:727980615667941417>',
    '<:trickster:727980595564642325>',
    '<:sorcerer:727980580259627058>',
    '<:samurai:727980356783046666>',
    '<:rogue:727980567605280809>',
    '<:priest:727980534827057163>',
    '<:paladin:727980520415428620>',
    '<:ninja:727980499754287134>',
    '<:necromancer:727980484206002209>',
    '<:mystic:727980454883623052>',
    '<:knight:727980424336375809>',
    '<:huntress:727980399652896779>',
    '<:bard:727980334540390451>',
    '<:assassin:727980311459266620>',
    '<:archer:727980295759986779>'
]

@client.command()
async def classes(ctx, id_):
    await ctx.channel.purge(limit=1)
    msg = await ctx.fetch_message(int(id_))
    for clas in classes_:
        await msg.add_reaction(clas)

toreactwith = [
    '<:puri:728166403433037925>',
    '<:qot:728166543585837117>',
    '<:paladin:727980520415428620>',
    '<:knight:727980424336375809>',
    '<:mystic:727980454883623052>',
    '<:archer:727980295759986779>'
]

@client.command()
async def classcheck(ctx, Title__):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title=Title__, color=0x00ff00)
    embed.add_field(name='\u200b', value='If you are playing mystic, react with <:mystic:727980454883623052>', inline=False)
    embed.add_field(name='\u200b', value='If you are playing archer (No QoT) , react with <:archer:727980295759986779>', inline=False)
    embed.add_field(name='\u200b', value='If you are playing knight, react with <:knight:727980424336375809>', inline=False)
    embed.add_field(name='\u200b', value='If you are playing paladin, react with <:paladin:727980520415428620>', inline=False)
    embed.add_field(name='\u200b', value='If you are a priest with a tome of purification, react with <:puri:728166403433037925>', inline=False)
    embed.add_field(name='\u200b', value='If you are an archer with a Quiver of Thunder, react with <:qot:728166543585837117>', inline=False)
    embed.add_field(name='\u200b', value='Ideally, there would be at least one of each of the key roles listed above. However, some are not as necessary, such as QoT and paladin.', inline=False)
    msg = await ctx.send(embed=embed)
    for reacton in toreactwith:
        await msg.add_reaction(reacton)
    

client.run('NzIyMDk5Njk1NzAyNTA3NjIw.XueJxQ.tiy1U8vqlxhZGsnzmPGfNmQEKfo')
