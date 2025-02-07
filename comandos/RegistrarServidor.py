import discord
from discord.ext import commands
from discord import app_commands

class RegistrarServidor(commands.cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="Registrar_Servidor")
    async def Registrar_Servidor(self, interaction: discord.Integration):
        pass

async def setup(bot):
    await bot.add_cog(RegistrarServidor(bot))