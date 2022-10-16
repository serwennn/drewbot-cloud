# REACTION ROLE

#disnake
import disnake
from disnake.ext import commands
from disnake import utils

#other
import requests
import json

#own
from main import botColor, blacklist, cur, conn
from replics import replic

class Rer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, ctx):
        cur.execute("""SELECT message, role, emoji FROM reactionrole WHERE guild = ?""", (ctx.guild_id,))
        content = cur.fetchall()

        for exemp in content:
            if ctx.message_id == exemp[0]:
                try:
                    channel = self.bot.get_channel(ctx.channel_id) # получаем объект канала
                    message = await channel.fetch_message(ctx.message_id) # получаем объект сообщения
                    member = utils.get(message.guild.members, id=ctx.user_id) # получаем объект пользователя который поставил реакцию
        
                    emoji = ctx.emoji # эмоджик который выбрал юзер
                    role = utils.get(message.guild.roles, id=exemp[1]) # объект выбранной роли (если есть)
                    if str(emoji) == str(exemp[2]):
                        try:
                            if member != self.bot.user:
                                await member.add_roles(role)
                                print(f"{ctx.guild_id} реакция добавлена.")
                        except:
                            embed = disnake.Embed(title=replic['error'], color=botColor)
                            embed.description = f"Я не могу выдавать роли на этом сообщении. Проверьте у бота права Админстратора и поставьте роль бота выше ролей, которые выдаются в этом экземпляре."
                            await self.bot.get_guild(ctx.guild_id).get_channel(ctx.channel_id).fetch_message(ctx.message_id).reply(embed=embed)
                except:
                    embed = disnake.Embed(title=replic['error'], color=botColor)
                    embed.description = "Я не могу выдавать роли на этом сообщении. Проверьте у бота права Админстратора и поставьте роль бота выше ролей, которые выдаются в этом экземпляре."
                    await self.bot.get_guild(ctx.guild_id).get_channel(ctx.channel_id).send(embed=embed)

    

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, ctx):
        cur.execute("""SELECT message, role, emoji FROM reactionrole WHERE guild = ?""", (ctx.guild_id,))
        content = cur.fetchall()

        for exemp in content:
            if ctx.message_id == exemp[0]:
                channel = self.bot.get_channel(ctx.channel_id) # получаем объект канала
                message = await channel.fetch_message(ctx.message_id) # получаем объект сообщения
                member = utils.get(message.guild.members, id=ctx.user_id) # получаем объект пользователя который поставил реакцию
    
                emoji = ctx.emoji # эмоджик который выбрал юзер
                role = utils.get(message.guild.roles, id=exemp[1]) # объект выбранной роли (если есть)
                if str(emoji) == str(exemp[2]):
                    await member.remove_roles(role)
                    print(f"{ctx.guild.name} реакция удалена.")


def setup(bot):
    bot.add_cog(Rer(bot))