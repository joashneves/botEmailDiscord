import discord
from discord.ext import commands
from discord import app_commands

tutorial = [ {"titulo": "Registrando",
               "descricao": "para se registrar no bot, voce precisa escrever `/registrar`, assim que voce confirma, ira aparecer um modal para voce prencher com nome, descrição, e pronome, sendo que o **nome voce não pode alterar depois**, mas se quiser trocar voce pode colocar o comando denovo, outro **aviso é que o servidor que voce se registrar vai ficar salvo como o servidor que voce se registrou**",
               "link": "https://github.com/joashneves/botEmailDiscord"},
            {"titulo": "Enviando email",
              "descricao": "Para enviar a postagem para todos os seus seguidores, basta escrever o comando `/enviar_postagem` que quem te segue e todos os canais do discord que estiverem configurado, para quem estiver te seguindo ele enviara no privado dessa pessoa, voce pode atribui link na sua postagem, ou pode tambem colocar imagem, sendo esses dois opcionais",
              "link": "https://github.com/joashneves/botEmailDiscord"},
              {"titulo": "Colocando rede social",
              "descricao": "Para colocar 1 de 5 redes sociais, voce pode usar o comando `/colocar_rede_social` que vai exigir o nome da sua rede social, e um link para ele, assim quando alguem usar o comando `/perfil` a pessoa vai ver suas redes sociais",
              "link": "https://github.com/joashneves/botEmailDiscord"},
              {"titulo": "Seguidores e seguindo",
              "descricao": "Conforme as pessoas enviam postagem, um botão de seguir ira aparecer, ao clicar naquele botão voce vai começar a seguir a pessoa, e ao seguir da pessoa todas as postagens da pessoa que voce esta seguindo irão aparecer no seu privado, caso deseje parar de seguir, é só clicar no botão **deixar de seguir**, e caso voce queira ver quem voce esta seguindo voce tem o comando `/exibir_seguindo` assim voce exibe uma lista de quem esta seguindo",
              "link": "https://github.com/joashneves/botEmailDiscord"},]

class ViewTutorial(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.index = 0

    def get_embed(self):
        tutoria_embed = tutorial[self.index]
        print(tutoria_embed)
        embed = discord.Embed(title=f"{tutoria_embed["titulo"]}",
            description=f"{tutoria_embed["descricao"]}",
            url=f"{tutoria_embed["link"]}",
            color=discord.Color.blue(),
            )
        return embed

    def update_buttons(self):
        """Atualiza o estado dos botões conforme a página atual."""
        self.clear_items()  # Remove botões antigos
        self.add_item(self.Anterior)
        self.add_item(self.Proximo)

    @discord.ui.button(label="<<<", custom_id="tutorial_botao_anterior", style=discord.ButtonStyle.primary)
    async def Anterior(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.index = (self.index - 1) % len(tutorial)
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label=">>>", custom_id="tutorial_botao_proximo", style=discord.ButtonStyle.primary)
    async def Proximo(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.index = (self.index + 1) % len(tutorial)
        await interaction.response.edit_message(embed=self.get_embed(), view=self)


class Tutorial(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Exibe um tutorial do bot!")
    async def tutorial(self, interaction: discord.Interaction):
        view = ViewTutorial()
        tutoria_embed = tutorial[0]
        print(tutoria_embed)
        embed = discord.Embed(title=f"{tutoria_embed["titulo"]}",
            description=f"{tutoria_embed["descricao"]}",
            url=f"{tutoria_embed["link"]}",
            color=discord.Color.blue(),
            )
        await interaction.response.send_message(view=view, embed=embed)

async def setup(bot):
    await bot.add_cog(Tutorial(bot))
