import discum
import re
import time
import threading
import multiprocessing
import json
import datetime
import fake_useragent
import random


version = "v2.2"

with open("data\config.txt","r") as file:
    info = file.read()
    info_json = json.loads(info)
    user_token = info_json["user_token"]
    channel_id = info_json["channel_id"]
    program_pause_frequency = info_json["program_pause_frequency"]
    time_to_pause = info_json["time_to_pause"]
    random_command_frequency = info_json["random_command_frequency"]

with open("data\pokemon.txt","r",encoding="utf8") as file:
    pokemon_list_string = file.read()
    
poketwo_id = "716390085896962058"
random_commands = ["p!m s --sh","p!m s","p!i "+str(random.randint(1,1000)),"p!bal","p!profile","p!v","p!p"]# List of random phrases that can be sent

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

def start_process():
    new_process = multiprocessing.Process(target=spam)
    new_process.start()
    return new_process

def stop_process(process_to_stop):
    process_to_stop.terminate()

def print_log(string):
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("[",current_time,"]",string)

def pause_program():
    global process
    if "process" in globals():# So the program isn't paused right away (Checks if the variable "process" exists yet)
        stop_process(process)
        print_log("program paused")
        time.sleep(time_to_pause)
        process = start_process()
        print_log("program unpaused")
    threading.Timer(program_pause_frequency,pause_program).start()
    
def random_command():
    global process
    if "process" in globals():

        if process.is_alive():
            phrase = random_commands[random.randint(0,len(random_commands)-1)]

            stop_process(process)
            time.sleep(1)

            bot.sendMessage(channel_id, phrase)

            if phrase == "p!m s":
                for _ in range(0,2):
                    time.sleep(1)
                    bot.sendMessage(channel_id, "p!n")

            process = start_process()
    threading.Timer(random_command_frequency,random_command).start()


@bot.gateway.command
def on_ready(resp):
    if resp.event.ready_supplemental: #ready_supplemental is sent after ready
        user = bot.gateway.session.user
        print_log("LOGGED INTO ACCOUNT: {}#{}".format(user['username'], user['discriminator']))

@bot.gateway.command
def on_message(resp):
    global process
    
    if resp.event.message:
        m = resp.parsed.auto()

        if m["channel_id"] == channel_id:# If message is in the right channel

            if m["author"]["id"] == poketwo_id:# If poketwo sends a message

                if m["embeds"]:# If message is an embedded message
                    embed_title = m["embeds"][0]["title"]
                
                    if "A wild pokémon has appeared!" in embed_title:# If wild pokemon appears
                        stop_process(process)
                        time.sleep(1)
                        bot.sendMessage(channel_id,"p!h")
                    elif "A new wild pokémon has appeared!" in embed_title:# If new wild pokemon appeared after one fled.
                        stop_process(process)
                        time.sleep(1)
                        bot.sendMessage(channel_id,"p!h")

                else:# If message is not an embedded message
                    content = m["content"]

                    if "The pokémon is " in content:# If message is a hint
                        solution = solve(content)
                        
                        if len(solution) == 0:
                            print_log("Pokemon could not be found in the database.")

                        else:
                            for i in range(0,len(solution)):
                                time.sleep(1)
                                bot.sendMessage(channel_id,"p!c " + solution[i])
                        process = start_process()

                    elif "Congratulations" in content:
                        split = content.split(" ")
                        msg = ""
                        for i in range (2,len(split)):
                            msg += split[i] + " "
                        print_log(msg)

                    elif "Whoa there. Please tell us you're human!" in content:
                        stop_process(process)

                        if input("Captcha detected, program paused. Press enter to restart."):
                            process = start_process()

if __name__ == "__main__":
    print(f"                        Poketwo Autocatcher {version}                       ")
    print("=============================================================================")
    print("Current Settings:")
    print(f"     Pause the program every: {program_pause_frequency} seconds for {time_to_pause} seconds.")
    print(f"     Send a random command every: {random_command_frequency} seconds when the program is not paused.")
    print("=============================================================================")
    print("Log:")
    print("====")

    pause_program()
    random_command()
    process = start_process()
    bot.gateway.run(auto_reconnect=True)