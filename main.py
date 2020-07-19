import discord
from discord.ext import commands, tasks
import random

client = commands.Bot(command_prefix='*')

@client.event
async def on_ready():
    print('{0.user} is connected'.format(client))

@client.command()
async def ping(ctx):
    await ctx.send("Pong! " + str(round(client.latency*1000)) + "ms")

@client.command(aliases=['8ball', 'eightball'])
async def _8ball(ctx, *, question):
    responses = ['Yes.',
                 'Maybe.',
                 'Ask again.',
                 'No.']

    await ctx.send("Question: " + question + '\nAnswer: ' + random.choice(responses))
    
# MATH

@client.command()
async def math(ctx):
    await ctx.send()

@client.command()
async def add(ctx, num1, num2):
    await ctx.send(str(int(num1) + int(num2)))

@client.command()
async def sub(ctx, num1, num2):
    await ctx.send(str(int(num1) - int(num2)))

@client.command(aliases=["multiply", "times"])
async def mult(ctx, num1, num2):
    await ctx.send(str(int(num1)*int(num2)))

@client.command()
async def roll(ctx, num):
    rollednum = random.randrange(1, int(num))
    await ctx.send("You rolled " + str(rollednum))

client.run('NzMzNDY4ODA1Njk0NzUwNzQw.XxDmKQ.SAJEVE2YO6sXsZ5up7R6TinlYt8')

