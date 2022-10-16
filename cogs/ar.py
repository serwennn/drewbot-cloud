# ENTERTAIMENT

#disnake
import disnake
from disnake.ext import commands
from disnake import utils

#other

#own
from main import botColor, blacklist, cur, conn
from replics import replic

class Aur(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        cur.execute("""SELECT role FROM autorole WHERE guild = ?""", (member.guild.id,))
        content = cur.fetchall()

        for exemp in content:
            role = utils.get(member.guild.roles, id=exemp[0])
            print(role)
            print(exemp)
            await member.add_roles(role, reason="Автороли. Присоединение к серверу.")

def setup(bot):
    bot.add_cog(Aur(bot))