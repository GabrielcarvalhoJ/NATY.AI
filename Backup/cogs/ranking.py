import discord
from discord.ext import commands
from discord import app_commands
from cogs.jogo import ranking_dict  # Corrigido para importar de 'cogs.jogo'

class Ranking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ranking", description="Veja o ranking global por média de tempo")
    async def ranking(self, interaction: discord.Interaction):
        if not ranking_dict:
            await interaction.response.send_message("📉 Ainda não há rankings registrados.")
            return

        medias = {uid: sum(ts)/len(ts) for uid, ts in ranking_dict.items()}
        top = sorted(medias.items(), key=lambda x: x[1])[:10]

        embed = discord.Embed(
            title="⏱️ Ranking por Tempo Médio",
            description="Quanto menor o tempo, melhor! 🥇",
            color=discord.Color.blue()
        )

        medalhas = ["🥇", "🥈", "🥉"]
        for i, (uid, media) in enumerate(top, 1):
            user = await self.bot.fetch_user(uid)
            medalha = medalhas[i-1] if i <= 3 else f"**#{i}**"
            tentativas = len(ranking_dict[uid])
            embed.add_field(
                name=f"{medalha} {user.name}",
                value=f"Média: **{media:.2f}s** | Tentativas: `{tentativas}`",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Ranking(bot))
