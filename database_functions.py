import keyvaluedatabase
import datetime
import discord
import os

db = keyvaluedatabase.DataBase('', 'database', current_directory = True)

async def get_database(ctx):
    keys = db.keys()
    for key in keys:
        value = db.get(key)
        if isinstance(value, int):
            await ctx.send(f'`\'{key}\': {value},`')
        else:
            await ctx.send(f'`\'{key}\': \'{value}\',`')
    for file in os.listdir():
        if file.startswith('muted '):
            open_file = open(file, 'r')
            read_file = open_file.read()
            if not read_file.strip() == '':
                await ctx.send(f'Muted in {ctx.guild.id}')
                for line in read_file.splitlines():
                    await ctx.send('`'+line+'`')
    await ctx.send('Done')

def add_xp(guild_id, user_id, xp_to_add):
    if db.isfound(f'levels {guild_id} {user_id}'):
        xp = db.get(f'levels {guild_id} {user_id}')
        xp += xp_to_add
        db.change(f'levels {guild_id} {user_id}', xp)
        print(f'added xp to {user_id} in {guild_id}')
    elif not db.isfound(f'levels {guild_id} {user_id}'):
        db.add(f'levels {guild_id} {user_id}', xp_to_add)

    if int(db.get(f'levels {guild_id} {user_id}')) < 0:
        db.change(f'levels {guild_id} {user_id}', 0)
    db.save()

def remove_xp(guild_id, user_id, xp_to_remove):
    if db.isfound(f'levels {guild_id} {user_id}'):
        xp = db.get(f'levels {guild_id} {user_id}')
        xp -= xp_to_remove
        db.change(f'levels {guild_id} {user_id}', xp)
    elif not db.isfound(f'levels {guild_id} {user_id}'):
        db.add(f'levels {guild_id} {user_id}', 0)

    if int(db.get(f'levels {guild_id} {user_id}')) < 0:
        db.change(f'levels {guild_id} {user_id}', 0)
    db.save()
    

def clear_xp(guild_id, user_id):
    if db.isfound(f'levels {guild_id} {user_id}'):
        db.delete(f'levels {guild_id} {user_id}')
        db.save()

def get_xp(guild_id, user_id):
    if db.isfound(f'levels {guild_id} {user_id}'):
        return db.get(f'levels {guild_id} {user_id}')
    else:
        return 0


def add_warning(guild_id, user_id, reason):
    for x in range(1, 100):
        if not db.isfound(f'warn {x} {guild_id} {user_id}'):
            db.add(f'warn {x} {guild_id} {user_id}', f'(Time of warn: {datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}) {reason}')
            db.save()
            return

def remove_warning(guild_id, user_id, index):
    if db.isfound(f'warn {index} {guild_id} {user_id}'):
        db.delete(f'warn {index} {guild_id} {user_id}')
        db.save()

def clear_warnings(guild_id, user_id):
    for x in range(1, 100):
        if db.isfound(f'warn {x} {guild_id} {user_id}'):
            db.delete(f'warn {x} {guild_id} {user_id}')
    db.save()

def get_warnings(guild_id, user_id):
    warnings = ''
    for x in range(1, 100):
        if db.isfound(f'warn {x} {guild_id} {user_id}'):
            warnings += f'**{x}.** ' + db.get(f'warn {x} {guild_id} {user_id}') + '\n'
    if warnings == '':
        return 'No warnings found :D'
    else:
        return warnings


def get_warnings_num(guild_id, user_id):
    value = 0
    for x in range(1, 100):
        if db.isfound(f'warn {x} {guild_id} {user_id}'):
            value += 1
        else:
            return value


def set_admin(guild_id, role_id):
    if db.isfound(f'admin {guild_id}'):
        db.change(f'admin {guild_id}', f'{role_id}')
    else:
        db.add(f'admin {guild_id}', f'{role_id}')
    db.save()


def set_muted(guild_id, role_id):
    if db.isfound(f'muted {guild_id}'):
        db.change(f'muted {guild_id}', f'{role_id}')
    else:
        db.add(f'muted {guild_id}', f'{role_id}')
    db.save()


def set_logs(guild_id, channel_id):
    if db.isfound(f'logs {guild_id}'):
        db.change(f'logs {guild_id}', f'{channel_id}')
    else:
        db.add(f'logs {guild_id}', f'{channel_id}')
    db.save()


def set_level(guild_id, index, role_id):
    if db.isfound(f'level {index} {guild_id}'):
        db.change(f'level {index} {guild_id}', f'{role_id}')
    else:
        db.add(f'level {index} {guild_id}', f'{role_id}')
    db.save()


def get_setup(guild_id):
    setup = ''
    if db.isfound(f'admin {guild_id}'):
        setup += db.get(f'admin {guild_id}') + '\n'
        if db.isfound(f'muted {guild_id}'):
            setup += db.get(f'muted {guild_id}') + '\n'
            if db.isfound(f'logs {guild_id}'):
                setup += db.get(f'logs {guild_id}') + '\n'
                i = 0
                for x in db.keys():
                    if x == f'level {i} {guild_id}':
                        setup += db.get(x) + '\n'
                        i += 1
    return setup

def get_admin(guild_id):
    if db.isfound(f'admin {guild_id}'):
        return db.get(f'admin {guild_id}')
    return 'None'

def get_muted(guild_id):
    if db.isfound(f'muted {guild_id}'):
        return db.get(f'muted {guild_id}')
    return 'None'

def get_logs(guild_id):
    if db.isfound(f'logs {guild_id}'):
        return db.get(f'logs {guild_id}')
    return 'None'

def get_level(guild_id, index):
    if db.isfound(f'level {index} {guild_id}'):
        return db.get(f'level {index} {guild_id}')
    return 'None'

def get_levels(guild_id):
    i = 1
    levels = ''
    for x in db.keys():
        if db.isfound(f'level {i} {guild_id}'):
            levels += db.get(f'level {i} {guild_id}') + '\n'
            i += 1
        else:
            break
    level_list = levels.splitlines()
    return level_list if len(level_list) > 1 else 'None'

def clear_setup(guild_id):
    if db.isfound(f'admin {guild_id}'):
        db.delete(f'admin {guild_id}')
    if db.isfound(f'muted {guild_id}'):
        db.delete(f'muted {guild_id}')
    if db.isfound(f'logs {guild_id}'):
        db.delete(f'logs {guild_id}')
    for x in range(100):
        if db.isfound(f'level {x} {guild_id}'):
            db.delete(f'level {x} {guild_id}')
    db.save()

def intTryParse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False
