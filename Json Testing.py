import json
import discord
from discord.ext import commands

client = commands.Bot(command_prefix="*")



@client.event
async def on_ready():
    print('{0.user} is connected.'.format(client))

@client.command()
async def xp(ctx, amount: int):
    author = str(ctx.author)
    with open("./data.json") as json_file:
        dumpData = json.load(json_file)
    json_file.close()
    print(dumpData)

    for user in dumpData['users']:
        if user["Name"] == str(ctx.author):
            user["XP"] += amount

    with open("./data.json", "w") as json_file:
        json.dump(dumpData, json_file)

client.run("NzMzNDY4ODA1Njk0NzUwNzQw.XxDmKQ.SAJEVE2YO6sXsZ5up7R6TinlYt8")