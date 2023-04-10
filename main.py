import discord
import os
from dotenv import load_dotenv
import sqlite3

bot = discord.Bot(intents=discord.Intents.all())
load_dotenv()
try:
    connection = sqlite3.connect("./data/db.sqlite")
    cur = connection.cursor()
except:
    print("[SOURCE] DATABASE NOT FOUND")


@bot.event
async def on_ready():
    print(f"[SOURCE] Logged as {bot.user}")
    try:
        getDbState = cur.execute("SELECT * FROM USERS")
    except:
        print("[SOURCE] USERS TABLE NOT EXISTS, CREATING...")
        cur.execute(
            "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, products TEXT)")


@bot.slash_command(guilds_ids=[os.environ['GUILD_ID']])
@discord.default_permissions(administrator=True)
async def create(ctx, usuario: discord.Option(discord.Member, 'Usuário a ser modificado')):
    embed = discord.Embed()
    embed.set_author(name=usuario.display_name, icon_url=usuario.display_avatar)
    embed.set_thumbnail(url=ctx.guild.icon)
    embed.color = 15844367
    embed.description = "```\nUtilize os botões abaixo para realizar alterações no usuário\n```"

    buttonAddProd = discord.ui.Button()
    buttonAddProd.custom_id = "addprod"
    buttonAddProd.style = discord.ButtonStyle.success
    buttonAddProd.label = "ADICIONAR PRODUTO"

    view = discord.ui.View()
    view.add_item(buttonAddProd)

    await ctx.respond(embed=embed, view=view, ephemeral=True)


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
