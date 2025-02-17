import random
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from pathlib import Path
from models.db import _Sessao

from comandos.Tutorial import ViewTutorial
from comandos.EnviarEmail import EmailView
from comandos.ExibirSeguindos import ExibirSeguindoView

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

permissoes = discord.Intents.default()
permissoes.message_content = True
permissoes.members = True

class Bot_modificado(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="%", intents=permissoes)

    async def setup_hook(self):
        self.add_view(ViewTutorial())
        self.add_view(EmailView())
        self.add_view(ExibirSeguindoView())

bot = Bot_modificado()

async def carregar_comandos():
    for arquivo in os.listdir("comandos"):
        if arquivo.endswith(".py"):
            await bot.load_extension(f"comandos.{arquivo[:-3]}")

@bot.event
async def on_ready():
    print("Iniciando")
    await carregar_comandos()
    try:
        synced = await bot.tree.sync()
        print(f"Comandos sincronizados {len(synced)} comandos")
    except Exception as e:
        print("Erro ao sincronizar comandos de barra: {e}")

    await bot.change_presence(
        activity=discord.Activity(
        type=discord.ActivityType.competing,
        name="Entragando email's!!"))

bot.run(TOKEN)
