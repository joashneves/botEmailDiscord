import discord
from discord.ext import commands
from discord.ui import Button
from discord import app_commands
from models.Usuario import Manipular_Usuario
from models.Servidor import Manipular_Servidor
from models.Seguindo import Manipular_seguidor
from models.RedeSocial import Manipular_redesSociais

class PerfilView(discord.ui.View):
    foo : bool = False
    def __init__(self, usuario ,apelido, descricao, pronome, post, id_Servidor):
        super().__init__(timeout=None)
        self.usuario = usuario
        self.apelido = apelido or "N/a"
        self.descricao = descricao
        self.pronome = pronome
        self.post = post
        self.servidor = Manipular_Servidor.Obter_servidor(id_Servidor)
        quantidade_seguidores = Manipular_seguidor.Obter_seguidores(usuario.id) or []
        self.quantidade_seguidores = len(quantidade_seguidores) or 0
        redesSociais = Manipular_redesSociais.Obter_redes_de_usuario(usuario.id)
        for rede in redesSociais:
            print(rede.link, rede.nome)
            botao = discord.ui.Button(label=f"{rede.nome}", style=discord.ButtonStyle.link, url=f"{rede.link}")
            self.add_item(item=botao)

    def get_embem(self):
        embed = discord.Embed(
            title=f'Perfil de : {self.apelido}',
            description=f'Bio : {self.descricao}',
            color=discord.Color.magenta()
        )
        embed.add_field(name="Pronomes", value=f"{self.pronome}", inline=True)
        embed.add_field(name="Posts", value=f"{self.post}", inline=True)
        embed.add_field(name="Seguidores!", value=f"{self.quantidade_seguidores}", inline=True)
        embed.set_thumbnail(url=self.usuario.avatar.url)
        embed.set_footer(text=f'Servidor origem: {self.servidor.email}')
        return embed

    @discord.ui.button(label="Seguir", style=discord.ButtonStyle.primary)
    async def seguir_botao(self, interaction: discord.Interaction, button: discord.ui.Button):
        usuario = Manipular_Usuario.Obter_usuario(interaction.user.id)
        if not usuario:
            await interaction.response.send_message("Voce não criou uma conta", ephemeral=True)
            return
        if interaction.user.id == self.usuario.id:
            await interaction.response.send_message("Voce não pode seguir voce mesmo!", ephemeral=True)
            return
        elif interaction.user.id != self.usuario.id:
            seguindo = Manipular_seguidor.Seguir_pessoa(interaction.user.id, self.usuario.id)
            if seguindo == True:
                await interaction.response.send_message(f"Voce agora esta seguindo {self.usuario.name}!", ephemeral=True)
            elif seguindo == False:
                await interaction.response.send_message(f"Voce ja esta seguindo {self.usuario.name}!", ephemeral=True)
            return

    @discord.ui.button(label="deixar de seguir", style=discord.ButtonStyle.red)
    async def deixar_seguir(self, interaction: discord.Interaction, button: discord.ui.Button):
        usuario = Manipular_Usuario.Obter_usuario(interaction.user.id)
        if not usuario:
            await interaction.response.send_message("Voce não criou uma conta", ephemeral=True)
            return
        if interaction.user.id == self.usuario.id:
            await interaction.response.send_message("Voce não pode deixar de seguir voce mesmo!", ephemeral=True)
            return
        seguidor = Manipular_seguidor.remover_seguidor(interaction.user.id, self.usuario.id)
        if seguidor == True:
            await interaction.response.send_message(f"Voce deixou de seguir {self.usuario.name}", ephemeral=True)
        elif seguidor == False:
            await interaction.response.send_message(f"Voce não segue esse usuario", ephemeral=True)


class Perfil(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="perfil", description="Captura um perfil ou seu proprio")
    async def exibir_perfil(self, interaction: discord.Interaction, usuario: discord.User = None):
        usuario = (usuario or interaction.user)
        usuario_encontrado = Manipular_Usuario.Obter_usuario(usuario.id)
        if not usuario_encontrado:
            await interaction.response.send_message(f'Usuario não existe', ephemeral=True)
            return
        view = PerfilView(usuario, usuario_encontrado.apelido, usuario_encontrado.descricao,
                          usuario_encontrado.pronome, usuario_encontrado.post, usuario_encontrado.id_ServidorBase)
        embed = view.get_embem()
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Perfil(bot))
