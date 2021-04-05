import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()


sad_words = [
  'sad','depressed', 'unhappy','angry', 'miserable', 'depressing','bitter', 'dismal','heartbroken','melancholy','pessimistic','somber','sorry','wistful','blue', 'down', 'hurting','not feeling good', 'not feelin good',"don't like",'stressed', 'helpless', 'hopeless', 'dying','feeling bad','not feeling well','sick','not perfect','dull'
  ]

starter_encouragements = [
  "Cheer up!",
  "Hang in there",
  "You are a great person/Bot!",
  "You are Cheer leader"
]
if 'responding' not in db.keys():
  db['responding'] = True

def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - " + json_data[0]['a']
  return (quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db['encouragements']
    encouragements.append(encouraging_message)
    db['encouragements'] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db['encouragements']
  if len(encouragements) > index:
    del encouragements[index]
    db['encouragements'] = encouragements


@client.event
async def on_ready():
  print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$hello') or msg.startswith('$hi'):
    await message.channel.send('Hello!')
  if msg.startswith('$inspire') or msg.startswith('inspire me'):
    quote = get_quote()
    await message.channel.send(quote)
  if db['responding']:
    options = starter_encouragements
    if 'encouragements' in db.keys():
      #options = options + db["encouragements"]
      options.extend(db["encouragements"])

    if any(word in msg.lower() for word in sad_words):
      #it will check if any of the message content the word from sad_words list
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith('$del'):
    encouragements = []
    if 'encouragements' in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragement(index)
      encouragements = db['encouragements']
    await message.channel.send(encouragements)

  if msg.startswith('$list'):
    encouragements = []
    if 'encouragements' in db.keys():
      encouragements = db['encouragements']
    await message.channel.send(encouragements)
  
  if msg.startswith('$responding'):
    value = msg.split('$responding ',1)[1]

    if value.lower() == 'true':
      db['responding'] = True
      await message.channel.send('Responding is on.')
    else:
      db['responding'] = False
      await message.channel.send('Responding is off.')


keep_alive()

client.run(os.getenv("TOKEN"))