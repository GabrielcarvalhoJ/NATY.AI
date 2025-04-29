import discord
from discord.ext import commands
from discord import app_commands

class Perfil(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="perfil", description="Veja o perfil do bot e como utilizá-lo")
    async def perfil(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤖 Perfil da Naty.AI",
            description="Olá! Eu sou a **Naty.AI**, sua companheira nos desafios de digitação! ⌨️🔥",
            color=discord.Color.purple()
        )
        embed.add_field(
            name="📚 Sobre mim",
            value="Fui criada para testar e melhorar sua velocidade de digitação com jogos rápidos e divertidos.",
            inline=False
        )
        embed.add_field(
            name="🛠️ Como usar",
            value=(
                "**/digitar** - Inicia um desafio\n"
                "**/ranking** - Mostra o ranking\n"
                "**/perfil** - Este menu"
            ),
            inline=False
        )
        embed.set_footer(text="Divirta-se com a Naty.AI! 🚀")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Perfil(bot))
