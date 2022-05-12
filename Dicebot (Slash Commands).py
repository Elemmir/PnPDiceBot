import discord
import re
import random
import os
import datetime
import typing

from discord import Client, Intents, Embed, Guild, Member
from discord.ext.commands import Bot
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_components import ComponentContext
from datetime import datetime

intents = discord.Intents.all()
client = Bot(command_prefix = "/", intents=intents)
slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    #Initialise the Bot
    print(str(datetime.now()) + ' - We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game('Prowlers & Paragons: Ultimate Edition'))


@slash.slash(name="Dice", description="Generate a Dice roll using the Xd format")
async def dice(ctx:SlashContext, roll:str, threshold:int=None):
    
    #Matches Discord Message for Xd Format
    regexmatch = re.findall("\d+[dD]\\b", roll)

    #Detects Number of Rolls in Xd Format
    dicenumberlength = len(regexmatch)
    dicenumberindex = 0

    #Proceeds if there is a Match
    if regexmatch:

        #Outputs Roll into Console
        print(str(datetime.now()) + " - Dice Command: " + roll)
        
        while dicenumberindex !=dicenumberlength:

            #Detected Roll
            detectedroll = regexmatch[dicenumberindex]
            
            #Strips the d to find number of Dice
            dicenumber = re.sub('[dD]', "", regexmatch[dicenumberindex])

            #Converting List to String
            diceindex = str(dicenumber)

            #Converting String to Number
            diceindex = int(diceindex)

            #Reset Results
            successes = 0
            diceresults = ""

            if diceindex > 100:
                dicesummary = discord.Embed(title="Command Error", description=('Dicebot only supports up to 100 dice.'), color=0xFF0000) #Red
                await ctx.send(embed=dicesummary)
                dicenumberindex = dicenumberindex +1
            else:
                while diceindex != 0:
            
                    #Dice Parameters
                    dicemin = 1
                    dicemax = 6

                    #Random Dice Roll
                    randomroll = random.randint(dicemin, dicemax)

                    #Dice Results
                    diceresult = str(randomroll)

                    if randomroll == 1:
                        diceindex = diceindex - 1
                        diceresults = diceresults + str(diceresult + ", ")

                    if randomroll == 2:
                        successes = successes + 1
                        diceindex = diceindex - 1
                        diceresults = diceresults + str("**" + diceresult + "**, ")

                    if randomroll == 3:
                        diceindex = diceindex - 1
                        diceresults = diceresults + str(diceresult + ", ")

                    if randomroll == 4:
                        successes = successes + 1
                        diceindex = diceindex - 1
                        diceresults = diceresults + str("**" + diceresult + "**, ")

                    if randomroll == 5:
                        diceindex = diceindex - 1
                        diceresults = diceresults + str(diceresult + ", ")

                    if randomroll == 6:
                        successes = successes + 2
                        diceindex = diceindex - 1
                        diceresults = diceresults + str("**" + diceresult + "**, ")

                if threshold == None:
                    #Message Output
                    dicesummary = discord.Embed(title=(str(successes) + str(' Successes')), description=(''), color=0x000000)
                    dicesummary.add_field(name=str(detectedroll + " Roll Summary:"), value=diceresults.rstrip(", "), inline=False)
                    dicesummary.add_field(name="Roll: ", value=">>> " + roll, inline=False)
                    await ctx.send(embed=dicesummary)

                    dicenumberindex = dicenumberindex +1
                else:

                    netsuccesses = successes - int(threshold)

                    #Colours
                    if netsuccesses > 0:
                        color = 0x00FF00 #Green
                    else:
                        color = 0xFF0000 #Red

                    #Message Output
                    dicesummary = discord.Embed(title=(str(netsuccesses) + str(' Net Successes')), description=(''), color=color)
                    dicesummary.add_field(name=str(detectedroll + " Roll Summary:"), value=diceresults.rstrip(", "), inline=False)
                    dicesummary.add_field(name=str("Threshold:"), value=threshold, inline=False)
                    dicesummary.add_field(name="Roll: ", value=">>> " + roll, inline=False)
                    await ctx.send(embed=dicesummary)

                    dicenumberindex = dicenumberindex +1
    else:
        #Message Output if incorrect format
        diceerror = discord.Embed(title=("Command Error"), description=('Please use the Xd Format when using the `roll` field.'), color=0xFF0000)
        await ctx.send(embed=diceerror)

    return
            
#Dicebot
client.run('INSERT API KEY HERE')