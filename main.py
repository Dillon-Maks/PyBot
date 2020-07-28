import sqlite3
import random
import discord
from discord.ext import commands
from discord.utils import find

client = commands.Bot(command_prefix='*')
conn = sqlite3.connect('users.db')

c = conn.cursor()

@client.event
async def on_ready():
    print('{0.user} is connected'.format(client))
    await client.change_presence(activity=discord.Game(name="Online"))

@client.event
async def on_member_join(member):
    c.execute("SELECT * FROM users WHERE UserID=?", [str(member.id)])
    user = c.fetchone()
    if member.id != client.user.id:
        if user is None:
            c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (str(member.id), 1, 0, 0))
            conn.commit()
        dm = client.get_user(member.id)
        await dm.send("Welcome to the server!")

@client.event
async def on_guild_join(guild):
    rules = find(lambda x: x.name == 'welcome-and-rules', guild.text_channels)
    if rules:
        await rules.send("PyBot is Here! Command Prefix is *")

@client.event
async def on_message(ctx):

    niceMsg = ctx.content.split(" ")
    containsNum = False
    for msg in niceMsg:
        if msg == "69":
            containsNum = True
        else:
            continue

    if containsNum:
        await ctx.channel.send(client.get_user(ctx.author.id).mention + " nice.")

    c.execute("SELECT * FROM users WHERE UserID=?", [str(ctx.author.id)])
    user = c.fetchone()
    if ctx.author.id != client.user.id:
        if user is None:
            c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (str(ctx.author.id), 1, 0, 0))
            conn.commit()
            c.execute("SELECT * FROM users WHERE UserID=?", [str(ctx.author.id)])
            user = c.fetchone()
        msgValue = round(pow(len(ctx.content), 0.35))
        newXP = user[2] + msgValue
        print(str(ctx.author) + " has gained " + str(msgValue) + "XP")

        if newXP >= round(100 * pow(user[1], 1.2)):
            currentLvl = user[1] + 1
            gainedCredits = user[3] + round(user[1] * 5)
            c.execute("UPDATE users SET Level=?, Currency=? Where UserID=?", (currentLvl, gainedCredits, str(ctx.author.id)))
            conn.commit()
            await ctx.channel.send(client.get_user(ctx.author.id).mention + " is now level " + str(user[1] + 1) + "! You gained " + str(round(user[1] * 5)) + " credits.")
        elif newXP < 100:
            c.execute("UPDATE users set Level=1 WHERE UserID=?", [str(ctx.author.id)])
            conn.commit()

        c.execute("UPDATE users SET XP=? WHERE UserID=?", (newXP, str(ctx.author.id)))
        conn.commit()
        await client.process_commands(ctx)

@client.command()
async def xpcheck(ctx):
    c.execute("SELECT * FROM users WHERE UserID=?", [str(ctx.author.id)])
    user = c.fetchone()
    await ctx.send("Level: " + str(user[1]) + "\n" + str(user[2]) + "/" + str(round(100 * pow(user[1], 1.2))))

@client.command()
async def creditcheck(ctx):
    c.execute("SELECT * FROM users WHERE UserID=?", [str(ctx.author.id)])
    user = c.fetchone()
    await ctx.send("Credits: " + str(user[3]))

@client.command()
async def coinflip(ctx, amount: str):
    c.execute("SELECT * FROM users WHERE UserID=?", [str(ctx.author.id)])
    user = c.fetchone()
    flippedSide = random.randrange(1, 3)

    if amount.isdigit():
        amount = int(amount)
        if user[3] < amount:
            await ctx.send(client.get_user(ctx.author.id).mention + " You do not have enough credits.")
        elif amount > 0:
            if flippedSide == 1:
                newCredit = user[3] + amount
                await ctx.send(client.get_user(ctx.author.id).mention + " WIN! You now have " + str(newCredit) + " credits.")
            else:
                newCredit = user[3] - amount
                await ctx.send(client.get_user(ctx.author.id).mention + " Loss! You now have " + str(newCredit) + " credits.")
            c.execute("UPDATE users SET Currency=? WHERE UserID=?", (newCredit, str(ctx.author.id)))
    else:
        await ctx.send(client.get_user(ctx.author.id).mention + " You must gamble a positive number of credits.")


client.run('NzMzNDY4ODA1Njk0NzUwNzQw.XxDmKQ.SAJEVE2YO6sXsZ5up7R6TinlYt8')





