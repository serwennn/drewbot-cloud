# SETTINGS

#disnake
import disnake
from disnake.ext import commands

#other
import requests
import json
import random

#own
from main import botColor, blacklist, conn, cur
from replics import replic

whitelist = []

class AccessStg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def access(self, ctx):
        pass
    
    @access.sub_command(description="Список ролей, которые имеют доступ к админ-командам Дрю.")
    async def list(self, ctx):
        if ctx.author.id != ctx.guild.owner_id:
            embed = disnake.Embed(title=f'🦊 : Административный доступ **{ctx.guild.name}**', color=botColor)
            if ctx.guild.icon != None: embed.set_thumbnail(ctx.guild.icon)
            embed.description = f"Доступ к данной команде имеет только владелец сервера!"
            await ctx.send(embed=embed)
            return

        async def delall_callback(interaction):
            if ctx.author.id == interaction.author.id:
                delembed = disnake.Embed(title=f'🦊 : Административный доступ **{ctx.guild.name}**', color=botColor)
                if ctx.guild.icon != None: delembed.set_thumbnail(ctx.guild.icon)
                delembed.description = f"Готово! Список ролей администрации был полностью очищен."

                cur.execute("""DELETE FROM access WHERE guild = ?""", (ctx.guild.id,))
                conn.commit()
                await interaction.response.edit_message(embed=delembed, view=None)
            else:
                embed = disnake.Embed(title=replic['error'], color=botColor)
                embed.description = "Доступ к этой функции имеет только тот кто вызвал её!"
                await interaction.response.send_message(embed=embed, ephemeral=True)
        
        cur.execute("""SELECT role FROM access WHERE guild = ?""", (ctx.guild.id,))
        content = cur.fetchall()

        embed = disnake.Embed(title=f'🦊 : Административный доступ **{ctx.guild.name}**', color=botColor)
        if ctx.guild.icon != None: embed.set_thumbnail(ctx.guild.icon)
        embed.description = random.choice(replic['loading'])
        await ctx.send(embed=embed)
        
        view = disnake.ui.View()
        if len(content) != 0:
            exemps = []
            for exemp in content:
                exemps.append(exemp)
                exempstoshow = int(exemps.index(exemp))+1
                try:
                    rolename = ctx.guild.get_role(exemp[0])
                    embed.add_field(name=f"{exempstoshow}. {rolename.name}", value=f"ID: `{rolename.id}`", inline=False)
                    embed.description = "Те кто имеют эти роли могут редактировать настройки Дрю на этом сервере:"
                except:
                    embed.add_field(name=f"{exempstoshow}. ⛔ РОЛЬ", value=f"ID: **{exemp}**", inline=False)
                    embed.description = "⚠️ : Некоторые данные не найдены. Скорее всего роль не найдена. Предлагаем заново пересоздать экземпляры с ⛔."
            
            buttondelete = disnake.ui.Button(style=disnake.ButtonStyle.danger, label="Очистить всё", emoji="🦊")
            buttondelete.callback = delall_callback
        else:
            buttondelete = disnake.ui.Button(style=disnake.ButtonStyle.danger, label="Очистить всё", emoji="🦊", disabled=True)
            embed.description = "Здесь нет ролей администрации. Чтобы их добавить используйте /access add."
        
        view.add_item(item=buttondelete)
        await ctx.edit_original_message(embed=embed, view=view)
    
    
    @access.sub_command(description="Добавить роль в список ролей, которые имеют доступ к админ-командам Дрю.")
    async def add(self, ctx, role: disnake.Role):
        if ctx.author.id != ctx.guild.owner_id:
            embed = disnake.Embed(title=f'🦊 : Административный доступ **{ctx.guild.name}**', color=botColor)
            if ctx.guild.icon != None: embed.set_thumbnail(ctx.guild.icon)
            embed.description = f"Доступ к данной команде имеет только владелец сервера!"
            await ctx.send(embed=embed)
            return
        
        cur.execute("""SELECT role FROM access WHERE guild = ?""", (ctx.guild.id,))
        content = cur.fetchall()

        embed = disnake.Embed(title=f'🦊 : Административный доступ **{ctx.guild.name}**', color=botColor)
        if ctx.guild.icon != None: embed.set_thumbnail(ctx.guild.icon)
        embed.description = random.choice(replic['loading'])
        await ctx.send(embed=embed)
        
        if len(content) <= 4: # +1
            if len(content) >= 1:
                listexemprole = []
                for addexemp in content:
                    listexemprole.append(addexemp[0])

                if role.id in listexemprole:
                    embed = disnake.Embed(title=replic['error'], color=botColor)
                    embed.description = "Эта роль уже добавлена!"
                    await ctx.edit_original_message(embed=embed)
                    return
            
            cur.execute("""INSERT INTO access VALUES (?, ?)""", (ctx.guild.id, role.id,))
            conn.commit()

            embed.description = "Роль была успешно добавлена!"
            await ctx.edit_original_message(embed=embed)
        else:
            embed = disnake.Embed(title=replic['error'], color=botColor)
            embed.description = "Извините, но вы не можете добавить больше 5 ролей администрации на одном сервере!"
            await ctx.edit_original_message(embed=embed)
    
    

    @access.sub_command(description="Удаляет роль из списка ролей, которые имеют доступ к админ-командам Дрю.")
    async def remove(self, ctx, number: int):
        if ctx.author.id != ctx.guild.owner_id:
            embed = disnake.Embed(title=f'🦊 : Административный доступ **{ctx.guild.name}**', color=botColor)
            if ctx.guild.icon != None: embed.set_thumbnail(ctx.guild.icon)
            embed.description = f"Доступ к данной команде имеет только владелец сервера!"
            await ctx.send(embed=embed)
            return
        
        cur.execute("""SELECT role FROM access WHERE guild = ?""", (ctx.guild.id,))
        content = cur.fetchall()

        embed = disnake.Embed(title=f'🦊 : Административный доступ **{ctx.guild.name}**', color=botColor)
        if ctx.guild.icon != None: embed.set_thumbnail(ctx.guild.icon)
        embed.description = random.choice(replic['loading'])
        await ctx.send(embed=embed)

        exemps = []
        for exemp in content:
            exemps.append(exemp)
        
        try:
            exemptodel = exemps[int(number)-1]
            cur.execute("""DELETE FROM access WHERE guild = ? AND role = ?""", (ctx.guild.id, exemptodel[0],))
            conn.commit()
        except IndexError:
            embed = disnake.Embed(title=replic['error'], color=botColor)
            embed.description = "Роли под таким номером нет! Используйте номер из таблицы /access list."
            await ctx.edit_original_message(embed=embed)
            return

        embed.description = "Готово! Роль была успешно удалена из списка."
        await ctx.edit_original_message(embed=embed)

    @remove.error
    async def rrremoveError(self, ctx, error):
        embed = disnake.Embed(title = replic['error'], color = botColor)
        embed.description = replic['unk_error']
        if isinstance(error, commands.RoleNotFound):
            embed.description = f"""🎭 : Такая роль не найдена!"""
        elif isinstance(error, commands.NotOwner):
            embed.description = f"""Доступ к данной команде имеет только владелец сервера!"""
        await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(AccessStg(bot))