import os
import discord
from nltk.corpus import stopwords
from dotenv import load_dotenv
from better_profanity import profanity
import csv
import pandas as pd


ppt = ''' ...!@#$%^&*(){}[]|._-`/?:;"'\,~12345678876543''' 

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
intents = discord.Intents.all()
client = discord.Client(intents=intents)
profanity.load_censor_words_from_file("badwords.txt")

stop_words = set(stopwords.words('english'))
new_list=[]
mydictionary = {}


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    general_channel = client.get_channel(821240198884229122)
    await general_channel.send('Hi, Im here!')


@client.event
async def on_member_join(member):
    guild = client.get_guild(821240198884229120)
    channel = guild.get_channel(821240198884229122)
    await channel.send(f'Welcome to the Instatute server {member.mention} !') # Welcome the member to the server
    await member.send(f'Welcome to the {guild.name} server, {member.name} ! Please adhere to Instatutes Code of Conduct. Harrasment & Profanity will NOT be tolerated !') # Welcome the member via DM

@client.event
async def on_message(message):
    print(message.content)
    if message.author == client.user: #don't do self-messages
        return
    if profanity.contains_profanity(message.content):
        await message.delete()
        await message.channel.send("don't send that again. Otherwise there will be actions")
        
        admin = client.get_channel(847436998834913301)
       
        await admin.send( f'{message.author.name}  is texting inappropriately.')

    if message.content == 'list':
        await message.channel.send('Top 10 Keywords Mentioned')
        df = pd.read_csv('book.csv', header = 0).groupby('Keywords', as_index=False).agg({'Frequency':'sum'}).drop_duplicates(keep=False)
        
        sorted_df = df.sort_values(by=["Frequency"], ascending=False)
        sorted_df.to_csv('book_sorted.csv', index=False)
        
        df2 = pd.read_csv('book_sorted.csv', header = 0)
        df2.index = df2.index + 1
        await message.channel.send(df2.head(10))
                
        
    else:
        
        wordstring=message.content
        wordlist=wordstring.split()
     
        filteredwordlist=[w.lower().strip(''' ...!@#$%^&*(){}[]|._-`/?:;"'\,~12345678876543''' ) for w in wordlist if ((w not in stop_words) & (w not in ppt))]
        filteredwordlist= list (dict.fromkeys(filteredwordlist))
    
        wordfreq = []
        wordfreq = [filteredwordlist.count(w.lower().strip(''' ...!@#$%^&*(){}[]|._-`/?:;"'\,~12345678876543''' )) for w in wordlist if ((w not in stop_words) & (w not in ppt))] # a list comprehension
        
        new_list = list(zip(filteredwordlist, wordfreq))        #remove duplicate
        #await message.channel.send(new_list)    
        
        with open('book.csv','a') as f2:
            writer = csv.writer(f2)
            writer.writerows(new_list)                          #append to csv
                                            #sort disctionary and display
    
    
client.run(TOKEN)
