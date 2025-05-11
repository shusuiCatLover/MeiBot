import discord
from discord.ext import commands
import random
import json
import os
import aiohttp
from datetime import datetime

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.guilds = True
intents.reactions = True
intents.message_content = True

CONFIG_FILE = "greet_config.json"
AUTOROLE_CONFIG_FILE = "autorole_config.json"
REACTION_ROLE_FILE = "reaction_roles.json"

def load_greet_channel():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file).get("greet_channel")
    return None

def save_greet_channel(channel_id):
    with open(CONFIG_FILE, "w") as file:
        json.dump({"greet_channel": channel_id}, file)

def load_autorole():
    if os.path.exists(AUTOROLE_CONFIG_FILE):
        with open(AUTOROLE_CONFIG_FILE, "r") as file:
            return json.load(file).get("autorole")
    return None

def save_autorole(role_id):
    with open(AUTOROLE_CONFIG_FILE, "w") as file:
        json.dump({"autorole": role_id}, file)

def load_reaction_roles():
    if os.path.exists(REACTION_ROLE_FILE):
        try:
            with open(REACTION_ROLE_FILE, "r") as file:
                content = file.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except json.JSONDecodeError:
            return {}
    return {}

def save_reaction_roles(data):
    with open(REACTION_ROLE_FILE, "w") as file:
        json.dump(data, file, indent=4)


# Lista de GIFs para boas-vindas
gifs = [
    "https://i.pinimg.com/originals/a0/90/c5/a090c5e7fc684e9fedaeab12869ff0c6.gif",
    "https://i.pinimg.com/originals/a8/bc/29/a8bc29ddeb018d9d32b488dcb6a1092f.gif",
    "https://i.pinimg.com/originals/8c/a3/9d/8ca39d6e212b131dee8d1ead530e9527.gif",
    "https://i.pinimg.com/originals/f5/f2/74/f5f27448c036af645c27467c789ad759.gif",
    "https://i.pinimg.com/originals/2f/43/76/2f437614d7fa7239696a8b34d5e41769.gif"
]

bot = commands.Bot(command_prefix=".", intents=intents)

def setup_general_commands(bot):
    @bot.command(name="addrole")
    @commands.has_permissions(administrator=True)
    async def addrole(ctx, role: discord.Role, message_id: int, emoji: str):
        data = load_reaction_roles()
        if str(message_id) not in data:
            data[str(message_id)] = {}
        data[str(message_id)][emoji] = role.id
        save_reaction_roles(data)

        embed = discord.Embed(
            title="✅ Reação de Cargo Adicionada",
            description=f"Reação {emoji} associada ao cargo {role.mention} na mensagem {message_id}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @bot.command(name="ajuda")
    async def ajuda(ctx):
        categories = {
            "⚔️ Moderação": """
            `kick (user) (reason)`: Expulsa um usuário do server.
            `ban (user) (reason)`: Bane um usuário do server.
            `clear (amount)`: Limpa mensagens.
            `ticket`: Cria um ticket de suporte.
            """,
            "🎶 Música": """
            `join`: Entra no canal de voz.
            `leave`: Sai do canal de voz.
            `play (link)`: Toca música.
            `stop`: Para a música.
            """,
            "🌀 Diversão": """
            `oi`: O bot te cumprimenta!
            `r (quantidade)d(tipo do dado)`: Rola dados.
            """,
            "🍰 RPG - Caketale": """
            `caketale`: Inicia a aventura no mundo do Caketale.
            `status`: Mostra o status do personagem.
            """
        }
        
        for category, description in categories.items():
            embed = discord.Embed(title=category, description=description, color=discord.Color.red())
            await ctx.send(embed=embed)

    @bot.command(name="autorole")
    @commands.has_permissions(administrator=True)
    async def autorole(ctx, role: discord.Role):
        save_autorole(role.id)

        embed = discord.Embed(
            title="✅ Cargo Automático Definido",
            description=f"Novos membros receberão automaticamente o cargo {role.mention}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @bot.command(name="oi", aliases=["ola", "Ola", "olá", "Olá", "hi", "hello", "hewwo"])
    async def oi(ctx):
        await ctx.send(f"Oi, {ctx.author.mention}! 👋")

    @bot.command(name="ping")
    async def ping(ctx):
        latency = bot.latency * 1000  # converte para milissegundos
        await ctx.send(f"🏓 Pong! Latência: `{latency:.2f}ms`")

    @bot.command(name="hora")
    async def hora(ctx):
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        await ctx.send(f"🕒 Agora são `{agora}`")

    @bot.command(name="avatar")
    async def avatar(ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(
            title=f"Avatar de {member.name}",
            color=discord.Color.blurple()
        )
        embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text="Apesar de tudo, ainda é você.")
        await ctx.send(embed=embed)

    @bot.command(name="wanted")
    async def wanted(ctx, member: discord.Member = None):
        member = member or ctx.author
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://nekobot.xyz/api/imagegen?type=wanted&url={avatar_url}") as resp:
                data = await resp.json()
                await ctx.send(data["message"])

    @bot.command(name="userinfo")
    async def userinfo(ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(
            title=f"Informações de {member}",
            color=discord.Color.blurple()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Nome", value=member.display_name, inline=True)
        embed.add_field(name="Entrou no servidor em", value=member.joined_at.strftime("%d/%m/%Y"), inline=False)
        embed.add_field(name="Conta criada em", value=member.created_at.strftime("%d/%m/%Y"), inline=False)
        await ctx.send(embed=embed)

    @bot.command(name="greet")
    @commands.has_permissions(administrator=True)
    async def set_greet_channel(ctx):
        save_greet_channel(ctx.channel.id)

        embed = discord.Embed(
            title="📢 Canal de Boas-vindas Definido",
            description=f"Canal de boas-vindas definido para {ctx.channel.mention}.",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @bot.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear(ctx, amount: int):
        if amount <= 0:
            await ctx.send("Por favor, especifique um número positivo de mensagens para apagar.", delete_after=5)
            return
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"{len(deleted)} mensagens apagadas.", delete_after=5)

@bot.event
async def on_member_join(member):
    greet_channel_id = load_greet_channel()
    
    if greet_channel_id:
        channel = bot.get_channel(greet_channel_id)
        
        if channel:
            selected_gif = random.choice(gifs)
            
            embed = discord.Embed(
                title="Bem-vindo!",
                description=f"Olá {member.mention}, seja bem-vindo ao servidor!",
                color=discord.Color.green()
            )
            embed.set_image(url=selected_gif)
            
            await channel.send(embed=embed)

    autorole_id = load_autorole()
    if autorole_id:
        role = member.guild.get_role(autorole_id)
        if role:
            await member.add_roles(role)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    REACTION_PROBABILITY = 0.2
    RANDOM_EMOJIS = ['✌️', '👋', '🐱', '❤️', '👀', '💅']

    if random.random() < REACTION_PROBABILITY:
        emoji = random.choice(RANDOM_EMOJIS)
        try:
            await message.add_reaction(emoji)
        except discord.HTTPException:
            pass

    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return

    data = load_reaction_roles()
    message_id = str(payload.message_id)
    if message_id in data and payload.emoji.name in data[message_id]:
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = guild.get_role(data[message_id][payload.emoji.name])
        if role and member:
            await member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    data = load_reaction_roles()
    message_id = str(payload.message_id)
    if message_id in data and payload.emoji.name in data[message_id]:
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = guild.get_role(data[message_id][payload.emoji.name])
        if role and member:
            await member.remove_roles(role)

def setup(bot):
    setup_general_commands(bot)