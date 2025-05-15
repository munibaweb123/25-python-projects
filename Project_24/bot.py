import discord
import os
from dotenv import load_dotenv
import requests
import json
import random
from keep_alive import keep_alive

# Filepath for the local database
DB_FILE = "encouragements.json"

# Helper function to load data from the JSON file
def load_encouragements():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as file:
            return json.load(file)
    return []

# Helper function to save data to the JSON file
def save_encouragements(encouragements):
    with open(DB_FILE, "w") as file:
        json.dump(encouragements, file)

def update_encouragements(encouragement):
    encouragements = load_encouragements()
    encouragements.append(encouragement)
    save_encouragements(encouragements)

def delete_encouragement(index):
    encouragements = load_encouragements()
    if len(encouragements) > index:
        del encouragements[index]
        save_encouragements(encouragements)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "sorrowful", "downcast", "disheartened", "despondent", "depressing"]
starter_encouragements = [
    "Cheer up!",
    "Hang in there!",
    "You are a great person!",
    "You are doing great!",
    "Keep going!",
    "You are amazing!",
    "Believe in yourself!",
    "You can do it!"
]

def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# Global variable to track responding state
responding = True

@client.event
async def on_message(message):
    global responding
    if message.author == client.user:
        return

    # Define options before using it
    options = starter_encouragements + load_encouragements()
    if message.content.startswith('$hello'):
        await message.channel.send('Hello! How can I help you today?')

    if message.content.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if responding and any(word in message.content for word in sad_words):
        await message.channel.send(random.choice(options))

    if message.content.startswith('$new'):
        try:
            encouragement_message = message.content.split("$new ", 1)[1]
            update_encouragements(encouragement_message)
            await message.channel.send("New encouraging message added.")
        except IndexError:
            await message.channel.send("Please provide a message to add after `$new`.")

    if message.content.startswith('$del'):
        try:
            index = int(message.content.split("$del ", 1)[1])
            encouragements = load_encouragements()
            if 0 <= index < len(encouragements):
                delete_encouragement(index)
                encouragements = load_encouragements()
                await message.channel.send(f"Deleted encouragement at index {index}.")
            else:
                await message.channel.send("Index out of range. Please provide a valid index.")
        except (ValueError, IndexError):
            await message.channel.send("Please provide a valid index to delete after `$del`.")

    if message.content.startswith('$list'):
        encouragements = load_encouragements()
        if encouragements:
            await message.channel.send("Encouragements:\n" + "\n".join(f"{i}: {e}" for i, e in enumerate(encouragements)))
        else:
            await message.channel.send("No encouragements found.")

    if message.content.startswith('$responding'):
        try:
            value = message.content.split("$responding ", 1)[1]
            if value.lower() == "true":
                responding = True
                await message.channel.send("Responding is on.")
            elif value.lower() == "false":
                responding = False
                await message.channel.send("Responding is off.")
            else:
                await message.channel.send("Invalid value! Use 'true' or 'false'.")
        except IndexError:
            await message.channel.send("Please specify 'true' or 'false' after the `$responding` command.")

# Load the bot token from the .env file
load_dotenv()
token = os.getenv('TOKEN')
if not token:
    raise ValueError("The TOKEN environment variable is not set or is empty.")

keep_alive()
client.run(token)