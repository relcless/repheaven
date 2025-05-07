import discord
from discord.ext import commands
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings = {}

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def infractions(self, ctx, member: discord.Member):
        """Shows the infractions (warnings) of a specific user."""
        user_id = str(member.id)
        warns = self.warnings.get(user_id, [])
        
        if not warns:
            return await ctx.send(f"{member.mention} nie ma żadnych ostrzeżeń.")
        
        embed = discord.Embed(
            title=f"📄 Ostrzeżenia {member}",
            color=discord.Color.red()
        )
        
        for i, reason in enumerate(warns, 1):
            embed.add_field(name=f"Ostrzeżenie {i}", value=reason, inline=False)
        
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str):
        """Warn a user for a specific reason."""
        user_id = str(member.id)
        
        if user_id not in self.warnings:
            self.warnings[user_id] = []
        
        self.warnings[user_id].append(reason)
        
        await ctx.send(f"{member.mention} został ostrzeżony. Powód: {reason}")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "Brak powodu"):
        """Kicks a member from the server."""
        try:
            await member.kick(reason=reason)
            await ctx.send(f"{member.mention} został wyrzucony z serwera. Powód: {reason}")
        except discord.Forbidden:
            await ctx.send("Nie mogę wyrzucić tego użytkownika. Upewnij się, że mam odpowiednie uprawnienia.")
        except discord.HTTPException:
            await ctx.send("Wystąpił błąd podczas próby wyrzucenia użytkownika.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = "Brak powodu"):
        """Bans a member from the server."""
        try:
            await member.ban(reason=reason)
            await ctx.send(f"{member.mention} został zbanowany z serwera. Powód: {reason}")
        except discord.Forbidden:
            await ctx.send("Nie mogę zbanować tego użytkownika. Upewnij się, że mam odpowiednie uprawnienia.")
        except discord.HTTPException:
            await ctx.send("Wystąpił błąd podczas próby zbanowania użytkownika.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, duration: str = None, *, reason: str = "Brak powodu"):
        """Mutes a member for a specific duration (optional)."""
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        
        if not mute_role:
            mute_role = await ctx.guild.create_role(name="Muted", permissions=discord.Permissions(send_messages=False, speak=False))
            
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(mute_role, send_messages=False)
            
            for channel in ctx.guild.voice_channels:
                await channel.set_permissions(mute_role, speak=False)
        
        await member.add_roles(mute_role, reason=reason)
        
        if duration:
            try:
                time_in_seconds = self.convert_duration_to_seconds(duration)
                await ctx.send(f"{member.mention} został zmutowany na {duration}. Powód: {reason}")
                await asyncio.sleep(time_in_seconds)
                await member.remove_roles(mute_role, reason="Czas mute'a minął")
                await ctx.send(f"{member.mention} nie jest już zmutowany.")
            except ValueError:
                await ctx.send("Niepoprawny format czasu. Użyj np. 10m (minuty), 1h (godziny).")
        else:
            await ctx.send(f"{member.mention} został zmutowany na zawsze. Powód: {reason}")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason: str = "Brak powodu"):
        """Unmutes a member."""
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    
        if not mute_role:
            return await ctx.send("Rola 'Muted' nie istnieje na tym serwerze.")
    
        if mute_role in member.roles:
            await member.remove_roles(mute_role, reason=reason)
            await ctx.send(f"{member.mention} został odmutowany. Powód: {reason}")
        else:
            await ctx.send(f"{member.mention} nie jest zmutowany.")

    def convert_duration_to_seconds(self, duration: str):
        """Convert a duration like '10m', '1h', etc., to seconds."""
        duration = duration.lower()
        if duration.endswith('m'):
            return int(duration[:-1]) * 60
        elif duration.endswith('h'):
            return int(duration[:-1]) * 3600
        elif duration.endswith('d'):
            return int(duration[:-1]) * 86400
        else:
            raise ValueError("Unsupported duration format")

async def setup(bot):
    print("Loading Moderation Cog...")  
    await bot.add_cog(Moderation(bot))
