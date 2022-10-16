# SETTINGS

#disnake
import disnake
from disnake.ext import commands

#other
import requests
import json

#own
from main import botColor, blacklist, conn, cur
from replics import replic

whitelist = []

class StgMsg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command()
    async def message(self, ctx):
        pass
    
    @message.sub_command(description="Настройка сообщения, которое будет отправляться при присоединении участника.")
    async def join(self, ctx, channel: disnake.TextChannel, text="{mention}, добро пожаловать!"):

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
        
        async def button_callback(interaction):
            if ctx.author.id == interaction.author.id:
                delembed = disnake.Embed(title=f'Приветствие новых участников', color=botColor)
                if ctx.guild.icon != None: delembed.set_thumbnail(url=ctx.guild.icon)
                delembed.description = f"Готово! Отныне я не буду присылать сообщения с приветствием новых участников."

                cur.execute("""DELETE FROM messageOnJoin WHERE guild = ?""", (ctx.guild.id,))
                conn.commit()
                await interaction.response.edit_message(embed=delembed, view=None)
            else:
                embed = disnake.Embed(title=replic['error'], color=botColor)
                embed.description = "Доступ к этой функции имеет только тот кто вызвал её!"
                await interaction.response.send_message(embed=embed, ephemeral=True)

        cur.execute("""SELECT channel, text FROM messageOnJoin WHERE guild = ?""", (ctx.guild.id,))
        content = cur.fetchone()

        embed = disnake.Embed(title=f'Приветствие новых участников', color=botColor)
        if ctx.guild.icon != None: embed.set_thumbnail(url=ctx.guild.icon)
        
        if content == None:
            cur.execute("""INSERT INTO messageOnJoin VALUES (?, ?, ?)""", (ctx.guild.id, channel.id, text,))
            conn.commit()
        else:
            cur.execute("""UPDATE messageOnJoin SET channel = ?, text = ? WHERE guild = ?""", (channel.id, text, ctx.guild.id,))
            conn.commit()
        
        embed.description = f"Готово! Теперь при присоединении участника на сервер, я буду отправлять сообщение в <#{channel.id}>, с этим текстом."
        if "{mention}" in text and "{member}" in text: embed.add_field(name="Текст:", value=text.format(member=ctx.author, mention=ctx.author.mention))
        elif "{member}" in text: embed.add_field(name="Текст:", value=text.format(member=ctx.author))
        elif "{mention}" in text: embed.add_field(name="Текст:", value=text.format(mention=ctx.author.mention))
        else: embed.add_field(name="Текст:", value=text)

        view = disnake.ui.View()
        item = disnake.ui.Button(style=disnake.ButtonStyle.danger, label="Очистить", emoji="🦊")
        item.callback = button_callback
        view.add_item(item=item)
        
        await ctx.send(embed=embed, view=view)


    @message.sub_command(description="Настройка сообщения, которое будет отправляться при уходе участника.")
    async def left(self, ctx, channel: disnake.TextChannel, text="{member}, прощай!"):

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
        
        async def button_callback(interaction):
            if ctx.author.id == interaction.author.id:
                delembed = disnake.Embed(title=f'Прощание с участниками', color=botColor)
                if ctx.guild.icon != None: delembed.set_thumbnail(url=ctx.guild.icon)
                delembed.description = f"Готово! Отныне я не буду присылать сообщения о уходе участников."
                
                cur.execute("""DELETE FROM messageOnLeft WHERE guild = ?""", (ctx.guild.id,))
                conn.commit()
                await interaction.response.edit_message(embed=delembed, view=None)
            else:
                embed = disnake.Embed(title=replic['error'], color=botColor)
                embed.description = "Доступ к этой функции имеет только тот кто вызвал её!"
                await interaction.response.send_message(embed=embed, ephemeral=True)

        cur.execute("""SELECT channel, text FROM messageOnLeft WHERE guild = ?""", (ctx.guild.id,))
        content = cur.fetchone()

        embed = disnake.Embed(title=f'Прощание с участниками', color=botColor)
        if ctx.guild.icon != None: embed.set_thumbnail(url=ctx.guild.icon)
        
        if content == None:
            cur.execute("""INSERT INTO messageOnLeft VALUES (?, ?, ?)""", (ctx.guild.id, channel.id, text,))
            conn.commit()
        else:
            cur.execute("""UPDATE messageOnLeft SET channel = ?, text = ? WHERE guild = ?""", (channel.id, text, ctx.guild.id,))
            conn.commit()
        
        embed.description = f"Готово! Теперь при уходе участника с сервера, я буду отправлять сообщение в <#{channel.id}>, с этим текстом."
        if "{mention}" in text and "{member}" in text: embed.add_field(name="Текст:", value=text.format(member=ctx.author, mention=ctx.author.mention))
        elif "{member}" in text: embed.add_field(name="Текст:", value=text.format(member=ctx.author))
        elif "{mention}" in text: embed.add_field(name="Текст:", value=text.format(mention=ctx.author.mention))
        else: embed.add_field(name="Текст:", value=text)

        view = disnake.ui.View()
        item = disnake.ui.Button(style=disnake.ButtonStyle.danger, label="Очистить", emoji="🦊")
        item.callback = button_callback
        view.add_item(item=item)
        
        await ctx.send(embed=embed, view=view)
    
    @commands.command()
    async def check(self, ctx):
        cur.execute("""SELECT channel, text FROM messageOnJoin WHERE guild = ?""", (ctx.guild.id,))
        content = cur.fetchone()

        print(content)


def setup(bot):
    bot.add_cog(StgMsg(bot))