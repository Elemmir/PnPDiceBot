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


@slash.slash(name="Help", description="Generate a list of Dicebot features")
async def help(ctx:SlashContext):
    
    helpembed = discord.Embed(title="`/dice` Command Features", description=(""), color=0x000000)
    helpembed.add_field(name="`roll` Field", value="**Required** - Enter a dice roll such as ***12d*** here. `roll` also supports any additional text such as ***12d Might Roll Against the Enemy***.", inline=False)
    helpembed.add_field(name="`threshold` Field", value="***Optional*** - Enter any number as the `threshold` for your roll. Dicebot will display ***Net Successes*** which is the total number of successes over or under the `threshold`.", inline=False)
    helpembed.add_field(name="Exploding Dice", value="***Optional*** - Enter a ***!*** at the end of a dice roll using the `roll` field, such as ***12d!*** will cause 6's to explode.", inline=False)
    helpembed.add_field(name="🔄 Emoji", value="***Optional*** - Clicking the 🔄 emoji will re-roll the dice for this command.", inline=False)
    helpembed.add_field(name="💥 Emoji", value="***Optional*** - Clicking the 💥 emoji will cause the dice for this command to explode.", inline=False)

    await ctx.send(embed=helpembed)

    print(str(datetime.now()) + " - Help Command")

    return


@slash.slash(name="Dice", description="Generate a dice roll using the Xd format")
async def dice(ctx:SlashContext, roll:str, threshold:int=None):

    await ctx.defer()
    
    #Matches Discord Message for Xd Format
    dicematch = re.findall("\d+[dD]\\b!?", roll)

    #Proceeds if there is a Match
    if dicematch:

        #Outputs Roll into Console
        print(str(datetime.now()) + " - Dice Command: " + roll)

        #Detected Roll
        detectedroll = dicematch[0]

        #Detected Explode
        detectedexplode = re.findall("\d+[dD]!", dicematch[0])
        if detectedexplode:
            explode = 1
        else:
            explode = 0
            
        #Strips the d to find number of Dice
        dicenumber = re.sub('[dD]!?', "", dicematch[0])

        #Converting List to String
        diceindex = str(dicenumber)

        #Converting String to Number
        diceindex = int(diceindex)

        #Reset Results
        successes = 0
        diceresults = ""
        explodeddice = 0

        if diceindex > 100:
            dicesummary = discord.Embed(title="Command Error", description=('Dicebot only supports up to 100 dice.'), color=0xFF0000) #Red
            await ctx.send(embed=dicesummary)
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
                    if explode == 1:
                        diceindex = diceindex + 1
                        explodeddice = explodeddice + 1

            if threshold == None:

                #Colours
                if explode == 0:
                    color = 0x000000
                else:
                    color = 0xFFA500

                #Message Output
                dicesummary = discord.Embed(title=(str(successes) + str(' Successes')), description=(''), color=color)
                dicesummary.add_field(name="Roll: ", value=">>> " + roll, inline=False)
                dicesummary.add_field(name=str(detectedroll + " Roll Summary:"), value=diceresults.rstrip(", "), inline=False)
                #if explode == 1:
                    #dicesummary.add_field(name=str("Exploded Dice: "),value = str(explodeddice), inline=False)
                await ctx.send(embed=dicesummary)
                await ctx.message.add_reaction("🔄")
                if explode == 0:
                    await ctx.message.add_reaction("💥")

            else:

                netsuccesses = successes - int(threshold)

                #Colours
                if netsuccesses > 0:
                    color = 0x00FF00 #Green
                else:
                    color = 0xFF0000 #Red

                #Message Output
                dicesummary = discord.Embed(title=(str(netsuccesses) + str(' Net Successes')), description=(''), color=color)
                dicesummary.add_field(name="Roll: ", value=">>> " + roll, inline=False)
                dicesummary.add_field(name=str(detectedroll + " Roll Summary:"), value=diceresults.rstrip(", "), inline=False)
                #if explode == 1:
                    #dicesummary.add_field(name=str("Exploded Dice: "),value = str(explodeddice), inline=False)
                dicesummary.add_field(name=str("Threshold:"), value=threshold, inline=False)
                await ctx.send(embed=dicesummary)
                await ctx.message.add_reaction("🔄")
                if explode == 0:
                    await ctx.message.add_reaction("💥")

    else:
        #Message Output if incorrect format
        diceerror = discord.Embed(title=("Command Error"), description=('Please use the Xd Format when using the `roll` field.'), color=0xFF0000)
        await ctx.send(embed=diceerror)

    return


#React Emojis
@client.event
async def on_raw_reaction_add(payload):

    #Checks the sender is not the Bot
    if payload.user_id == 971458596967690360:
            return

    #Re-Roll Emoji
    if payload.emoji.name == "🔄":

        #Gets Message Payload
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        embed = message.embeds[0]
        embed1 = embed.fields[0]
        embed1 = str(embed1)

        #Detects More Than 1 Embed Fields
        if len(embed.fields) > 1:
            embed2 = embed.fields[1]
            embed2 = str(embed2)

        #Detects More Than 2 Embed Fields
        if len(embed.fields) > 2:
            embed3 = embed.fields[2]
            thresholdmatch = re.findall("Threshold", str(embed3))
        else:
            thresholdmatch = 0

        #Regex Matching
        dicematch = re.findall("\d+[dD]\\b!?", embed1)
        explosionmatch = re.findall("Exploding Summary:", embed1)
        
        #Detected Roll in lieu of Slash Command Parameter
        roll = re.sub("(EmbedProxy\(name='Roll:', value='>>> )", "", embed1)
        roll = re.sub("(', inline=False\))", "", str(roll))

        #Detected Threshold in lieu of Slash Command Parameter
        if thresholdmatch:
            threshold = re.sub("(EmbedProxy\(name='Threshold:', value=')", "", str(embed3))
            threshold = re.sub("(', inline=False\))", "", str(threshold))

        #Detected Explosion via Emoji
        if explosionmatch:
            explosionroll = re.sub("(EmbedProxy\(name=')", "", embed1)
            explosionroll = re.sub("([dD]!? Exploding Summary:', value='[*123456, ]*', inline=False\))", "", str(explosionroll))
            explosionroll = explosionroll + "d!"

            #Outputs Roll into Console
            print(str(datetime.now()) + " - Exploding Command")

            #Force Explode
            explode = 1

            #Strips the d to find number of Dice
            dicenumber = re.sub('[dD]!?', "", explosionroll)

            #Converting List to String
            diceindex = dicenumber

            #Converting String to Number
            diceindex = int(diceindex)

            #Reset Results
            successes = 0
            diceresults = ""
            explodeddice = 0

            if diceindex > 100:
                dicesummary = discord.Embed(title="Command Error", description=('Dicebot only supports up to 100 dice.'), color=0xFF0000) #Red
                await ctx.send(embed=dicesummary)
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
                        diceresults = diceresults + str("**" + diceresult + "**, ")
                        explodeddice = explodeddice + 1

                    
                #Message Output
                dicesummary = discord.Embed(title=(str(successes) + str(' Successes')), description=(''), color=0xFFA500) #Orange
                dicesummary.add_field(name=str(explosionroll + " Exploding Dice Summary:"), value=diceresults.rstrip(", "), inline=False)
                #dicesummary.add_field(name=str("Exploded Dice: "),value = str(explodeddice), inline=False)
                messageembed = await message.channel.send(embed=dicesummary)
                await messageembed.add_reaction("🔄")

                return

        #Proceeds if there is a Match
        if dicematch:

            #Outputs Roll into Console
            print(str(datetime.now()) + " - Re-Roll Command")

            #Detected Roll
            detectedroll = dicematch[0]

            #Detected Explode
            detectedexplode = re.findall("\d+[dD]!", dicematch[0])
            if detectedexplode:
                explode = 1
            else:
                explode = 0
            
            #Strips the d to find number of Dice
            dicenumber = re.sub('[dD]!?', "", dicematch[0])

            #Converting List to String
            diceindex = str(dicenumber)

            #Converting String to Number
            diceindex = int(diceindex)

            #Reset Results
            successes = 0
            diceresults = ""
            explodeddice = 0

            if diceindex > 100:
                dicesummary = discord.Embed(title="Command Error", description=('Dicebot only supports up to 100 dice.'), color=0xFF0000) #Red
                await ctx.send(embed=dicesummary)
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
                        if explode == 1:
                            diceindex = diceindex + 1
                            explodeddice = explodeddice + 1

                if thresholdmatch:
                    netsuccesses = successes - int(threshold)

                    #Colours
                    if netsuccesses > 0:
                        color = 0x00FF00 #Green
                    else:
                        color = 0xFF0000 #Red

                    #Message Output
                    dicesummary = discord.Embed(title=(str(netsuccesses) + str(' Net Successes')), description=(''), color=color)
                    dicesummary.add_field(name="Roll: ", value=">>> " + roll, inline=False)
                    dicesummary.add_field(name=str(detectedroll + " Roll Summary:"), value=diceresults.rstrip(", "), inline=False)
                    #if explode == 1:
                        #dicesummary.add_field(name=str("Exploded Dice: "),value = str(explodeddice), inline=False)
                    dicesummary.add_field(name=str("Threshold:"), value=threshold, inline=False)
                    messageembed = await message.channel.send(embed=dicesummary)
                    await messageembed.add_reaction("🔄")
                    if explode == 0:
                        await messageembed.add_reaction("💥")
                            
                else:
                    #Message Output
                    dicesummary = discord.Embed(title=(str(successes) + str(' Successes')), description=(''), color=0x00FFFF) #Blue
                    dicesummary.add_field(name="Roll: ", value=">>> " + roll, inline=False)
                    dicesummary.add_field(name=str(detectedroll + " Re-Roll Summary:"), value=diceresults.rstrip(", "), inline=False)
                    #if explode == 1:
                        #dicesummary.add_field(name=str("Exploded Dice: "),value = str(explodeddice), inline=False)
                    messageembed = await message.channel.send(embed=dicesummary)
                    await messageembed.add_reaction("🔄")
                    if explode == 0:
                        await messageembed.add_reaction("💥")
                    
        else:
            #Message Output if incorrect format
            diceerror = discord.Embed(title=("Command Error"), description=('Please use the Xd Format when using the `roll` field.'), color=0xFF0000) #Red
            await message.channel.send(embed=diceerror)

        return


    #Exploding Emoji
    if payload.emoji.name == "💥":

        #Gets Message Payload
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        embed = message.embeds[0]
        embed1 = embed.fields[0]
        embed1 = str(embed1)
        rollsummary = embed.fields[1]
        rollsummary = str(rollsummary)

        dicematch = re.findall("\d+[dD]\\b!?", embed1)

        #Detected Roll in lieu of Slash Command Parameter
        roll = re.sub("(EmbedProxy\(name='Roll:', value='>>> )", "", embed1)
        roll = re.sub("(', inline=False\))", "", str(roll))

        #Detected 6's
        sixes = rollsummary.count("6")

        #Message Output if there are 0 6's
        if sixes <= 0:
            diceerror = discord.Embed(title=("Command Error"), description=("Please ensure you have rolled 6's before spending resolve on exploding dice."), color=0xFF0000)
            await message.channel.send(embed=diceerror)
            return

        #Detected Roll in lieu of Slash Command Parameter
        roll = (str(sixes) + "d!")

        #Proceeds if there is a Match
        if dicematch:

            #Outputs Roll into Console
            print(str(datetime.now()) + " - Exploding Command")
        
            #Detected Roll
            detectedroll = dicematch[0]

            #Force Explode
            explode = 1

            #Strips the d to find number of Dice
            dicenumber = re.sub('[dD]!?', "", dicematch[0])

            #Converting List to String
            diceindex = str(sixes)

            #Converting String to Number
            diceindex = int(diceindex)

            #Reset Results
            successes = 0
            diceresults = ""
            explodeddice = 0

            if diceindex > 100:
                dicesummary = discord.Embed(title="Command Error", description=('Dicebot only supports up to 100 dice.'), color=0xFF0000) #Red
                await ctx.send(embed=dicesummary)
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
                        diceresults = diceresults + str("**" + diceresult + "**, ")
                        explodeddice = explodeddice + 1

                    
                #Message Output
                dicesummary = discord.Embed(title=(str(successes) + str(' Successes')), description=(''), color=0xFFA500) #Orange
                dicesummary.add_field(name=str(str(sixes) + "d! Exploding Summary:"), value=diceresults.rstrip(", "), inline=False)
                #dicesummary.add_field(name=str("Exploded Dice: "),value = str(explodeddice), inline=False)
                messageembed = await message.channel.send(embed=dicesummary)
                await messageembed.add_reaction("🔄")
                    
        else:
            #Message Output if incorrect format
            diceerror = discord.Embed(title=("Command Error"), description=('Please use the Xd Format when using the `roll` field.'), color=0xFF0000)
            await message.channel.send(embed=diceerror)

        return

#Dicebot
client.run('INSERT API KEY HERE')
