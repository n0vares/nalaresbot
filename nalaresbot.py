#!/usr/bin/python3

import discord
from discord.ext import commands
import datetime
import asyncio

# Channel IDs
insulin_chan = 1199845543040536646
pee_chan = 1199845325301628999
glucose_chan = 1200450606691795114
walk_chan = 1200482230636662885

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix="/", intents=intents)

class PetCare(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def embed(self, ctx, title, description, chan):
        embed = discord.Embed(title=title, description=description)
        channel = self.bot.get_channel(chan)
        await ctx.respond(content='Logged', ephemeral=True)
        await channel.send(embed=embed)

    @commands.slash_command(name="npee")
    async def log_npee(self, ctx):
        """Log when Nala Pees"""
        await self.log_pee(ctx, "Nala")

    @commands.slash_command(name="apee")
    async def log_apee(self, ctx):
        """Log when Ares Pees"""
        await self.log_pee(ctx, "Ares")

    @commands.slash_command(name="pee")
    async def log_pee_both(self, ctx):
        """Log when Nala and Ares Both Pee"""
        await self.log_pee(ctx, "Nala and Ares")

    async def log_pee(self, ctx, dog_name):
        time = datetime.datetime.now().strftime("%I:%M %p")
        title = f"{dog_name} peed"
        message = f"{dog_name} peed at {time}"
        await self.embed(ctx, title, message, pee_chan)

    @commands.slash_command(name="insulin")
    async def log_insulin(self, ctx):
        """Log when Nala received her insulin shot and set a reminder for the next dose (12 hours)"""
        time = datetime.datetime.now().strftime("%I:%M %p")
        title = "Nala was given her insulin"
        message = f"Nala was given her insulin at {time}"
        await self.embed(ctx, title, message, insulin_chan)

        # Reminder logic
        next_shot_time = (datetime.datetime.now() + datetime.timedelta(hours=12)).strftime("%I:%M %p")
        reminder_message = f"The 12-hour timer has started. Nala will need her next shot at {next_shot_time}."
        await self.embed(ctx, "Insulin Reminder", reminder_message, insulin_chan)

        # Wait for 12 hours
        await asyncio.sleep(12 * 3600)
        final_reminder_message = f"@everyone: it is {next_shot_time}. Time for Nala's next insulin shot!"
        await self.embed(ctx, "Insulin Reminder", final_reminder_message, insulin_chan)

    @commands.slash_command(name="glucose")
    async def log_glucose(self, ctx, value: int):
        """Log Nala's glucose level and set a reminder for the next test (2 hrs)"""
        time = datetime.datetime.now().strftime("%I:%M %p")
        title = f"Nala's glucose level was {value}"
        message = f"Nala's glucose level was {value} at {time}"
        await self.embed(ctx, title, message, glucose_chan)

        # Reminder logic
        next_test_time = (datetime.datetime.now() + datetime.timedelta(hours=2)).strftime("%I:%M %p")
        final_reminder_message = f"A 2-hour alert is set for the next glucose test. The next test will be at {next_test_time}."
        await self.embed(ctx, "Glucose Test Reminder", final_reminder_message, glucose_chan)

        # Wait for 2 hours
        await asyncio.sleep(2 * 3600)
        await self.embed(ctx, "@everyone: Glucose Test Reminder: {next_test_time}", final_reminder_message, glucose_chan)

    @commands.slash_command(name="awalk")
    async def log_awalk(self, ctx):
        """Log that Ares was walked"""
        time = datetime.datetime.now().strftime("%I:%M %p")
        message = f"Ares was walked at {time}"
        await self.embed(ctx, "Ares Walk", message, walk_chan)

    @commands.slash_command(name="nwalk")
    async def log_nwalk(self, ctx):
        """Log that Nala was walked"""
        time = datetime.datetime.now().strftime("%I:%M %p")
        message = f"Nala was walked at {time}"
        await self.embed(ctx, "Nala Walk", message, walk_chan)

    @commands.slash_command(name="walk")
    async def log_walk(self, ctx):
        """Log that both dogs were walked"""
        time = datetime.datetime.now().strftime("%I:%M %p")
        message = f"Both dogs were walked at {time}"
        await self.embed(ctx, "Dog Walk", message, walk_chan)

# Register the cog
bot.add_cog(PetCare(bot))

@bot.event
async def on_ready():
    print(f"{bot.user.name} v1.0.4h is connected!")

bot.run("Bot Token")
