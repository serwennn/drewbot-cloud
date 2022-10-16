# MODERATION

#disnake
import disnake
from disnake.ext import commands

#own
from main import botColor, blacklist
from replics import replic

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    #@commands.command(aliases=["мьют", "мут"], sync_commands=True)
    @commands.slash_command(aliases=["мьют", "мут"], description="Даёт мьют указанному участнику.")
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: disnake.Member, time: str="15m", *, reason="Причина не указана."):
        if str(ctx.author.id) in str(blacklist):
            embed = disnake.Embed(title=replic['blacklist_error'][0], color=botColor)
            embed.description = replic['blacklist_error'][1]
            await ctx.send(embed=embed)

        if int(time[0:-1]) == int(time[0:-1]):

            if member == ctx.author:
                embed = disnake.Embed(title=replic["error"], color=botColor)
                embed.description = f'''Вы не можете дать мьют самому себе!'''
                await ctx.send(embed=embed)
                return


            authorindex, memberindex = 0, 0
            for role in ctx.guild.roles:
                if role.id == ctx.author.top_role.id:
                    authorindex = ctx.guild.roles.index(role)
                if role.id == member.top_role.id:
                    memberindex = ctx.guild.roles.index(role)

            if int(authorindex) > int(memberindex):
                await member.timeout(duration=to_time(time), reason=f"Дал мьют: {ctx.author}(ID: {ctx.author.id}). Причина: \"{reason}.\"")
            else:
                embed = disnake.Embed(title=replic["error"], color=botColor)
                embed.description = "У вас не хватает прав для мьюта участника!"
                await ctx.send(embed=embed)
                return

            if 's' in time or 'с' in time:
                timewhat = 'секунд(-ы)'
            if 'm' in time or 'м' in time:
                timewhat = 'минут(-ы)'
            if 'h' in time or 'ч' in time:
                timewhat = 'часа(-ов)'
            if 'd' in time or 'д' in time:
                timewhat = 'дней(-я)'
            if 'w' in time or 'н' in time:
                timewhat = 'неделя(-и)'
            timetext = str(time[0:-1] + " " + timewhat)

            embed = disnake.Embed(title=f'**🦦 : {member} получил мьют!**', color=botColor)
            embed.description = f'''Участник: **{member.mention} ({member})**\nПродолжительность: **{timetext}**.\nДал мьют: **{ctx.author} (ID: {ctx.author.id})**.\nПричина выдачи: **{reason}**'''
            await ctx.send(embed=embed)

    @mute.error
    async def muteError(self, ctx, error):
        embed = disnake.Embed(title=replic['error'], color=botColor)
        if isinstance(error, commands.MissingPermissions):
            embed.description = f"""У вас не хватает прав для мьюта участника!"""
        elif isinstance(error, commands.BotMissingPermissions):
            embed.description = f"""Мне не хватает прав для мьюта участника!"""
        await ctx.send(embed=embed)
        

    @commands.slash_command(aliases=["размьют", "размут"], description="Снимает мьют с указанного участника.")
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: disnake.Member, *, reason="Причина не указана."):
        if str(ctx.author.id) in str(blacklist):
            embed = disnake.Embed(title=replic['blacklist_error'][0], color=botColor)
            embed.description = replic['blacklist_error'][1]
            await ctx.send(embed=embed)

        authorindex, memberindex = 0, 0
        for role in ctx.guild.roles:
            if role.id == ctx.author.top_role.id:
                authorindex = ctx.guild.roles.index(role)
            if role.id == member.top_role.id:
                memberindex = ctx.guild.roles.index(role)

        if int(authorindex) > int(memberindex):
            await member.timeout(duration=None, reason=f"Снял мьют: {ctx.author}(ID: {ctx.author.id}). Причина: \"{reason}.\"")
        else:
            embed = disnake.Embed(title=replic["error"], color=botColor)
            embed.description = "У вас не хватает прав для снятия мьюта с участника!"
            await ctx.send(embed=embed)
            return

        embed = disnake.Embed(title=f'**🕊️ : С {member} сняли мьют!**', color=botColor)
        embed.description = f'''Участник: **{member.mention} ({member})**.\nСнял мьют: **{ctx.author} (ID: {ctx.author.id})**.\nПричина снятия: **{reason}**'''
        await ctx.send(embed = embed)

    @unmute.error
    async def unmuteError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = disnake.Embed( title = replic['error'], color = botColor)
            embed.description = f"""У вас не хватает прав для снятия мьюта с участника!"""
            await ctx.send(embed = embed)
    

    @commands.slash_command(aliases=["кик"], description="Кикает указанного участника с сервера.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: disnake.Member, *, reason='Причина не указана'):
        if str(ctx.author.id) in str(blacklist):
            embed = disnake.Embed(title=replic['blacklist_error'][0], color=botColor)
            embed.description = replic['blacklist_error'][1]
            await ctx.send(embed=embed)

        if member.id == ctx.author.id:
            embed = disnake.Embed(title=replic['error'], color=botColor)
            embed.description = f"""Вы не можете кикнуть себя!"""
            await ctx.send(embed=embed)
            return

        
        authorindex, memberindex = 0, 0
        for role in ctx.guild.roles:
            if role.id == ctx.author.top_role.id:
                authorindex = ctx.guild.roles.index(role)
            if role.id == member.top_role.id:
                memberindex = ctx.guild.roles.index(role)

        if int(authorindex) > int(memberindex):
            embed = disnake.Embed(title=f'🐑** : Вы были кикнуты с {ctx.guild.name}**', color=botColor)
            embed.description = f"""Вы были кикнуты с сервера {ctx.guild.name} (ID: {ctx.guild.id})\nКикнул: {ctx.author} (ID: {ctx.author.id})\nПричиной повлияло: {reason}"""
            await member.kick(reason=f"Кикнул: {ctx.author}(ID: {ctx.author.id}). Причина: \"{reason}\"")
        else:
            embed = disnake.Embed(title=replic["error"], color=botColor)
            embed.description = "У вас не хватает прав для кика участника!"
            await ctx.send(embed=embed)
            return

        embed = disnake.Embed(title='🐑 : Участник был кикнут!', color=botColor)
        embed.description = f"""Участник: **{member.mention} ({member})**.\nКикнул: **{ctx.author} (ID: {ctx.author.id})**.\nПричина кика: **{reason}**"""
        await ctx.send(embed=embed)
        
    @kick.error
    async def kickError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = disnake.Embed(title=replic['error'], color=botColor)
            embed.description = f"""У вас не хватает прав для кика участника!"""
            await ctx.send(embed=embed)


    @commands.slash_command(aliases=["бан"], description="Банит пользователя на сервере.")
    @commands.has_permissions(moderate_members=True)
    async def ban(self, ctx, member: disnake.User, *, reason='Причина не указана'):
        if str(ctx.author.id) in str(blacklist):
            embed = disnake.Embed(title=replic['blacklist_error'][0], color=botColor)
            embed.description = replic['blacklist_error'][1]
            await ctx.send(embed=embed)

        if member.id == ctx.author.id:
            embed = disnake.Embed(title=replic['error'], color=botColor)
            embed.description = f"""Вы не можете забанить себя!"""
            await ctx.send(embed=embed)
            return

        authorindex, memberindex = 0, 0
        for role in ctx.guild.roles:
            if role.id == ctx.author.top_role.id:
                authorindex = ctx.guild.roles.index(role)
            if role.id == member.top_role.id:
                memberindex = ctx.guild.roles.index(role)

        if int(authorindex) > int(memberindex):
            embed = disnake.Embed(title=f'🥀** : Вы были забанены на {ctx.guild.name}**', color=botColor)
            embed.description = f"""Вы были забанены на сервере {ctx.guild.name} (ID: {ctx.guild.id})\nЗабанил: {ctx.author} (ID: {ctx.author.id})\nПричиной повлияло: {reason}"""
            await member.send(embed=embed)
            await ctx.guild.ban(member, reason=f"Забанил: {ctx.author}(ID: {ctx.author.id}). Причина: \"{reason}\"")
        else:
            embed = disnake.Embed(title=replic["error"], color=botColor)
            embed.description = "У вас не хватает прав для бана участника!"
            await ctx.send(embed=embed)
            return

        embed = disnake.Embed(title=f'🥀** : {member} был забанен!**', color=botColor)
        embed.description = f"""Участник: **{member.mention} ({member})**.\nЗабанил: **{ctx.author}**.\nПричина бана: **{reason}**"""
       
        await ctx.send(embed=embed)

    @ban.error
    async def banError(self, ctx, error):
        embed = disnake.Embed(title=replic['error'], color=botColor)
        embed.description = replic['unk_error']
        if isinstance(error, commands.MissingPermissions):
            embed.description = f"""У вас не хватает прав для бана участника!"""
        elif isinstance(error, commands.UserNotFound):
            embed.description = f"""Такой участник не найден!"""
        await ctx.send(embed=embed)


    @commands.slash_command(aliases=["разбан"], description="Снимает бан с пользователя.")
    @commands.has_permissions(moderate_members=True)
    async def unban(self, ctx, id, *, reason='Причина не указана'):
        if str(ctx.author.id) in str(blacklist):
            embed = disnake.Embed(title=replic['blacklist_error'][0], color=botColor)
            embed.description = replic['blacklist_error'][1]
            await ctx.send(embed=embed)

        try:
            user = await self.bot.fetch_user(id)
            await ctx.guild.unban(user, reason=f"Разбанил: {ctx.author}(ID: {ctx.author.id}). Причина: \"{reason}\"")

            embed = disnake.Embed(title=f'🌹** : {user} был разбанен!**', color=botColor)
            embed.description = f"""Участник: **{user} (ID: {id})**.\nРазбанил: **{ctx.author}**.\nПричина разбана: **{reason}**"""
            await ctx.send(embed=embed)
        except:
            embed = disnake.Embed(title=replic['error'], color=botColor)
            embed.description = f"""Пользователь не найден или вы указали неверное значение. Используйте ID для разбана пользователя."""
            await ctx.send(embed=embed)

    @unban.error
    async def unbanError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = disnake.Embed(title=replic['error'], color=botColor)
            embed.description = f"""У вас не хватает прав для разбана участника!"""
            await ctx.send(embed=embed)


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
    bot.add_cog(Mod(bot))