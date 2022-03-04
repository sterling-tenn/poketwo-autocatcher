import sys, subprocess

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

with open("data/config.json", "a") as file:
    install('discord.py-self')
    print("\nInput your discord authorization token:")
    auth_token = input()
    file.write("{\n")
    file.write(f'   "user_token" : "{auth_token}",\n')
    print("Now, input the Channel ID of the channel for spamming:")
    spam_id = input()
    file.write(f'   "spam_id" : "{spam_id}",\n')
    print("Now, input the Channel ID of the channel for catching:")
    catch_id = input()
    file.write(f'   "catch_id" : "{catch_id}",\n')
    file.write("}")
    exec(open('main.py').read())