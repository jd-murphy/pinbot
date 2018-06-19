import random
import requests
import asyncio
import csv
import discord
from discord.ext.commands import Bot
from discord import Game


# Gym Helper bot for BCS Pokemon Go - developed with love for this awesome community by  @Aydenandjordan  6/18/2018 
TOKEN = 'NDU4NDI4NTM5MzM1ODY4NDM4.DgngZw.vqbhW9XCPARtNm2Dggh1yDYSpEQ'
BOT_PREFIX = ("!")
GYMS = {}


client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')
@client.command()
async def help():
    msg = ("!pin [gym name]    Get a location pin for the gym. Please type one word unique to the gym name OR more than one word in quotation marks, such as: \n" + \
    "\t!pin fellowship\n" + \
    "\t!pin \"sky cutter\"\n" + \
    "If multiple gyms have a common name, the bot will ask you to clarify which gym you need a pin for. Ex, searching for American will return the following:\n" + \
    "\t1.  Spanish American War\n" + \
    "\t2.  The American Mile\n" + \
    "\t3.  The American Mile: 1840\n" + \
    "\t4.  American Hackberry\n" + \
    "\t5.  Brazos Valley African American Museum\n" + \
    ":point_right:     Type $pin [number] to get your pin" )
    await client.say(msg)


@client.event
async def on_ready():
    loadGyms()
    await client.change_presence(game=Game(name="Pokemon Go, duh"))
    print("Logged in as " + client.user.name)


@client.command(pass_context=True,
                description='Get a location pin for the gym.', 
                brief='Get a location pin for the gym.')
async def pin(context, gym_name):    
    matches = []
    for key, value in GYMS.items():
        if gym_name.lower() in key.lower():
            name = key
            gym = value
            matches.append([name, gym])

    print('matches contains ' + str(len(matches)) + ' results')
    if len(matches) > 1:
        
        gymsString = ''
        i = 1
        print("matching gyms: \n")
        for k in matches:
            print(k[0] + " " + k[1])
            gymsString += (str(i) + ".  " + k[0] + "\n")
            i+=1
        
        await client.send_message(context.message.channel, 'Were you looking for one of these gyms?\n' + gymsString + "\nType **$pin [number]** to get your pin")

        def check(msg):
            return msg.content.startswith('$pin')

        message = await client.wait_for_message(author=context.message.author, check=check)
        num = message.content[len('$pin'):].strip()
        print('num: ' + str(num))
        await client.send_message(message.channel, matches[int(num)-1][0] + "\n" + matches[int(num)-1][1])
    else:        
        await client.say(matches[0][0] + "\n" + matches[0][1]) 


def loadGyms():
    with open("gyms.txt", mode="r") as infile:
        reader = csv.reader(infile)
        for row in reader:
            k = row[0]
            v = row[2]
            GYMS[k] = v
    print('Testing loaded gyms...')
    print(GYMS['Dixie Chicken'])


@client.event
async def on_message(message):

    if 'bad bot' in message.content.lower():
        await client.send_message(message.channel, ":sweat:")
    elif 'good bot' in message.content.lower():
        await client.send_message(message.channel, ":heart_eyes::heart_eyes::heart_eyes:")
    
    await client.process_commands(message)
        

# async def list_servers():
#     await client.wait_until_ready()
#     while not client.is_closed:
#         print("Current servers:")
#         for server in client.servers:
#             print(server.name)
#         await asyncio.sleep(6)

# client.loop.create_task(list_servers())

client.run(TOKEN)