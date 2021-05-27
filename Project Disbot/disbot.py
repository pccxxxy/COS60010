#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 16 15:50:38 2021

@author: brandonxu
"""

import os
import discord
#from discord.ext import commands
from nltk.corpus import stopwords
from dotenv import load_dotenv
import csv
import pandas as pd


ppt = ''' ...!@#$%^&*(){}[]|._-`/?:;"'\,~12345678876543''' 

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
guild = discord.Guild
stop_words = set(stopwords.words('english'))
new_list=[]
mydictionary = {}


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    print(message.content)
    if message.author == client.user: #don't do self-messages
        return
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