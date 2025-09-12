import os
import discord
from discord.ext import commands
import aiohttp
import json
import dotenv

# Charger le fichier .env
dotenv.load_dotenv()

# Charger les tokens depuis des variables d'environnement
SHAPES_API_KEY = os.environ.get("SHAPES_API_KEY")  # par exemple : LCT1S3D0OAY8ZGQPT5365JYQ0VUJIROSZKETRXI8TTI
SHAPE_USERNAME = os.environ.get("SHAPE_USERNAME")  # le nom de ton shape : “<shape-username>”
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")    # ton token Discord

# Vérification (optionnel mais conseillé)
if not SHAPES_API_KEY or not SHAPE_USERNAME or not DISCORD_TOKEN:
    raise ValueError("Les variables d'environnement SHAPES_API_KEY, SHAPE_USERNAME et DISCORD_TOKEN doivent être définies")

# Intents pour pouvoir lire les messages
intents = discord.Intents.default()
intents.message_content = True  # pour permettre au bot de lire le contenu des messages

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is ready.")

@bot.command(name="shape")
async def shape_command(ctx, *, user_text: str):
    """Commande qui envoie le texte à l’API Shapes et renvoie la réponse."""
    # Préparer la requête à Shapes.inc
    api_url = "https://api.shapes.inc/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {SHAPES_API_KEY}",
        "Content-Type": "application/json",
        "X-User-Id": str(ctx.author.id),    # optionnel mais recommandé pour le contexte utilisateur
        "X-Channel-Id": str(ctx.channel.id), # idem pour le contexte canal
    }
    body = {
        "model": f"shapesinc/{SHAPE_USERNAME}",
        "messages": [
            {"role": "user", "content": user_text}
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, headers=headers, json=body) as resp:
            if resp.status != 200:
                await ctx.reply("Désolé, l’API Shapes a renvoyé une erreur.")
                return
            resp_json = await resp.json()

    # On suppose que la réponse a ce format : resp_json["choices"][0]["message"]["content"]
    try:
        bot_reply = resp_json["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        await ctx.reply("Désolé, je n’ai pas compris la réponse de l’API.")
        return

    await ctx.reply(bot_reply)

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)