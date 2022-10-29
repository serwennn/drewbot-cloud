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

class StgRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.slash_command()
    async def reactionrole(self, ctx):
        global subcombot
        subcombot = self.bot

    @reactionrole.sub_command(description="Отправляет список всех экзмепляров ролей за реакцию на этом сервере.")
    async def list(self, ctx):

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

        async def delall_callback(interaction):
            if ctx.author.id == interaction.author.id:
                delembed = disnake.Embed(title=f'🎭 : Роли за реакцию **{ctx.guild.name}**', color=botColor)
                if ctx.guild.icon != None: delembed.set_thumbnail(ctx.guild.icon)
                delembed.description = f"Готово! Список ролей за реакции полностью очищен."

                cur.execute("""DELETE FROM reactionrole WHERE guild = ?""", (ctx.guild.id,))
                conn.commit()
                await interaction.response.edit_message(embed=delembed, view=None)
            else:
                embed = disnake.Embed(title=replic['error'], color=botColor)
                embed.description = "Доступ к этой функции имеет только тот кто вызвал её!"
                await interaction.response.send_message(embed=embed, ephemeral=True)
        
        async def selectmenu_callback(interaction):
            async def exempdel(interaction):
                if ctx.author.id == interaction.author.id:
                    cur.execute("""DELETE FROM reactionrole WHERE guild = ? AND role = ?""", (ctx.guild.id, rolename.id,))
                    conn.commit()

                    embed = disnake.Embed(title=f'🎭 : Роли за реакцию **{ctx.guild.name}**', color=botColor)
                    if ctx.guild.icon != None: embed.set_thumbnail(ctx.guild.icon)
                    embed.description = "Готово! Экземпляр был успешно удален."
                    await interaction.response.edit_message(embed=embed, view=None)
                else:
                    embed = disnake.Embed(title=replic['error'], color=botColor)
                    embed.description = "Доступ к этой функции имеет только тот кто вызвал её!"
                    await interaction.response.send_message(embed=embed, ephemeral=True)

            if ctx.author.id == interaction.author.id:
                embed = disnake.Embed(title=f'🎭 : Роли за реакцию **{ctx.guild.name}**', color=botColor)
                if ctx.guild.icon != None: embed.set_thumbnail(ctx.guild.icon)
                embed.description = f"Подробная информация о экзмепляре **#{exempstoshow}**."

                embed.add_field(name="**🎀 : О роли:**", value=f"Название: {rolename.mention}\nID: `{rolename.id}`", inline=True)
                if message != "None": embed.add_field(name="**✉️ : О сообщении:**", value=f"Ссылка: [Перейти]({message.jump_url})\nID: `{message.id}`", inline=True)
                else: embed.add_field(name="**✉️ : О сообщении:**", value=f"Для получения ссылки на сообщение, введите эту команду в канале, где это сообщение.\nID: `{exemp[0]}`", inline=True)
                embed.add_field(name=f"**{exemp[2]} : Эмодзи:**", value=f"Если польз. эмодзи удален, вам придется заново настроить экземпляр.", inline=False)
                
                view = disnake.ui.View()
                buttondel = disnake.ui.Button(style=disnake.ButtonStyle.danger, label="Удалить", emoji="🦊")
                buttondel.callback = exempdel
                view.add_item(item=buttondel)
                await interaction.response.edit_message(embed=embed, view=view)
            else:
                embed = disnake.Embed(title=replic['error'], color=botColor)
                embed.description = "Доступ к этой функции имеет только тот кто вызвал её!"
                await interaction.response.send_message(embed=embed, ephemeral=True)
        
        cur.execute("""SELECT message, role, emoji FROM reactionrole WHERE guild = ?""", (ctx.guild.id,))
        content = cur.fetchall()

        embed = disnake.Embed(title=replic['loading_text'], color=botColor)
        if ctx.guild.icon != None: embed.set_thumbnail(ctx.guild.icon)
        embed.description = random.choice(replic['loading'])
        await ctx.send(embed=embed)
        
        view = disnake.ui.View()
        selectopt = []
        if len(content) != 0:
            exemps = []
            for exemp in content:
                exemps.append(exemp)
                exempstoshow = int(exemps.index((exemp[0], exemp[1], exemp[2])))+1

                try: message = await ctx.channel.fetch_message(exemp[0]) # for selectmenu learn more func
                except: message = "None"

                try:
                    rolename = ctx.guild.get_role(exemp[1])
                    selectopt.append(disnake.SelectOption(label=rolename.name, description=f"#{exempstoshow}. Нажмите, для подробной информации."))
                    embed.add_field(name=f"**#{exempstoshow}.** {rolename.name}", value=f"ID Сообщения: `{exemp[0]}` Эмодзи: {exemp[2]}", inline=False)
                    embed.description = "Список экземпляров ролей за реакцию:"
                except:
                    selectopt.append(disnake.SelectOption(label="⛔ НЕДОСТАТОЧНО ДАННЫХ", description=f"#{exempstoshow}. Нажмите, для подробной информации."))
                    embed.add_field(name=f"**#{exempstoshow}.** ⛔ РОЛЬ ID: **{exemp[1]}**", value=f"ID Сообщения: ⛔ СООБЩЕНИЕ Эмодзи: {exemp[2]}", inline=False)
                    embed.description = "⚠️ : Некоторые данные не найдены. Скорее всего один из экземпляров не нашёл роль или сообщение. Предлагаем заново пересоздать экземпляры с ⛔."
            
            buttondelete = disnake.ui.Button(style=disnake.ButtonStyle.danger, label="Очистить всё", emoji="🦊")
            buttondelete.callback = delall_callback
            selectmenu = disnake.ui.Select(options=selectopt)
            selectmenu.callback = selectmenu_callback
        else:
            selectmenu = disnake.ui.Select(options=[disnake.SelectOption(label="Здесь ничего нет", description="Добавьте роли за реакции!", emoji="🦊")], disabled=True)
            buttondelete = disnake.ui.Button(style=disnake.ButtonStyle.danger, label="Очистить всё", emoji="🦊", disabled=True)
            embed.description = "Здесь нет экземпляров ролей за реакцию. Чтобы их добавить используйте /reationrole add (ID роли) (ID Сообщения) (Эмодзи)."
        
        view.add_item(item=buttondelete)
        view.add_item(item=selectmenu)

        await ctx.edit_original_message(embed=embed, view=view)



    @reactionrole.sub_command(description="Добавляет один или сразу несколько экзмепляров ролей за реакции на одно сообщение.")
    async def add(self, ctx, message, roles, emojis):
        
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

        roles, emojis = roles.split(" "), emojis.split(" ")
        pairs = []

        cur.execute("""SELECT message, role, emoji FROM reactionrole WHERE guild = ?""", (ctx.guild.id,))
        content = cur.fetchall()

        embed = disnake.Embed(title=replic['loading_text'], color=botColor)
        if ctx.guild.icon != None: embed.set_thumbnail(ctx.guild.icon)
        embed.description = random.choice(replic['loading'])
        await ctx.send(embed=embed)
        
        lastroles = []
        for role in roles:
            if role in lastroles:
                embed = disnake.Embed(title=replic['error'], color=botColor)
                embed.description = "Роли не могут повторяться.\nСледуйте образцу ниже:"
                embed.set_image("https://media.discordapp.net/attachments/1030143536424824862/1030144530848174160/unknown.png")
                await ctx.edit_original_message(embed=embed)
                return
            lastroles.append(role)

        lastemojies = []
        for emoji in emojis:
            if emoji in lastemojies:
                embed = disnake.Embed(title=replic['error'], color=botColor)
                embed.description = "Эмодзи не могут повторяться.\nСледуйте образцу ниже:"
                embed.set_image("https://media.discordapp.net/attachments/1030143536424824862/1030144530848174160/unknown.png")
                await ctx.edit_original_message(embed=embed)
                return
            lastemojies.append(emoji)

        try: message = await ctx.channel.fetch_message(message)
        except:
            embed = disnake.Embed(title=replic['error'], color=botColor)
            embed.description = "Такого сообщения не было найдено! Используйте ID сообщения, сообщение должно находится в этом же канале.\nСледуйте образцу ниже:"
            embed.set_image("https://media.discordapp.net/attachments/1030143536424824862/1030144530848174160/unknown.png")
            await ctx.edit_original_message(embed=embed)
            return

        for elementrole in roles:
            try: role = disnake.utils.get(ctx.guild.roles, id=int(elementrole[3:-1]))
            except:
                embed = disnake.Embed(title=replic['error'], color=botColor)
                embed.description = "Упоминания ролей должны быть разделены пробелами. Следуйте образцу ниже:"
                embed.set_image("https://media.discordapp.net/attachments/1030143536424824862/1030144530848174160/unknown.png")
                await ctx.edit_original_message(embed=embed)
                return

        for elementemoji in emojis:
            try:
                await message.add_reaction(elementemoji)
                await message.remove_reaction(elementemoji, subcombot.user)
            except:
                embed = disnake.Embed(title=replic['error'], color=botColor)
                embed.description = "Эмодзи должны быть разделены пробелами.\nСледуйте образцу ниже:"
                embed.set_image("https://media.discordapp.net/attachments/1030143536424824862/1030144530848174160/unknown.png")
                await ctx.edit_original_message(embed=embed)
                return
            
        try:
            for i in range(len(roles)):
                
                role = disnake.utils.get(ctx.guild.roles, id=int(str(roles[i])[3:-1]))
                try:
                    testm = await ctx.guild.fetch_member(subcombot.user.id)
                    await testm.add_roles(role)
                    await testm.remove_roles(role)
                except:
                    embed = disnake.Embed(title=replic["error"], color=botColor)
                    embed.description = "Одна из ролей выше моей, поэтому я не смогу выдавать её. Пожалуйста, переместите мою роль выше."
                    await ctx.edit_original_message(embed=embed)
                    return

                pairs.append([roles[i], emojis[i]])
                embed.add_field(name=role, value=f"ID: `{role.id}` Эмодзи: {emojis[i]}", inline=False)
        except:
            embed = disnake.Embed(title=replic['error'], color=botColor)
            embed.description = "Количество эмодзи и ролей должны быть одинаковы.\nСледуйте образцу ниже:"
            embed.set_image("https://media.discordapp.net/attachments/1030143536424824862/1030144530848174160/unknown.png")
            await ctx.edit_original_message(embed=embed)
            return
        
        if (len(content) + len(roles)) <= 20: # +1
            if len(content) >= 1:
                listexemprole = []
                for addexemp in content:
                    listexemprole.append(addexemp[1])

                if role.id in listexemprole:
                    embed = disnake.Embed(title=replic['error'], color=botColor)
                    embed.description = "Эта роль уже используется в другом экземпляре!"
                    await ctx.edit_original_message(embed=embed)
                    return
            
            for pair in pairs:
                await message.add_reaction(pair[1])

                cur.execute("""INSERT INTO reactionrole VALUES (?, ?, ?, ?)""", (ctx.guild.id, message.id, str(pair[0])[3:-1], pair[1],)) #pair[1] = emoji ; str(pair[0])[3:-1] = id role
                conn.commit()
        else:
            embed = disnake.Embed(title=replic['error'], color=botColor)
            embed.description = "Извините, но вы не можете создать больше 20 экземпляров ролей за реакцию на одном сервере!"
            await ctx.edit_original_message(embed=embed)
            return
        
        embed.description = "Готово! Все роли и эмодзи успешно привязаны к этому сообщению. Чтобы получить полный список экзмепляров ролей за реакции введите /reactionrole list."
        await ctx.edit_original_message(embed=embed)








    @commands.slash_command()
    async def autorole(self, ctx):
        pass

    @autorole.sub_command(description="Отправляет список всей экзмепляров авторолей на этом сервере.")
    async def list(self, ctx):

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

        async def delall_callback(interaction):
            if ctx.author.id == interaction.author.id:
                embed = disnake.Embed(title=f'🎭 : Автороли **{ctx.guild.name}**', color=botColor)
                if ctx.guild.icon != None: embed.set_thumbnail(ctx.guild.icon)
                embed.description = f"Готово! Список авторолей полностью очищен."

                cur.execute("""DELETE FROM autorole WHERE guild = ?""", (ctx.guild.id,))
                conn.commit()
                await interaction.response.edit_message(embed=embed, view=None)
            else:
                embed = disnake.Embed(title=replic['error'], color=botColor)
                embed.description = "Доступ к этой функции имеет только тот кто вызвал её!"
                await interaction.response.send_message(embed=embed, ephemeral=True)
        
        async def selectmenu_callback(interaction):
            async def exempdel(interaction):
                if ctx.author.id == interaction.author.id:
                    cur.execute("""DELETE FROM autorole WHERE guild = ? AND role = ?""", (ctx.guild.id, rolename.id,))
                    conn.commit()

                    embed = disnake.Embed(title=f'🎭 : Автороли **{ctx.guild.name}**', color=botColor)
                    if ctx.guild.icon != None: embed.set_thumbnail(ctx.guild.icon)
                    embed.description = "Готово! Экземпляр был успешно удален."
                    await interaction.response.edit_message(embed=embed, view=None)
                else:
                    embed = disnake.Embed(title=replic['error'], color=botColor)
                    embed.description = "Доступ к этой функции имеет только тот кто вызвал её!"
                    await interaction.response.send_message(embed=embed, ephemeral=True)

            if ctx.author.id == interaction.author.id:
                embed = disnake.Embed(title=f'🎭 : Автороли **{ctx.guild.name}**', color=botColor)
                if ctx.guild.icon != None: embed.set_thumbnail(ctx.guild.icon)
                embed.description = f"Подробная информация о экзмепляре **#{exempstoshow}**."

                embed.add_field(name="**🎀 : О роли:**", value=f"Название: {rolename.mention}\nID: `{rolename.id}`", inline=True)
                
                view = disnake.ui.View()
                buttondel = disnake.ui.Button(style=disnake.ButtonStyle.danger, label="Удалить", emoji="🦊")
                buttondel.callback = exempdel
                view.add_item(item=buttondel)
                await interaction.response.edit_message(embed=embed, view=view)
            else:
                embed = disnake.Embed(title=replic['error'], color=botColor)
                embed.description = "Доступ к этой функции имеет только тот кто вызвал её!"
                await interaction.response.send_message(embed=embed, ephemeral=True)
        
        
        cur.execute("""SELECT role FROM autorole WHERE guild = ?""", (ctx.guild.id,))
        content = cur.fetchall()

        embed = disnake.Embed(title=replic['loading_text'], color=botColor)
        if ctx.guild.icon != None: embed.set_thumbnail(ctx.guild.icon)
        embed.description = random.choice(replic['loading'])
        await ctx.send(embed=embed)

        embed = disnake.Embed(title=f'🎭 : Автороли **{ctx.guild.name}**', color=botColor)
        if ctx.guild.icon != None: embed.set_thumbnail(ctx.guild.icon)
        
        view = disnake.ui.View()
        selectopt = []
        print(content)
        if len(content) != 0:
            exemps = []
            for exemp in content:
                exemps.append(exemp[0])
                exempstoshow = int(exemps.index((exemp[0])))+1
                try:
                    rolename = ctx.guild.get_role(exemp[0])
                    selectopt.append(disnake.SelectOption(label=rolename.name, description=f"{exempstoshow}. Нажмите, для подробной информации.", emoji="🦊"))
                    embed.add_field(name=f"{exempstoshow}. {rolename.name}", value=f"ID: `{rolename.id}`", inline=False)
                    embed.description = "Список экземпляров авторолей:"
                except:
                    embed.add_field(name=f"{exempstoshow}. Роль: ⛔ РОЛЬ", value=f"ID: `{exemp[0]}`", inline=False)
                    embed.description = "⚠️ : Некоторые данные не найдены. Скорее всего один из экземпляров не нашёл роль. Предлагаем заново пересоздать экземпляры с ⛔."
            
            buttondelete = disnake.ui.Button(style=disnake.ButtonStyle.danger, label="Очистить всё", emoji="🦊")
            buttondelete.callback = delall_callback
            selectmenu = disnake.ui.Select(options=selectopt)
            selectmenu.callback = selectmenu_callback
        else:
            selectmenu = disnake.ui.Select(options=[disnake.SelectOption(label="Здесь ничего нет", description="Добавьте автороли!", emoji="🦊")], disabled=True)
            buttondelete = disnake.ui.Button(style=disnake.ButtonStyle.danger, label="Очистить всё", emoji="🦊", disabled=True)
            embed.description = "Здесь нет экземпляров авторолей. Чтобы их добавить используйте /autorole add."
        
        view.add_item(item=buttondelete)
        view.add_item(item=selectmenu)

        await ctx.edit_original_message(embed=embed, view=view)
    


    @autorole.sub_command(description="Создаёт новый экземпляр автороли.")
    async def add(self, ctx, role: disnake.Role):

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
            embed = disnake.Embed(title=replic['blacklist_error'][0], color=botColor)
            embed.description = replic['blacklist_error'][1]
            await ctx.send(embed=embed)
            return

        cur.execute("""SELECT role FROM autorole WHERE guild = ?""", (ctx.guild.id,))
        content = cur.fetchall()

        embed = disnake.Embed(title=replic['loading_text'], color=botColor)
        if ctx.guild.icon != None: embed.set_thumbnail(ctx.guild.icon)
        embed.description = random.choice(replic['loading'])
        await ctx.send(embed=embed)

        try:
            testm = await ctx.guild.fetch_member(self.bot.user.id)
            await testm.add_roles(role)
            await testm.remove_roles(role)
        except:
            embed = disnake.Embed(title=replic["error"], color=botColor)
            embed.description = "Эта роль выше моей роли, поэтому я не смогу выдавать её. Пожалуйста, переместите мою роль выше."
            await ctx.edit_original_message(embed=embed)
            return

        if len(content) <= 9: # +1
            if len(content) >= 1:
                listexemprole = []
                for addexemp in content:
                    listexemprole.append(addexemp[0])

                if role.id in listexemprole:
                    embed = disnake.Embed(title=replic['error'], color=botColor)
                    embed.description = "Эта роль уже используется в другом экземпляре!"
                    await ctx.edit_original_message(embed=embed)
                    return
            
            cur.execute("""INSERT INTO autorole VALUES (?, ?)""", (ctx.guild.id, role.id,))
            conn.commit()

            embed = disnake.Embed(title=f'🎭 : Автороли **{ctx.guild.name}**', color=botColor)
            if ctx.guild.icon != None: embed.set_thumbnail(ctx.guild.icon)
            embed.description = "Новый экземпляр успешно добавлен!"
            await ctx.edit_original_message(embed=embed)
        else:
            embed = disnake.Embed(title=replic['error'], color=botColor)
            embed.description = "Извините, но вы не можете создать больше 10 экземпляров авторолей на одном сервере!"
            await ctx.edit_original_message(embed=embed)
    
    @add.error
    async def rraddError(self, ctx, error):
        embed = disnake.Embed(title = replic['error'], color = botColor)
        embed.description = replic['unk_error']
        if isinstance(error, commands.RoleNotFound):
            embed.description = f"""🎭 : Такая роль не найдена!"""
        await ctx.edit_original_message(embed = embed)


def setup(bot):
    bot.add_cog(StgRoles(bot))