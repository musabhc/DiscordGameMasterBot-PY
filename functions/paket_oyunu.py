import discord
from discord.ext import commands
from discord.ui import Button, View
import random
import asyncio
import os

# Paket dosyalarının yolu
PAKETLER_DOSYASI_YOLU = 'kelime_paketleri/'

# Paketleri dosyadan okuyarak yükleme fonksiyonu
def paketleri_yukle():
    paketler = {}
    for dosya_adı in os.listdir(PAKETLER_DOSYASI_YOLU):
        if dosya_adı.endswith('.txt'):
            paket_adı = dosya_adı.replace('.txt', '')
            with open(os.path.join(PAKETLER_DOSYASI_YOLU, dosya_adı), 'r', encoding='utf-8') as dosya:
                kelimeler = dosya.read().splitlines()
                paketler[f"Paket {paket_adı}"] = kelimeler
    return paketler

# Paketleri yükle
paketler = paketleri_yukle()

async def paket_oyunu_command(ctx):
    bot = ctx.bot  # Get the bot instance from the context

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

                for remaining_time in range(3, 0, -1):
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

# Create a command for `paket_oyunu_command`
paket_oyunu_command = commands.Command(paket_oyunu_command, name='paketOyunu')
