# EMBED CONTSTRUCT

#disnake
import disnake
from disnake.ext import commands

#other
import requests
import json
import random

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

        embed = disnake.Embed(title=replic["loading_text"], color=botColor)
        embed.description = random.choice(replic['loading'])
        await ctx.send(embed=embed)

        if str(ctx.author.id) in str(blacklist):
            embed = disnake.Embed(title=['blacklist_error'][0], color=botColor)
            embed.description = replic['blacklist_error'][1]
            await ctx.edit_original_message(embed=embed)
            return

        if title == None and description == None and thumbnail_url == None:
            embed = disnake.Embed(color=botColor, title=f"Это пример Embed'a")  # Создание Embed'a
            embed.description = f"Лисица, лиса, обыкнове́нная лиси́ца или ры́жая лиси́ца — хищное млекопитающее семейства псовых, наиболее распространённый и самый крупный вид рода лисиц. Длина тела 60—90 см, хвоста — 40—60 см, масса — 6—10 кг."
            embed.set_thumbnail(url=f"https://faunistics.com/wp-content/uploads/2019/05/1.jpg")  # Устанавливаем картинку Embed'a
            await ctx.delete_original_message()  # Удаляем сообщение проверки
            await ctx.channel.send(embed=embed)  # Отправляем Embed, как обычное сообщение
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
        await ctx.delete_original_message()  # Удаляем сообщение проверки
        await ctx.channel.send(embed=embed)  # Отправляем Embed, как обычное сообщение


def setup(bot):
    bot.add_cog(Emb(bot))