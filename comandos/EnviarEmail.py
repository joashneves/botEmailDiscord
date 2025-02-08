import discord
from discord.ext import commands
from discord import app_commands
from models.Servidor import Manipular_Servidor
from models.Usuario import Manipular_Usuario

class EmailView(discord.ui.View):
    def __init__(self, interaction, titulo, mensagem, imagem):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.titulo = titulo
        self.mensagem = mensagem
        self.imagem = imagem

    def get_embem(self):
        embed = discord.Embed(
            title=f"{self.titulo}",
            description=f"{self.mensagem}",
            color=discord.Color.blue(),
        )
        if self.imagem:
            embed.set_image(url=self.imagem)
        embed.set_footer(
                text=f"Enviado por: {self.interaction.user.name}",
                icon_url=self.interaction.user.display_avatar.url,
            )
        return embed

class EnviarEmail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="enviar_postagem", description="Envia um post para todos os servidores e quem te segue")
    async def EnviarEmail(self, interaction: discord.Interaction, titulo: str, mensagem: str, imagem: discord.Attachment):
        id_usuario = interaction.user.id
        print(interaction)
        usuario = Manipular_Usuario.Obter_usuario(id_usuario)
        if not usuario:
            await interaction.response.send_message("Voce não criou uma conta", ephemeral=True)
            return
        view = EmailView(interaction, titulo, mensagem, imagem)
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
        

async def setup(bot):
    await bot.add_cog(EnviarEmail(bot))