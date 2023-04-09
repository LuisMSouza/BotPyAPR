import discord
import os
from dotenv import load_dotenv
from tinydb import Query, TinyDB

bot = discord.Bot(intents=discord.Intents.all())
load_dotenv()
db = TinyDB('data/data.json')


@bot.event
async def on_ready():
    print(f"[SOURCE] Logged as {bot.user}")


@bot.slash_command(guilds_ids=[os.environ['GUILD_ID']])
@discord.default_permissions(administrator=True)
async def info(ctx):
    User = Query()
    search = db.search(User.id == ctx.user.id)
    if not search:
        await ctx.respond(content="Nada encontrado", ephemeral=True)
        return
    


@bot.event
async def on_member_remove(member):
    guild_channels = member.guild.channels
    embed = discord.Embed()
    embed.description = f"{member}, saiu do servidor :("
    embed.set_footer(text=f"ID do usuário: {member.id}")
    embed.set_author(name=f"{member.display_name}",
                     icon_url=f"{member.display_avatar}")
    embed.set_thumbnail(url=f"{member.display_avatar}")
    embed.color = 15844367
    for channel in guild_channels:
        if channel.id == int("730839460903649351"):
            await channel.send(embed=embed)


@bot.event
async def on_member_join(member):
    guild_channels = member.guild.channels
    embed = discord.Embed()
    embed.description = f"Olá <@{member.id}>, conheça nossos serviços e produtos!"
    embed.title = "Bem vindo(a)!"
    embed.set_image(
        url="https://media.tenor.com/S5gJsF7DFdIAAAAd/bem-vindo.gif")
    embed.set_footer(text=f"ID do usuário: {member.id}")
    embed.set_author(name=f"{member.display_name}",
                     icon_url=f"{member.display_avatar}")
    embed.set_thumbnail(url=f"{member.display_avatar}")
    embed.color = 15844367
    for channel in guild_channels:
        if channel.id == int("727001878310944838"):
            await channel.send(content=f"<@{member.id}>", embed=embed)

bot.run(os.environ['TOKEN'])
