import discord
from discord.ext import commands
from API import set_event

client = commands.Bot(command_prefix = 'rb.')

@client.event
async def on_ready():
    print('Open')

@client.command()
async def event(ctx, dungeon, time, info):
    embed = discord.Embed(title='Event Started', color=0x00ff00)
    embed.add_field(name='\u200b', value='Dungeon being run: '+dungeon, inline=False)
    embed.add_field(name='\u200b', value='This event will take place '+time, inline=False)
    embed.add_field(name='Info', value='This event will be ran in the '+dungeon+' category. React to this message with :thumbsup: to be given access to the channels', inline=False)
    embed.add_field(name='Extra info from the Raid Leader', value=info, inline=False)
    toreactto = await ctx.send(embed=embed)
    await toreactto.add_reaction('\N{THUMBS UP SIGN}')
    file = open('event.txt', 'w')
    file.write(str(toreactto.id))
    file.close()
    file = open('role.txt', 'w')
    file.write(str(dungeon))
    file.close()
    guild = ctx.guild
    rolemade = await guild.create_role(name=dungeon)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        rolemade: discord.PermissionOverwrite(read_messages=True)
    }
    category = await guild.create_category_channel(dungeon, overwrites=overwrites)
    plan = await guild.create_text_channel('raid-plan', category=category)
    chat = await guild.create_text_channel('raid-chat', category=category)
    vc = await guild.create_voice_channel('raid-vc', category=category)
    set_event(ctx.author.display_name, dungeon, info)

@client.event
async def on_raw_reaction_add(payload):
    try:
        message_id = payload.message_id
        file = open('event.txt', 'r')
        eventreac = int(file.readlines()[0])
        file.close()
        file = open('role.txt', 'r')
        eventrole = (file.readlines()[0])
        file.close()
        print(str(eventreac))
        if message_id == eventreac:
            print('match')
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
            print(guild)
            roletogive = discord.utils.get(guild.roles, name=eventrole)
            print(roletogive.name)
            sender = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            print(sender.id)
            await sender.add_roles(roletogive)
    except:
        pass

@client.command()
async def end_event(ctx, dungeon, turnout):
    try:
        file = open('event.txt', 'w')
        file.close()
        file = open('role.txt', 'r')
        eventrole = (file.readlines()[0])
        file.close()
        file = open('role.txt', 'w')
        file.close()
        guild = ctx.guild
        roletogive = discord.utils.get(guild.roles, name=eventrole)
        for channel in ctx.guild.channels:
            if channel.name in ['raid-plan', 'raid-chat', 'raid-vc', eventrole]:
                await channel.delete()
        for rolet in ctx.guild.roles:
            if rolet.name == eventrole:
                await rolet.delete()
    except:
        pass
    embed = discord.Embed(title='Event concluded', color=0x00ff00)
    embed.add_field(name='Dungeon Ran', value=dungeon, inline=False)
    embed.add_field(name='Turnout', value=turnout, inline=False)
    await ctx.send(embed=embed)
    set_event('[]', '[]', '[]')



client.run('NzI5NjI5ODExMjIzNDI5MjAx.XwLuuw._cPNCSeB-8r723NKmdB8hSsdEnM')
