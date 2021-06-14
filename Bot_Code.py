import discord
import os
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from discord.ext import commands
import asyncio
from keep_alive import keep_alive
import pytz 

bot = commands.Bot(command_prefix='!')
client = discord.Client()

def get_it():
    response = requests.get("https://www.schoolsolver.com/questions/")
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    New_qn = data.find_all('tr')[1]

    col_vals = New_qn.find_all('td')
    l = []

    for x in col_vals[:3]:
        d = x.text
        d = d.replace('\n','')
        l.append(d)

    tz_NY = pytz.timezone('Asia/Kolkata')   
    datetime_NY = datetime.now(tz_NY) 
    now = datetime_NY.strftime("%H:%M:%S - (%d/%m)")
    
    print('Price = ',l[0])
    print('Category = ', l[1])
    print('Title =  ', l[2])
    print('At time of: ', now)
    print('')
    return l

def get_msg(link):
    tz_NY = pytz.timezone('Asia/Kolkata')   
    datetime_NY = datetime.now(tz_NY)  
    nl = '\n'
    now = datetime_NY.strftime("%H:%M:%S - (%d/%m)")
    ans = f'New Questions Guyss!! {nl}Price = {link[0]} {nl}Category = {link[1]} {nl}Title = {link[2]} {nl}Indian Time: {now} {nl}'

    return ans

async def finder():
    await bot.wait_until_ready()
    channel = bot.get_channel(int(os.environ['channelId']))
    initial_link = get_it()
    #await channel.send(get_msg(initial_link))
    while(True):
        try:
            current_link = get_it()
        except:
            continue
        #await channel.send(get_msg(current_link))
        if(initial_link) != current_link:
            await channel.send(get_msg(current_link))
            initial_link = current_link
        time.sleep(10)
    await asyncio.sleep(10)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

print("start")
keep_alive()

bot.loop.create_task(finder())
bot.run(os.environ['token'])
