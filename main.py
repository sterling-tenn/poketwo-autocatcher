import discum
import re
import time
import threading
import multiprocessing
import json


version = "v2.0"

with open("data\info.txt","r") as file:
    info = file.read()
    info_json = json.loads(info)
    user_token = info_json["user_token"]
    channel_id = info_json["channel_id"]

with open("data\pokemon.txt","r",encoding="utf8") as file:
    pokemon_list_string = file.read()
    
poketwo_id = "716390085896962058"

bot = discum.Client(token=user_token, log={"console":False, "file":False})


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

def start_process():
    new_process = multiprocessing.Process(target=spam)
    new_process.start()
    return new_process

def stop_process(process_to_stop):
    process_to_stop.terminate()


@bot.gateway.command
def helloworld(resp):
    global process
    
    if resp.event.ready_supplemental: #ready_supplemental is sent after ready
        user = bot.gateway.session.user
        print("Logged in as {}#{}".format(user['username'], user['discriminator']))
        process = start_process()
    if resp.event.message:
        m = resp.parsed.auto()

        if m["channel_id"] == channel_id:# If message is in the right channel

            if m["author"]["id"] == poketwo_id:# If poketwo sends a message

                if m["embeds"]:# If message is an embedded message
                    embed_title = m["embeds"][0]["title"]
                
                    if "A wild pokémon has appeared!" in embed_title:# If wild pokemon appears
                        stop_process(process)
                        time.sleep(2)
                        bot.sendMessage(channel_id,"p!h")
                    elif "A new wild pokémon has appeared!" in embed_title:# If new wild pokemon appeared after one fled.
                        stop_process(process)
                        time.sleep(2)
                        bot.sendMessage(channel_id,"p!h")

                else:# If message is not an embedded message
                    content = m["content"]

                    if "The pokémon is " in content:# If message is a hint
                        solution = solve(content)
                        
                        if len(solution) == 0:
                            print("Pokemon could not be found in the database.")

                        else:
                            for i in range(0,len(solution)):
                                time.sleep(2)
                                bot.sendMessage(channel_id,"p!c " + solution[i])
                        process = start_process()

if __name__ == "__main__":
    bot.gateway.run(auto_reconnect=True)