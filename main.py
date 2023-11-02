import openai
from lxml import html
import bs4
from bs4 import BeautifulSoup
import numpy as np
import os
import discord
import requests
import json
import random
from requests import get

OPENAI_KEY = os.environ['OPEN_AI']
openai.api_key = OPENAI_KEY

tanki_url = ['https://ratings.tankionline.com/en/']
result = []
tanki_url


def random_line(sad):
  lines = open(sad).read().splitlines()
  return random.choice(lines)


def encouragement(encourage):
  lines = open(encourage).read().splitlines()
  return random.choice(lines)


intents = discord.Intents().all()
client = discord.Client(intents=intents)


def get_quotes():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return (quote)


def get_meme():
  content = get("https://meme-api.herokuapp.com/gimme").text
  data = json.loads(content)
  return (data)


random_emojis = [
  '\U0001F644', '\U0001F600', '\U0001F604', '\U0001F923', '\U0001f305',
  '\U0001f31d', '\U0001F321', '\U0001f308', '\U0001f329', '\U0001f329',
  '\U0001f326', '\U0001f634', '\U0001f305'
]


@client.event
async def on_ready():

  print('Welcome !! {0.user} This Bot Is powered by Dark Soul'.format(client))


my_secret = os.environ['my_secret']


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$hi' or '$hello'):
    await message.channel.send('Hello  {} '.format(message.author.name) +
                               random.choice(random_emojis))

  cars = ["$quote", "$help", "$hello", '$info']

  if (message.content == '$help'):
    embed = discord.Embed(title="General Commands",
                          description='\n\n'.join(str(x) for x in cars),
                          color=0xfffb00)

  clan_players = ["- Pragmatic", "- QueenLily", "- The_Dark_Soul", '- Extint','- Autonomous','- Misfortune', '- Redrover','- Echo','- Insurge','- Span', '-Misdirection']
  if (message.content == '$cp'):
    embed = discord.Embed(title="Clan Players",
                          description='\n\n'.join(str(x) for x in clan_players),
                          color=0x00ffff) 

    await message.channel.send(embed=embed)

  if msg.startswith('$quote'):
    quote = get_quotes()
    embed = discord.Embed(title=quote, description=None, color=0xfffb00)
    await message.channel.send(embed=embed)

  if msg.startswith('$em'):
    await message.channel.send(encouragement("encourage.txt"))

  if (msg == '$info'):
    embed = discord.Embed(
      title='\b Information About the Creater',
      description=
      'This Bot is powered by **The Dark Soul**, Coding Language is _"Python"_',
      color=0xffd700)
    await message.channel.send(embed=embed)

  if msg.startswith('$meme'):
    meme = get_meme()
    embed = discord.Embed(title=meme, color=0xfffb00, description=None)
    await message.channel.send(embed=embed)

  if client.user in message.mentions:

    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=f"{message.content}",
      max_tokens=2048,
      temperature=0.5,
    )
    await message.channel.send(response.choices[0].text)

  result = []

  def script(link):
    #   page=requests.get(link).text
    #  soup=BeautifulSoup(page,'lxml')
    # text=[p.text for p in soup.find('div', class_='leaderboard__list')]

    page = requests.get(link).text
    soup = BeautifulSoup(page, 'lxml')
    title = soup.find(class_='generic-header')
    text = title.text if title else ''
    content = ''
    leaderboard = soup.find('header', class_='generic-header')
    if leaderboard:
      content = [p.text for p in leaderboard]
    return text, content

  if (msg == '$wr'):
    for i in tanki_url:
      a = script(i)
      title = a[0]
      content = a[1]
      link = i
      result.append((title, content, link))

    if result:
      await message.channel.send(result)
    else:
      await message.channel.send("No data found.")


client.run(my_secret)
