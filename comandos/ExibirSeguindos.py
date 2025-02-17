import discord
from discord.ext import commands
from discord import app_commands
from models.Usuario import Manipular_Usuario
from models.Seguindo import Manipular_seguidor

class ExibirSeguindoView(discord.ui.View):
    def __init__(self, seguindos):
        super().__init__(timeout=None)
        self.seguindos = seguindos
        self.index = 0

    async def get_embem(self, interaction: discord.Interaction):
        seguindo = self.seguindos[self.index]
        usuario = Manipular_Usuario.Obter_usuario(seguindo.id_usuario_alvo)
        usuario_id = interaction.client.get_user(usuario.id_discord)
        embed = discord.Embed(
            title=f'Perfil de : {usuario.apelido}',
            description=f'Bio : {usuario.descricao}',
            color=discord.Color.magenta()
        )
        embed.add_field(name="Pronomes", value=f"{usuario.pronome}", inline=True)
        embed.add_field(name="Posts", value=f"{usuario.post}", inline=True)
        embed.set_image(url=usuario_id.avatar.url)
        await interaction.response.edit_message(embed=embed, view=self)
        return embed

    @discord.ui.button(label="deixar de seguir", custom_id="botao_deixar_seguir_seguindo", style=discord.ButtonStyle.red)
    async def deixar_seguir(self, interaction: discord.Interaction, button: discord.ui.Button):
        usuario = Manipular_Usuario.Obter_usuario(interaction.user.id)
        if not usuario:
            await interaction.response.send_message("Voce não criou uma conta", ephemeral=True)
            return
        seguindo = self.seguindos[self.index]
        if interaction.user.id == seguindo.id_usuario_alvo:
            await interaction.response.send_message("Voce não pode deixar de seguir voce mesmo!", ephemeral=True)
            return
        seguidor = Manipular_seguidor.remover_seguidor(interaction.user.id, seguindo.id_usuario_alvo)
        if seguidor == True:
            await interaction.response.send_message(f"Voce deixou de seguir", ephemeral=True)
        elif seguidor == False:
            await interaction.response.send_message(f"Voce não segue esse usuario", ephemeral=True)

    @discord.ui.button(label="<<<", style=discord.ButtonStyle.primary)
    async def anterior_botao(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index = (self.index - 1) % len(self.seguindos)
        await self.get_embem(interaction)
    @discord.ui.button(label=">>>", style=discord.ButtonStyle.primary)
    async def proximo_botao(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index = (self.index + 1) % len(self.seguindos)
        await self.get_embem(interaction)

class ExibirSeguindos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="exibir_seguindo", description="Mostra um lista das pessoas que voce esta seguindo")
    async def exibir_seguindo(self, Interaction: discord.Interaction):
        seguindo_lista = Manipular_seguidor.Obter_seguindo(Interaction.user.id)
        if not seguindo_lista:
            await Interaction.response.send_message("Voce não esta seguindo ninguem", ephemeral=True)
            return
        view = ExibirSeguindoView(seguindo_lista)
        seguindoEmbed = await view.get_embem(Interaction)
        await Interaction.response.send_message(embed=seguindoEmbed, view=view)



async def setup(bot):
    await bot.add_cog(ExibirSeguindos(bot))
