# ENTERTAIMENT

#disnake
import disnake
from disnake.ext import commands

#other
import requests
import json
import random

#own
from main import botColor, blacklist
from replics import replic

class Ent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(description="Отправляет случайное фото лисы! ヾ(•ω• )o", aliases=["лис"])
    async def fox(self, ctx):
        if str(ctx.author.id) in str(blacklist):
            embed = disnake.Embed(title=replic['blacklist_error'][0], color=botColor)
            embed.description = replic['blacklist_error'][1]
            await ctx.send(embed=embed)

        response = requests.get('https://some-random-api.ml/img/fox')  # Get-запрос
        json_data = json.loads(response.text)  # Извлекаем JSON

        embed = disnake.Embed(color=botColor,
                            title='**🦊 : Случайно фото Лисички:**')  # Создание Embed'a
        embed.set_image(url=json_data['link'])  # Устанавливаем картинку Embed'a
        await ctx.send(embed=embed)  # Отправляем Embed


    @commands.slash_command(description="Отправляет случайное фото кошечки! ᓚᘏᗢ", aliases=["кот"])
    async def cat(self, ctx):
        if str(ctx.author.id) in str(blacklist):
            embed = disnake.Embed(title=replic['blacklist_error'][0], color=botColor)
            embed.description = replic['blacklist_error'][1]
            await ctx.send(embed=embed)

        response = requests.get('https://some-random-api.ml/img/cat')  # Get-запрос
        json_data = json.loads(response.text)  # Извлекаем JSON

        embed = disnake.Embed(color=botColor,
                            title='**😻 : Случайно фото Кошечки:**')  # Создание Embed'a
        embed.set_image(url=json_data['link'])  # Устанавливаем картинку Embed'a
        await ctx.send(embed=embed)  # Отправляем Embed


    @commands.slash_command(description="Отправляет случайное фото пёселя! ^-^", aliases=["пёс", "пес"])
    async def dog(self, ctx):
        if str(ctx.author.id) in str(blacklist):
            embed = disnake.Embed(title=replic['blacklist_error'][0], color=botColor)
            embed.description = replic['blacklist_error'][1]
            await ctx.send(embed=embed)

        response = requests.get('https://some-random-api.ml/img/dog')  # Get-запрос
        json_data = json.loads(response.text)  # Извлекаем JSON

        embed = disnake.Embed(color=botColor,
                            title='**🐶 : Случайно фото Пёсика:**')  # Создание Embed'a
        embed.set_image(url=json_data['link'])  # Устанавливаем картинку Embed'a
        await ctx.send(embed=embed)  # Отправляем Embed
    
    #@commands.command(aliases=["саня", "alexandr"])
    #async def sanya(self, ctx):
    #    photos = ["1010121568757755924/unknown.png", "1010121664572428288/unknown.png", "1010121779190190080/unknown.png", "1010122200889692251/Discord_PPbWZD5CHM.png",
    #              "1010122201179111484/Discord_bHpCoMIpXT.png", "1010122201476902912/Discord_t17PaYHqyt.png", "1010122201871155232/Discord_86WYFctA7Z.png",
    #              "1010122202173153350/Discord_3fhYpgV5ee.png", "1010128039931281418/Discord_OVw5J6DI1y.png", "1010128040354926623/Discord_Cfbf7wsUWD.png", "1010128715621072957/unknown.png",
    #              "1010128882806046841/unknown.png", "1010129311333879808/unknown.png", "1010129513969102878/unknown.png", "1010131814406443018/unknown.png"]
    #    photo = random.choice(photos)
    #    await ctx.send(f"https://media.discordapp.net/attachments/1010121538953035786/{photo}")
    
    @commands.command(aliases=["корольишут", "киш"])
    async def korolishut(self, ctx):
        await ctx.send("")


def setup(bot):
    bot.add_cog(Ent(bot))