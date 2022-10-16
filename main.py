import disnake
from disnake.ext import commands

import os
import sqlite3

botVersion, botVersionDate = '', ''
with open("appconfig.ini", 'r', encoding='utf-8') as configsource:
    for line in configsource:
        line = line.split("=")
        if line[0] == "version":
            botVersion = str(line[1])[1:-2]
        if line[0] == "versiondate":
            botVersionDate = str(line[1])[1:-2]
        if line[0] == "isdebug":
            if line[1] == "True":
                botPrefix = 'b!'
                botToken = 'MTAwNzU2NzE1ODUwNDU5NTUzNg.GkTIIT._a1wwzi1Y80AxPPxJ9HNiWidshLMyhv95RU7TM'
            else:
                botPrefix = 'd!'
                botToken = 'OTk5NTYzMTQ0Mjc4MDYxMDg2.G4WkNX.KNbKgg82ULA1Renl8B-XWtWk0IJF0Ix864rcWA'

botColor = 0xf4a261
dev = [735371414533701672, 981234922800951307]

blacklist = []
with open("blacklist.txt", 'r', encoding='utf-8') as blsource:
    for line in blsource:
        blacklist.append(line)

bot = commands.Bot(command_prefix = commands.when_mentioned_or(botPrefix), intents = disnake.Intents.all(),
                   activity = disnake.Game("drewsupport.github.io"), status = disnake.Status.idle,
                   sync_commands_debug=True)
bot.remove_command('help')

conn = sqlite3.connect("guilds.db")
cur = conn.cursor()

# GENERAL
cur.execute("""CREATE TABLE IF NOT EXISTS access (guild INTEGER, role INTEGER)""")
# ROLES
cur.execute("""CREATE TABLE IF NOT EXISTS reactionrole (guild INTEGER, message INTEGER, role INTEGER, emoji STRING)""")
cur.execute("""CREATE TABLE IF NOT EXISTS autorole (guild INTEGER, role INTEGER)""")
# AUTOMODERATION
cur.execute("""CREATE TABLE IF NOT EXISTS banlink (guild INTEGER, type STRING, punish STRING, text STRING)""")
# MESSAGE EVENTS
cur.execute("""CREATE TABLE IF NOT EXISTS messageOnJoin (guild INTEGER, channel INTEGER, text STRING)""")
cur.execute("""CREATE TABLE IF NOT EXISTS messageOn (guild INTEGER, channel INTEGER, text STRING)""")

conn.commit()

# LOAD, UNLOAD AND RELOAD COGS
@bot.command(description="Средство разработки.")
async def load(ctx, extension):
    embed = disnake.Embed(title=f'Системное сообщение о статусе', color=botColor)
    if int(ctx.author.id) in dev:
        try:
            bot.load_extension(f"cogs.{extension}")
            embed.description = f"**{extension}** был успешно загружен!"
        except:
            embed.description = f"**{extension}** уже загружен либо такого файла нет!"
    else:
        embed.description = f"Загрузка **{extension}** была прервана:\nВы не разработчик или доверенное лицо!"
    await ctx.send(embed=embed)

@bot.command(description="Средство разработки.")
async def unload(ctx, extension):
    embed = disnake.Embed(title=f'Системное сообщение о статусе', color=botColor)
    if int(ctx.author.id) in dev:
        try:
            bot.unload_extension(f"cogs.{extension}")
            embed.description = f"**{extension}** был успешно выгружен."
        except:
            embed.description = f"**{extension}** уже выгружен либо такого файла нет!"
    else:
        embed.description = f"Выгрузка **{extension}** была прервана:\nВы не разработчик или доверенное лицо."
    await ctx.send(embed=embed)

@bot.command(aliases=["r"], description="Средство разработки.")
async def reload(ctx, extension="all"):
    embed = disnake.Embed(title=f'Системное сообщение о статусе', color=botColor)
    if int(ctx.author.id) in dev:
        if extension != "all":
            bot.unload_extension(f"cogs.{extension}")
            bot.load_extension(f"cogs.{extension}")
            embed.description = f"**{extension}** успешно перезагружен."
        else:
            for filename in os.listdir('./cogs'):
                if filename.endswith(".py"):
                    try: bot.load_extension(f"cogs.{filename[:-3]}")
                    except Exception:
                        bot.unload_extension(f"cogs.{filename[:-3]}")
                        bot.load_extension(f"cogs.{filename[:-3]}")
            embed.description = f"Все файлы были успешно перезагружены."
    else:
        embed.description = f"Перезагрузка **{extension}** была прервана:\nВы не разработчик или доверенное лицо."
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    embed = disnake.Embed(title=f'⚠️ : Важное объявление', color=botColor)
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1010121538953035786/1021288851148378132/unknown.png?width=607&height=607")
    embed.description = "Из-за новой политики Discord для ботов и их разработчиков, с 31 августа 2022 года была прекращена возможность использовать текстовые команды в ботах свыше 100 серверов. Мы желаем развития нашего бота, поэтому тоже перешли на новые слэш-команды. Чтобы получить весь список команд, теперь нужно написать /help, и выбрать соответствующую команду."
    await ctx.send(embed=embed)

@bot.command()
async def send(ctx, *, message):
    if ctx.author.id == 735371414533701672:
        if message == "!premium":
            embed = disnake.Embed(title=f'🎉 : Поздравляем, и спасибо!', color=botColor)
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1010121538953035786/1021288851148378132/unknown.png?width=607&height=607")
            embed.description = "Теперь на вашем сервере активирована улучшенная версия Дрю, с большими функциями и возможностями! Спасибо за то, что поддерживаете нас и нашего бота! Мы будем рады помочь вам на нашем [сервере поддержки](https://discord.gg/3Zhbx7uQtp), и ваши идеи для бота будут для нас в приоритете. Лисьи благодарности вам, спасибо за использование бота!"
            embed.set_footer(text="Рассылка. Дрю любит вас! ~<3")
            await ctx.send(embed=embed)
        else: await ctx.send(message)

#for filename in os.listdir('./cogs'):
#    if filename.endswith(".py"):
#        print(f"Загрузка файла: {filename}\nБраузер файлов: {os.listdir('./cogs')}")
#        bot.load_extension(f"cogs.{filename[:-3]}")

for a, b, files in os.walk('./cogs'):
    for file in files:
        print(f"Браузер файлов: \"{file}\" (f{a})")
        if file.endswith('.py'):
            print(f"Ког обнаружен: {file}")
            bot.load_extension(f"cogs.{file[:-3]}")

# RUN RELEASE OR DEBUG BOT
bot.run(botToken)