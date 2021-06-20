import discum
import re
import time
import threading
import multiprocessing
import json
import datetime
import fake_useragent
import random
import ctypes


version = "v2.4.1"

with open("data\config.txt","r") as file:
    info = json.loads(file.read())
    user_token = info["user_token"]
    channel_id = info["channel_id"]

with open("data\pokemon.txt","r",encoding="utf8") as file:
    pokemon_list_string = file.read()
    
with open("data\legendaries.txt","r") as file:
    legendary_list = file.read()

with open("data\mythics.txt","r") as file:
    mythic_list = file.read()
    
poketwo_id = "716390085896962058"

num_pokemon = 0
num_shinies = 0
num_legendaries = 0
num_mythics = 0
num_fled = 0

user_agent = fake_useragent.UserAgent()

bot = discum.Client(token=user_token, log=False, user_agent=user_agent.chrome)


def solve(message):
    hint = []

    for i in range(15,len(message) - 1):
        if message[i] != "\\":
            hint.append(message[i])

    hint_string = ""
    for i in hint:
        hint_string += i
        
    hint_replaced = hint_string.replace("_",".")
    solution = re.findall('^'+hint_replaced+'$',pokemon_list_string, re.MULTILINE)
    return solution

def spam():
    while True:
        bot.sendMessage(channel_id, version)
        time.sleep(2)

def start_spam_process():
    new_process = multiprocessing.Process(target=spam)
    new_process.start()
    return new_process

def stop_process(process_to_stop):
    process_to_stop.terminate()

def print_log(string):
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("[",current_time,"]",string)

def update_title():
    ctypes.windll.kernel32.SetConsoleTitleW(f"Pokemon Caught: {num_pokemon} || Shinies: {num_shinies} || Legendaries: {num_legendaries} || Mythics: {num_mythics} || Fled: {num_fled}")


@bot.gateway.command
def on_ready(resp):
    if resp.event.ready_supplemental:
        user = bot.gateway.session.user
        print_log("LOGGED INTO ACCOUNT: {}#{}".format(user['username'], user['discriminator']))

@bot.gateway.command
def on_message(resp):
    global spam_process

    if resp.event.message:
        m = resp.parsed.auto()

        if m["channel_id"] == channel_id:# If message is in the right channel

            if m["author"]["id"] == poketwo_id:# If poketwo sends a message

                if m["embeds"]:# If message is an embedded message
                    embed_title = m["embeds"][0]["title"]
                
                    if "A wild pokémon has appeared!" in embed_title:# If wild pokemon appears
                        stop_process(spam_process)
                        time.sleep(2)
                        bot.sendMessage(channel_id,"p!h")

                    elif "A new wild pokémon has appeared!" in embed_title:# If new wild pokemon appeared after one fled.
                        global num_fled
                        num_fled += 1
                        update_title()

                        print_log("A pokemon has fled.")

                        stop_process(spam_process)
                        time.sleep(2)
                        bot.sendMessage(channel_id,"p!h")

                else:# If message is not an embedded message
                    content = m["content"]

                    if "The pokémon is " in content:# If message is a hint
                        solution = solve(content)
                        
                        if len(solution) == 0:
                            print_log("Pokemon could not be found in the database.")

                        else:
                            for i in range(0,len(solution)):
                                time.sleep(2)
                                bot.sendMessage(channel_id,"p!c " + solution[i])
                        spam_process = start_spam_process()

                    elif "Congratulations" in content:# If pokemon is caught
                        global num_pokemon
                        num_pokemon += 1

                        if "These colors seem unusual..." in content:# If pokemon is shiny
                            global num_shinies
                            num_shinies += 1

                        split = content.split(" ")
                        msg = ""
                        for i in range (2,len(split)):
                            msg += split[i] + " "
                        print_log(msg)

                        pokemon = split[7].replace("!","")

                        if re.findall('^'+pokemon+'$',legendary_list,re.MULTILINE):# If pokemon is legendary
                            global num_legendaries
                            num_legendaries += 1

                        if re.findall('^'+pokemon+'$',mythic_list,re.MULTILINE):# If pokemon is mythic
                            global num_mythics
                            num_mythics += 1
                        
                        update_title()

                    elif "Whoa there. Please tell us you're human!" in content:# If captcha appears
                        stop_process(spam_process)
                        
                        print_log("Captcha detected, program paused. Press enter to restart.")
                        input()
                        bot.sendMessage(channel_id,"p!h")

if __name__ == "__main__":
    update_title()
    print(f"                        Poketwo Autocatcher {version}                       ")
    print("=============================================================================")
    print("Log:")
    print("====")

    spam_process = start_spam_process()
    bot.gateway.run(auto_reconnect=True)