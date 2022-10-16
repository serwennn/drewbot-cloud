# INFORMATION

#disnake
import disnake
from disnake.ext import commands

#own
from main import botColor, blacklist, botVersion, botVersionDate
from replics import replic

class Inf(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def helpcommand(self, ctx, command):
        try:
            embed = disnake.Embed(color=botColor, title=f'Подробнее о комманде **{command}**')
            embed.description = "Все что в () — обязательно, в <> — по-желанию."
            embed.add_field(name='Краткое описание команды', value=replic[command][0], inline=False)
            embed.add_field(name='Полное описание команды', value=replic[command][2], inline=False)
            embed.add_field(name='Синтаксис и примеры', value=replic[command][1], inline=False)
            embed.set_footer(text=f"Создатель — seltfox#2356. Версия DrewBot {botVersion} - от {botVersionDate}")
            await ctx.send(embed=embed)
        except:
            embed = disnake.Embed(color=botColor, title=f'Ошибка!')
            embed.description = "Такая команда не найдена!"
            await ctx.send(embed=embed)

    @commands.slash_command(aliases=["помощь", "хелп"], description="Отправляет сообщение со справкой о всех командах или же определённой команды.")
    async def help(self, ctx, command=None):
        if str(ctx.author.id) in str(blacklist):
            embed = disnake.Embed(title=replic['blacklist_error'][0], color=botColor)
            embed.description = replic['blacklist_error'][1]
            await ctx.send(embed=embed)

        if command != None:
            await self.helpcommand(ctx, command)
            return

        embed = disnake.Embed(color=botColor, title='🦊 : **Список всех команд DrewBot:**')  # Создание Embed'a
        embed.set_thumbnail("https://media.discordapp.net/attachments/1010121538953035786/1021288851148378132/unknown.png?width=607&height=607")
        embed.description = "Чтобы получить подробную информацию о определенной команде, введите `/help <название команды>`."

        embed.add_field(name="""☔ : **Модерация:**""", value="""`mute` `unmute` `kick` `ban` `unban`""", inline=False)
        embed.add_field(name="""🏵️ : **Информация:**""", value="""`server` `user` `avatar`""", inline=False)
        embed.add_field(name="""🛠️ : **Настройки:**""", value="""~~`whitelist`~~ ~~`anticrash`~~ `reactionrole` `autorole`""", inline=False)
        embed.add_field(name="""🌊 : **Развлечения:**""", value="""`fox` `cat` `dog`""", inline=False)
        embed.add_field(name="""🍚 : **Бот:**""", value="""`help` `info` `ping` """, inline=False)

        embed.set_footer(text=f"Создатель — seltfox#2356. Версия DrewBot {botVersion} - от {botVersionDate}")

        view = disnake.ui.View()
        item = disnake.ui.Button(style=disnake.ButtonStyle.red, label="Сервер Поддержки", emoji="🦊", url="https://discord.gg/B9mQ26fCWN")
        view.add_item(item=item)
        await ctx.send(embed=embed, view=view)  # Отправляем Embed


    @commands.slash_command(description="Текущий пинг Discord API бота.", aliases=["пинг"])
    async def ping(self, ctx):
        if str(ctx.author.id) in str(blacklist):
            embed = disnake.Embed(title=replic['blacklist_error'][0], color=botColor)
            embed.description = replic['blacklist_error'][1]
            await ctx.send(embed=embed)

        embed = disnake.Embed(title='Понг!', color=botColor)
        embed.description = f"""**🦊 : Фыр! Пинг Discord API: `{round(self.bot.latency * 1000)}`мс**."""
        await ctx.send(embed=embed)
    

    @commands.slash_command(description="Информация и статистика DrewBot.", aliases=["инфо"])
    async def info(self, ctx):
        if str(ctx.author.id) in str(blacklist):
            embed = disnake.Embed(title=replic['blacklist_error'][0], color=botColor)
            embed.description = replic['blacklist_error'][1]
            await ctx.send(embed=embed)

        embed = disnake.Embed(title='✨ : **Информация и Статистика DrewBot:**', color=botColor)
        embed.add_field(
            name="🧬 : **Информация бота:**",
            #value=f"Шард этого сервера: `#{str(ctx.guild.shard_id)}`",
            value=f"Версия: **{botVersion}**\nДата релиза: **{botVersionDate}**\nКол-во серверов: **{str(len(self.bot.guilds))}**",
            inline=True)
        embed.add_field(
            name="🥣 : **Авторы:**",
            value="Создатель: **seltfox#2356**\nОформление: **_iwnuply#2418**",
            inline=True)

        embed.set_footer(text=f"Создатель — seltfox#2356. Версия DrewBot {botVersion} - от {botVersionDate}")
        await ctx.send(embed=embed)
    

    @commands.slash_command(description="Отправляет подробную статистику о данном сервере.", aliases=["сервер"])
    async def server(self, ctx):
        if str(ctx.author.id) in str(blacklist):
            embed = disnake.Embed(title=replic['blacklist_error'][0], color=botColor)
            embed.description = replic['blacklist_error'][1]
            await ctx.send(embed=embed)

        embed = disnake.Embed(title=f'🌙 : Статистика о сервере **{ctx.guild.name}**', color=botColor)

        bot, user = 0, 0
        for member in ctx.guild.members:
            if member.bot == True:
                bot += 1
            else:
                user += 1

        verlvl = "Не удалось определить"
        if "medium" in ctx.guild.verification_level:
            verlvl = "Средний"
        if "low" in ctx.guild.verification_level:
            verlvl = "Низкий"
        if "high" in ctx.guild.verification_level:
            verlvl = "Высокий"
        if "highest" in ctx.guild.verification_level:
            verlvl = "Наивысший"
        if "none" in ctx.guild.verification_level:
            verlvl = "Нет"

        embed.description = f"""Владелец: **{ctx.guild.owner}**\nСоздан: `{str(ctx.guild.created_at)[:-13]}`"""
        embed.add_field(name="🦊 : **Участники:**",
            value=f"Всего: {bot+user}\nЛюдей: {user}\nБотов: {bot}",
            inline=True)
        embed.add_field( name="☕ : **Каналы:**",
            value=f"Всего: {int(len(ctx.guild.text_channels))+int(len(ctx.guild.voice_channels))}\nТекстовые: {len(ctx.guild.text_channels)}\nГолосовые: {len(ctx.guild.voice_channels)}",
            inline=True)
        embed.add_field(name="🍚 : **Прочее:**",
            value=f"Всего Категорий: {len(ctx.guild.categories)}\nРолей: {len(ctx.guild.roles)}\nЭмодзи: {len(ctx.guild.emojis)}")

        embed.add_field(name="☔ : **Уровень верификации:**", value=f"{verlvl}")

        if ctx.guild.icon != None: embed.set_thumbnail(url=ctx.guild.icon)
        await ctx.send(embed=embed)
    

    @commands.slash_command(description="Отправляет статистику о аккаунте указанного пользователя.", aliases=["юзер", "уч"])
    async def user(self, ctx, member: disnake.Member=None):
        if str(ctx.author.id) in str(blacklist):
            embed = disnake.Embed(title=replic['blacklist_error'][0], color=botColor)
            embed.description = replic['blacklist_error'][1]
            await ctx.send(embed=embed)

        if member == None: member = ctx.author
    
        embed = disnake.Embed(title=f'🌙 : Информация о **{member}**', color=botColor)

        if member.raw_status == "online":
            status = "В сети"
        if member.raw_status == "offline":
            status = "Не в сети"
        if member.raw_status == "dnd":
            status = "Не беспокоить"
        if member.raw_status == "idle":
            status = "Неактивен"

        embed.add_field(name="☀️ : **Статус:**", value=status, inline=True)
        embed.add_field(name="🧬 : **ID:**", value=member.id, inline=True)
        embed.add_field(name="🍚 : **Присоединился:**", value=f"`{str(member.joined_at)[:-13]}`", inline=False)
        embed.add_field(name="🌀 : **Высшая роль:**", value=f"`{member.top_role}`")

        if member.avatar != None: embed.set_thumbnail(url=member.avatar)
        await ctx.send(embed=embed)
    

    @commands.slash_command(description="Отправляет аватар указанного пользователя в оригинальном размере.", aliases=["ава", "ava", "аватар"])
    async def avatar(self, ctx, member: disnake.Member=None):
        if str(ctx.author.id) in str(blacklist):
            embed = disnake.Embed(title=replic['blacklist_error'][0], color=botColor)
            embed.description = replic['blacklist_error'][1]
            await ctx.send(embed=embed)

        if member == None: member = ctx.author
        
        embed = disnake.Embed(title=f'Аватар **{member}**', color=botColor)
        embed.set_image(member.avatar)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Inf(bot))