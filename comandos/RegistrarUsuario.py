import discord
from discord.ext import commands
from discord import app_commands
import models
from models.Usuario import Manipular_Usuario

class RegistrarUsuario(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
async def setup(bot):
    await bot.add_cog(RegistrarUsuario(bot))