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


class Msg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, ctx):
        cur.execute("""SELECT channel, text FROM messageOnJoin WHERE guild = ?""", (ctx.guild.id,))
        content = cur.fetchone()

        channelid = content[0]
        text = content[1]

        if content != None:
            channel = ctx.guild.get_channel(channelid)

            embed = disnake.Embed(title=f'Присоединение участника', color=botColor)
            if ctx.avatar != None: embed.set_thumbnail(url=ctx.avatar)

            if "{mention}" in text and "{member}" in text: embed.description = text.format(member=ctx, mention=ctx.mention)
            elif "{member}" in text: embed.description = text.format(member=ctx)
            elif "{mention}" in text: embed.description = text.format(mention=ctx.mention)
            else: embed.description = text
            
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, ctx):
        cur.execute("""SELECT channel, text FROM messageOnLeft WHERE guild = ?""", (ctx.guild.id,))
        content = cur.fetchone()

        channelid = content[0]
        text = content[1]

        if content != None:
            channel = ctx.guild.get_channel(channelid)

            embed = disnake.Embed(title=f'Уход участника', color=botColor)
            if ctx.avatar != None: embed.set_thumbnail(url=ctx.avatar)

            if "{mention}" in text and "{member}" in text: embed.description = text.format(member=ctx, mention=ctx.mention)
            elif "{member}" in text: embed.description = text.format(member=ctx)
            elif "{mention}" in text: embed.description = text.format(mention=ctx.mention)
            else: embed.description = text

            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Msg(bot))