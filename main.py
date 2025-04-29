import discord
import time
import random
import asyncio
from discord.ext import commands
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import json

intents = discord.Intents.default()
intents.message_content = True

# Funções de Configuração
def carregar_configuracao():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"CANAL_PERMITIDO_ID": None}

def salvar_configuracao(config):
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

# Carregar configuração
config = carregar_configuracao()

bot = commands.Bot(command_prefix="!", intents=intents)

# Função assíncrona para carregar os Cogs
async def load_cogs():
    try:
        await bot.load_extension("cogs.jogo")  # Certifique-se de que os cogs estão no diretório cogs
        print("✅ Cog 'jogo' carregado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao carregar o Cog 'jogo': {e}")

    try:
        await bot.load_extension("cogs.ranking")
        print("✅ Cog 'ranking' carregado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao carregar o Cog 'ranking': {e}")

    try:
        await bot.load_extension("cogs.perfil")
        print("✅ Cog 'perfil' carregado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao carregar o Cog 'perfil': {e}")

# Criação de comando '/configurar_canal' no Cog

class Configuracao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="configurar_canal", description="Configure o canal permitido para os jogos. (Admin)")
    @app_commands.checks.has_permissions(administrator=True)
    async def configurar_canal(self, interaction: discord.Interaction, canal: discord.TextChannel):
        config["CANAL_PERMITIDO_ID"] = canal.id
        salvar_configuracao(config)
        await interaction.response.send_message(f"✅ Canal permitido configurado para {canal.mention} com sucesso!")

# Adicionando o Cog 'Configuração'
async def setup_hook():
    await load_cogs()
    # Carregar o cog 'configuracao' que contém o comando /configurar_canal
    await bot.add_cog(Configuracao(bot))

# Chama o setup_hook ao iniciar o bot
bot.setup_hook = setup_hook

@bot.event
async def on_ready():
    await bot.tree.sync()  # sincroniza GLOBAL apenas UMA vez
    print(f"🤖 {bot.user} está online e comandos sincronizados globalmente!")

bot.run("TOKEN")
