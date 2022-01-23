import discum, re, time, multiprocessing, json, datetime, random

version = 'v2.6'

with open('data/config.json','r') as file:
    info = json.loads(file.read())
    user_token = info['user_token']
    channel = info['channel_id']

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

poketwo = '716390085896962058'
bot = discum.Client(token=user_token, log=False)

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

def spam():
  while True:
    bot.sendMessage(channel, random.randint(1, 100000000000))
    time.sleep(2)

def _spam():
    new_process = multiprocessing.Process(target=spam)
    new_process.start()
    return new_process

def stop(process):
    process.terminate()

def log(str):
    now = datetime.datetime.now()
    current_time = now.strftime('%H:%M:%S')
    print(f'[{current_time}]', str)

@bot.gateway.command
def on_ready(resp):
    if resp.event.ready_supplemental:
        user = bot.gateway.session.user
        log(f'Logged into account: {user["username"]}#{user["discriminator"]}')

@bot.gateway.command
def on_message(resp):
    global spamming

    if resp.event.message:
        m = resp.parsed.auto()
        if m['channel_id'] == channel:
            if m['author']['id'] == poketwo:
                if m['embeds']:
                    embed_title = m['embeds'][0]['title']
                    if 'wild pokémon has appeared!' in embed_title:
                        stop(spamming)
                        time.sleep(2)
                        bot.sendMessage(channel, 'p!h')
                    elif "Congratulations" in embed_title:
                        embed_content = m['embeds'][0]['description']
                        if 'now level' in embed_content:
                            stop(spamming)
                            split = embed_content.split(' ')
                            a = embed_content.count(' ')
                            level = int(split[a].replace('!', ''))
                            if level == 100:
                                bot.sendMessage(channel, f"p!s {to_level}")
                                with open('data/level.txt', 'r') as fi:
                                    data = fi.read().splitlines(True)
                                with open('data/level.txt', 'w') as fo:
                                    fo.writelines(data[1:])
                                spamming = _spam()
                            else:
                                spamming = _spam()
                else:
                    content = m['content']
                    if 'The pokémon is ' in content:
                        if len(solve(content)) == 0:
                            log('Pokemon not found.')
                        else:
                            for i in solve(content):
                                time.sleep(2)
                                bot.sendMessage(channel, f'p!c {i}')
                        spamming = _spam()

                    elif 'Congratulations' in content:
                        global shiny
                        global legendary
                        global num_pokemon
                        global mythical
                        num_pokemon += 1
                        split = content.split(' ')
                        pokemon = split[7].replace('!','')
                        if 'These colors seem unusual...' in content:
                            shiny += 1
                            log(f'A shiny Pokémon was caught! Pokémon: {pokemon}')
                            log(f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}')
                        elif re.findall('^'+pokemon+'$', legendary_list, re.MULTILINE):
                            legendary += 1
                            log(f'A legendary Pokémon was caught! Pokémon: {pokemon}')
                            log(f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}')
                        elif re.findall('^'+pokemon+'$', mythical_list, re.MULTILINE):
                            mythical += 1
                            log(f'A mythical Pokémon was caught! Pokémon: {pokemon}')
                            log(f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}')
                        else:
                            print(f'Total Pokémon Caught: {num_pokemon}')

                    elif 'human' in content:
                        stop(spamming)
                        log('Captcha detected; autocatcher paused. Press enter to restart.')
                        input()
                        bot.sendMessage(channel, 'p!h')

if __name__ == '__main__':
    print(f'Pokétwo Autocatcher {version}\nA FOSS Pokétwo autocatcher\nEvent Log:')
    spamming = _spam()
    bot.gateway.run(auto_reconnect=True)