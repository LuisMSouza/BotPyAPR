import discord
import os
from dotenv import load_dotenv
import sqlite3
import mercadopago
from utils.validator import validate_cpf, validate_email

bot = discord.Bot(intents=discord.Intents.all())
load_dotenv()
sdk = mercadopago.SDK(os.environ['MP_TOKEN'])

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


@bot.slash_command(guilds_ids=[os.environ['GUILD_ID']], name="ticket", description="Envia a mensagem de ticket", custom_id="teste")
@discord.default_permissions(administrator=True)
async def ticket(ctx):
    embedTicket = discord.Embed()
    embedTicket.set_thumbnail(url=ctx.guild.icon)
    embedTicket.description = "> __**Como abrir um ticket?**__\n```\nBasta clicar no botão abaixo dessa mensagem e em seguida informe seu nome e sobre o que se trata o ticket, em seguida, será criado um novo ambiente para que você possa conversar diretamente com nossa equipe.\n```"
    embedTicket.set_image(url="")
    embedTicket.color = 2829617

    buttonTicket = discord.ui.Button()
    buttonTicket.custom_id = "ticket"
    buttonTicket.style = discord.ButtonStyle.success
    buttonTicket.label = "ABRIR TICKET"
    buttonTicket.emoji = "<:email:1096099607643168800>"

    view = discord.ui.View()
    view.add_item(buttonTicket)
    await ctx.channel.send(embeds=[embedTicket], view=view)
    await ctx.respond(content="Mensagem enviada", ephemeral=True)


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


@bot.event
async def on_interaction(interaction):
    if interaction.type == discord.InteractionType.application_command:
        if interaction.data['name'] == 'ticket':
            embedTicket = discord.Embed()
            embedTicket.set_thumbnail(url=interaction.guild.icon)
            embedTicket.description = "> __**Como abrir um ticket?**__\n```\nBasta clicar no botão abaixo dessa mensagem e em seguida informe seu nome e sobre o que se trata o ticket, em seguida, será criado um novo ambiente para que você possa conversar diretamente com nossa equipe.\n```"
            embedTicket.set_image(url="")
            embedTicket.color = 2829617

            buttonTicket = discord.ui.Button()
            buttonTicket.custom_id = "ticket"
            buttonTicket.style = discord.ButtonStyle.success
            buttonTicket.label = "ABRIR TICKET"
            buttonTicket.emoji = "<:email:1096099607643168800>"

            view = discord.ui.View()
            view.add_item(buttonTicket)
            await interaction.channel.send(embeds=[embedTicket], view=view)
            await interaction.response.send_message(content="```\nMensagem enviada\n```", ephemeral=True)

    if interaction.type == discord.InteractionType.component:
        if interaction.custom_id == "ticket":
            channels = await interaction.guild.fetch_channels()
                    

bot.run(os.environ['TOKEN'])
