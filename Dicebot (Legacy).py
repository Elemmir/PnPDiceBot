import discord
import re
import random

client = discord.Client()

@client.event
async def on_ready():
    #Initialise the Bot
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game('Prowlers & Paragons: Ultimate Edition'))

@client.event

async def on_message(message):

    #Do not reply to ourselves
    if message.author == client.user:
        return
    
    #Copies Discord Message for Processing
    discordmessage = message.content

    #Matches Discord Message for Xd Format
    regexmatch = re.findall("\d+[dD]\\b", discordmessage)

    #Detects Number of Rolls in Xd Format
    dicenumberlength = len(regexmatch)
    dicenumberindex = 0

    #Proceeds if there is a Match
    if regexmatch:

        #Outputs Roll into Console
        print("Original Message: " + discordmessage)
        
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
                await message.channel.send("Dicebot only supports up to 100 dice - please try again")
                dicenumberindex = dicenumberindex +1
            else:
                while diceindex != 0:
            
                    #Dice Parameters
                    dicemin = 1
                    dicemax = 6

                    #Random Dice Roll
                    diceroll = random.randint(dicemin, dicemax)

                    #Dice Results
                    diceresult = str(diceroll)

                    if diceroll == 1:
                        diceindex = diceindex - 1
                        diceresults = diceresults + str(diceresult + ", ")

                    if diceroll == 2:
                        successes = successes + 1
                        diceindex = diceindex - 1
                        diceresults = diceresults + str("**" + diceresult + "**, ")

                    if diceroll == 3:
                        diceindex = diceindex - 1
                        diceresults = diceresults + str(diceresult + ", ")

                    if diceroll == 4:
                        successes = successes + 1
                        diceindex = diceindex - 1
                        diceresults = diceresults + str("**" + diceresult + "**, ")

                    if diceroll == 5:
                        diceindex = diceindex - 1
                        diceresults = diceresults + str(diceresult + ", ")

                    if diceroll == 6:
                        successes = successes + 2
                        diceindex = diceindex - 1
                        diceresults = diceresults + str("**" + diceresult + "**, ")

                #Message Output
                dicesummary = discord.Embed(title=(str(successes) + str(' Successes ')), description=(''), color=0xffffff)
                dicesummary.add_field(name=str("*" + (detectedroll) + " Roll Summary:*"), value=diceresults.rstrip(", "), inline=False)
                dicesummary.add_field(name="*Raw Input:* ", value=">>> " + discordmessage, inline=False)
                await message.channel.send(embed=dicesummary)

                dicenumberindex = dicenumberindex +1
              


client.run('INSERT DISCORD API KEY HERE')
