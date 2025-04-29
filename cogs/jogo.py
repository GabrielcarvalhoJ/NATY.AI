import discord
import random
import time
import asyncio
from discord.ext import commands
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# Verifique se a importação da configuração está correta
from utils.config import config  # <- Certifique-se de que está importando corretamente

ranking_dict = {}

def generate_text_image(text):
    largura, altura = 800, 200
    img = Image.new("RGB", (largura, altura), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 30)
    except IOError:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    text_x = (largura - (bbox[2] - bbox[0])) // 2
    text_y = (altura - (bbox[3] - bbox[1])) // 2
    draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font)
    buffer = BytesIO()
    img.save(buffer, 'PNG')
    buffer.seek(0)
    return buffer

def start_typing_test():
    phrases = [
        "O rato roeu a roupa do rei de Roma.",
        "Quem com ferro fere, com ferro será ferido",
        "A prática leva à perfeição.",
        "Não deixe para amanhã o que pode fazer hoje.",
        "Água mole em pedra dura, tanto bate até que fura",
        "Mais vale um pássaro na mão do que dois voando.",
        "De grão em grão, a galinha enche o papo.",
        "Quem espera sempre alcança.",
        "Casa de ferreiro, espeto de pau.",
        "Deus ajuda quem cedo madruga."
    ]
    phrase = random.choice(phrases)
    return phrase, generate_text_image(phrase)

class Jogo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="digitar", description="Teste sua velocidade de digitação com estilo!")
    async def start_typing(self, interaction: discord.Interaction):
        canal_permitido_id = config.get("CANAL_PERMITIDO_ID")

        if canal_permitido_id is None:
            await interaction.response.send_message(
                "⚠️ O canal permitido ainda não foi configurado. Use `/configurar_canal` para definir!",
                ephemeral=True
            )
            return

        if interaction.channel.id != int(canal_permitido_id):
            canal = self.bot.get_channel(int(canal_permitido_id))
            await interaction.response.send_message(
                f"❌ Este jogo só pode ser jogado no canal: {canal.mention}",
                ephemeral=True
            )
            return

        phrase, image_buffer = start_typing_test()
        await interaction.response.send_message("📝 **Desafio iniciado!** Digite a frase abaixo o mais rápido que puder:")
        mensagem_frase = await interaction.channel.send(file=discord.File(image_buffer, filename='text.png'))

        start_time = time.time()
        limit = 30

        while True:
            try:
                msg = await self.bot.wait_for(
                    'message',
                    timeout=limit - (time.time() - start_time),
                    check=lambda m: m.author == interaction.user and m.channel == interaction.channel
                )

                if msg.content.strip() == phrase:
                    elapsed = time.time() - start_time
                    uid = interaction.user.id
                    ranking_dict.setdefault(uid, []).append(elapsed)
                    await interaction.channel.send(
                        f"🎉 **Parabéns, {interaction.user.mention}!** Você fez em **{elapsed:.2f} segundos**!"
                    )
                    await mensagem_frase.delete()
                    await msg.delete()
                    break
                else:
                    remaining = limit - (time.time() - start_time)
                    await interaction.channel.send(f"❌ **Errado!** Tente de novo. ⏳ Tempo: **{remaining:.2f}s**")

            except asyncio.TimeoutError:
                await interaction.channel.send("⏰ **Tempo esgotado!**")
                await mensagem_frase.delete()
                break

async def setup(bot):
    await bot.add_cog(Jogo(bot))