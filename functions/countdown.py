import discord
from discord.ext import commands
import asyncio

async def countdown_command(ctx, timeInput: str):
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

# Create a command for `countdown_command`
countdown_command = commands.Command(countdown_command, name='timer')
