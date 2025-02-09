import discord
from discord import app_commands
from discord.ext import commands
from models.Usuario import Manipular_Usuario
from models.RedeSocial import Manipular_redesSociais

def find_urls_in_string(string):
    x = string.split()
    return [i for i in x if i.find("https:")==0 or i.find("http:")==0]

class RemoverRedeSelect(discord.ui.Select):
    def __init__(self):
        placeholder = "ESCOLHA UMA REDE PARA REMOVER!!!!!"
        min_values = 1 # the minimum number of values that must be selected by the users
        max_values = 1 # the maximum number of values that can be selected by the users
        options=[
            discord.SelectOption(label="aaaaaa", description="aaaaa"),
            discord.SelectOption(label="asdasdasd", description="dsfwesf")
        ]
        super().__init__(placeholder=placeholder, options=options, min_values=min_values, max_values=max_values)

    async def callback(self, interaction: discord.Interaction):
        ...

class RemoverRedeView(discord.ui.View):
    def __init__(self):
        super().__init__()


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
    async def remover_rede(self, interaction: discord.Interaction):
        view = RemoverRedeView()
        view.add_item(RemoverRedeSelect)
        redesSociais = Manipular_redesSociais.Obter_redes_de_usuario(interaction.user.id)

        for rede in redesSociais:
            print(f"{rede.link, rede.nome}")

        await interaction.response.send_message(view=view)

async def setup(bot):
    await bot.add_cog(RegistrarSocial(bot))
