# SETTINGS

#disnake
import disnake
from disnake.ext import commands

#other

#own
from main import *
from replic import replic

whitelist = []


class Aud(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #@commands.command()
    async def banlink(ctx, type, *, punish):
        cur.execute("""SELECT type, punish FROM banlink WHERE guild = ?""", (ctx.guild.id,))
        status = cur.fetchone()


        if type == "all" or type == "invite" or type == "off": pass
        else:
            embed = disnake.Embed(title='Ошибка!', color=botColor)
            embed.description = "Возникла ошибка при попытки добавлении типа блокировки ссылок. Проверьте правильность введённых данных."
            await ctx.send(embed=embed)
            return

        if str(ctx.author.id) not in str(blacklist):
            puncom = punish.split()
            if puncom[0] == "mute":
                try:
                    to_time(puncom[1])
                    cur.execute("""UPDATE banlink SET type = ? AND punish = ? WHERE guild = ?""", (type, punish, ctx.guild.id,))
                    conn.commit()
                except:
                    embed = disnake.Embed(title='Ошибка!', color=botColor)
                    embed.description = "Возникла ошибка при попытки добавления наказания — мьют. Проверьте правильность введённых данных."
                    await ctx.send(embed=embed)

        else:
            embed = disnake.Embed(title='Отказано в доступе', color=botColor)
            embed.description = replic['blacklist_message']
            await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, ctx):
        cur.execute("""SELECT type, punish FROM banlink WHERE guild = ?""", (ctx.guild.id,))
        content = cur.fetchone()

        all_links = ["https://", "http://"]
        invite_links = ["https://discord.gg/", "discord.gg/", "discord.com/invite/"]
        white_links = ["tenor.com", "media.discordapp.net", "discordapp.net"]
        white_format = [".mp4", ".gif", ".png", ".bmp", ".jpg", ".jpeg", ".mpeg", ".svg"]
        
        if content[0] == "all":
            for i in all_links:
                if i in ctx.content:
                    for y in white_links:
                        if y not in ctx.content:
                            if ctx.content[-4:] not in white_format:

                                if "mute" in content[1]:
                                    await ctx.author.timeout(duration=to_time( str( content[1] )[-2:] ), reason=f"Автомодерация. Отправление ссылки: {ctx.author}({ctx.author.id}).")
                                elif "kick" in content[1]:
                                    await ctx.guild.timeout(user=ctx.author, duration=to_time( str( content[1] )[-2:-1] ), reason=f"Дал мьют(таймаут): {ctx.author}({ctx.author.id}).")

                                embed = disnake.Embed(title='Автомодерация!', color=botColor)
                                embed.description = f"Участник **{ctx.author}** (ID: {ctx.author.id}) попал под систему автомодерации, за **отправление ссылки**, что запрещено на этом сервере.\nНаказание: {content[1]}"
                                await ctx.reply(embed=embed)
                                return

        elif content[0] == "invite":
            for i in invite_links:
                if i in ctx.content:
                    if ctx.content in ctx.content:

                        if "mute" in content[1]:
                            await ctx.author.timeout(duration=to_time( str( content[1] )[-2:] ), reason=f"Автомодерация. Отправление ссылки-приглашения: {ctx.author}({ctx.author.id}).")  
                        elif "kick" in content[1]:
                            ctx.guild.timeout(user=ctx.author, duration=to_time( str( content[1] )[-2:-1] ), reason=f"Дал мьют(таймаут): {ctx.author}({ctx.author.id}).")
                        
                        embed = disnake.Embed(title='Автомодерация!', color=botColor)
                        embed.description = f"Участник **{ctx.author}** (ID: {ctx.author.id}) попал под систему автомодерации, за **отправление ссылки-приглашения**, что запрещено на этом сервере.\nНаказание: {content[1]}"
                        await ctx.reply(embed=embed)
                        return
                        

def to_time(string):
    date_types = {
    "s": 1,
    "m": 60,
    "h": 60*60,
    "d": 60*60*24,
    "w": 60*60*24*7,
    "M": 60*60*24*30,
    "y": 60*60*24*365,
    "с": 1,
    "м": 60,
    "ч": 60*60,
    "д": 60*60*24,
    "н": 60*60*24*7,
    "М": 60*60*24*30,
    "г": 60*60*24*365,
    "л": 60*60*24*365,
    }
    letter = string[-1]
    if letter not in date_types:
        return
    try:
        a = int(string[:-1])
        return a * date_types[letter]
    except Exception:
        return


def setup(bot):
    bot.add_cog(Aud(bot))