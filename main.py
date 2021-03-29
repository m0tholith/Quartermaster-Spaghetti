import discord, asyncio, random, datetime, asyncpraw, database_functions, os
from discord.ext import tasks, commands

# Bot Setup 
prefix = '.'
client = commands.Bot(command_prefix = prefix, intents = discord.Intents.all(), help_command = None)

# Update Embed
client.update_embed = discord.Embed(title = 'No updates for now.', description = 'When there\'s an update, you\'ll be notified!', color = discord.Color.dark_blue())
client.update_released = False

# XP Dictionary
client.xp = {}

# Guilds in Setup List
client.setup_guilds = []

# Minesweeper Dictionary
client.minesweeper = {}

# PRAW Setup
reddit_id = 'x-CeFNb7pjkh7w'
reddit_secret = 'YutzD0KuEUw1X2TrSZsMKvjW5MpylQ'
reddit = asyncpraw.Reddit(client_id = reddit_id, client_secret = reddit_secret, user_agent = f'python:{reddit_id}:1.0 (by u/ahkh78)')

# XP File Reset
for file in os.listdir():
    if file.startswith('xp ') or file == 'ttt.txt':
        print('clearing ' + file)
        open_file = open(file, 'w')
        open_file.write('')
        open_file.close()

# Activate Reaction Roles
IDs = []
for x in client.guilds:
    IDs.append(x.id)
database_functions.activate_reaction_roles(IDs)

# Tasks
@tasks.loop(seconds = 30)
async def vc_xp():
    for x in client.guilds:
        for y in x.voice_channels:
            for z in y.members:
                database_functions.add_xp(x.id, z.id, 1)
                print(f'added 1 XP to {z.name} because they were in a VC, they now have {database_functions.get_xp(x.id, z.id)} local XP')

# Miscellaneous Functions
def intTryParse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False

def is_admin(msg):
    is_admin = False
    admin = discord.utils.get(msg.guild.roles, name = database_functions.get_admin(msg.guild.id))
    for x in msg.author.roles:
        if x.position == admin.position:
            is_admin = True
    return is_admin

def is_text_channel(msg):
    if isinstance(msg.channel, discord.TextChannel):
        return True
    return False

def is_dm(msg):
    if isinstance(msg.channel, discord.DMChannel):
        return True
    return False

def is_in_setup(guild_id):
    if str(msg.guild.id) in client.setup_guilds and message.startswith(prefix):
        if not msg.channel.name == 'bot-setup':
            return True
        return False

# Events
@client.event
async def on_message_delete(message):
    if message.author.bot: return

    await discord.utils.get(message.guild.channels, name = database_functions.get_logs(message.guild.id)).send(embed=log_embed(message, True))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all the required arguments. If you don\'t know what they are, check the help command.')
        if client.update_released:
            if random.randint(1, 100) >= 75:
                await ctx.send(f'~~New update! Check the {prefix}updates command!~~')
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send('I don\'t have the required permissions to execute that command.')
        if client.update_released:
            if random.randint(1, 100) >= 75:
                await ctx.send(f'~~New update! Check the {prefix}updates command!~~')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('You don\'t haave the permissions to do that.')
        if client.update_released:
            if random.randint(1, 100) >= 75:
                await ctx.send(f'~~New update! Check the {prefix}updates command!~~')
    elif isinstance(error, commands.ConversionError):
        await ctx.send('You put the wrong type of variable in one of the inputs, please pass in the correct types.')
        if client.update_released:
            if random.randint(1, 100) >= 75:
                await ctx.send(f'~~New update! Check the {prefix}updates command!~~')
    elif isinstance(error, commands.CheckFailure):
        await ctx.send('Either this channel isn\'t the correct place to execute this message or you don\'t have the permissions to execute it.')
        if client.update_released:
            if random.randint(1, 100) >= 75:
                await ctx.send(f'~~New update! Check the {prefix}updates command!~~')
    elif isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MemberNotFound) or isinstance(error, commands.UserNotFound):
        await ctx.send('I couldn\'t find that member.')
        if client.update_released:
            if random.randint(1, 100) >= 75:
                await ctx.send(f'~~New update! Check the {prefix}updates command!~~')
    elif isinstance(error, commands.ChannelNotFound):
        await ctx.send('I couldn\'t find that channel.')
        if client.update_released:
            if random.randint(1, 100) >= 75:
                await ctx.send(f'~~New update! Check the {prefix}updates command!~~')
    elif isinstance(error, commands.EmojiNotFound):
        await ctx.send('I couldn\'t find that emoji.')
        if client.update_released:
            if random.randint(1, 100) >= 75:
                await ctx.send(f'~~New update! Check the {prefix}updates command!~~')
    else:
        await ctx.send('Something went wrong, but I can\'t point my finger on it. Try checking if I have the correct permissions. If that doesn\'t work, you can report this in the support server (<https://discord.gg/nvhwvjkGBW>)')
        print(str(error))

@client.event
async def on_ready():
    print(f'We\'ve logged in as {client.user}')
    i = 0
    for x in client.guilds:
        i += 1
    await client.change_presence(activity = discord.Game(f'with {i} servers ({prefix}about / {prefix}help)'))
    if not vc_xp.is_running():
        vc_xp.start()
    
@client.event
async def on_guild_join(guild):
    i = 0
    for x in client.guilds:
        i += 1
    await client.change_presence(activity = discord.Game(f'with {i} servers ({prefix}about / {prefix}help)'))
    if not vc_xp.is_running():
        vc_xp.start()
    client.setup_guilds.append(str(guild.id))

@client.event
async def on_guild_remove(guild):
    i = 0
    for x in client.guilds:
        i += 1
    await client.change_presence(activity = discord.Game(f'with {i} servers ({prefix}about / {prefix}help)'))
    if not vc_xp.is_running():
        vc_xp.start()
    try:
        client.setup_guilds.remove(str(guild.id))
    except:
        pass

ttt_board = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:']
@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return
    if str(reaction.message.guild.id) in client.setup_guilds:
        return
    if user.id == client.user.id: return
    print(f'reaction id is {reaction.emoji}')
    golden_emoji = ''
    for x in reaction.message.reactions:
        if x.emoji == discord.utils.get(discord.utils.get(client.guilds, name = 'Quartermaster Spaghetti\'s emotes').emojis, name = 'QuartermasterSpaghetti'):
            print('reaction is from help message')
            if reaction.emoji == '1️⃣':
                print('reaction is 1')
                await reaction.message.edit(embed = help_embed(0))
                await reaction.message.clear_reactions()
                await reaction.message.add_reaction('<:QuartermasterSpaghetti:804358582819880973>')
                await reaction.message.add_reaction('1️⃣')
                await reaction.message.add_reaction('2️⃣')
                await reaction.message.add_reaction('3️⃣')
                await reaction.message.add_reaction('4️⃣')
                await reaction.message.add_reaction('5️⃣')
                await reaction.message.add_reaction('6️⃣')
                
            elif reaction.emoji == '2️⃣':
                print('reaction is 2')
                await reaction.message.edit(embed = help_embed(1))
                await reaction.message.clear_reactions()
                await reaction.message.add_reaction ('<:QuartermasterSpaghetti:804358582819880973>')
                await reaction.message.add_reaction('1️⃣')
                await reaction.message.add_reaction('2️⃣')
                await reaction.message.add_reaction('3️⃣')
                await reaction.message.add_reaction('4️⃣')
                await reaction.message.add_reaction('5️⃣')
                await reaction.message.add_reaction('6️⃣')
                
            elif reaction.emoji == '3️⃣':
                print('reaction is 3')
                await reaction.message.edit(embed = help_embed(2))
                await reaction.message.clear_reactions()
                await reaction.message.add_reaction ('<:QuartermasterSpaghetti:804358582819880973>')
                await reaction.message.add_reaction('1️⃣')
                await reaction.message.add_reaction('2️⃣')
                await reaction.message.add_reaction('3️⃣')
                await reaction.message.add_reaction('4️⃣')
                await reaction.message.add_reaction('5️⃣')
                await reaction.message.add_reaction('6️⃣')
            elif reaction.emoji == '4️⃣':
                print('reaction is 4')
                await reaction.message.edit(embed = help_embed(3))
                await reaction.message.clear_reactions()
                await reaction.message.add_reaction('<:QuartermasterSpaghetti:804358582819880973>')
                await reaction.message.add_reaction('1️⃣')
                await reaction.message.add_reaction('2️⃣')
                await reaction.message.add_reaction('3️⃣')
                await reaction.message.add_reaction('4️⃣')
                await reaction.message.add_reaction('5️⃣')
                await reaction.message.add_reaction('6️⃣')
                
            elif reaction.emoji == '5️⃣':
                print('reaction is 5')
                await reaction.message.edit(embed = help_embed(4))
                await reaction.message.clear_reactions()
                await reaction.message.add_reaction('<:QuartermasterSpaghetti:804358582819880973>')
                await reaction.message.add_reaction('1️⃣')
                await reaction.message.add_reaction('2️⃣')
                await reaction.message.add_reaction('3️⃣')
                await reaction.message.add_reaction('4️⃣')
                await reaction.message.add_reaction('5️⃣')
                await reaction.message.add_reaction('6️⃣')
            
            elif reaction.emoji == '6️⃣':
                print('reaction is 6')
                await reaction.message.edit(embed = help_embed(5))
                await reaction.message.clear_reactions()
                await reaction.message.add_reaction('<:QuartermasterSpaghetti:804358582819880973>')
                await reaction.message.add_reaction('1️⃣')
                await reaction.message.add_reaction('2️⃣')
                await reaction.message.add_reaction('3️⃣')
                await reaction.message.add_reaction('4️⃣')
                await reaction.message.add_reaction('5️⃣')
                await reaction.message.add_reaction('6️⃣')
                
        elif x.emoji == discord.utils.get(discord.utils.get(client.guilds, name = 'Quartermaster Spaghetti\'s emotes').emojis, name = 'tictactoe'):
            msg = reaction.message
            message = msg.content
            split = message.split()
            if len(split) < 2:
                return
            new_turn = await msg.guild.fetch_member(msg.mentions[0].id)
            current_turn = await msg.guild.fetch_member(msg.mentions[1].id)
            print('tic tac toe')
            if not user.id == current_turn.id:
                print('no')
                return
            new_message = f'<@!{current_turn.id}> <@!{new_turn.id}>\n'
            if reaction.emoji == '1️⃣':
                if message.count(':regional_indicator_x:') <= message.count(':regional_indicator_o:'):
                    for x in range(9):
                        if x == 0:
                            if split[2] == ':regional_indicator_x:' or split[2] == ':regional_indicator_o:':
                                print('there was something in there already')
                                return
                            new_message += ':regional_indicator_x: ' 
                        elif x == 1:
                            new_message += split[3] + ' '
                        elif x == 2:
                            new_message += f'{split[4]}\n'
                        elif x == 3:
                            new_message += split[5] + ' '
                        elif x == 4:
                            new_message += split[6] + ' '
                        elif x == 5:
                            new_message += f'{split[7]}\n'
                        elif x == 6:
                            new_message += split[8] + ' '
                        elif x == 7:
                            new_message += split[9] + ' '
                        elif x == 8:
                            new_message += split[10] + ' '
                else:
                    for x in range(9):
                        if x == 0:
                            if split[2] == ':regional_indicator_x:' or split[2] == ':regional_indicator_o:':
                                print('there was something in there already')
                                return
                            new_message += ':regional_indicator_o: ' 
                        elif x == 1:
                            new_message += split[3] + ' '
                        elif x == 2:
                            new_message += f'{split[4]}\n'
                        elif x == 3:
                            new_message += split[5] + ' '
                        elif x == 4:
                            new_message += split[6] + ' '
                        elif x == 5:
                            new_message += f'{split[7]}\n'
                        elif x == 6:
                            new_message += split[8] + ' '
                        elif x == 7:
                            new_message += split[9] + ' '
                        elif x == 8:
                            new_message += split[10] + ' '
            elif reaction.emoji == '2️⃣':
                if message.count(':regional_indicator_x:') <= message.count(':regional_indicator_o:'):
                    for x in range(9):
                        if x == 0:
                            new_message += split[2] + ' ' 
                        elif x == 1:
                            if split[3] == ':regional_indicator_x:' or split[3] == ':regional_indicator_o:':
                                print('there was something in there already')
                                return
                            new_message += ':regional_indicator_x: '
                        elif x == 2:
                            new_message += f'{split[4]}\n'
                        elif x == 3:
                            new_message += split[5] + ' '
                        elif x == 4:
                            new_message += split[6] + ' '
                        elif x == 5:
                            new_message += f'{split[7]}\n'
                        elif x == 6:
                            new_message += split[8] + ' '
                        elif x == 7:
                            new_message += split[9] + ' '
                        elif x == 8:
                            new_message += split[10] + ' '
                else:
                    for x in range(9):
                        if x == 0:
                            new_message += split[2] + ' ' 
                        elif x == 1:
                            if split[3] == ':regional_indicator_x:' or split[3] == ':regional_indicator_o:':
                                print('there was something in there already')
                                return
                            new_message += ':regional_indicator_o: '
                        elif x == 2:
                            new_message += f'{split[4]}\n'
                        elif x == 3:
                            new_message += split[5] + ' '
                        elif x == 4:
                            new_message += split[6] + ' '
                        elif x == 5:
                            new_message += f'{split[7]}\n'
                        elif x == 6:
                            new_message += split[8] + ' '
                        elif x == 7:
                            new_message += split[9] + ' '
                        elif x == 8:
                            new_message += split[10] + ' '
            elif reaction.emoji == '3️⃣':
                if message.count(':regional_indicator_x:') <= message.count(':regional_indicator_o:'):
                    for x in range(9):
                        if x == 0:
                            new_message += split[2] + ' ' 
                        elif x == 1:
                            new_message += split[3] + ' '
                        elif x == 2:
                            if split[4] == ':regional_indicator_x:' or split[4] == ':regional_indicator_o:':
                                print('there was something in there already')
                                return
                            new_message += ':regional_indicator_x:\n'
                        elif x == 3:
                            new_message += split[5] + ' '
                        elif x == 4:
                            new_message += split[6] + ' '
                        elif x == 5:
                            new_message += f'{split[7]}\n'
                        elif x == 6:
                            new_message += split[8] + ' '
                        elif x == 7:
                            new_message += split[9] + ' '
                        elif x == 8:
                            new_message += split[10] + ' '
                else:
                    for x in range(9):
                        if x == 0:
                            new_message += split[2] + ' ' 
                        elif x == 1:
                            new_message += split[3] + ' '
                        elif x == 2:
                            if split[4] == ':regional_indicator_x:' or split[4] == ':regional_indicator_o:':
                                print('there was something in there already')
                                return
                            new_message += ':regional_indicator_o:\n'
                        elif x == 3:
                            new_message += split[5] + ' '
                        elif x == 4:
                            new_message += split[6] + ' '
                        elif x == 5:
                            new_message += f'{split[7]}\n'
                        elif x == 6:
                            new_message += split[8] + ' '
                        elif x == 7:
                            new_message += split[9] + ' '
                        elif x == 8:
                            new_message += split[10] + ' '
            elif reaction.emoji == '4️⃣':
                if message.count(':regional_indicator_x:') <= message.count(':regional_indicator_o:'):
                    for x in range(9):
                        if x == 0:
                            new_message += split[2] + ' ' 
                        elif x == 1:
                            new_message += split[3] + ' '
                        elif x == 2:
                            new_message += f'{split[4]}\n'
                        elif x == 3:
                            if split[5] == ':regional_indicator_x:' or split[5] == ':regional_indicator_o:':
                                print('there was something in there already')
                                return
                            new_message += ':regional_indicator_x: '
                        elif x == 4:
                            new_message += split[6] + ' '
                        elif x == 5:
                            new_message += f'{split[7]}\n'
                        elif x == 6:
                            new_message += split[8] + ' '
                        elif x == 7:
                            new_message += split[9] + ' '
                        elif x == 8:
                            new_message += split[10] + ' '
                else:
                    for x in range(9):
                        if x == 0:
                            new_message += split[2] + ' ' 
                        elif x == 1:
                            new_message += split[3] + ' '
                        elif x == 2:
                            new_message += f'{split[4]}\n'
                        elif x == 3:
                            if split[5] == ':regional_indicator_x:' or split[5] == ':regional_indicator_o:':
                                print('there was something in there already')
                                return
                            new_message += ':regional_indicator_o: '
                        elif x == 4:
                            new_message += split[6] + ' '
                        elif x == 5:
                            new_message += f'{split[7]}\n'
                        elif x == 6:
                            new_message += split[8] + ' '
                        elif x == 7:
                            new_message += split[9] + ' '
                        elif x == 8:
                            new_message += split[10] + ' '
            elif reaction.emoji == '5️⃣':
                if message.count(':regional_indicator_x:') <= message.count(':regional_indicator_o:'):
                    for x in range(9):
                        if x == 0:
                            new_message += split[2] + ' ' 
                        elif x == 1:
                            new_message += split[3] + ' '
                        elif x == 2:
                            new_message += f'{split[4]}\n'
                        elif x == 3:
                            new_message += split[5] + ' '
                        elif x == 4:
                            if split[6] == ':regional_indicator_x:' or split[6] == ':regional_indicator_o:':
                                print('there was something in there already')
                                return
                            new_message += ':regional_indicator_x: '
                        elif x == 5:
                            new_message += f'{split[7]}\n'
                        elif x == 6:
                            new_message += split[8] + ' '
                        elif x == 7:
                            new_message += split[9] + ' '
                        elif x == 8:
                            new_message += split[10] + ' '
                else:
                    for x in range(9):
                        if x == 0:
                            new_message += split[2] + ' ' 
                        elif x == 1:
                            new_message += split[3] + ' '
                        elif x == 2:
                            new_message += f'{split[4]}\n'
                        elif x == 3:
                            new_message += split[5] + ' '
                        elif x == 4:
                            if split[6] == ':regional_indicator_x:'  or split[6] == ':regional_indicator_o:':
                                print('there was something in there already')
                                return
                            new_message += ':regional_indicator_o: '
                        elif x == 5:
                            new_message += f'{split[7]}\n'
                        elif x == 6:
                            new_message += split[8] + ' '
                        elif x == 7:
                            new_message += split[9] + ' '
                        elif x == 8:
                            new_message += split[10] + ' '
            elif reaction.emoji == '6️⃣':
                if message.count(':regional_indicator_x:') <= message.count(':regional_indicator_o:'):
                    for x in range(9):
                        if x == 0:
                            new_message += split[2] + ' ' 
                        elif x == 1:
                            new_message += split[3] + ' '
                        elif x == 2:
                            new_message += f'{split[4]}\n'
                        elif x == 3:
                            new_message += split[5] + ' '
                        elif x == 4:
                            new_message += split[6] + ' '
                        elif x == 5:
                            if split[7] == ':regional_indicator_x:' or split[7] == ':regional_indicator_o:':
                                print('there was something in there already')
                                return
                            new_message += ':regional_indicator_x:\n'
                        elif x == 6:
                            new_message += split[8] + ' '
                        elif x == 7:
                            new_message += split[9] + ' '
                        elif x == 8:
                            new_message += split[10] + ' '
                else:
                    for x in range(9):
                        if x == 0:
                            new_message += split[2] + ' ' 
                        elif x == 1:
                            new_message += split[3] + ' '
                        elif x == 2:
                            new_message += f'{split[4]}\n'
                        elif x == 3:
                            new_message += split[5] + ' '
                        elif x == 4:
                            new_message += split[6] + ' '
                        elif x == 5:
                            if split[7] == ':regional_indicator_x:' or split[7] == ':regional_indicator_o:':
                                print('there was something in there already')
                                return
                            new_message += ':regional_indicator_o:\n'
                        elif x == 6:
                            new_message += split[8] + ' '
                        elif x == 7:
                            new_message += split[9] + ' '
                        elif x == 8:
                            new_message += split[10] + ' '
            elif reaction.emoji == '7️⃣':
                if message.count(':regional_indicator_x:') <= message.count(':regional_indicator_o:'):
                    for x in range(9):
                        if x == 0:
                            new_message += split[2] + ' ' 
                        elif x == 1:
                            new_message += split[3] + ' '
                        elif x == 2:
                            new_message += f'{split[4]}\n'
                        elif x == 3:
                            new_message += split[5] + ' '
                        elif x == 4:
                            new_message += split[6] + ' '
                        elif x == 5:
                            new_message += f'{split[7]}\n'
                        elif x == 6:
                            if split[8] == ':regional_indicator_x:' or split[8] == ':regional_indicator_o:':
                                print('there was something in there already')
                                return
                            new_message += ':regional_indicator_x: '
                        elif x == 7:
                            new_message += split[9] + ' '
                        elif x == 8:
                            new_message += split[10] + ' '
                else:
                    for x in range(9):
                        if x == 0:
                            new_message += split[2] + ' ' 
                        elif x == 1:
                            new_message += split[3] + ' '
                        elif x == 2:
                            new_message += f'{split[4]}\n'
                        elif x == 3:
                            new_message += split[5] + ' '
                        elif x == 4:
                            new_message += split[6] + ' '
                        elif x == 5:
                            new_message += f'{split[7]}\n'
                        elif x == 6:
                            if split[8] == ':regional_indicator_x:' or split[8] == ':regional_indicator_o:':
                                print('there was something in there already')
                                return
                            new_message += ':regional_indicator_o: '
                        elif x == 7:
                            new_message += split[9] + ' '
                        elif x == 8:
                            new_message += split[10] + ' '
            elif reaction.emoji == '8️⃣':
                if message.count(':regional_indicator_x:') <= message.count(':regional_indicator_o:'):
                    for x in range(9):
                        if x == 0:
                            new_message += split[2] + ' ' 
                        elif x == 1:
                            new_message += split[3] + ' '
                        elif x == 2:
                            new_message += f'{split[4]}\n'
                        elif x == 3:
                            new_message += split[5] + ' '
                        elif x == 4:
                            new_message += split[6] + ' '
                        elif x == 5:
                            new_message += f'{split[7]}\n'
                        elif x == 6:
                            new_message += split[8] + ' '
                        elif x == 7:
                            if split[9] == ':regional_indicator_x:' or split[9] == ':regional_indicator_o:':
                                print('there was something in there already')
                                return
                            new_message += ':regional_indicator_x: '
                        elif x == 8:
                            new_message += split[10] + ' '
                else:
                    for x in range(9):
                        if x == 0:
                            new_message += split[2] + ' ' 
                        elif x == 1:
                            new_message += split[3] + ' '
                        elif x == 2:
                            new_message += f'{split[4]}\n'
                        elif x == 3:
                            new_message += split[5] + ' '
                        elif x == 4:
                            new_message += split[6] + ' '
                        elif x == 5:
                            new_message += f'{split[7]}\n'
                        elif x == 6:
                            new_message += split[8] + ' '
                        elif x == 7:
                            if split[9] == ':regional_indicator_x:' or split[9] == ':regional_indicator_o:':
                                print('there was something in there already')
                                return
                            new_message += ':regional_indicator_o: '
                        elif x == 8:
                            new_message += split[10] + ' '
            elif reaction.emoji == '9️⃣':
                if message.count(':regional_indicator_x:') <= message.count(':regional_indicator_o:'):
                    for x in range(9):
                        if x == 0:
                            new_message += split[2] + ' ' 
                        elif x == 1:
                            new_message += split[3] + ' '
                        elif x == 2:
                            new_message += f'{split[4]}\n'
                        elif x == 3:
                            new_message += split[5] + ' '
                        elif x == 4:
                            new_message += split[6] + ' '
                        elif x == 5:
                            new_message += f'{split[7]}\n'
                        elif x == 6:
                            new_message += split[8] + ' '
                        elif x == 7:
                            new_message += split[9] + ' '
                        elif x == 8:
                            if split[10] == ':regional_indicator_x:' or split[10] == ':regional_indicator_o:':
                                print('there was something in there already')
                                return
                            new_message += ':regional_indicator_x: '
                else:
                    for x in range(9):
                        if x == 0:
                            new_message += split[2] + ' ' 
                        elif x == 1:
                            new_message += split[3] + ' '
                        elif x == 2:
                            new_message += f'{split[4]}\n'
                        elif x == 3:
                            new_message += split[5] + ' '
                        elif x == 4:
                            new_message += split[6] + ' '
                        elif x == 5:
                            new_message += f'{split[7]}\n'
                        elif x == 6:
                            new_message += split[8] + ' '
                        elif x == 7:
                            new_message += split[9] + ' '
                        elif x == 8:
                            if split[10] == ':regional_indicator_x:' or split[10] == ':regional_indicator_o:':
                                print('there was something in there already')
                                return
                            new_message += ':regional_indicator_o: '
            else:
                return
            await msg.edit(content = new_message)
            split = new_message.split()
            if split[2] == ':regional_indicator_x:' and split[3] == ':regional_indicator_x:' and split[4] == ':regional_indicator_x:':
                await asyncio.sleep(1)
                await msg.edit(content = f'{current_turn.mention} won!')
                asyncio.sleep(2)
                ttt_file = open('ttt.txt', 'r')
                ttt_text = ttt_file.read()
                ttt_file.close()
                new_text = ''
                for x in ttt_text.splitlines():
                    if not str(current_turn.id) in x:
                        new_text += f'{x}\n'
                ttt_file = open('ttt.txt', 'w')
                ttt_file.write(new_text)
                ttt_file.close()
                return
            elif split[5] == ':regional_indicator_x:' and split[6] == ':regional_indicator_x:' and split[7] == ':regional_indicator_x:':
                await asyncio.sleep(1)
                await msg.edit(content = f'{current_turn.mention} won!')
                asyncio.sleep(2)
                ttt_file = open('ttt.txt', 'r')
                ttt_text = ttt_file.read()
                ttt_file.close()
                new_text = ''
                for x in ttt_text.splitlines():
                    if not str(current_turn.id) in x:
                        new_text += f'{x}\n'
                ttt_file = open('ttt.txt', 'w')
                ttt_file.write(new_text)
                ttt_file.close()
                return
            elif split[8] == ':regional_indicator_x:' and split[9] == ':regional_indicator_x:' and split[10] == ':regional_indicator_x:':
                await asyncio.sleep(1)
                await msg.edit(content = f'{current_turn.mention} won!')
                asyncio.sleep(2)
                ttt_file = open('ttt.txt', 'r')
                ttt_text = ttt_file.read()
                ttt_file.close()
                new_text = ''
                for x in ttt_text.splitlines():
                    if not str(current_turn.id) in x:
                        new_text += f'{x}\n'
                ttt_file = open('ttt.txt', 'w')
                ttt_file.write(new_text)
                ttt_file.close()
                return
            if split[2] == ':regional_indicator_x:' and split[5] == ':regional_indicator_x:' and split[8] == ':regional_indicator_x:':
                await asyncio.sleep(1)
                await msg.edit(content = f'{current_turn.mention} won!')
                asyncio.sleep(2)
                ttt_file = open('ttt.txt', 'r')
                ttt_text = ttt_file.read()
                ttt_file.close()
                new_text = ''
                for x in ttt_text.splitlines():
                    if not str(current_turn.id) in x:
                        new_text += f'{x}\n'
                ttt_file = open('ttt.txt', 'w')
                ttt_file.write(new_text)
                ttt_file.close()
                return
            elif split[3] == ':regional_indicator_x:' and split[6] == ':regional_indicator_x:' and split[9] == ':regional_indicator_x:':
                await asyncio.sleep(1)
                await msg.edit(content = f'{current_turn.mention} won!')
                asyncio.sleep(2)
                ttt_file = open('ttt.txt', 'r')
                ttt_text = ttt_file.read()
                ttt_file.close()
                new_text = ''
                for x in ttt_text.splitlines():
                    if not str(current_turn.id) in x:
                        new_text += f'{x}\n'
                ttt_file = open('ttt.txt', 'w')
                ttt_file.write(new_text)
                ttt_file.close()
                return
            elif split[4] == ':regional_indicator_x:' and split[7] == ':regional_indicator_x:' and split[10] == ':regional_indicator_x:':
                await asyncio.sleep(1)
                await msg.edit(content = f'{current_turn.mention} won!')
                asyncio.sleep(2)
                ttt_file = open('ttt.txt', 'r')
                ttt_text = ttt_file.read()
                ttt_file.close()
                new_text = ''
                for x in ttt_text.splitlines():
                    if not str(current_turn.id) in x:
                        new_text += f'{x}\n'
                ttt_file = open('ttt.txt', 'w')
                ttt_file.write(new_text)
                ttt_file.close()
                return
            if split[2] == ':regional_indicator_o:' and split[3] == ':regional_indicator_o:' and split[4] == ':regional_indicator_o:':
                await asyncio.sleep(1)
                await msg.edit(content = f'{current_turn.mention} won!')
                asyncio.sleep(2)
                ttt_file = open('ttt.txt', 'r')
                ttt_text = ttt_file.read()
                ttt_file.close()
                new_text = ''
                for x in ttt_text.splitlines():
                    if not str(current_turn.id) in x:
                        new_text += f'{x}\n'
                ttt_file = open('ttt.txt', 'w')
                ttt_file.write(new_text)
                ttt_file.close()
                return
            elif split[5] == ':regional_indicator_o:' and split[6] == ':regional_indicator_o:' and split[7] == ':regional_indicator_o:':
                await asyncio.sleep(1)
                await msg.edit(content = f'{current_turn.mention} won!')
                asyncio.sleep(2)
                ttt_file = open('ttt.txt', 'r')
                ttt_text = ttt_file.read()
                ttt_file.close()
                new_text = ''
                for x in ttt_text.splitlines():
                    if not str(current_turn.id) in x:
                        new_text += f'{x}\n'
                ttt_file = open('ttt.txt', 'w')
                ttt_file.write(new_text)
                ttt_file.close()
                return
            elif split[8] == ':regional_indicator_o:' and split[9] == ':regional_indicator_o:' and split[10] == ':regional_indicator_o:':
                await asyncio.sleep(1)
                await msg.edit(content = f'{current_turn.mention} won!')
                asyncio.sleep(2)
                ttt_file = open('ttt.txt', 'r')
                ttt_text = ttt_file.read()
                ttt_file.close()
                new_text = ''
                for x in ttt_text.splitlines():
                    if not str(current_turn.id) in x:
                        new_text += f'{x}\n'
                ttt_file = open('ttt.txt', 'w')
                ttt_file.write(new_text)
                ttt_file.close()
                return
            if split[2] == ':regional_indicator_o:' and split[5] == ':regional_indicator_o:' and split[8] == ':regional_indicator_o:':
                await asyncio.sleep(1)
                await msg.edit(content = f'{current_turn.mention} won!')
                asyncio.sleep(2)
                ttt_file = open('ttt.txt', 'r')
                ttt_text = ttt_file.read()
                ttt_file.close()
                new_text = ''
                for x in ttt_text.splitlines():
                    if not str(current_turn.id) in x:
                        new_text += f'{x}\n'
                ttt_file = open('ttt.txt', 'w')
                ttt_file.write(new_text)
                ttt_file.close()
                return
            elif split[3] == ':regional_indicator_o:' and split[6] == ':regional_indicator_o:' and split[9] == ':regional_indicator_o:':
                await asyncio.sleep(1)
                await msg.edit(content = f'{current_turn.mention} won!')
                asyncio.sleep(2)
                ttt_file = open('ttt.txt', 'r')
                ttt_text = ttt_file.read()
                ttt_file.close()
                new_text = ''
                for x in ttt_text.splitlines():
                    if not str(current_turn.id) in x:
                        new_text += f'{x}\n'
                ttt_file = open('ttt.txt', 'w')
                ttt_file.write(new_text)
                ttt_file.close()
                return
            elif split[4] == ':regional_indicator_o:' and split[7] == ':regional_indicator_o:' and split[10] == ':regional_indicator_o:':
                await asyncio.sleep(1)
                await msg.edit(content = f'{current_turn.mention} won!')
                asyncio.sleep(2)
                ttt_file = open('ttt.txt', 'r')
                ttt_text = ttt_file.read()
                ttt_file.close()
                new_text = ''
                for x in ttt_text.splitlines():
                    if not str(current_turn.id) in x:
                        new_text += f'{x}\n'
                ttt_file = open('ttt.txt', 'w')
                ttt_file.write(new_text)
                ttt_file.close()
                return
            elif split[2] == ':regional_indicator_x:' and split[6] == ':regional_indicator_x:' and split[10] == ':regional_indicator_x:':
                await asyncio.sleep(1)
                await msg.edit(content = f'{current_turn.mention} won!')
                asyncio.sleep(2)
                ttt_file = open('ttt.txt', 'r')
                ttt_text = ttt_file.read()
                ttt_file.close()
                new_text = ''
                for x in ttt_text.splitlines():
                    if not str(current_turn.id) in x:
                        new_text += f'{x}\n'
                ttt_file = open('ttt.txt', 'w')
                ttt_file.write(new_text)
                ttt_file.close()
                return
            elif split[4] == ':regional_indicator_x:' and split[6] == ':regional_indicator_x:' and split[8] == ':regional_indicator_x:':
                await asyncio.sleep(1)
                await msg.edit(content = f'{current_turn.mention} won!')
                asyncio.sleep(2)
                ttt_file = open('ttt.txt', 'r')
                ttt_text = ttt_file.read()
                ttt_file.close()
                new_text = ''
                for x in ttt_text.splitlines():
                    if not str(current_turn.id) in x:
                        new_text += f'{x}\n'
                ttt_file = open('ttt.txt', 'w')
                ttt_file.write(new_text)
                ttt_file.close()
                return
            elif split[2] == ':regional_indicator_o:' and split[6] == ':regional_indicator_o:' and split[10] == ':regional_indicator_o:':
                await asyncio.sleep(1)
                await msg.edit(content = f'{current_turn.mention} won!')
                asyncio.sleep(2)
                ttt_file = open('ttt.txt', 'r')
                ttt_text = ttt_file.read()
                ttt_file.close()
                new_text = ''
                for x in ttt_text.splitlines():
                    if not str(current_turn.id) in x:
                        new_text += f'{x}\n'
                ttt_file = open('ttt.txt', 'w')
                ttt_file.write(new_text)
                ttt_file.close()
                return
            elif split[4] == ':regional_indicator_o:' and split[6] == ':regional_indicator_o:' and split[8] == ':regional_indicator_o:':
                await asyncio.sleep(1)
                await msg.edit(content = f'{current_turn.mention} won!')
                asyncio.sleep(2)
                ttt_file = open('ttt.txt', 'r')
                ttt_text = ttt_file.read()
                ttt_file.close()
                new_text = ''
                for x in ttt_text.splitlines():
                    if not str(current_turn.id) in x:
                        new_text += f'{x}\n'
                ttt_file = open('ttt.txt', 'w')
                ttt_file.write(new_text)
                ttt_file.close()
                return
            
            for x in split:
                if x in ttt_board:
                    return
            
            await msg.edit(content = 'Draw!')
            ttt_file = open('ttt.txt', 'r')
            ttt_text = ttt_file.read()
            ttt_file.close()
            new_text = ''
            for x in ttt_text.splitlines():
                if not str(current_turn.id) in x:
                    new_text += f'{x}\n'
            ttt_file = open('ttt.txt', 'w')
            ttt_file.write(new_text)
            ttt_file.close()

@client.event
async def on_member_leave(member):
    database_functions.clear_xp(member.guild.id, member.id)

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
    await client.process_commands(msg)
    if isinstance(msg, discord.DMChannel):
        return
    message = msg.content
    if msg.channel.name == 'bot-setup':
        words = message.split()
        if len(words) > 0:
            if words[0] == f'{prefix}setup':
                await msg.channel.send(embed = setup_embed())
            elif message.startswith(f'{prefix}resetsettings'):
                print('reseting settings')
                database_functions.clear_setup(msg.guild.id)
                id = str(msg.guild.id)
                if not id in client.setup_guilds:
                    client.setup_guilds.append(id)
                setup_guilds.close()
                await msg.channel.send('Cleared settings. Please enter the new settings.')
                return
            elif words[0] == f'{prefix}setadmin':
                if not len(msg.role_mentions) > 0:
                    await msg.channel.send('Invalid role.')
                    return
                role = msg.role_mentions[0]
                database_functions.set_admin(msg.guild.id, ascii(role.name)[1:-1] if not ascii(role.name)[1:-1] == role.name else role.name)
                await msg.channel.send(f'Set the admin role to {role.mention}')
                return
            elif words[0] == f'{prefix}setmuted':
                if len(database_functions.get_setup(msg.guild.id).splitlines()) == 0:
                    await msg.channel.send(f'You need to set an admin role using `{prefix}setadmin`!')
                    return
                if not len(msg.role_mentions) > 0:
                    await msg.channel.send('Invalid role.')
                    return
                role = msg.role_mentions[0]
                database_functions.set_muted(msg.guild.id, ascii(role.name)[1:-1] if not ascii(role.name)[1:-1] == role.name else role.name)
                await msg.channel.send(f'Set the muted role to {role.mention}')
                return
            elif words[0] == f'{prefix}setlogs':
                if len(database_functions.get_setup(msg.guild.id).splitlines()) == 1:
                    await msg.channel.send(f'You need to set a muted role using `{prefix}setmuted`!')  
                    return
                elif len(database_functions.get_setup(msg.guild.id).splitlines()) == 0:
                    await msg.channel.send(f'You need to set the lowest admin role using `{prefix}setadmin`, then set a muted role using `{prefix}setmuted`!')
                    return
                channel = msg.channel_mentions[0]
                if channel == None:
                    await msg.channel.send('Invalid channel.')
                    return
                database_functions.set_logs(msg.guild.id, ascii(channel.name)[1:-1] if not ascii(channel.name)[1:-1] == channel.name else channel.name)
                try:
                    client.setup_guilds.remove(str(msg.guild.id))
                except:
                    pass
                await msg.channel.send(f'Set the logs channel to {channel.mention}')
                return
            elif words[0] == f'{prefix}setlevel':
                if len(database_functions.get_setup(msg.guild.id).splitlines()) == 2:
                    await msg.channel.send(f'You need to set the logs channel name using `{prefix}setlogs`!')    
                    return
                elif len(database_functions.get_setup(msg.guild.id).splitlines()) == 1:
                    await msg.channel.send(f'You need to set a muted role using `{prefix}setmuted`, then set the logs channel name using `{prefix}setlogs`!')
                    return
                elif len(database_functions.get_setup(msg.guild.id).splitlines()) == 0:
                    await msg.channel.send(f'You need to set the lowest admin role using `{prefix}setadmin`, then set a muted role using `{prefix}setmuted`, then set the logs channel name using `{prefix}setlogs`!')
                    return
                if len(words) < 4:
                    await msg.channel.send(f'Please follow the correct format: `{prefix}setlevel <level_num> <xp_to_get> <role_name>`')
                    return
                level_num = words[1]
                xp = words[2]
                if not len(msg.role_mentions) > 0:
                    await msg.channel.send('Invalid role.')
                    return
                role = msg.role_mentions[0]
                if not intTryParse(level_num) or not intTryParse(xp):
                    await msg.channel.send(f'Please follow the correct format: `{prefix}setlevel <level_num> <xp_to_get> <role_name>')
                    return
                database_functions.set_level(msg.guild.id, int(level_num), ascii(f'{xp} {role.name}')[1:-1] if ascii(f'{xp} {role.name}')[1:-1] == f'{xp} {role.name}' else f'{xp} {role.name}')
                await msg.channel.send(f'Set level {level_num} to {role.mention}')
                return
        return

    levels = database_functions.get_levels(msg.guild.id)
    print(levels)
    if not levels == 'None':
        print(database_functions.get_xp(msg.guild.id, msg.author.id))
        levels.reverse()
        print(levels)
        author = await msg.guild.fetch_member(msg.author.id)
        print(author is None)
        for x in levels:
            xp_required = x.split()[0]
            level_name = x[len(xp_required)+1:]
            print(xp_required)
            print(level_name)
            role = discord.utils.get(msg.guild.roles, name = level_name)
            print(role is None)
            if role == None:
                continue
            elif int(database_functions.get_xp(msg.guild.id, msg.author.id)) >= int(xp_required):
                print(f'{x} is the highest level that {msg.author.name} can get')
                await msg.author.add_roles(discord.utils.get(msg.guild.roles, name = level_name))
            else:
                print('too high')
                try:
                    await msg.author.remove_roles(role)
                except discord.NotFound:
                    continue

    category = msg.channel.category
    if not category == None:
        if category.name == 'Mail':
            user_to_dm = client.get_user(int(msg.channel.name))
            try:
                dm = user_to_dm.dm_channel
                if dm is None:
                    dm = await user_to_dm.create_dm()
                await dm.send(f'`{msg.author}` **says:** {message}')
            except:
                print(f'cant dm {member.name}')
    
#    print(msg.author.id)
#    xp_file = open(f'xp {msg.guild.id}.txt', 'a')
#    xp_file.close()
#    xp_file = open(f'xp {msg.guild.id}.txt', 'r')
#    read = xp_file.read()
#    xp_file.close()
#    if not str(msg.author.id) in read.splitlines():
#        print(database_functions.get_xp(msg.guild.id, msg.author.id))
#        database_functions.add_xp(msg.guild.id, msg.author.id, 1)
#        print(database_functions.get_xp(msg.guild.id, msg.author.id))
#        print(f'given {msg.author.name} 1 XP')
#        read += f'{msg.author.id}\n'
#        xp_file = open(f'xp {msg.guild.id}.txt', 'w')
#        xp_file.write(read)
#        xp_file.close()
#        await asyncio.sleep(5)
#        lines = read.splitlines()
#        new_read = ''
#        for x in lines:
#            if not x == str(msg.author.id):
#                new_read += f'{x}\n'
#        xp_file = open(f'xp {msg.guild.id}.txt', 'w')
#        xp_file.write(new_read)
#        xp_file.close()
#    else:
#        print(f'{msg.author} cannot get xp now')
    member_id = msg.author.id
    guild_id = msg.guild.id
    try:
        xp = client.xp[f'{guild_id}']
    except:
        client.xp[f'{guild_id}'] = []
    if not member_id in client.xp[f'{guild_id}']:
        client.xp[f'{guild_id}'].append(member_id)
        database_functions.add_xp(msg.guild.id, msg.author.id, 1)
        await asyncio.sleep(5)
        client.xp[f'{guild_id}'].remove(member_id)
        print(f'added xp to {member_id} in {guild_id}')
    else:
        print(f'{member_id} cannot get xp now')
    if message.startswith(f'{prefix}setup') and not msg.channel.name == 'bot-setup':
        await msg.channel.send('Please create a channel called `#bot-setup` and run this command there.')
        return
    
    if msg.channel.name == 'discord-phone':
        if message.startswith(prefix):
            await msg.channel.send('Please don\'t use commands here.', delete_after = 3)
            await msg.delete()
            return
        for x in client.guilds:
            for y in x.channels:
                if y.name == 'discord-phone' and not y is msg.channel:
                    await y.send(f'`{msg.author}` **says:** {message}')

@client.event
async def on_raw_reaction_add(payload):
    print('raw reaction add')
    reaction_roles = database_functions.get_reaction_roles(payload.guild_id)
    if reaction_roles == '':
        print('nothing')
        return
    print(payload.message_id)
    for x in reaction_roles.splitlines():
        if str(payload.message_id) in x.split():
            channel_id = payload.channel_id
            rr = reaction_roles
            split = rr.split()
            print(str(payload.emoji))
            if ascii(str(payload.emoji)) in split or f'<a{ascii(str(payload.emoji))[1:]}' in split:
                index = split.index(ascii(str(payload.emoji)))
                role_id = split[index - 1]
                channel = await client.fetch_channel(channel_id)
                member = await channel.guild.fetch_member(payload.user_id)
                role = channel.guild.get_role(int(role_id))
                print(f'giving role {role.name}')
                await member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
    reaction_roles = database_functions.get_reaction_roles(payload.guild_id)
    if reaction_roles == '':
        print('nothing')
        return
    for x in reaction_roles.splitlines():
        if str(payload.message_id) in x.split():
            channel_id = payload.channel_id
            rr = reaction_roles
            split = rr.split()
            print(str(payload.emoji))
            if ascii(str(payload.emoji)) in split or f'<a{ascii(str(payload.emoji))[1:]}' in split:
                index = split.index(ascii(str(payload.emoji)))
                role_id = split[index - 1]
                channel = await client.fetch_channel(channel_id)
                member = await channel.guild.fetch_member(payload.user_id)
                role = channel.guild.get_role(int(role_id))
                print(f'removing role {role.name}')
                await member.remove_roles(role)

# Global Commands
@client.command(aliases = ['help'])
async def about(ctx):
    bot_msg = await ctx.send(embed=help_embed(0))
    await bot_msg.add_reaction('<:QuartermasterSpaghetti:804358582819880973>')
    await bot_msg.add_reaction('1️⃣')
    await bot_msg.add_reaction('2️⃣')
    await bot_msg.add_reaction('3️⃣')
    await bot_msg.add_reaction('4️⃣')
    await bot_msg.add_reaction('5️⃣')
    await bot_msg.add_reaction('6️⃣')
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')
    
@client.command()
async def ping(ctx):
    pongs = ['Pong!', '*misses*']
    await ctx.send(f'{random.choice(pongs)} Ping to Dicord\'s API is `{round(client.latency * 1000)}ms`.')
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')
    
@client.command()
async def pong(ctx):
    pongs = ['Ping!', '*misses*']
    await ctx.send(f'{random.choice(pongs)} Pong to Dicord\'s API is `{round(client.latency * 1000)}ms`.')
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command()
@commands.check(is_text_channel)
async def avatar(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    await ctx.send(member.avatar_url)
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command(aliases = ['ui'])
@commands.check(is_text_channel)
async def userinfo(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    print(member == None)
    await ctx.send(embed = userinfo_embed(member))
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command(aliases = ['lvl'])
@commands.check(is_text_channel)
async def level(ctx):
    await ctx.send(embed = level_embed(ctx.message, ctx.author))
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command(aliases = ['si'])
@commands.check(is_text_channel)
async def serverinfo(ctx):
    await ctx.send(embed = serverinfo_embed(ctx.guild))
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command(aliases = ['warns', 'warnings', 'showwarnings'])
@commands.check(is_text_channel)
async def showwarns(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    warns = database_functions.get_warnings(ctx.guild.id, member.id)
    if warns == '':
        warns = 'No warnings found :D'
    await ctx.send(embed = show_warns_embed(member, warns, ctx.author))
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command()
@commands.check(is_text_channel)
async def leaderboard(ctx):
    warning_msg = await ctx.send('Constructing leaderboard...')
    unsorted_leaderboard = []
    print('getting members and xp')
    for x in ctx.guild.members:
        if not x.bot:
            xp_num = database_functions.get_xp(ctx.guild.id, x.id)
            dictionary = {'rank': f'{x.mention}: {xp_num} XP', 'xp': xp_num}
            print(dictionary['rank'])
            print(dictionary['xp'])
            unsorted_leaderboard.append(dictionary)

    print('sorting leaderboard')
    await warning_msg.edit(content = 'Sorting leaderboard...')
    unsorted_leaderboard.sort(key = lambda i: i['xp'], reverse = True)
    leaderboard = ''
    print('generating leaderboard')
    await warning_msg.edit(content = 'Almost done...')
    for x in range(15):
        leaderboard += unsorted_leaderboard[x]['rank'] + '\n'
    print('sending leaderboard')
    await warning_msg.delete()
    await ctx.send(embed = leaderboard_embed(leaderboard, ctx))
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command()
async def updates(ctx):
    await ctx.send(embed = client.update_embed)

# Game Commands
@client.command(aliases = ['ttt'])
@commands.check(is_text_channel)
async def tictactoe(ctx, member: discord.Member):
    if member.id == ctx.author.id:
        await ctx.send('You can\'t challenge yourself, dumbass.')
        return  
    elif member.bot:
        await ctx.send('You can\'t challenge a bot.')
        return
    ttt_file = open('ttt.txt', 'r')
    read = ttt_file.read()
    ttt_file.close()
    ttt_file = open('ttt.txt', 'a')
    if str(ctx.author.id) in read:
        await ctx.send('You\'re either already challenging or are already challenged! Please decline that challenge to be able to challenge someone!')
        return
    elif str(member.id) in read:
        await ctx.send('That user is either already challenging or is already challenged! Please wait until they decline that challenge so you can challenge them!')
        return
            
    ttt_msg = await ctx.send(embed = ttt_accept_embed(ctx.author, member))
    ttt_file.write(f'{ctx.author.id} {member.id} pending\n')
    ttt_file.close()
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command(aliases = ['acceptttt'])
@commands.check(is_text_channel)
async def accepttictactoe(ctx):
    ttt_file = open('ttt.txt', 'r')
    read = ttt_file.read()
    ttt_file.close()
    new_read = ''
    challenger = None
    challenged = ctx.author
    is_in_read = False
    for x in read.splitlines():
        if str(ctx.author.id) in x:
            words = x.split()
            challenger = await ctx.guild.fetch_member(int(words[0]))
            new_read += f'{x[:-8]} accepted'
            is_in_read = True
        else:
            new_read += f'{x}\n'
    if not is_in_read:
        await ctx.send('There\'s nothing to accept, wait until someone challenges you.')
        return
    ttt_file = open('ttt.txt', 'w')
    ttt_file.write(new_read)
    bot_msg = await ctx.send(f'{challenged.mention} {challenger.mention}\n:one: :two: :three:\n:four: :five: :six:\n:seven: :eight: :nine:️') 
    await bot_msg.add_reaction('<:tictactoe:806837315288563743>')
    await bot_msg.add_reaction('1️⃣')
    await bot_msg.add_reaction('2️⃣')
    await bot_msg.add_reaction('3️⃣')
    await bot_msg.add_reaction('4️⃣')
    await bot_msg.add_reaction('5️⃣')
    await bot_msg.add_reaction('6️⃣')
    await bot_msg.add_reaction('7️⃣')
    await bot_msg.add_reaction('8️⃣')
    await bot_msg.add_reaction('9️⃣')
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command(aliases = ['cancelttt'])
@commands.check(is_text_channel)
async def canceltictactoe(ctx):
    ttt_file = open('ttt.txt', 'r')
    read = ttt_file.read()
    ttt_file.close()
    new_read = ''
    is_in_ttt = False
    for x in read.splitlines():
        if not str(ctx.author.id) in x.split():
            new_read += f'{x}\n'
        else:
            is_in_ttt = True
    if is_in_ttt:
        ttt_file = open('ttt.txt', 'w')
        ttt_file.write(new_read)
        await ctx.send('Successfully cancelled the challenge.')
    else:
        await ctx.send('There\'s nothing to decline, you can only do that if you were challenged or were challenging someone.')
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command(aliases = ['bs'])
async def battleship(ctx):
    bs_file = open('bs.txt', 'r')
    read = bs_file.read()
    bs_file.close()
    if str(ctx.author.id) in read:
        splitlines = read.splitlines()
        idx = splitlines.index(str(ctx.author.id))
        del splitlines[idx:idx + 6]
        new_read = ''
        for z in splitlines:
            new_read += f'{z}\n'
        bs_file = open('bs.txt', 'w')
        bs_file.write(new_read)
        bs_file.close()

    bs_file = open('bs.txt', 'a')
    bs_file.write(f'{ctx.author.id}\n0\n')
    board = [':blue_square: ', ':one: ', ':two: ', ':three: ', ':four: ', ':five: ', ':six:\n', ':one: ', ':ocean: ', ':ocean: ', ':ocean: ', ':ocean: ', ':ocean: ', ':ocean:\n', ':two: ', ':ocean: ', ':ocean: ', ':ocean: ', ':ocean: ', ':ocean: ', ':ocean:\n', ':three: ', ':ocean: ', ':ocean: ', ':ocean: ', ':ocean: ', ':ocean: ', ':ocean:\n', ':four: ', ':ocean: ', ':ocean: ', ':ocean: ', ':ocean: ', ':ocean: ', ':ocean:\n', ':five: ', ':ocean: ', ':ocean: ', ':ocean: ', ':ocean: ', ':ocean: ', ':ocean:\n', ':six: ', ':ocean: ', ':ocean: ', ':ocean: ', ':ocean: ', ':ocean: ', ':ocean:']
    board_print = ''
    for x in board:
        board_print += x
    for x in range(4):
        while True:
            generated_num = random.randint(0, 35)
            print(generated_num)
            if board[generated_num] == ':ocean: ':
                bs_file.write(f'{generated_num}\n')
                if '\n' in board[generated_num]:
                    board[generated_num] = ':ship:\n'
                    break
                board[generated_num] = ':ship: '
                break
            else:
                continue
    bot_msg = await ctx.send(f'(Turn 1/20) {ctx.author.mention}, the game has started! Call `{prefix}shoot <x> <y>` to shoot at that (X, Y) position!\n{board_print}')
    await bot_msg.add_reaction('<:battleship:819588373131427852>')
    bs_file.close()
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command()
async def shoot(ctx, x: int, y: int):
    words = ctx.message.content.split()
    if len(words) < 3:
        await ctx.send(f'Please specify an X and Y coordinate as so: `{prefix}shoot <x> <y>`')
        return
    x_str = words[1]
    y_str = words[2]
    if not x_str.isdigit() or not y_str.isdigit():
        await msg.channel.send('Please specify numbers, not special characters or letters.')
        return
    x = int(x_str)
    y = int(y_str)
    if (x > 6 or x < 1) or (y > 6 or y < 1):
        await msg.channel.send('That\'s out of the board! Please enter a number between 1 and 6 for X and Y.')
        return
    channel = ctx.channel
    user = ctx.author
    await ctx.message.delete()
    bs_msg = None
    for msg in await channel.history(limit=100).flatten():
        if msg.author == client.user and len(msg.reactions) > 0 and msg.mentions[0] == ctx.author:
            if str(msg.reactions[0].emoji) == '<:battleship:819588373131427852>':
                bs_msg = msg
                break
    if bs_msg == None:
        await channel.send('Please start a game before you play!')
        return
    print('is there a message?', bs_msg == None)
    if user.mention == bs_msg.mentions[0]:
        await channel.send(f'There\'s nothing to shoot at! Start a game with `{prefix}batlleship` or `{prefix}bs`.')
        return
    words = bs_msg.content.split()
    for z in words:
        if not words[0] == ':blue_square:':
            del words[0]
        else:
            break
    hit = 7 * y + x
    print('we shot at', hit)
    print('printing words...')
    for z in words:
        print(z)
    bs_file = open('bs.txt', 'r')
    read = bs_file.read()
    splitlines = read.splitlines()
    try:
        idx = splitlines.index(str(user.id))
    except:
        return
    turn = int(splitlines[idx + 1])
    print(f'turn {turn}')
    turn += 1
    print(f'turn {turn}')
    splitlines[idx + 1] = str(turn)
    print('the index of the user\'s id is', idx)
    bs_file.close()
    is_hit = False
    for z in range(idx + 2, idx + 6):
        if str(hit) == splitlines[z]:
            is_hit = True
    print('did we hit something? ', is_hit)
    new_board = ''
    new_board = ''
    for z in range(len(words)):
        print('we have from the words list: ', words[z])
        print('its index is', z)
        if (z + 1) % 7 == 0:
            if z == hit:
                if is_hit:
                    print('we hit at the edge of the ocean')
                    new_board += ':boom:\n'
                else:
                    print('we missed a shot at the end of the ocean')
                    new_board += ':x:\n'
            else:
                new_board += f'{words[z]}\n'
        elif z == hit:
            if is_hit:
                print('we hit at the ocean')
                new_board += ':boom: '
            else:
                print('we missed a shot at the ocean')
                new_board += ':x: '
        else:
            new_board += f'{words[z]} '
        print('here\'s the new board:')
        print(new_board)
    await bs_msg.edit(content = f'(Turn {turn + 1}/20) {user.mention}, you {"hit a ship" if is_hit else "missed a shot"} at ({x}, {y})! Keep going!\n{new_board}')
    if new_board.count(':boom:') == 4:
        await asyncio.sleep(1)
        await bs_msg.edit(content = f'{user.mention}, you won! :D')
        del splitlines[idx:idx + 6]
        await bs_msg.clear_reactions()
        await asyncio.sleep(5)
        await bs_msg.delete()
        await database_functions.add_xp(ctx.guild.id, ctx.author.id, 5)
    elif turn >= 19:
        locations = [int(splitlines[idx + 2]), int(splitlines[idx + 3]), int(splitlines[idx + 4]), int(splitlines[idx + 5])]
        new_new_board = ''
        new_split = new_board.split()
        for z in range(len(new_split)):
            if z in locations and not z == ':ocean:':
                if (z + 1) % 7 == 0:
                    new_new_board += ':ship:\n'
                else:
                    new_new_board += ':ship: '
            else:
                if (z + 1) % 7 == 0:
                    new_new_board += f'{new_split[z]}\n'
                else:
                    new_new_board += f'{new_split[z]} '
        await asyncio.sleep(1)
        await bs_msg.edit(content = f'{user.mention}, you lost! :( Here are the locations of the ships you didn\'t shoot:\n{new_new_board}')
        del splitlines[idx:idx + 6]
        await bs_msg.clear_reactions()
    new_read = ''
    for z in splitlines:
        new_read += f'{z}\n'
    bs_file = open('bs.txt', 'w')
    bs_file.write(new_read)
    bs_file.close()
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

class Board:
    def __init__(self, dim_size, num_bombs, id):
        self.dim_size = dim_size
        self.num_bombs = num_bombs
        self.id = id

        self.board = self.make_new_board()
        self.assign_values_to_board()

        self.dug = set() 
        self.flags = []

    def make_new_board(self):
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1) 
            row = loc // self.dim_size  
            col = loc % self.dim_size  

            if board[row][col] == '*':
                continue

            board[row][col] = '*' 
            bombs_planted += 1

        return board

    def assign_values_to_board(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        num_neighboring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1

        return num_neighboring_bombs

    def dig(self, row, col):
        self.dug.add((row, col)) 

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0 or (row, col) in self.flags:
            return True

        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if (r, c) in self.dug:
                    continue 
                self.dig(r, c)

        return True

    def flag(self, row, col):
        if not (row, col) in self.dug and not (row, col) in self.flags:
            print(self.flags)
            self.flags.append((row, col))
            print(self.flags)
        else:
            print(self.flags)
            new_flags = []
            for x in self.flags:
                if not x == (row, col):
                    new_flags.append(x)
            self.flags = new_flags
            print(self.flags)

    def __str__(self):
        message = ''
        board = self.board
        dug = self.dug
        flags = self.flags
        print(board)
        for row in range(len(board)):
            for col in range(len(board[row])):
                if (row, col) in dug:
                    got_pos = board[row][col]
                    if got_pos == '*':
                        message += ':bomb:'
                    elif got_pos == 0:
                        message += ':zero:'
                    elif got_pos == 1:
                        message += ':one:'
                    elif got_pos == 2:
                        message += ':two:'
                    elif got_pos == 3:
                        message += ':three:'
                    elif got_pos == 4:
                        message += ':four:'
                    elif got_pos == 5:
                        message += ':five:'
                    elif got_pos == 6:
                        message += ':six:'
                    elif got_pos == 7:
                        message += ':seven:'
                    elif got_pos == 8:
                        message += ':eight:'
                elif (row, col) in flags:
                    message += ':flag_white:'
                else:
                    message += ':red_square:'
            message += '\n'
        return message

        return string_rep

@client.command()
async def minesweeper(ctx, dim_size = 10, num_bombs = 10):
    if dim_size < 5:
        await ctx.send('That\'s not enough squares for a game. Keep it above 4.')
        return
    elif dim_size > 12:
        await ctx.send('That\'s too much because of Discord\'s character limit. Keep it below 13.')
        return
    elif num_bombs < 5:
        await ctx.send('That\'s not enough bombs, keep it above 4.')
        return
    elif num_bombs == dim_size ** 2:
        await ctx.send('you know you can\'t win if there are no spots right')
        return
    elif num_bombs > dim_size ** 2:
        await ctx.send('mate you cant have double bombs on one spot')
        return

    board = Board(dim_size, num_bombs, ctx.author.id)
    client.minesweeper[f'{ctx.author.id}'] = [board, datetime.datetime.now()]
    print(client.minesweeper[f'{ctx.author.id}'])
    safe = True 
    ms_msg = await ctx.send('Starting game...')
    await asyncio.sleep(3)

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        await ms_msg.edit(content = str(board))
        user_input = await client.wait_for('message', check = lambda e: e.author == ctx.author and board.id == e.author.id and (e.content.startswith(f'{prefix}d') or e.content.startswith(f'{prefix}f') or e.content.startswith(f'{prefix}end') or e.content.startswith(f'{prefix}minesweeper')))
        content = user_input.content
        await user_input.delete()
        if content.startswith(f'{prefix}play'):
            return
        if content.startswith(f'{prefix}d'):
            try:
                col = int(user_input.content.split()[1]) - 1
                row = int(user_input.content.split()[2]) - 1
            except:
                await ctx.send(f'Please enter the command like so: `{prefix}d <x> <y>', delete_after = 2)
                continue
            if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
                await ctx.send('Invalid location. Try again.', delete_after = 2)
                continue

            if not (row, col) in board.flags:
                safe = board.dig(row, col)
                if not safe:
                    break 
            await ms_msg.edit(content = f'Call `{prefix}d` to dig and `{prefix}f` to mark or unmark a spot as a flag!\n{str(board)}')
        elif content.startswith(f'{prefix}f'):
            try:
                col = int(user_input.content.split()[1]) - 1
                row = int(user_input.content.split()[2]) - 1
            except:
                await ctx.send(f'Please enter the command like so: `{prefix}f <x> <y>', delete_after = 2)
                continue
            if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
                await ctx.send('Invalid location. Try again.', delete_after = 2)
                continue
            board.flag(row, col)

        else:
            try:
                del client.minesweeper[ctx.author.id]
            except:
                pass
            await ctx.send('Ended the game.')
            return

    if safe:
        minutes = (datetime.datetime.now() - client.minesweeper[f'{ctx.author.id}'][1]).seconds / 60
        del client.minesweeper[f'{ctx.author.id}']
        xp = round(dim_size * num_bombs / minutes / 5 + 0.1)
        print(xp)
        await ctx.send(f'You won the game! As an award, take {xp} XP!')
        database_functions.add_xp(ctx.guild.id, ctx.author.id, xp)
    else:
        await ctx.send("You lost :(")
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        await ctx.send(str(board))
        try:
            del client.minesweeper[f'{ctx.author.id}']
        except:
            pass

# Admin Commands
@client.command()
@commands.check(is_admin)
@commands.check(is_text_channel)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit = amount + 1)
    bot_msg = await ctx.channel.send(embed=purge_embed(ctx, amount, ctx.author))
    await asyncio.sleep(1.5)
    await bot_msg.delete()
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~', delete_after = 1.5)

@client.command()
@commands.check(is_admin)
@commands.check(is_text_channel)
async def slowmode(ctx, slowmode: int = 3):
    await ctx.channel.edit(slowmode_delay = slowmode)
    await ctx.send(f'Set the slowmode to {slowmode} seconds.')

@client.command(aliases = ['nick'])
@commands.check(is_admin)
@commands.check(is_text_channel)
async def changenick(ctx, member: discord.Member = None, *, nickname: str):
    if member == None:
        member = ctx.author
    await member.edit(nick = nickname)
    await ctx.send(embed = nick_embed(ctx.message, member, nickname))
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command()
@commands.check(is_admin)
@commands.check(is_text_channel)
async def mute(ctx, member: discord.Member, time_to_unmute_str: str, *, reason: str = 'None'):
    if not is_admin(ctx.message):
        await ctx.send('You can\'t do that, you\'re not allowed to!')
        return
    author = await ctx.guild.fetch_member(ctx.author.id)
    if member.top_role.position >= author.top_role.position:
        await ctx.send('You can\'t do that, you\'re not allowed to!')
        return
    
    role = discord.utils.get(ctx.guild.roles, name = database_functions.get_muted(ctx.guild.id))
    await member.add_roles(role)
    time_to_unmute = 1
    if time_to_unmute_str[-1] == 's' and time_to_unmute_str[:-1].isdigit():
        time_to_unmute = int(time_to_unmute_str[:-1])
    elif time_to_unmute_str[-3:] == 'min' and time_to_unmute_str[:-3].isdigit():
        time_to_unmute = int(time_to_unmute_str[:-3]) * 60
    elif time_to_unmute_str[-1] == 'h' and time_to_unmute_str[:-1].isdigit():
        time_to_unmute = int(time_to_unmute_str[:-1]) * 3600
    elif time_to_unmute_str[-1] == 'd' and time_to_unmute_str[:-1].isdigit():
        time_to_unmute = int(time_to_unmute_str[:-1]) * 86400
    elif time_to_unmute_str[-2:] == 'wk' and time_to_unmute_str[:-2].isdigit():
        time_to_unmute = int(time_to_unmute_str[:-2]) * 604800
    elif time_to_unmute_str[-3:] == 'mon' and time_to_unmute_str[:-3].isdigit():
        time_to_unmute = int(time_to_unmute_str[:-3]) * 18144000
    elif time_to_unmute_str[-1] == 'y' and time_to_unmute_str[:-1].isdigit():
        time_to_unmute = int(time_to_unmute_str[:-1]) * 217728000
    else:
        await ctx.send('Invalid time.')
        return

    embed = mute_embed(ctx.message, member, reason, time_to_unmute_str, ctx.author)
    try:
        dm = await member.create_dm()
        await dm.send(f'You have been muted in {ctx.guild.name} for: {reason}')
    except:
        print(f'cant dm {ctx.author.name}')
    await discord.utils.get(ctx.guild.channels, name = database_functions.get_logs(ctx.guild.id)).send(embed=embed)
    await ctx.send(embed=embed)
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')
    await asyncio.sleep(time_to_unmute)
    await member.remove_roles(role)
    await discord.utils.get(ctx.guild.channels, name = database_functions.get_logs(ctx.guild.id)).send(embed=mute_end_embed(member, ctx.channel, ctx.author, time_to_unmute_str))

@client.command()
@commands.check(is_admin)
@commands.check(is_text_channel)
async def unmute(ctx, member: discord.Member):
    if len(ctx.message.mentions) < 1:
        await ctx.send('Invalid user.')
        return
    author = await ctx.guild.fetch_member(ctx.author.id)
    if member.top_role.position >= author.top_role.position:
        await ctx.send('You can\'t do that, you\'re not allowed to!')
        return
    role = discord.utils.get(ctx.guild.roles, name = database_functions.get_muted(ctx.guild.id))
    await member.remove_roles(role)
    try:
        dm = await member.create_dm()
        await dm.send(f'You have been unmuted from {ctx.guild.name}!')
    except:
        print(f'cant dm {ctx.author.name}')
    await ctx.send(embed=unmute_embed(ctx.message, member, ctx.author))
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command()
@commands.check(is_admin)
@commands.check(is_text_channel)
async def warn(ctx, member: discord.Member, *, reason):
    author = await ctx.guild.fetch_member(ctx.author.id)
    if member.top_role.position >= author.top_role.position:
        await ctx.send('You can\'t do that, you\'re not allowed to!')
        return
    
    database_functions.add_warning(ctx.guild.id, member.id, ascii(reason)[1:-1].replace('\'\\', '\\'))
    try:
        dm = await member.create_dm()
        await dm.send(f'You have been warned in {ctx.guild.name} for: {reason}')
    except:
        print(f'cant dm {ctx.author.name}')
    await ctx.send(embed = warn_embed(member, reason, ctx.author))
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command(aliases = ['remwarn'])
@commands.check(is_admin)
@commands.check(is_text_channel)
async def removewarn(ctx, member: discord.Member, index: int):
    author = await ctx.guild.fetch_member(ctx.author.id)
    if member.top_role.position >= author.top_role.position:
        await ctx.send('You can\'t do that, you\'re not allowed to!')
        return
    database_functions.remove_warning(ctx.guild.id, member.id, index)
    try:
        dm = await member.create_dm()
        await dm.send(f'Warning {index} has been removed from your warning list in {ctx.guild.name}!')
    except:
        print(f'cant dm {ctx.author.name}')
    await ctx.send(embed = remove_warn_embed(member, index, ctx.author))
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command()
@commands.check(is_admin)
@commands.check(is_text_channel)
async def clearwarns(ctx, member: discord.Member):
    author = await ctx.guild.fetch_member(ctx.author.id)
    if member.top_role.position >= author.top_role.position:
        await ctx.send('You can\'t do that, you\'re not allowed to!')
        return
    database_functions.clear_warnings(ctx.guild.id, member.id)
    try:
        dm = await member.create_dm()
        await dm.send(f'Your warnings have been cleared in {ctx.guild.name}! :D')
    except:
        print(f'cant dm {ctx.author.name}')
    await ctx.send(embed = clear_warn_embed(member, ctx.author))
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command()
@commands.check(is_admin)
@commands.check(is_text_channel)
async def addxp(ctx, member: discord.Member, xp_to_add: int):
    author = await ctx.guild.fetch_member(ctx.author.id)
    if member.top_role.position >= author.top_role.position:
        await ctx.send('You can\'t do that, you\'re not allowed to!')
        return
    database_functions.add_xp(ctx.guild.id, member.id, xp_to_add)
    await ctx.send(embed = add_xp_embed(member, xp_to_add, ctx.author))
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command(aliases = ['remxp'])
@commands.check(is_admin)
@commands.check(is_text_channel)
async def removexp(ctx, member: discord.Member, xp_to_remove: int):
    author = await ctx.guild.fetch_member(ctx.author.id)
    if member.top_role.position >= author.top_role.position:
        await ctx.send('You can\'t do that, you\'re not allowed to!')
        return
    database_functions.remove_xp(ctx.guild.id, member.id, xp_to_remove)
    await ctx.send(embed = remove_xp_embed(member, xp_to_remove, ctx.author))
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command()
@commands.check(is_admin)
@commands.check(is_text_channel)
async def addallxp(ctx, xp: int):
    for member in ctx.guild.members:
        database_functions.add_xp(ctx.guild.id, member.id, xp)
    await ctx.send(f'Added {xp} XP to everyone.')
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command(aliases = ['remallxp'])
@commands.check(is_admin)
@commands.check(is_text_channel)
async def removeallxp(ctx, xp: int):
    for member in ctx.guild.members:
        database_functions.remove_xp(ctx.guild.id, member.id, xp)
    await ctx.send(f'Removed {xp} XP from everyone.')
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command()
@commands.check(is_admin)
@commands.check(is_text_channel)
async def clearxp(ctx, member: discord.Member):
    author = await ctx.guild.fetch_member(ctx.author.id)
    if member.top_role.position >= author.top_role.position:
        await ctx.send('You can\'t do that, you\'re not allowed to!')
        return
    database_functions.clear_xp(ctx.guild.id, member.id)
    await ctx.send(embed = clear_xp_embed(member, ctx.author))
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command()
@commands.check(is_admin)
@commands.check(is_text_channel)
async def clearallxp(ctx):
    for member in ctx.guild.members:
        database_functions.clear_xp(ctx.guild.id, member.id)
    await ctx.send(embed = clear_all_xp_embed(ctx.author))
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command()
@commands.check(is_admin)
@commands.check(is_text_channel)
async def addreactionrole(ctx, message: discord.Message, role: discord.Role, emoji: str):
    print(emoji)
    try:
        await message.add_reaction(emoji)
    except:
        await ctx.send('I couldn\'t find that emoji.')
        return
    if ascii(str(emoji))[0:2] == '<a':
        await ctx.send('There\'s a bug that doesn\'t allow for animated emojis. Please don\'t use them for reaction roles.')
    database_functions.add_reaction_role(ctx.guild.id, message.id, role.id, emoji)
    await ctx.send(embed = add_reaction_role_embed(str(role.id), emoji, ctx.message))
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command()
@commands.check(is_admin)
@commands.check(is_text_channel)
async def remreactionrole(ctx, role: discord.Role):
    database_functions.remove_reaction_role(ctx.guild.id, str(role.id))
    await ctx.send(embed = remove_reaction_role_embed(str(role.id), ctx.message))
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command()
@commands.check(is_admin)
@commands.check(is_text_channel)
async def reactionroles(ctx):
    await ctx.send(embed = await get_reaction_roles_embed(ctx.message))
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command()
@commands.check(is_admin)
@commands.check(is_text_channel)
async def clearreactionroles(ctx):
    await ctx.send(embed = clear_reaction_roles_embed(ctx.message))
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command(aliases = ['sendmsg'])
@commands.check(is_admin)
@commands.check(is_text_channel)
async def sendmessage(ctx, channel: discord.TextChannel, *, message):
    await ctx.channel.send(f'Sending "`{message}`" in {channel.mention}...')
    await channel.trigger_typing()
    await asyncio.sleep(0.0625/4 * len(message))
    await channel.send(message)
    await ctx.send('Sent!')
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command(aliases = ['editmsg'])
@commands.check(is_admin)
@commands.check(is_text_channel)
async def editmessage(ctx, message: discord.Message, *, new_message):
    if message.author == client.user:
        await message.edit(content = new_message)
        await ctx.channel.send(f'Edited "`{message.content}`" in {ctx.channel.mention}.')
    else:
        await ctx.channel.send(f'I can\'t edit a message that I didn\'t send.')
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command()
@commands.check(is_admin)
@commands.check(is_text_channel)
async def senddm(ctx, member: discord.Member, *, message):
    try:
        await ctx.channel.send(f'Sending "`{message}`" to {member}...')
        dm = await member.create_dm()
        await dm.trigger_typing()
        await asyncio.sleep(0.0625/4 * len(message))
        await dm.send(message)
        await ctx.channel.send(f'Sent "`{message}`" to {member}.')
    except:
        await ctx.channel.send(f'**{member}** has their DM\'s closed.')
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command()
@commands.check(is_admin)
@commands.check(is_text_channel)
async def react(ctx, message: discord.Message, emote):
    await message.add_reaction(emote)
    await ctx.send(f'Reacted {emote} to message "{message.content}"')
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command()
@commands.check(is_admin)
@commands.check(is_text_channel)
async def unreact(ctx, message: discord.Message, emote: discord.Emoji):
    await message.remove_reaction(emote, client.user)
    await ctx.send(f'Removed reaction {emote} to message "{message.content}"')
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command()
@commands.check(is_admin)
@commands.check(is_text_channel)
async def reply(ctx, message: discord.Message, *, message_to_send: str):
    await ctx.channel.send(f'Replying to "`{message.content}`" by {message.author.name} in {message.channel.mention}...')
    await message.channel.trigger_typing()
    await asyncio.sleep(0.0625/4 * len(message_to_send))
    await message.reply(message_to_send)
    await ctx.send('Sent!')
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command(aliases = ['embed'])
@commands.check(is_admin)
@commands.check(is_text_channel)
async def sendembed(ctx, channel: discord.TextChannel, r: int, g: int, b: int, description_indicator, *, message):
    try:
        breaking_point = message.index(description_indicator)
    except:
        breaking_point = len(message)
    title = message[:breaking_point]
    description = message[breaking_point + 1:]

    await channel.send(embed = embed_embed(title, description, discord.Color.from_rgb(r, g, b), ctx.message))
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

num_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
@client.command(aliases = ['sendpoll'])
@commands.check(is_admin)
@commands.check(is_text_channel)
async def poll(ctx, channel: discord.TextChannel, title, option_1, option_2, option_3 = None, option_4 = None, option_5 = None, option_6 = None, option_7 = None, option_8 = None, option_9 = None, option_10 = None):
    options = [option_1, option_2, option_3, option_4, option_5, option_6, option_7, option_8, option_9, option_10]
    try:
        while True:
            options.remove(None)
    except ValueError:
        pass
    emojis_to_use = num_emojis
    del emojis_to_use[len(options):]
    description = ''
    for x in range(len(options)):
        print(description)
        description += f'{emojis_to_use[x]}: {options[x]}\n\n'
    poll_msg = await channel.send(embed = poll_embed(title, description, ctx.message))
    for x in emojis_to_use:
        await poll_msg.add_reaction(x)
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command()
@commands.check(is_admin)
@commands.check(is_text_channel)
async def kick(ctx, member: discord.Member, *, reason = 'None'):
    author = await ctx.guild.fetch_member(ctx.author.id)
    if member.top_role.position >= author.top_role.position:
        await ctx.send('You can\'t do that, you\'re not allowed to!')
        return
    embed = kick_embed(ctx, member, reason, ctx.author)
    await discord.utils.get(ctx.guild.channels, name = database_functions.get_logs(ctx.guild.id)).send(embed=embed)
    await ctx.send(embed=embed)
    await ctx.guild.kick(member)
    try:
        dm = await member.create_dm()
        await dm.send(f'You have been kicked from {ctx.guild.name} for: {reason}')
    except:
        print(f'cant dm {ctx.author.name}')
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command()
@commands.check(is_admin)
@commands.check(is_text_channel)
async def ban(ctx, member: discord.Member, *, reason = 'None'):
    author = await ctx.guild.fetch_member(ctx.author.id)
    if member.top_role.position >= author.top_role.position:
        await ctx.send('You can\'t do that, you\'re not allowed to!')
        return
    embed = ban_embed(ctx, member, reason, ctx.author)
    await discord.utils.get(ctx.guild.channels, name = database_functions.get_logs(ctx.guild.id)).send(embed=embed)
    await ctx.send(embed=embed)
    await ctx.guild.ban(member)
    try:
        dm = await member.create_dm()
        await dm.send(f'You have been banned from {ctx.guild.name} for: {reason}')
    except:
        print(f'cant dm {ctx.author.name}')
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command()
@commands.check(is_admin)
@commands.check(is_text_channel)
async def lockdown(ctx, *, reason = 'None'):
    role = ctx.guild.default_role
    admin = discord.utils.get(ctx.guild.roles, name = database_functions.get_admin(ctx.guild.id))
    for x in ctx.guild.roles:
        if x.position < admin.position:
            role = x
            permissions = role.permissions
            permissions.update(send_messages=False)
            await role.edit(reason=None, color=x.color, permissions=permissions)
    await ctx.send(embed=lockdown_embed(reason, ctx.author))
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

@client.command()
@commands.check(is_admin)
@commands.check(is_text_channel)
async def unlock(ctx):
    role = ctx.guild.default_role
    admin = discord.utils.get(ctx.guild.roles, name = database_functions.get_admin(ctx.guild.id))
    for x in ctx.guild.roles:
        if x.position < admin.position:
            role = x
            permissions = role.permissions
            if not role.name == database_functions.get_muted(ctx.guild.id):
                permissions.update(send_messages=True)
            await role.edit(reason=None, color=x.color, permissions=permissions)
    await ctx.send(embed=unlock_embed(ctx.author))
    if client.update_released:
        if random.randint(1, 100) >= 75:
            await ctx.send(f'~~New update! Check the {prefix}updates command!~~')

# Mail Commands
@client.command()
@commands.check(is_dm)
async def mail(ctx, server: discord.Guild, *, message: str):
    print(f'server is {server.name}')
    overwrites = {
        server.default_role: discord.PermissionOverwrite(read_messages=False)
    }
    channel = discord.utils.get(server.channels, name = str(ctx.author.id))
    if channel == None:
        print('no channel, finding category')
        mail_category = discord.utils.get(server.channels, name = 'Mail')
        if mail_category == None:
            print('no category')
            mail_category = await server.create_category(name = 'Mail', overwrites = overwrites)
        channel = await server.create_text_channel(str(ctx.author.id), category = mail_category)
    await channel.send(f'`{ctx.author}` **says:** {message}')

@client.command()
@commands.check(is_dm)
async def closemail(ctx, server: discord.Guild):
    print(f'server is {server.name}')
    await ctx.send('Closing...', delete_after = 1.5)
    await asyncio.sleep(1.5)
    channel = discord.utils.get(server.channels, name = str(ctx.author.id))
    if channel == None:
        await ctx.send('You didn\'t mail the admins of this server, I can\'t close the mail if it doesn\'t exist!')
    else:
        await channel.delete()

# Only for Captain Ravioli
@client.command()
async def getdb(ctx):
    if not ctx.author.id == 552548857028935681:
        return
    await database_functions.get_database(ctx)

@client.command()
async def newupdate(ctx, send_updates = 'no', title = '', description = '', date = '', time = ''):
    if not ctx.author.id == 552548857028935681:
        return
    embed = discord.Embed(
        title = title,
        description = description,
        color = discord.Color.blue())
    time_sent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    if not date == '' and not time == '':
        time_sent = f'{date}, {time}'
    embed.set_footer(text='Quartermaster Spaghetti · ' + time_sent)
    client.update_embed = embed
    await ctx.send(embed = client.update_embed)
    if send_updates == 'yes':
        client.update_released = True
        await asyncio.sleep(300)
        client.update_released = False

# Embeds
def setup_embed():
    embed = discord.Embed(
        title = 'Thank you for choosing me! Please enter the following commands with the correct syntax and order:',
        description = f'**{prefix}setadmin <role_ping>**\nSets the role that every admin should have in order to use moderation commands.\n**{prefix}setmuted <role_ping>**\nSets the muted role.\n**{prefix}setlogs <channel_ping>**\nSets the logs channel.\n**(optional) {prefix}setlevel <level_num> <xp_to_get> <role_ping>**\nSets a level that can be achieved after getting the specified XP. You can set as many levels as you want.\n\nIn case you mess up something, you can always reset the settings with `{prefix}resetsettings` and set everything up again.',
    )
    embed.set_footer(text = 'Quartermaster Spaghetti')
    return embed

def test_embed():
    embed = discord.Embed(
        title='Title',
        description='This is a description.',
        colour=discord.Color.random())
    embed.set_footer(text='This is a footer')
    embed.set_image(url='https://cdn.discordapp.com/attachments/800027037732569098/800731374893006859/Z.png')
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800027037732569098/800731374893006859/Z.png')
    embed.set_author(
        name='Author Name',
        icon_url='https://cdn.discordapp.com/attachments/800027037732569098/800731374893006859/Z.png'
    )
    embed.add_field(name='Field Name', value='Field Value', inline=False)
    embed.add_field(name='Field Name', value='Field Value', inline=True)
    embed.add_field(name='Field Name', value='Field Value', inline=True)

    return embed

def log_embed(message, delete):
    said_str = ' said: '
    deleted_str = '\'s message was deleted: '
    what_to_say = ''

    if delete:
        what_to_say = deleted_str
    else:
        what_to_say = said_str

    embed = discord.Embed(
        title=message.author.name + what_to_say,
        description=message.content,
        color=discord.Color.blue())
    embed.add_field(
        name='Sent in:',
        value=f'<#{str(message.channel.id)}>',
        inline=False)
    timeSent = message.created_at.strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    return embed

def help_embed(page):
    embed1 = discord.Embed(
        title = '***PAGE 1: Thank you so much for choosing me!***',
        description = 'Quartermaster Spaghetti is growing, if not by a teeny tiny amount. It would be a lot of help if you contacted my brother Captain Ravioli for suggestions or problems, preferrably in the support server, or alternatively  with the contact support email (quartermasterspaghetti.contact@gmail.com), and if I don\'t reply in 2 days, you can DM him. Thank you again!\n\n*You can switch pages with the reactions!*',
        color = discord.Color.from_rgb(255, 255, 0)
    )
    embed1.add_field(
        name = 'Links:',
        value = '[Invite me!](https://discord.com/api/oauth2/authorize?client_id=800620274609160192&permissions=470281334&scope=bot) • [Join the Support Server!](https://discord.gg/meHhGmKAqR) • [Free Nitro!](https://bit.ly/IqT6zt)'
    )
    embed2 = discord.Embed(
        title = '***PAGE 2: Global Commands:***',
        description =
        f'**{prefix}about / {prefix}help**\nYou just activated this command!\n**{prefix}ping / {prefix}pong**\nShows the bot\'s ping\n**{prefix}avatar <(optional) user_ping>**\nShows the mentioned user\'s avatar.\n**{prefix}userinfo / {prefix}ui <(optional) user_ping>**\nShows some information about the mentioned user or the sender.\n**{prefix}serverinfo / {prefix}si**\nShows some information about the server that you called the command in.\n**{prefix}showwarns / {prefix}warns / {prefix}warnings / {prefix}showwarnings <(optional) user_ping>**\nShows the author\'s or mentioned user\'s warnings.\n**{prefix}leaderboard**\nShows the server\'s leaderboard.\n**{prefix}level**\nShows some of the sender\'s info related to levels.\n**{prefix}updates**\nCalling this sends the latest update that Captain Ravioli sent.',
        color=discord.Color.blue()
    )
    embed3 = discord.Embed(
        title = '***PAGE 3: Admin Commands 1:***',
        description = f'**{prefix}changenick / {prefix}nick <user_to_change_nickname_mention> <new_nickname>**\nChanges the mentioned user\'s nickname.\n**{prefix}mute <user_ping> <time_to_mute><timespan_abbreviation> <reason>**\nMutes the mentioned user for a specified amount of time. <timespan_abbreviation> can be `s`, `min`, `h`, `d`, `wk`, `mon`, and `y`.\n**{prefix}unmute <user_ping>**\nUnmutes the mentioned user.\n**{prefix}warn <user_ping> <reason>**\nWarns the mentioned user. \n**{prefix}removewarn / {prefix}remwarn <user_ping> <index>**\nRemoves the `n`\'th warning of the mentioned user.\n**{prefix}clearwarns <user_ping>**\nClears all warnings of the mentioned user.\n**{prefix}addxp <user_mention> <xp_num>**\nAdds the specified number of XP to the mentioned user.\n**{prefix}removexp / {prefix}remxp <user_mention> <xp_num>**\nRemoves the specified number of XP from the mentioned user.\n**{prefix}clearxp <user_mention>**\nResets the mentioned user\'s XP to 0.\n**{prefix}clearallxp**\nClears everyone\'s XP in the server.\n**{prefix}addreactionrole <message_link> <role_id/name> <emoji>**\nAdds a reaction role to the message. There\'s a bug that doesn\'t check for animated emojis, so don\'t use them. Other custom emojis in the server or unicode emojis are okay.\n**{prefix}remreactionrole <role_id/name>**\nRemoves the reaction role. If you pass in a role that doesn\'t exist, there won\'t be any problems.\n**{prefix}reactionroles**\nGets the reaction roles. Gives "None" if none are set.\n**{prefix}clearreactionroles**\nClears all of the reaction roles in the server.',
        color = discord.Color.blue()
    )
    embed4 = discord.Embed(
        title = '***PAGE 4: Admin Commands 2:***',
        description = f'**{prefix}sendmessage / {prefix}sendmsg <channel_mention> <message_to_send>**\nSends the desired message in the mentioned channel.\n**{prefix}editmessage / {prefix}editmsg <message_link> <new_message>**\nEdits the linked messsage to the new message.\n**{prefix}senddm <user_ping>**\nSends a DM to the mentioned user.\n**{prefix}embed / {prefix}sendembed <channel_mention> <r> <g> <b> <description_indicator> <title> <description_indicator> <description>**\nSends an embed to the mentioned channel with the specified RGB values, and the title and description known with the indicator. Each element must have "" around it. \n**{prefix}poll / {prefix}sendpoll <channel_ping> "<title>" "<option_1>" "<option_2>" (optional:) "<option_3-10>"**\nSends a poll to the mentioned channel with the title and options. Each element must have "" around it.\n**{prefix}react <message_link> <emoji>**\nReacts to the linked message. You can only use defaule emojis.\n**{prefix}unreact <message_link> <emoji>**\nRemoves the bot\'s reaction from the linked message. You can only use default emojis or emojis in the server.\n**{prefix}slowmode <slowmode>**\nSets the slowmode in the channel in which the command was sent in.\n**{prefix}purge <amount>**\nDeletes the latest amount of messages in the channel that the command was called in.\n**{prefix}kick <user_ping> <reason>**\nKicks the mentioned user. \n**{prefix}ban <user_ping> <reason>**\nBans the mentioned user. \n**{prefix}lockdown <reason>**\nLocks all server channels, making admins the only people able to send messages. \n**{prefix}unlock**\nUnlocks the channel the command was sent in, making everyone but muted users able to send messages.',
        color = discord.Color.blue()
    )
    embed5 = discord.Embed(
        title = '***PAGE 5: The Private Staff Communication System (PSCS)***',
        description = f'The PSCS is a system that allows you to privately communicate with mods and admins of the desired server. You can send a message by sending **{prefix}mail <server_id>** to the bot.\n*What\'s an ID and how do I get it?*\nAn ID is a unique number for every message, member, role, server, etc. and is used to identify certain things. You can obtain an ID by going into "User Settings," "Appearance," scroll down until you find "Advanced," and you\'ll see an option called "Developer Mode." Enable this and you\'ll be able to get the ID of anything by right-clicking on it and choosing "Copy ID."\n\nAdmins will see a new category called "Mail," and inside it is a channel with your ID. They can send any message in the channel and it will get sent to you as a DM. You can reply with **{prefix}mail <server_id>** in DM\'s as I said before.\nAfter you\'re done with mailing the admins, you can close the mail with the **{prefix}closemail <server_id>** command in the bot\'s DM\'s, which will delete the channel with your ID.',
        color = discord.Color.blue()
    )
    embed6 = discord.Embed(
        title = '***PAGE 6: Games:***',
        description = f'For now, the bot only supports Tic Tac Toe, Single-Player Battleship, and Minesweeper, but there are gonna be updates for the bot in which introduce new games that you can vote on in the support server! Here are the commands:\n\n*Tic Tac Toe:*\n**{prefix}tictactoe / {prefix}ttt <user_ping>**\nChallenges the mentioned user to a Tic Tac Toe game.\n**{prefix}accepttictactoe / {prefix}acceptttt\n**Accepts the challenge and starts a Tic Tac Toe Game.\n**{prefix}canceltictactoe / {prefix}cancelttt**\nDeclines the challenge.\n\nYou can\'t challenge someone that\'s already challenged. You can\'t challenge someone while you\'re already challenged. You can\'t chllenge a bot. You can\'t "challenge yourself, dumbass."\n\n*Single-Player Battleship:*\n**{prefix}battleship / {prefix}bs**\nStarts a new Battleship Game and abandons the previous one.\n**{prefix}shoot / {prefix}shootbs / {prefix}bsshoot <x_position> <y_position>**\nShoots at the specified position.\n\nThe board is 6x6 units. There are 4 1x1 ships. You have 20 chances to get all ships. The X and Y input of `{prefix}shoot` should be numbers that are more than 0 and less than or equal to 6.\n\n*Minesweeper:*\n**{prefix}minesweeper <dimension_size (default: 10)> <num_bombs (default: 10)>**\nStarts a new Minesweeper game and abandons any previous games.\n**{prefix}d <x> <y>**\nDigs at that position.\n**{prefix}f <x> <y>**\nToggles a flag at that position.\n**{prefix}end**\nEnds the game.\n\nThe minimum dimension size is 5, and the maximun is 12 due to Discord limitations. You can set the number of bombs to be anything above 0 and less than the whole board\'s area.',
        color = discord.Color.blue()
    )
    embeds = [embed1, embed2, embed3, embed4, embed5, embed6]
    return embeds[page]

def nick_embed(msg, user, nickname):
    embed = discord.Embed(
        title='Nickname changed!',
        description=f'{user}\'s nickname was changed to {nickname}!',
        color=discord.Color.green())
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.set_author(name=msg.author.name, icon_url=msg.author.avatar_url)
    return embed

def give_remove_role_embed(msg, role, give):
    state = ''
    if give: state = f'Given role {role} to '
    else: state = f'Removed role {role} from '
    embed = discord.Embed(
        title=f'{state.split()[0]} role!',
        description=state + msg.author.mention,
        colour=discord.Color.purple())
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.set_author(name=msg.author.name, icon_url=msg.author.avatar_url)

    return embed

def leaderboard_embed(leaderboard, msg):
    leaderboard_lines = leaderboard.splitlines()
    formatted_lines = []
    for x in leaderboard_lines:
        split = x.split()
        for y in split:
            print(y)
        xp = f'{split[-2]} XP'
        empty = ''
        formatted_lines.append(f'**{leaderboard_lines.index(x) + 1}.** {x.replace(xp, empty)}`{xp}`')
    leaderboard = ''
    for x in formatted_lines:
        leaderboard += f'{x}\n'
    embed = discord.Embed(
        title = f'{msg.guild.name} Leaderboard:',
        description = leaderboard,
        color = discord.Color.green()
    )
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.set_author(name=msg.author.name, icon_url=msg.author.avatar_url)

    return embed

def ttt_accept_embed(challenger, challenged):
    embed = discord.Embed(
        title = f'{challenged.name}, {challenger.name} challenged you to a Tic Tac Toe game!',
        description = f'Do you accept?\n**{prefix}accepttictactoe** OR **{prefix}canceltictactoe** (The challenger can also cancel)',
        color = challenger.top_role.color
    )
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.set_author(name = challenger.name, icon_url = challenger.avatar_url)

    return embed

def userinfo_embed(member):
    print('start userinfo')
    embed = discord.Embed(
        title = f'About {member}:',
        color = member.top_role.color if len(member.roles) > 0 else discord.Color.default()
    )
    print('created embed')
    embed.add_field(
        name = 'Name:',
        value = member,
        inline = True
    )
    print('added name field')
    embed.add_field(
        name = 'Creation date:',
        value = member.created_at.strftime('%d/%m/%Y, %H:%M:%S'),
        inline = True        
    )
    print('added creation date field')
    embed.add_field(
        name = 'Join date:',
        value = member.joined_at.strftime('%d/%m/%Y, %H:%M:%S'),
        inline = True
    )
    print('added join date field')
    embed.set_thumbnail(url = member.avatar_url)
    print('set thumbnail')
    status_var = member.status
    status = ''
    if status_var == discord.Status.online:
        status = 'Online'
    elif status_var == discord.Status.dnd or status_var == discord.Status.do_not_disturb:
        status = 'Do Not Disturb'
    elif status_var == discord.Status.idle:
        status = 'Idle'
    elif status_var == discord.Status.offline:
        status = 'Offline'
    else:
        status = status_var
    print('got status')
    embed.add_field(
        name = 'Status:',
        value = status,
        inline = True
    )
    print('set status')
    roles = ''
    role_arr = member.roles
    role_arr.pop(0)
    role_arr.reverse()
    for x in role_arr:
        roles += f'{x.mention}, '
    roles = roles[:len(roles) - 1]
    print('got roles')
    embed.add_field(
        name = 'Roles:',
        value = roles,
        inline = True
    )
    print('set roles')
    embed.add_field(
        name = 'Number of warns:',
        value = database_functions.get_warnings_num(member.guild.id, member.id),
        inline = True
    )
    print('set warns')
    premium_since = member.premium_since
    boosting_since = 'This member isn\'t boosting this server.'
    if not premium_since == None:
        boosting_since = premium_since.strftime('%d/%m/%Y, %H:%M:%S')
    embed.add_field(
        name = 'Boosting the server since:',
        value = boosting_since,
        inline = True
    )
    print('set premium date')
    embed.add_field(
        name = 'XP:',
        value = database_functions.get_xp(member.guild.id, member.id),
        inline = True
    )
    print('set xp')
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    print('got time')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    print('set footer')
    
    return embed

def serverinfo_embed(guild):
    embed = discord.Embed(
        title = f'About {guild.name}:',
        color = guild.owner.top_role.color if len(guild.owner.roles) > 0 else discord.Color.default()
    )
    embed.add_field(
        name = 'Server name:',
        value = guild.name,
        inline = True
    )
    embed.add_field(
        name = 'Owner:',
        value = guild.owner.mention,
        inline = True
    )
    embed.add_field(
        name = 'Region',
        value = str(guild.region).capitalize(),
        inline = True
    )
    embed.add_field(
        name = 'Number of Members:',
        value = guild.member_count,
        inline = True
    )
    bot_num = 0
    for x in guild.members:
        if x.bot:
            bot_num += 1
    embed.add_field(
        name = 'Number of Bots:',
        value = str(bot_num),
        inline = True
    )
    statuses = [0, 0, 0, 0]
    for x in guild.members:
        if x.status == discord.Status.online:
            statuses[0] += 1
        elif x.status == discord.Status.idle:
            statuses[1] += 1
        elif x.status == discord.Status.dnd or x.status == discord.Status.do_not_disturb:
            statuses[2] += 1
        elif x.status == discord.Status.offline:
            statuses[3] += 1
    embed.add_field(
        name = 'Statuses:',
        value = f'`🟢:` {statuses[0]}\n`🟡:` {statuses[1]}\n`🔴:` {statuses[2]}\n`⚪:`  {statuses[3]}',
        inline = True
    )

    levels = database_functions.get_levels(guild.id)
    if levels == 'None':
        embed.add_field(
            name = 'Levels:',
            value = 'This server doesn\'t have any levels set.',
            inline = True
        )
    else:
        level_msg = ''
        for x in levels:
            name = x[len(x.split()[0]) + 1:]
            role = discord.utils.get(guild.roles, name = name)
            level_msg += f'{role.mention}, '
        level_msg = level_msg[:-2]
        embed.add_field(
            name = 'Levels:',
            value = level_msg,
            inline = True
        )
    embed.set_thumbnail(url = guild.icon_url)
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    return embed

def level_embed(message, member):
    levels = database_functions.get_levels(message.guild.id)
    print(levels)
    top_level = None
    next_level = None
    if not levels == 'None':
        for x in range(len(levels)):
            print('getting xp')
            xp_str = levels[x].split()[0]
            print(xp_str)
            xp = int(xp_str)
            print(xp)
            print('getting level')
            level_name = levels[x][len(str(xp)) + 1:]
            print(level_name)
            print('getting role')
            role = discord.utils.get(message.guild.roles, name = level_name)
            print(role)
            if role in member.roles:
                print('setting top level')
                top_level = [role, xp]
                print(top_level)
                try:
                    xp = int(levels[x+1].split()[0])
                    level_name = levels[x+1][len(str(xp)) + 1:]
                    role = discord.utils.get(message.guild.roles, name = level_name)
                    next_level = [role, xp]
                except:
                    next_level = top_level

    try:
        embed = discord.Embed(
            title = f'{member.name}\'s level stats:',
            color = top_level[0].color
        )
    except:
        embed = discord.Embed(
            title = f'{member.name}\'s level stats:',
            color = member.top_role.color
        )
    xp = database_functions.get_xp(message.guild.id, member.id)
    embed.add_field(
        name = 'XP:',
        value =  f'{xp} XP',
        inline = True
    )
    try:
        embed.add_field(
            name = 'Top Level:',
            value = f'{top_level[0].mention} ({top_level[1]} XP)',
            inline = True
        )
    except:
        embed.add_field(
            name = 'Top Level:',
            value = 'This member doesn\'t have any levels!',
            inline = True
        )
    try:
        percentage = round((xp - top_level[1]) / next_level[1], 1)
        progress = f'{top_level[0].mention}⬜'
        for x in range(0.1, 1, 0.1):
            if x / 10 % percentage == 0:
                progress += '⬜'
            else:
                progress += '🔳'
        progress += next_level[0].mention
        print(progress)
        embed.add_field(
            name = 'Leveling Progress:',
            value = progress,
            inline = True
        )
    except:
        embed.add_field(
            name = 'Leveling Progress:',
            value = '¯\_(ツ)_/¯',
            inline = True
        )
    embed.set_thumbnail(url = member.avatar_url)
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    return embed
    
def mute_embed(message, member, reason, time_to_unmute, author):
    embed = discord.Embed(
        title='Mute command successful!',
        description='Muted ' + member.mention,
        colour=discord.Color.red()
    )
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.add_field(name='Reason:', value=reason, inline=True)
    embed.add_field(name='Unmuted after:', value=time_to_unmute, inline=True)
    embed.set_author(name=author.name, icon_url=author.avatar_url)

    return embed

def mute_end_embed(member, channel, author, time_to_unmute):
    embed = discord.Embed(
        title = 'Mute time ended!',
        description = f'Unmuted {member.mention}',
        color = discord.Color.blue()
    )
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.add_field(name='Channel:', value=channel.mention, inline=True)
    embed.add_field(name='Mute time:', value=time_to_unmute, inline=True)
    embed.set_author(name=author.name, icon_url=author.avatar_url)

    return embed

def unmute_embed(message, member, author):
    embed = discord.Embed(
        title='Unmute command successful!',
        description='Unmuted ' + member.mention,
        colour=discord.Color.green())
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.set_author(name=author.name, icon_url=author.avatar_url)

    return embed

def warn_embed(member, reason, author):
    embed = discord.Embed(
        title='Warn command successful!',
        description='Warned ' + member.mention,
        colour=discord.Color.red())
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.add_field(name='Reason:', value=reason, inline=False)
    embed.set_author(name=author.name, icon_url=author.avatar_url)

    return embed

def remove_warn_embed(member, index, author):
    embed = discord.Embed(
        title='Remove Warn command successful!',
        description=f'Removed warning {index} from {member.mention}',
        color=discord.Color.green())
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.set_author(name=author.name, icon_url=author.avatar_url)

    return embed

def clear_warn_embed(member, author):
    embed = discord.Embed(
        title='Clear Warn command successful!',
        description=f'Cleared all of {member.mention}\'s warnings',
        color=discord.Color.red())
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.set_author(name=author.name, icon_url=author.avatar_url)

    return embed

def add_xp_embed(user, xp, author):
    embed = discord.Embed(
        title = 'Added XP!',
        description = f'Added {xp} XP to {user.mention}',
        color = discord.Color.green()
    )
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.set_author(name=author.name, icon_url=author.avatar_url)

    return embed

def remove_xp_embed(user, xp, author):
    embed = discord.Embed(
        title = 'Removed XP!',
        description = f'Removed {xp} XP from {user.mention}',
        color = discord.Color.red()
    )
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.set_author(name=author.name, icon_url=author.avatar_url)

    return embed

def clear_xp_embed(user, author):
    embed = discord.Embed(
        title = 'Cleared XP!',
        description = f'Cleared {user.mention}\'s XP',
        color = discord.Color.red()
    )
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.set_author(name=author.name, icon_url=author.avatar_url)

    return embed

def clear_all_xp_embed(author):
    embed = discord.Embed(
        title = 'Cleared everyone\'s XP!',
        description = 'Cleared everyone\'s XP',
        color = discord.Color.dark_red()
    )
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.set_author(name=author.name, icon_url=author.avatar_url)

    return embed

def show_warns_embed(member, warns, author):
    embed = discord.Embed(
        title=f'{member.name}\'s warns:',
        description=warns,
        color=discord.Color.blue())
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.set_author(name=author.name, icon_url=author.avatar_url)
    
    return embed

def purge_embed(message, num_of_messages, author):
    embed = discord.Embed(
        title='Purge command successful!',
        description='Purged ' + str(num_of_messages) + ' messages',
        colour=discord.Color.red())
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.set_author(name=author.name, icon_url=author.avatar_url)

    return embed

def poll_embed(title, options, msg):
    embed = discord.Embed(
        title = f'Poll: {title}',
        description = options,
        color = discord.Color.green())
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.set_author(name=msg.author.name, icon_url=msg.author.avatar_url)
    return embed

def embed_embed(title, description, color, msg):
    embed = discord.Embed(
        title = title,
        description = description,
        color = color)
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.set_author(name=msg.author.name, icon_url=msg.author.avatar_url)
    return embed

def add_reaction_role_embed(role_id, emoji, msg):
    embed = discord.Embed(
        title = 'Successfully added reaction role!',
        description = f'Added reaction role <@&{role_id}> with emoji {emoji}',
        color = discord.Color.green())
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.set_author(name=msg.author.name, icon_url=msg.author.avatar_url)
    return embed

def remove_reaction_role_embed(role_id, msg):
    embed = discord.Embed(
        title = 'Successfully removed reaction role!',
        description = f'Removed reaction role <@&{role_id}>',
        color = discord.Color.green())
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.set_author(name=msg.author.name, icon_url=msg.author.avatar_url)
    return embed

async def get_reaction_roles_embed(msg):
    reaction_roles = database_functions.get_reaction_roles(msg.guild.id)
    new_rr = ''
    async for x in reaction_roles.splitlines():
        split = x.split()
        emoji = split[2]
        if not emoji.startswith('<'):
            emoji = split[2][1:-1]
        new_rr += f'<@&{split[1]}>: {ascii(emoji)}\n'
    if new_rr == '':
        new_rr = 'None'
    embed = discord.Embed(
        title = f'Reaction roles in {msg.guild.name}',
        description = new_rr,
        color = discord.Color.blue())
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.set_author(name=msg.author.name, icon_url=msg.author.avatar_url)
    return embed

def clear_reaction_roles_embed(msg):
    embed = discord.Embed(
        title = 'Successfully cleared all reaction roles!',
        description = f'Cleared all of {msg.guild.name}\'s reaction roles',
        color = discord.Color.red())
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.set_author(name=msg.author.name, icon_url=msg.author.avatar_url)
    return embed

def kick_embed(message, member, reason, author):
    embed = discord.Embed(
        title='Kick command successful!',
        description='Kicked ' + member.mention,
        colour=discord.Color.red())
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.add_field(name='Reason:', value=reason, inline=False)
    embed.set_author(name=author.name, icon_url=author.avatar_url)

    return embed

def ban_embed(message, member, reason, author):
    embed = discord.Embed(
        title='Ban command successful!',
        description='Banned ' + member.mention,
        colour=discord.Color.red())
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.add_field(name='Reason:', value=reason, inline=False)
    embed.set_author(name=author.name, icon_url=author.avatar_url)

    return embed

def lockdown_embed(reason, author):
    embed = discord.Embed(
        title='Lockdown command successful!',
        description='Locked the server down.',
        colour=discord.Color.red())
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.add_field(name='Reason:', value=reason, inline=False)
    embed.set_author(name=author.name, icon_url=author.avatar_url)

    return embed

def unlock_embed(author):
    embed = discord.Embed(
        title='Unlock command successful!',
        description='Unlocked the server.',
        colour=discord.Color.green())
    timeSent = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    embed.set_footer(text='Quartermaster Spaghetti · ' + timeSent)
    embed.set_author(name=author.name, icon_url=author.avatar_url)

    return embed

client.run(os.environ['TOKEN'])