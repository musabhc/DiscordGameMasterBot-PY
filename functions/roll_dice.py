import discord
from discord.ext import commands
import random

async def roll_dice_command(ctx, *, arg: str):
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

# Create a command for `roll_dice_command`
roll_dice_command = commands.Command(roll_dice_command, name='roll')
