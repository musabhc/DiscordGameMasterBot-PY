import asyncio
import discord
from discord.ext import commands
from discord.ui import Button, View
import os
import random
import secrets

# Directory of Word Packages
Word_Packages_Directory = 'word-packages/'

# Read and load packages from file
def load_packages():
    packages = {}
    for file_name in os.listdir(Word_Packages_Directory):
        if file_name.endswith('.txt'):
            package_name = file_name.replace('.txt', '')
            with open(os.path.join(Word_Packages_Directory, file_name), 'r', encoding='utf-8') as file:
                words = file.read().splitlines()
                packages[package_name] = words
    return packages

# Load Packages
packs = load_packages()

# Define the command using the decorator
@commands.command(name='wordGame')
async def word_game_func(ctx):
    bot = ctx.bot  # Get the bot instance from the context

    view = View()

    packs_button = Button(label="Packages", style=discord.ButtonStyle.primary)
    play_button = Button(label="Play", style=discord.ButtonStyle.success)

    view.add_item(packs_button)
    view.add_item(play_button)

    async def packs_callback(interaction):
        packs_view = View()
        for pack in packs.keys():
            packet_button = Button(label=pack, style=discord.ButtonStyle.primary)
            packs_view.add_item(packet_button)

            async def packs_button_callback(interaction, selected_package=pack):
                pack_words = f"{selected_package} words:\n" + "\n".join(packs[selected_package])
                await interaction.response.send_message(pack_words, ephemeral=True)

            packet_button.callback = packs_button_callback

        await interaction.response.send_message("Select package:", view=packs_view, ephemeral=True)

    packs_button.callback = packs_callback

    async def play_callback(interaction):
        pack_view = View()
        join_time = 5
        for pack in packs.keys():
            package_button = Button(label=pack, style=discord.ButtonStyle.primary)
            pack_view.add_item(package_button)

            async def packs_button_callback(interaction, selected_package=pack):
                await interaction.response.send_message(f"Selected pack: {selected_package}. Join within {join_time} seconds!", ephemeral=False)
                countdown_message = await interaction.followup.send(f"Selected pack: {selected_package}. Join within {join_time} seconds!")
                join_button = Button(label="Join", style=discord.ButtonStyle.success)
                join_view = View()
                join_view.add_item(join_button)

                participants = []

                async def join_button_callback(interaction):
                    participants.append(interaction.user.id)
                    await interaction.response.send_message("You joined the game!", ephemeral=True)

                join_button.callback = join_button_callback

                await countdown_message.edit(view=join_view)

                for remaining_time in range(join_time, 0, -1):
                    await countdown_message.edit(content=f"Selected pack: {selected_package}. Join within {remaining_time} seconds!")
                    await asyncio.sleep(1)
                random.shuffle(participants)
                agent = secrets.choice(participants)
                participants.remove(agent)

                agent_user = await bot.fetch_user(agent)
                await agent_user.send("You're the agent!")
                word = random.choice(packs[selected_package])
                for user in participants:
                    users = await bot.fetch_user(user)
                    await users.send(f"Pack: {pack} Random word: {word}")

                await countdown_message.edit(content=f"Selected pack: {selected_package}. The game has begun!", view=None)

            package_button.callback = packs_button_callback

        await interaction.response.send_message("Select package:", view=pack_view)

    play_button.callback = play_callback

    await ctx.send("Welcome to the Word Pack game! Would you like to see the packs or start the game?", view=view)