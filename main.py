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
                botToken = 'MTAwNzU2NzE1ODUwNDU5NTUzNg.G8-eem.kO2oMXnJHgzXJGO6DkDiHyx1xnfFCKa3yvyUOw'
            else:
                botPrefix = 'd!'
                botToken = 'OTk5NTYzMTQ0Mjc4MDYxMDg2.GNsLXT.Mzvg_W6U3ymtSggSq8O7VH7msJGQJvuXnw9MRg'

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
cur.execute("""CREATE TABLE IF NOT EXISTS banspam (guild INTEGER, spamcount INTEGER, spamtime INTEGER, punish STRING, text STRING)""")
cur.execute("""CREATE TABLE IF NOT EXISTS banlink (guild INTEGER, type STRING, punish STRING, text STRING)""")
# MESSAGE EVENTS
cur.execute("""CREATE TABLE IF NOT EXISTS messageOnJoin (guild INTEGER, channel INTEGER, text STRING)""")
cur.execute("""CREATE TABLE IF NOT EXISTS messageOn (guild INTEGER, channel INTEGER, text STRING)""")

conn.commit()

# LOAD, UNLOAD AND RELOAD COGS
@bot.command(description="Средство разработки.")
async def load(ctx, extension):
    embed = disnake.Embed(title=f'Жүйе күйінің хабары', color=botColor)
    if int(ctx.author.id) in dev:
        try:
            bot.load_extension(f"cogs.{extension}")
            embed.description = f"**{extension}** сәтті жүктелді!"
        except:
            embed.description = f"**{extension}** әлдеқашан жүктелген немесе ондай файл жоқ!"
    else:
        embed.description = f"**{extension}**-ды(ты) жүктеп салу үзілді:\nСіз әзірлеуші немесе сенімді адам емеспіз!"
    await ctx.send(embed=embed)

@bot.command(description="Средство разработки.")
async def unload(ctx, extension):
    embed = disnake.Embed(title=f'Жүйе күйінің хабары', color=botColor)
    if int(ctx.author.id) in dev:
        try:
            bot.unload_extension(f"cogs.{extension}")
            embed.description = f"**{extension}** сәтті тоқтады!"
        except:
            embed.description = f"**{extension}** әлдеқашан тоқтап қалды немесе ондай файл жоқ!"
    else:
        embed.description = f"**{extension}**-ды(ты) тоқтату үзілді:\nСіз әзірлеуші немесе сенімді адам емеспіз!"
    await ctx.send(embed=embed)

@bot.command(aliases=["r"], description="Средство разработки.")
async def reload(ctx, extension="all"):
    embed = disnake.Embed(title=f'Жүйе күйінің хабары', color=botColor)
    if int(ctx.author.id) in dev:
        if extension != "all":
            bot.unload_extension(f"cogs.{extension}")
            bot.load_extension(f"cogs.{extension}")
            embed.description = f"**{extension}** сәтті қайта жүктелді."
        else:
            for filename in os.listdir('./cogs'):
                if filename.endswith(".py"):
                    try: bot.load_extension(f"cogs.{filename[:-3]}")
                    except Exception:
                        bot.unload_extension(f"cogs.{filename[:-3]}")
                        bot.load_extension(f"cogs.{filename[:-3]}")
            embed.description = f"Барлық файлдар сәтті қайта жүктелді."
    else:
        embed.description = f"**{extension}**-ды(ты) қайта жүктеу үзілді:\nСіз әзірлеуші немесе сенімді адам емеспіз!"
    await ctx.send(embed=embed)


# OTHER
@bot.command()
async def help(ctx):
    embed = disnake.Embed(title=f'⚠️ : Важное объявление', color=botColor)
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1010121538953035786/1021288851148378132/unknown.png?width=607&height=607")
    embed.description = "Из-за новой политики Discord для ботов и их разработчиков, с 31 августа 2022 года была прекращена возможность использовать текстовые команды в ботах свыше 100 серверов. Мы желаем развития нашего бота, поэтому тоже перешли на новые слэш-команды. Чтобы получить весь список команд, теперь нужно написать /help, и выбрать соответствующую команду."
    await ctx.send(embed=embed)

@bot.event
async def on_guild_join(guild):
    channel = guild.text_channels[0]

    if str(guild.owner_id) not in blacklist:
        embed = disnake.Embed(title=f'<:logopng:1028692260000383147> Привет, **{guild}**!', color=botColor)
        embed.description=f"""Спасибо, что добавили меня на **{guild}**! Я многофункциональный обладатель рыжих лапок, который поможет вам в настройке вашего сервера. Если у вас возникли вопросы, вы можете задать их на [сервере поддержки](https://discord.gg/B9mQ26fCWN) DrewBot. А теперь я бы хотел рассказать вам о некоторых моих преимуществах:"""
        embed.add_field(name="🥢 : **Роли за реакции**", value="Одна из удобнейших настроек ролей за реакции! Можно добавить вплоть до 20 экземпляров ролей за реакции на один сервер!", inline=False)
        embed.add_field(name="🍀 : **Автороли**", value="Такие же удобные и простые в настройки автороли! Вплоть до 10 экземпляров авторолей на один сервер!", inline=False)
        embed.add_field(name="🍂 : **Сообщения о приходе/уходе участников**", value="Вы можете задать с каким текстом и в какой канал будет отправляться сообщение о приходе (а также уходе, но его нужно настроить отдельно) участника!", inline=False)
        embed.add_field(name="🏮 : **Развлечения**", value="Случайные гифки и картинки животных и многое другое, что вам абсолютно не нужно, но возможно чуть чуть развлечет участников вашего сервера!", inline=False)
        embed.add_field(name="🌸 : **Базовые команды модерации**", value="Самые обыкновенные команды, которые копируют абсолютно весь функционал обычных функции Discord, но пусть будет!", inline=False)
        embed.add_field(name="🦾 : **Гибкая настройка**", value="Большинство команд можно гибко настроить под себя и свой сервер!", inline=False)
        embed.add_field(name="⏳ : **Автомодерация**", value="А вот это появится в скором будущем...", inline=False)
        
        embed.set_footer(text=f"Создатель: seltfox#2356. Все права под защитой рыжих лапок. Версия: {botVersion} ({botVersionDate})")
        await channel.send(embed=embed)
    else:
        embed = disnake.Embed(title=f'\*Грустный фырк\*', color=botColor)
        embed.description = f"Спасибо, что добавили меня на **{guild}**, но к сожалению я не смогу работать тут, так как создатель сервера находится в черном списке бота. Если у вас возникли вопросы, вы можете задать их на [сервере поддержки](https://discord.gg/B9mQ26fCWN) DrewBot."
        await channel.send(embed=embed)
        await guild.leave()

@bot.command()
async def onguild(ctx):
    embed = disnake.Embed(title=f'<:logopng:1028692260000383147> Привет, **{ctx.guild}**!', color=botColor)
    embed.description=f"""Спасибо, что добавили меня на **{ctx.guild}**! Я многофункциональный обладатель рыжих лапок, который поможет вам в настройке вашего сервера. Если у вас возникли вопросы, вы можете задать их на [сервере поддержки](https://discord.gg/B9mQ26fCWN) DrewBot. А теперь я бы хотел рассказать вам о некоторых моих преимуществах:"""
    embed.add_field(name="`🥢` : **Роли за реакции**", value="Одна из удобнейших настроек ролей за реакции! Можно добавить вплоть до 20 экземпляров ролей за реакции на один сервер!", inline=False)
    embed.add_field(name="`🍀` : **Автороли**", value="Такие же удобные и простые в настройки автороли! Вплоть до 10 экземпляров авторолей на один сервер!", inline=False)
    embed.add_field(name="`🍂` : **Сообщения о приходе/уходе участников**", value="Вы можете задать с каким текстом и в какой канал будет отправляться сообщение о приходе (а также уходе, но его нужно настроить отдельно) участника!", inline=False)
    embed.add_field(name="`🏮` : **Развлечения**", value="Случайные гифки и картинки животных и многое другое, что вам абсолютно не нужно, но возможно чуть чуть развлечет участников вашего сервера!", inline=False)
    embed.add_field(name="`🌸` : **Базовые команды модерации**", value="Самые обыкновенные команды, которые копируют абсолютно весь функционал обычных функции Discord, но пусть будет!", inline=False)
    embed.add_field(name="`🦾` : **Гибкая настройка**", value="Большинство команд можно гибко настроить под себя и свой сервер!", inline=False)
    embed.add_field(name="`⏳` : **Автомодерация**", value="А вот это появится в скором будущем...", inline=False)
    
    embed.set_footer(text=f"Создатель: seltfox#2356. Все права под защитой рыжих лапок. Версия: {botVersion} ({botVersionDate})")
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

@bot.event
async def on_ready():
    if botPrefix == "d!": print("[МАҢЫЗДЫ ХАБАР] DrewBot іске қосылды.")
    else: print("[МАҢЫЗДЫ ХАБАР] DrewBot Beta іске қосылды. (Дамыту Режимі)")


#for filename in os.listdir('./cogs'):
#    if filename.endswith(".py"):
#        print(f"Загрузка файла: {filename}\nБраузер файлов: {os.listdir('./cogs')}")
#        bot.load_extension(f"cogs.{filename[:-3]}")

for a, b, files in os.walk('./cogs'):
    for file in files:
        if file.endswith('.py'):
            print(f"Файл шолғышы: {file} ({a})")
            print(f"Ког ашылды:   {file}")
            bot.load_extension(f"cogs.{file[:-3]}")


# RUN RELEASE OR DEBUG BOT
bot.run(botToken)