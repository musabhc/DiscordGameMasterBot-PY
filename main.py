import os
import discord
import asyncio
from typing import Final
from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands
from discord.ui import Button, View
import random

# LOAD TOKEN
load_dotenv()
Token: Final[str] = os.getenv('DISCORD_TOKEN')

# Setup Bot
intents: Intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Paketler
paketler = {
    "Paket 1: Şarkıcılar": ["Mahmut Tuncer", "Yıldız Tilbe", "Ahmet Kaya"],
    "Paket 2: Dizi Karakterleri": ["Çaycı Hüseyin", "Polat Alemdar", "Light Selami"],
    "Paket 3: Youtuberlar": ["Lanet Kel", "Enes Batur", "Enis Kirazoğlu"]
}

# /game komutu
@bot.command(name='paketOyunu')
async def game(ctx):
    view = View()

    paketler_button = Button(label="Paketler", style=discord.ButtonStyle.primary)
    oyuna_basla_button = Button(label="Oyuna başla", style=discord.ButtonStyle.success)

    view.add_item(paketler_button)
    view.add_item(oyuna_basla_button)

    async def paketler_callback(interaction):
        paketler_mesaji = ""
        for paket, kelimeler in paketler.items():
            paketler_mesaji += f"{paket}: {', '.join(kelimeler)}\n"
        await interaction.response.send_message(paketler_mesaji, ephemeral=False)

    async def oyuna_basla_callback(interaction):
        paket_view = View()
        for paket in paketler.keys():
            paket_button = Button(label=paket, style=discord.ButtonStyle.primary)
            paket_view.add_item(paket_button)

            async def paket_button_callback(interaction, paket=paket):
                await interaction.response.send_message(f"{paket} paketi seçildi. 15 saniye içinde katılabilirsiniz!", ephemeral=False)
                countdown_message = await interaction.followup.send(f"{paket} paketi seçildi. Oyuna katılmak için tıklayın! Kalan süre: 15 saniye")
                katil_button = Button(label="Katıl", style=discord.ButtonStyle.success)
                katil_view = View()
                katil_view.add_item(katil_button)

                katilimcilar = []

                async def katil_button_callback(interaction):
                    katilimcilar.append(interaction.user.id)
                    await interaction.response.send_message("Katıldınız!", ephemeral=True)

                katil_button.callback = katil_button_callback

                await countdown_message.edit(view=katil_view)

                for remaining_time in range(15, 0, -1):
                    await countdown_message.edit(content=f"{paket} paketi seçildi. Oyuna katılmak için tıklayın! Kalan süre: {remaining_time} saniye")
                    await asyncio.sleep(1)

                if katilimcilar:
                    kazanan = random.choice(katilimcilar)
                    katilimcilar.remove(kazanan)
                    kazanan_kullanici = await bot.fetch_user(kazanan)
                    await kazanan_kullanici.send("Ajansın")
                    for katilimci in katilimcilar:
                        kelime = random.choice(paketler[paket])
                        kullanici = await bot.fetch_user(katilimci)
                        await kullanici.send(f"{paket} paketinden rastgele kelime: {kelime}")

                await countdown_message.edit(content=f"{paket} paketi seçildi. Oyuna katılmak için tıklayın! Kalan süre: 0 saniye", view=None)

            paket_button.callback = paket_button_callback

        await interaction.response.send_message("Bir paket seçin:", view=paket_view)

    paketler_button.callback = paketler_callback
    oyuna_basla_button.callback = oyuna_basla_callback

    await ctx.send("Kelime Paketi oyununa hoşgeldin! Paketleri görmek mi yoksa oyuna başlamak mı istersin?", view=view)

# /roll komutu
@bot.command(name='roll')
async def roll(ctx, *, arg: str):
    try:
        if '+' in arg:
            # Format: XdY + Z
            dice_part, bonus = arg.split('+')
            dice_part = dice_part.strip()
            bonus = int(bonus.strip())
        else:
            # Format: XdY
            dice_part = arg.strip()
            bonus = 0

        num_dice, dice_type = dice_part.split('d')
        num_dice = int(num_dice)
        dice_type = int(dice_type)

        rolls = [random.randint(1, dice_type) for _ in range(num_dice)]
        total = sum(rolls) + bonus

        await ctx.send(f"Rolls: {rolls} = toplam {total}")

    except Exception as e:
        await ctx.send(f"Hata: {e}")

# Timer
@bot.command()
async def timer(ctx, timeInput: str):
    try:
        try:
            time = int(timeInput)
        except ValueError:
            convertTimeList = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'S': 1, 'M': 60, 'H': 3600, 'D': 86400}
            time = int(timeInput[:-1]) * convertTimeList[timeInput[-1]]
        if time > 86400:
            await ctx.send("I can't do timers over a day long")
            return
        if time <= 0:
            await ctx.send("Timers don't go into negatives :/")
            return
        if time >= 3600:
            message = await ctx.send(f"Timer: {time // 3600} hours {time % 3600 // 60} minutes {time % 60} seconds")
        elif time >= 60:
            message = await ctx.send(f"Timer: {time // 60} minutes {time % 60} seconds")
        elif time < 60:
            message = await ctx.send(f"Timer: {time} seconds")
        while True:
            try:
                await asyncio.sleep(5)
                time -= 5
                if time >= 3600:
                    await message.edit(content=f"Timer: {time // 3600} hours {time % 3600 // 60} minutes {time % 60} seconds")
                elif time >= 60:
                    await message.edit(content=f"Timer: {time // 60} minutes {time % 60} seconds")
                elif time < 60:
                    await message.edit(content=f"Timer: {time} seconds")
                if time <= 0:
                    await message.edit(content="Ended!")
                    await ctx.send(f"{ctx.author.mention} Your countdown has ended!")
                    break
            except Exception as e:
                print(f"Error during countdown: {e}")
                break
    except Exception as e:
        await ctx.send(f"Error: {e}")
        await ctx.send(f"Alright, first you gotta let me know how I'm gonna time **{timeInput}**....")

# Startup for bot
@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is now running!')

# Main Entry Point
def main() -> None:
    bot.run(Token)

if __name__ == '__main__':
    main()

