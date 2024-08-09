import os
import discord
import asyncio
from typing import Final
from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands
from functions.roll_dice import roll_dice_command
from functions.countdown import countdown_command
from functions.word_game import word_game_func

# LOAD TOKEN
load_dotenv()
Token: Final[str] = os.getenv('DISCORD_TOKEN')

# Setup Bot
intents: Intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Load commands from functions
bot.add_command(roll_dice_command)
bot.add_command(countdown_command)
bot.add_command(word_game_func)

# Startup for bot
@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is now running!')

# Main Entry Point
def main() -> None:
    bot.run(Token)

if __name__ == '__main__':
    main()
