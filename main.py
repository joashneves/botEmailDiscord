import random
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from pathlib import Path

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

permissoes = discord.Intents.default()
permissoes.message_content = True
permissoes.members = True

async def carregar_comandos():
    for arquivo in os.listdir("comandos"):
        if arquivo.endswith(".py"):
            await bot.load_extension(f"comandos.{arquivo[:-3]}")

bot = commands.Bot(command_prefix="$", intents=permissoes)

@bot.event
async def on_ready():
    print("Iniciando")
    await carregar_comandos()
    await bot.change_presence(
        activity=discord.Activity(
        type=discord.ActivityType.competing,
        name="Entragando email's!!"))

bot.run(TOKEN)