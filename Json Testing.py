import json
import discord
from discord.ext import commands

client = commands.Bot(command_prefix="*")



@client.event
async def on_ready():
    print('{0.user} is connected.'.format(client))

@client.command()
async def xp(ctx, amount):
    author = str(ctx.author)
    dumpData = {}
    dumpData['users'] = []
    dumpData['users'].append({
        "Name": author,
        "XP": amount
    })

    with open("./data.json", "w") as jsonSave:
        json.dump(dumpData, jsonSave)




client.run("NzMzNDY4ODA1Njk0NzUwNzQw.XxDmKQ.SAJEVE2YO6sXsZ5up7R6TinlYt8")