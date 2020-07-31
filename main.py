import sqlite3
import schedule
import random
import discord
import time
import asyncio
from Token import token
from discord.ext import commands
from discord.utils import find

client = commands.Bot(command_prefix='*')
conn = sqlite3.connect('users.db')

c = conn.cursor()

def job():
    c.execute("UPDATE users SET DailyClaim=1 WHERE UserID=204808276397785088")
    conn.commit()
    print("updated.")

schedule.every().day.at("10:00").do(job)

#loop.run_forever()
#    schedule.run_pending()
#    time.sleep(15) # wait one minute

# When the bot loads, sets the activity to "Online" and prints to console
@client.event
async def on_ready():
    print('{0.user} is connected'.format(client))
    await client.change_presence(activity=discord.Game(name="Online"))

# On member join, adds user if the do not exist. Also dms user
@client.event
async def on_member_join(member):

    # Checking if user is in DB already
    c.execute("SELECT * FROM users WHERE UserID=?", [str(member.id)])
    user = c.fetchone()
    print(member.bot)
    if not member.bot:
        if user is None:
            c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (str(member.id), 1, 0, 0, str(member)))
            conn.commit()

        # Sending user a direct message
        dm = client.get_user(member.id)
        await dm.send("Welcome to the server!")

# When the Bot joins a server...
@client.event
async def on_guild_join(guild):

    # Find the channel titled "welcome-and-rules" and send message
    rules = find(lambda x: x.name == 'welcome-and-rules', guild.text_channels)
    if rules:
        await rules.send("PyBot is Here! Command Prefix is *")

    # Else, send it into the system channel
    else:
        if guild.system_channel is not None:
            await guild.system_channel.send("PyBot is Here! Command Prefix is *")

# Called on every message
@client.event
async def on_message(ctx):

    # Used to reply with "nice" every time "69" is in a message
    niceMsg = ctx.content.split(" ")
    containsNum = False
    for msg in niceMsg:
        if msg == "69":
            containsNum = True
        else:
            continue

    # Seeing if "69" exists
    if containsNum:
        await ctx.channel.send(client.get_user(ctx.author.id).mention + " nice.")

    # Getting the authors database entry
    c.execute("SELECT * FROM users WHERE UserID=?", [str(ctx.author.id)])
    user = c.fetchone()

    # Checking to see if message author is not the bot
    if not ctx.author.bot:

        # If user is not in the database, add them and fetch user entry again
        if user is None:
            c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (str(ctx.author.id), 1, 0, 0, str(ctx.author)))
            conn.commit()
            c.execute("SELECT * FROM users WHERE UserID=?", [str(ctx.author.id)])
            user = c.fetchone()

        # Creating a value for the message contents
        msgValue = round(pow(len(ctx.content), 0.35))
        newXP = user[2] + msgValue
        print(str(ctx.author) + " has gained " + str(msgValue) + "XP")

        # Updating users Username if it has changed
        if str(ctx.author) != user[4]:
            c.execute("UPDATE users SET Username=? WHERE UserID=?", [str(ctx.author), str(ctx.author.id)])
            conn.commit()

        # Checking to see if the user has enough xp to level up
        if newXP >= round(100 * pow(user[1], 1.2)):
            currentLvl = user[1] + 1
            gainedCredits = user[3] + round(user[1] * 5)
            c.execute("UPDATE users SET Level=?, Currency=? Where UserID=?", (currentLvl, gainedCredits, str(ctx.author.id)))
            conn.commit()
            await ctx.channel.send(client.get_user(ctx.author.id).mention + " is now level " + str(user[1] + 1) + "! You gained " + str(round(user[1] * 5)) + " credits.")
        # If user is below 100 XP, they are level 1
        elif newXP < 100:
            c.execute("UPDATE users set Level=1 WHERE UserID=?", [str(ctx.author.id)])
            conn.commit()

        # Updating XP for the user
        c.execute("UPDATE users SET XP=? WHERE UserID=?", (newXP, str(ctx.author.id)))
        conn.commit()
        await client.process_commands(ctx)

# Command to let the user check their XP
@client.command()
async def xpcheck(ctx):
    c.execute("SELECT * FROM users WHERE UserID=?", [str(ctx.author.id)])
    user = c.fetchone()
    await ctx.send(client.get_user(ctx.author.id).mention + "\nLevel: " + str(user[1]) + "\n" + str(user[2]) + "/" + str(round(100 * pow(user[1], 1.2))))

# Command to let user check their credits
@client.command()
async def creditcheck(ctx):
    c.execute("SELECT * FROM users WHERE UserID=?", [str(ctx.author.id)])
    user = c.fetchone()
    await ctx.send(client.get_user(ctx.author.id).mention + "\nCredits: " + str(user[3]))

# Gamble command to flip a coin to either receive or lose the bet
@client.command()
async def coinflip(ctx, amount: str):

    # Getting the user & picking random num
    c.execute("SELECT * FROM users WHERE UserID=?", [str(ctx.author.id)])
    user = c.fetchone()
    flippedSide = random.randrange(1, 3)

    # Making sure the amount are digits
    if amount.isdigit():
        amount = int(amount)

        # Making sure user has enough credits
        if user[3] < amount:
            await ctx.send(client.get_user(ctx.author.id).mention + " You do not have enough credits.")
        elif amount > 0:

            # If random num = 1, WIN! Add credits
            if flippedSide == 1:
                newCredit = user[3] + amount
                await ctx.send(client.get_user(ctx.author.id).mention + " WIN! You now have " + str(newCredit) + " credits.")

            # If random num = 2, LOSE! Lose credits
            else:
                newCredit = user[3] - amount
                await ctx.send(client.get_user(ctx.author.id).mention + " Loss! You now have " + str(newCredit) + " credits.")
            c.execute("UPDATE users SET Currency=? WHERE UserID=?", (newCredit, str(ctx.author.id)))

    # Error message
    else:
        await ctx.send(client.get_user(ctx.author.id).mention + " You must gamble a positive number of credits.")


# Pay other users credits with this commmand
@client.command()
async def pay(ctx, receiver: str, amount: str):

    # Checking if receiver is bot
    if receiver == str(client.user):
        await ctx.send(client.get_user(ctx.author.id).mention + " I do not want your money...")

    # Making sure amount is number
    elif amount.isdigit():
        amount = int(amount)

        # Fetching the user and and receiver
        c.execute("SELECT * FROM users WHERE UserID=?", [str(ctx.author.id)])
        user = c.fetchone()
        c.execute("SELECT * FROM users WHERE Username=?", [receiver])
        receiver = c.fetchone()

        # Making sure the receiver is not the user
        if receiver == user:
            await ctx.send(client.get_user(ctx.author.id).mention + " You may not pay yourself.")

        # Making sure receiver exists
        elif receiver is not None:

            # Checking to make sure user has enough credits
            if amount > user[3]:
                await ctx.send(client.get_user(ctx.author.id).mention + " You do not have enough credits.")

            # Subtracting amount from user and paying the receiver
            else:
                userNewCredit = user[3] - amount
                receiverNewCredit = receiver[3] + amount
                c.execute("UPDATE users SET Currency=? WHERE UserID=?", (userNewCredit, str(ctx.author.id)))
                conn.commit()
                c.execute("UPDATE users SET Currency=? WHERE UserID=?", (receiverNewCredit, receiver[0]))
                conn.commit()
                await ctx.send(client.get_user(ctx.author.id).mention + " You have successfully paid " + client.get_user(int(receiver[0])).mention + " " + str(amount) + " credits.")

        # Error message
        else:
            await ctx.send(client.get_user(ctx.author.id).mention + " You must enter a valid username. Make sure to include the # and numbers. You may not pay yourself.")
    # Error message
    else:
        await ctx.send(client.get_user(ctx.author.id).mention + " You must enter a postive integer.")


client.run(token)




