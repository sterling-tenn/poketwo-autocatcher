import re, asyncio, json, random, string
from discord.ext import commands
from discord.ext import tasks

version = 'v2.7.1'

with open('data/config.json','r') as file:
    info = json.loads(file.read())
    user_token = info['user_token']
    channel_id = info['channel_id']

with open('data/pokemon.txt', 'r', encoding='utf8') as file:
    pokemon_list = file.read()
with open('data/legendary.txt','r') as file:
    legendary_list = file.read()
with open('data/mythical.txt','r') as file:
    mythical_list = file.read()
with open('data/level.txt','r') as file:
    to_level = file.readline()

num_pokemon = 0
shiny = 0
legendary = 0
mythical = 0

poketwo = 716390085896962058
bot = commands.Bot(command_prefix="->", self_bot=True)
intervals = [1.5, 1.6, 1.7, 1.8, 1.9]

def solve(message):
    hint = []
    for i in range(15,len(message) - 1):
        if message[i] != '\\':
            hint.append(message[i])
    hint_string = ''
    for i in hint:
        hint_string += i
    hint_replaced = hint_string.replace('_', '.')
    solution = re.findall('^'+hint_replaced+'$', pokemon_list, re.MULTILINE)
    return solution

@tasks.loop(seconds=random.choice(intervals))
async def spam():
    channel = bot.get_channel(int(channel_id))
    await channel.send(f'{random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=random.choice([7, 8, 9, 10]))}')

@spam.before_loop
async def before_spam():
    await bot.wait_until_ready()

spam.start()

@bot.event
async def on_ready():
    print(f'Logged into account: {bot.user.name}')

@bot.event
async def on_message(message):
    channel = bot.get_channel(int(channel_id))
    if message.channel.id == int(channel_id):
        if message.author.id == poketwo:
            if message.embeds:
                embed_title = message.embeds[0].title
                if 'wild pokémon has appeared!' in embed_title:
                    spam.cancel()
                    await asyncio.sleep(1.5)
                    await channel.send('p!h')
                elif "Congratulations" in embed_title:
                    embed_content = message.embeds[0].description
                    if 'now level' in embed_content:
                        spam.cancel()
                        split = embed_content.split(' ')
                        a = embed_content.count(' ')
                        level = int(split[a].replace('!', ''))
                        if level == 100:
                            await channel.send(f"p!s {to_level}")
                            with open('data/level.txt', 'r') as fi:
                                data = fi.read().splitlines(True)
                            with open('data/level.txt', 'w') as fo:
                                fo.writelines(data[1:])
                            spam.start()
                        else:
                            spam.start()

            else:
                content = message.content
                if 'The pokémon is ' in content:
                    if not len(solve(content)):
                        print('Pokemon not found.')
                    else:
                        for i in solve(content):
                            await asyncio.sleep(1.5)
                            await channel.send(f'p!c {i}')
                    spam.start()

                elif 'Congratulations' in content:
                    global shiny
                    global legendary
                    global num_pokemon
                    global mythical
                    num_pokemon += 1
                    split = content.split(' ')
                    pokemon = split[7].replace('!','')
                    if 'seem unusual...' in content:
                        shiny += 1
                        print(f'Shiny Pokémon caught! Pokémon: {pokemon}')
                        print(f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}')
                    elif re.findall('^'+pokemon+'$', legendary_list, re.MULTILINE):
                        legendary += 1
                        print(f'Legendary Pokémon caught! Pokémon: {pokemon}')
                        print(f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}')
                    elif re.findall('^'+pokemon+'$', mythical_list, re.MULTILINE):
                        mythical += 1
                        print(f'Mythical Pokémon caught! Pokémon: {pokemon}')
                        print(f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}')
                    else:
                        print(f'Total Pokémon Caught: {num_pokemon}')

                elif 'human' in content:
                    spam.cancel()
                    print('Captcha detected; autocatcher paused. Press enter to restart, after solving captcha manually.')
                    input()
                    await channel.send('p!h')
    if not message.author.bot:
        await bot.process_commands(message)

print(f'Pokétwo Autocatcher {version}\nA completely free and open-source Pokétwo autocatcher\nEvent Log:')
bot.run(f"{user_token}")