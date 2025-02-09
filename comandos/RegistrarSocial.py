import discord
from discord import app_commands
from discord.ext import commands
from models.Usuario import Manipular_Usuario
from models.RedeSocial import Manipular_redesSociais

def find_urls_in_string(string):
    x = string.split()
    return [i for i in x if i.find("https:")==0 or i.find("http:")==0]

class RegistrarSocial(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="colocar_rede_social", description="Coloca uma de 5 redes sociais no seu perfil")
    async def colocar_social(self, interaction: discord.Interaction, redesocial: str, link: str):
        link = find_urls_in_string(link)
        usuario = Manipular_Usuario.Obter_usuario(interaction.user.id)
        if not usuario:
            await interaction.response.send_message("Favor se registrar com `/registrar`", ephemeral=True)
            return
        if len(redesocial) > 30:
            await interaction.response.send_message("Nome da rede social não pode ter mais de 30 caracteres", ephemeral=True)
            return
        if not link or len(link) > 1:
            await interaction.response.send_message("Link não encontrado ou dois ou mais links", ephemeral=True)
            return
        redes_lista = Manipular_redesSociais.Obter_redes_de_usuario(interaction.user.id)
        if len(redes_lista) >= 5:
            await interaction.response.send_message("Maximos de redes alcançado", ephemeral=True)
            return
        print(f"Registrando... {redesocial, link[0]} ")
        Manipular_redesSociais.Criar_redes(interaction.user.id, redesocial, link[0])
        await interaction.response.send_message(f"Registrado, Redes : {redesocial} = {link}", ephemeral=True)

    @app_commands.command(name="remover_rede", description="remove uma das redes socias")
    async def remover_rede(self, interaction: discord.Interaction, rede:str):
        redes = Manipular_redesSociais.Obter_redes_de_usuario(interaction.user.id)
        if not redes:
            await interaction.response.send_message(f"Voce não tem redes", ephemeral=True)
            return
        removido_rede = Manipular_redesSociais.Remover_rede(interaction.user.id, rede)
        if removido_rede:
            await interaction.response.send_message(f"removido : {rede}", ephemeral=True)
            return
        await interaction.response.send_message(f"falha ao remover", ephemeral=True)


    @remover_rede.autocomplete('rede')
    async def remover_rede_autocomplete(self,interact: discord.Interaction, pesquisa:str):
        print(pesquisa)
        opcaoes = []
        redes = Manipular_redesSociais.Obter_redes_de_usuario(interact.user.id)
        for rede in redes:
            rede_option = app_commands.Choice(name=f"{rede.nome}", value=f"{rede.nome}")
            opcaoes.append(rede_option)
        return opcaoes

async def setup(bot):
    await bot.add_cog(RegistrarSocial(bot))
