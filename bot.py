import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORDTOKEN")
COMPSERVER = int(os.getenv("COMPSERVER"))
RANKSERVER = int(os.getenv("RANKSERVER"))

ROLES = ["Advanced", "Expert", "Intermediate", "Novice"]

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(
    command_prefix="..",
    intents=intents
    )

@bot.event
async def on_ready():
    print(f"{bot.user} is up and running!")


async def sync(user_id: int):
    compServer = bot.get_guild(COMPSERVER)
    rankServer = bot.get_guild(RANKSERVER)

    compMember = compServer.get_member(user_id)
    rankMember = rankServer.get_member(user_id)

    if not compMember or not rankMember:
        return

    compRoles = {role.name for role in compMember.roles}
    rankRoles = {role.name: role for role in rankServer.roles}

    for roleName in ROLES:
        role = rankRoles.get(roleName)
        if not role:
            continue

        if roleName in compRoles:
            if role not in rankMember.roles:
                await rankMember.add_roles(role, reason="role sync")
        else:
            if role in rankMember.roles:
                await rankMember.remove_roles(role, reason="role sync")


@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    if after.guild.id == COMPSERVER:
        await sync(after.id)
        print("synced {member.id}")


@bot.event
async def on_member_join(member: discord.Member):
    if member.guild.id == RANKSERVER:
        await sync(member.id)
        print("synced {member.id}")

bot.run(TOKEN)
