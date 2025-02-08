import discord
from discord.ext import commands
from discord import app_commands
import models
from models.Usuario import Manipular_Usuario
from models.Servidor import Manipular_Servidor

class RegisterModal(discord.ui.Modal):
    def __init__(self, nome, id_servidor):
        super().__init__(title="Registrar Usuario")
        self.nome = nome
        self.id_servidor = id_servidor

    nome_usuario = discord.ui.TextInput(
        label="Nome",
        placeholder=f"Nome que sera exibido antes do @(Se ja registrado não muda)",
        max_length=25)
    descricao_usuario = discord.ui.TextInput(
        label="Descrição",
        placeholder="Escreva uma descrição",
        max_length=255,
        style=discord.TextStyle.long)
    pronome = discord.ui.TextInput(
        label="Pronomes",
        placeholder="Escreva seus pronomes (opicional)",
        max_length=8,
        required=False)
    
    async def on_submit(self, interaction:discord.Interaction):
        id_discord = interaction.user.id
        apelido = self.nome_usuario.value or "N/a"
        descricao = self.descricao_usuario.value
        pronome = self.pronome.value
        id_servidor = self.id_servidor
        existir_usuario = Manipular_Usuario.Obter_usuario(id_discord)
        if not existir_usuario:
            Manipular_Usuario.Criar_usuario(id_discord, apelido, descricao, pronome, id_servidor)
            await interaction.response.send_message("Usuario criado", ephemeral=True)
        elif existir_usuario:
            Manipular_Usuario.Atualiza_usuario(id_discord, descricao, pronome)
            await interaction.response.send_message("Usuario atulizado", ephemeral=True)

class RegistrarUsuario(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="registrar", description="abre modal para se registrar se ja regristrado, atualiza")
    async def Registrar_usuario(self, interaction:discord.Interaction):
        nome = interaction.user.display_name
        id_guild = interaction.guild.id
        listaServidores = Manipular_Servidor.Obter_todos_servidore()
        print(listaServidores)
        for servidores in listaServidores:
            if servidores.id_servidor == id_guild:
                await interaction.response.send_modal(RegisterModal(nome, id_guild))
                return
        await interaction.response.send_message("Servidor não esta cadastrado!", ephemeral=True)
    
async def setup(bot):
    await bot.add_cog(RegistrarUsuario(bot))