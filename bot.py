import random
import requests
import asyncio
import csv
import discord
from discord.ext.commands import Bot
from discord import Game
from os import environ
import uctwilio 
import pyrebase_worker


# Gym Helper bot for BCS Pokemon Go - developed with love for this awesome community by  @Aydenandjordan  6/18/2018 
TOKEN = environ['TOKEN']
BOT_PREFIX = ("$", "+")
GYMS = {}

client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')
@client.command()
async def help():
    msg = ("**$pin [gym name]**    Get a location pin for the gym. Please type one word unique to the gym name OR more than one word in quotation marks, such as: \n" + \
    "\t**$pin fellowship**\n" + \
    "\t**$pin \"sky cutter\"**\n" + \
    "If multiple gyms have similar names, the bot will ask you to clarify which gym you need a pin for. For example, searching **$pin American** will return the following:\n" + \
    "\t1.  Spanish American War\n" + \
    "\t2.  The American Mile\n" + \
    "\t3.  The American Mile: 1840\n" + \
    "\t4.  American Hackberry\n" + \
    "\t5.  Brazos Valley African American Museum\n" + \
    "To select an option from the list, just type **show [number]** to choose the correct gym.\n\n" + \
    ":point_right:     Type **$pin [gym name]** to get started!" )
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
    
    if gym_name.lower() == "ai":
        gym_name = "Animal Industries"
    if gym_name.lower() == "etb":
        gym_name = "Emerging Technologies"
    if gym_name.lower() == "wa":
        gym_name = "Wilderness Awakened"

    matches = []
    for key, value in GYMS.items():
        if gym_name.lower() in key.lower():
            name = key
            gym = value
            matches.append([name, gym])

    # print('matches contains ' + str(len(matches)) + ' results')
    if len(matches) > 1:
        
        gymsString = ''
        i = 1
        print("matching gyms: \n")
        for k in matches:
            print(k[0] + " " + k[1])
            gymsString += (str(i) + ".  " + k[0] + "\n")
            i+=1
        
        await client.send_message(context.message.channel, 'Were you looking for one of these gyms?\n' + gymsString + "\nType **show [number]** to get your pin")

        def check(msg):
            return msg.content.lower().startswith('show')

        message = await client.wait_for_message(author=context.message.author, check=check)
        num = message.content[len('show'):].strip()
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


@client.command(pass_context=True)
async def twilioCheck(context): 
    if context.message.author.id == environ['adminID']:
        print("Running twilio check.")
        result = uctwilio.check()
        member = discord.utils.get(context.message.server.members, id=environ['adminID'])
        await client.send_message(member, result)
        



@client.command(pass_context=True)
async def pyrebasePush(context, name, phone, bcspogo, aqua):
    if context.message.author.id == environ['adminID']:
        pyrebase_worker.push(name, phone, bcspogo, aqua)


@client.command(pass_context=True)
async def pyrebaseGet(context):
    if context.message.author.id == environ['adminID']:
        data = pyrebase_worker.getData()
        names = ""
        for user in data.each():
            userDict = user.val()
            userInfo = ""
            userInfo += ("``` " + userDict["name"] + " \n " + userDict["phone"] + " \n ")
            if userDict["BCS Pokemon Go"] == 'true':
                userInfo += "[3TS]"
            if userDict["Team Aqua's Hideout"] == 'true':
                userInfo += "[Aqua]"
            userInfo += " ```"
            names += userInfo
        await client.send_message(context.message.author, ' Here is the list of users signed up for twilio hundy notifications ->\n' + names)


@client.command(pass_context=True)
async def pyrebaseGetByServer(context, server):
    if context.message.author.id == environ['adminID']:
        pyrebase_worker.getByServer(server)    


@client.command(pass_context=True)
async def pyrebaseRemove(context, name):
    if context.message.author.id == environ['adminID']:
        pyrebase_worker.remove(name)


@client.command(pass_context=True)
async def logMe(context, msg):
    pyrebase_worker.log(msg)



@client.command(pass_context=True)
async def manage(context):
    # if context.message.author.id == environ['adminID']:
    #     data = pyrebase_worker.getLogs()
    #     with open('log.txt', 'w') as f:
    #         for line in data.val().items():
    #             f.write(str(line))
    
       
        embed=discord.Embed(title="Dashboard", url="https://node-bot-dashboard.herokuapp.com/dashboard")
        embed.set_author(name="Bot Manager")
        await client.send_message(context.message.author, embed=embed)






@client.event
async def on_message(message):

    # Role: Hundy Chaser   ID: 403060533017837569          
    if '<@&403060533017837569>' in message.content:
        print('@HundyChaser mention! (3ts)')
        status = uctwilio.report3TS(message)
        pyrebase_worker.log(status)
        print('status from : uctwilio.report3TS()' + status)
        member = discord.utils.get(message.server.members, id=environ['adminID'])
        await client.send_message(member, status)

    # Role: HundyHunters   ID: 398995832978014210          
    if '<@&398995832978014210>' in message.content:
        print('@HundyHunters mention! (aqua)')
        status = uctwilio.reportAqua(message)
        pyrebase_worker.log(status)
        print('status from : uctwilio.reportAqua()' + status)
        member = discord.utils.get(message.server.members, id=environ['adminID'])
        await client.send_message(member, status)

   

    if client.user in message.mentions:
        if 'we rockin\' and rollin\'' in message.content.lower() or 'we rockin and rollin' in message.content.lower():
            await client.send_message(message.channel, "We're rockin\' and rollin\', baby")
        if 'thanks' in message.content.lower() or 'thank you' in message.content.lower():
            await client.send_message(message.channel, "Anything for you kid. :ok_hand:")
        if 'your the best' in message.content.lower() or 'you\'re the best' in message.content.lower() \
            or 'youre the best' in message.content.lower() or 'youre the best,' in message.content.lower() \
            or 'your the best,' in message.content.lower() or 'you\'re the best,' in message.content.lower():
            await client.send_message(message.channel, "I know. :stuck_out_tongue:")

    if 'bad bot' in message.content.lower():
        await client.send_message(message.channel, ":sweat:")
    elif 'good bot' in message.content.lower():
        await client.send_message(message.channel, ":heart_eyes::heart_eyes::heart_eyes:")
    
    await client.process_commands(message)
        

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("\n\n\n\nCURRENT SERVERS:")
        for server in client.servers:
            print(server.name)
            for role in server.roles:
                print('Role: ' + role.name + "   ID: " + role.id)
        await asyncio.sleep(600)


client.loop.create_task(list_servers())
client.run(TOKEN)