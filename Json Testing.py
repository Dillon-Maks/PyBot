import json
import discord
from discord.ext import commands

client = commands.Bot(command_prefix="*")



@client.event
async def on_ready():
    print('{0.user} is connected.'.format(client))

@client.command()
async def xpcheck(ctx):
    with open("./data.json") as json_file:
        dumpData = json.load(json_file)
    json_file.close()

    usercount = 0
    for user in dumpData['users']:
        if user["Name"] == str(ctx.author):
            await ctx.send(str(ctx.author) + " has " + str(user["XP"]) + "XP")
        else:
            usercount += 1
            continue
    if usercount == len(dumpData["users"]):
        dumpData['users'].append({
            "Name": str(ctx.author),
            "XP": 0
        })
        await ctx.send(str(ctx.author) + " has " + str(user["XP"]) + "XP")

    with open("./data.json", "w") as json_file:
        json.dump(dumpData, json_file)
    json_file.close()

@client.event
async def on_message(message):
    with open("./data.json") as json_file:
        dumpData = json.load(json_file)
    json_file.close()

    # Finding the User & Updating Values
    usercount = 0
    for user in dumpData['users']:
        if user["Name"] == str(message.author):
            user["XP"] += 5
            break
        else:
            usercount += 1
            continue
    # Adding new users to the JSON if they do not exist
    if usercount == len(dumpData['users']):
        dumpData['users'].append({
            "Name": str(message.author),
            "XP": 5
        })

    # Writing to the file
    with open("./data.json", "w") as json_file:
        json.dump(dumpData, json_file)

    await client.process_commands(message)


client.run("NzMzNDY4ODA1Njk0NzUwNzQw.XxDmKQ.SAJEVE2YO6sXsZ5up7R6TinlYt8")