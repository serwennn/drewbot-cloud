# EMBED CONTSTRUCT

#disnake
import disnake
from disnake.ext import commands

#other
import requests
import json

#own
from main import botColor, blacklist, cur, conn
from replics import replic

class Emb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(description="Создание эмбеда через бота.")
    async def embed(self, ctx, title=None, description=None, thumbnail_url=None):

        # ACCESS CHECK
        access = cur.execute("""SELECT role FROM access WHERE guild = ?""", (ctx.guild.id,)).fetchone()
        if access != None:
            for role in ctx.author.roles:
                if role.id not in access: isAccessed = False
                else: isAccessed = True; break
            if isAccessed == False and int(ctx.author.id) != int(ctx.guild.owner_id): await ctx.send(embed = disnake.Embed(title=replic['error'], description="У вас нет доступа к этой функции!", color=botColor)); return
        else:
            if ctx.author.id != ctx.guild.owner_id: await ctx.send(embed = disnake.Embed(title=replic['error'], description="У вас нет доступа к этой функции!", color=botColor)); return
        # END CHECK

        if str(ctx.author.id) in str(blacklist):
            embed = disnake.Embed(title=['blacklist_error'][0], color=botColor)
            embed.description = replic['blacklist_error'][1]
            await ctx.send(embed=embed)
            return

        if title == None and description == None and thumbnail_url == None:
            embed = disnake.Embed(color=botColor, title=f"Заголовок")  # Создание Embed'a
            embed.description = f"Какое-то описание эмбеда, фыр. Алекса́ндр Серге́евич Пу́шкин — русский поэт, драматург и прозаик, заложивший основы русского реалистического направления, литературный критик и теоретик литературы, историк, публицист, журналист. Один из самых авторитетных литературных деятелей первой трети XIX века."
            embed.set_thumbnail(url=f"http://t3.gstatic.com/licensed-image?q=tbn:ANd9GcTBRwzHpl8wDuliAEf_9vscFznaLQHZtUZvukHOwhaIJOqQW8ZyUHamhNjd5DntNVR3")  # Устанавливаем картинку Embed'a
            await ctx.send(embed=embed)  # Отправляем Embed
            return
    
        if title == None or description == None:
            embed = disnake.Embed(color=botColor, title=replic['error'])  # Создание Embed'a
            embed.description = f"Были введены неправильные данные. Заголовок и описание не могут быть пустыми."
        else:
            embed = disnake.Embed(color=botColor, title=f"{title}")  # Создание Embed'a
            embed.description = f"{description}"
            if thumbnail_url != None:
                embed.set_thumbnail(url=f"{thumbnail_url}")  # Устанавливаем картинку Embed'a
        
        if ctx.author.avatar != None: embed.set_footer(text=f"Автор: {ctx.author}", icon_url=ctx.author.avatar)
        else: embed.set_footer(text=f"Автор: {ctx.author}")
        await ctx.send(embed=embed)  # Отправляем Embed


def setup(bot):
    bot.add_cog(Emb(bot))