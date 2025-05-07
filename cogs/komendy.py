from discord.ext import commands
from discord.utils import get
import discord
from urllib.parse import urlparse, parse_qs
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
from urllib.parse import quote

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings = {}  

    
    @commands.command()
    async def komendy(self, ctx):
        embed = discord.Embed(
            title="Lista Komend",
            description="Prefix serwera to jest = ! (ps. wszystkie komendy piszemy małą literą)",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1368940706273558619/1369391231938986035/26035EE8-1F30-42A8-A2E4-1499CB66F0E9.png?ex=681c5937&is=681b07b7&hm=517acf696e5724f9015825ff663a8d294b77407810ad07a5a602bcde2d16ec91&")
        embed.add_field(name="Info", value="informacje o nas oraz nasze social media", inline=False)
        embed.add_field(name="Komendy", value="pokazuje wszystkie komendy na serwerze", inline=False)
        embed.add_field(name="Whoami", value="pokazuje kim jesteś", inline=False)
        embed.add_field(name="Giveaway", value="robi giveaway, usage: !giveaway _TWOJCZASWSEKUNDACH_ _NAGRODA_", inline=False)
        embed.add_field(name="Mute", value="mutuje, usage: !mute _@UŻYTKOWNIK_ _POWÓD_", inline=False)
        embed.add_field(name="Ban", value="banuje, usage: !ban _@UŻYTKOWNIK_ _POWÓD_", inline=False)
        embed.add_field(name="Kick", value="kickuje, usage: !kick _@UŻYTKOWNIK_ _POWÓD_", inline=False)
        embed.add_field(name="Infractions", value="sprawdza warny, usage: !infractions _@UŻYTKOWNIK_ ", inline=False)
        embed.add_field(name="Warns", value="warnuje, usage: !warn _@UŻYTKOWNIK_ _POWÓD_ ", inline=False)
        await ctx.send(embed=embed)

   
    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(
            title="Info O Nas",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1368940706273558619/1369391231938986035/26035EE8-1F30-42A8-A2E4-1499CB66F0E9.png?ex=681c5937&is=681b07b7&hm=517acf696e5724f9015825ff663a8d294b77407810ad07a5a602bcde2d16ec91&")
        embed.set_image(url="https://cdn.discordapp.com/attachments/982713007413022740/1369313183654797392/banner_example.png")
        embed.add_field(name="Instagram", value="<:ri:1369697043601428480>  https://www.instagram.com/repheav3n/", inline=False)
        embed.add_field(name="Tiktok", value="<:rtt:1369697036328370206>  https://www.tiktok.com/@repheav3n", inline=False)
        embed.add_field(name="Discord Link", value="<:rd:1369697045006389389>  https://discord.gg/3TbUKKg7hA", inline=False)
        embed.add_field(name="AcBuy", value="<:rac:1369702805602046067> https://www.acbuy.com/login?loginStatus=register&code=VI533L  ", inline=False)
        await ctx.send(embed=embed)

   
    @commands.command()
    async def whoami(self, ctx):
        user = ctx.author
        embed = discord.Embed(
            title="Kim Jesteś?",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1368940706273558619/1369391231938986035/26035EE8-1F30-42A8-A2E4-1499CB66F0E9.png?ex=681c5937&is=681b07b7&hm=517acf696e5724f9015825ff663a8d294b77407810ad07a5a602bcde2d16ec91&")
        embed.add_field(name="Nazwa", value=str(user), inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Dołączył na serwer", value=user.joined_at.strftime("%Y-%m-%d %H:%M:%S") if user.joined_at else "Unknown", inline=False)
        embed.set_image(url=user.avatar.url if user.avatar else user.default_avatar.url)
        await ctx.send(embed=embed)


async def setup(bot):
        await bot.add_cog(General(bot))
