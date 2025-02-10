import discord
from discord.ext import commands
from discord import app_commands
from models.Servidor import Manipular_Servidor
from models.Usuario import Manipular_Usuario
from models.Seguindo import Manipular_seguidor
from datetime import datetime
import pytz

class EmailView(discord.ui.View):
    def __init__(self, usuario, apelido, titulo, mensagem, imagem, link):
        super().__init__(timeout=None)
        self.usuario = usuario
        self.apelido = apelido
        self.titulo = titulo
        self.mensagem = mensagem
        self.imagem = imagem
        self.link = link
        self.fuso_brasilia = pytz.timezone("America/Sao_Paulo")


    def get_embem(self):
        embed = discord.Embed(
            title=f"{self.titulo}",
            description=f"{self.mensagem}",
            color=discord.Color.blue(),
        )
        if self.imagem:
            embed.set_image(url=self.imagem)
        agora = datetime.now(self.fuso_brasilia)
        agora_formatado = agora.strftime("%d/%m/%y")
        embed.set_footer(
                text=f"Enviado em: {agora_formatado}",
            )
        embed.set_author(name=self.apelido, icon_url=self.usuario.display_avatar.url)
        if self.link:
            embed.set_author(name=self.apelido, icon_url=self.usuario.display_avatar.url, url=self.link)
        return embed

    @discord.ui.button(label="Seguir", style=discord.ButtonStyle.primary)
    async def seguir_botao(self, interaction: discord.Interaction, button: discord.ui.Button):
        usuario = Manipular_Usuario.Obter_usuario(interaction.user.id)
        if not usuario:
            await interaction.response.send_message("Voce não criou uma conta", ephemeral=True)
            return
        if interaction.user.id == self.usuario.id:
            await interaction.response.send_message("Voce não pode deixar de seguir voce mesmo!", ephemeral=True)
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
            await interaction.response.send_message("Voce não pode seguir voce mesmo!", ephemeral=True)
            return
        seguidor = Manipular_seguidor.remover_seguidor(interaction.user.id, self.usuario.id)
        if seguidor:
            await interaction.response.send_message(f"Voce deixou de seguir {self.usuario.name}", ephemeral=True)
        elif seguidor == False:
            await interaction.response.send_message(f"Voce não segue esse usuario", ephemeral=True)


class EnviarEmail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="enviar_postagem", description="Envia um post para todos os servidores e quem te segue")
    async def EnviarEmail(self, interaction: discord.Interaction, titulo: str, mensagem: str, imagem: discord.Attachment = None, link:str = None):
        id_usuario = interaction.user.id
        imagem = (imagem or None)
        link = (link or None)
        print(interaction)
        usuario = Manipular_Usuario.Obter_usuario(id_usuario)
        if not usuario:
            await interaction.response.send_message("Voce não criou uma conta", ephemeral=True)
            return
        view = EmailView(interaction.user, usuario.apelido, titulo, mensagem, imagem, link)
        embedEmail = view.get_embem()
        feeds_lista = Manipular_Servidor.Obter_todos_feeds()
        print(feeds_lista)
        if feeds_lista:
            for feed in feeds_lista:
                channel = interaction.client.get_channel(feed.id_chat)
                if isinstance(channel, discord.TextChannel):
                    try:
                        await channel.send(embed=embedEmail, view=view)
                    except discord.DiscordException as error:
                        print(f"Erro ao enviar mensagem para {channel.name} : {error}")
        dms_seguidores = Manipular_seguidor.Obter_seguidores(id_usuario)
        if dms_seguidores:
            for seguidor in dms_seguidores:
                usuario_atual = interaction.client.get_user(seguidor.id_usuario_seguidor)
                try:
                    await usuario_atual.send(embed=embedEmail, view=view)
                except discord.DiscordException as error:
                        print(f"Erro ao enviar mensagem para {channel.name} : {error}")
        Manipular_Usuario.Atualiza_post(interaction.user.id)
        await interaction.response.send_message("Email enviado a todos!", ephemeral=True)


async def setup(bot):
    await bot.add_cog(EnviarEmail(bot))
