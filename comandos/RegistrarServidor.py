import discord
from discord.ext import commands
from discord import app_commands
import models
from models.Servidor import Manipular_Servidor
class RegistrarServidor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="registrar_servidor", description="Registrar servidor")
    @app_commands.describe(email="Nome do @ do servidor MAX 50 caracteres")
    @app_commands.describe(channel="Canal aonde vai enviar as postagens")
    @app_commands.default_permissions(manage_guild=True)
    async def Registrar_Servidor(self,
                                  interaction: discord.Interaction,
                                  email: str,
                                  channel: discord.TextChannel,):
        id_sevidor = interaction.guild.id
        email_formatada = email.strip()
        id_chat = channel.id
        print(email_formatada.isalpha())
        if len(email_formatada) > 50 or email_formatada.isalpha() == False:
            await interaction.response.send_message(f'o {email} passou de 50 caracteres ou não pode ter espaço', ephemeral=True)
            return 
        servidor = Manipular_Servidor.Obter_servidor(id_sevidor)
        print(servidor)
        if servidor:
            await interaction.response.send_message(f'o {servidor.email} ja existe!', ephemeral=True)
            return
        elif not servidor:
            registrarServidor = Manipular_Servidor.Registrar_servidor(id_sevidor, email_formatada, id_chat)
            print(registrarServidor)
            await interaction.response.send_message(f'Servidor registrado {id_sevidor}, {email_formatada}, {id_chat}', ephemeral=True)
            return
        print()
        print(f'Debug Registrar_servidor: {id_sevidor}, {email}:{len(email)}, {id_chat}')
        await interaction.response.send_message(f'Algo deu errado!', ephemeral=True)


async def setup(bot):
    await bot.add_cog(RegistrarServidor(bot))