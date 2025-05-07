import discord
from discord.ext import commands

class Invites(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.invite_cache = {}
        self.user_invite_map = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Invite tracking cog is ready.")

        for guild in self.bot.guilds:
            invites = await guild.invites()
            self.invite_cache[guild.id] = invites

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild

      
        if guild.id not in self.invite_cache:
            self.invite_cache[guild.id] = await guild.invites()

        old_invites = self.invite_cache.get(guild.id, [])
        new_invites = await guild.invites()

        inviter = None
        for new_invite in new_invites:
            old_invite = next((i for i in old_invites if i.code == new_invite.code), None)
            if old_invite and new_invite.uses > old_invite.uses:
                inviter = new_invite.inviter
                break

  
        self.invite_cache[guild.id] = new_invites

        if inviter:
            self.user_invite_map.setdefault(inviter.id, []).append(member.id)
            print(f"✅ {member} dołączył, zaproszony przez {inviter}")

            
            channel = discord.utils.get(guild.text_channels, name="【💎】𝗪𝗜𝗧𝗔𝗠𝗬")  
            if channel:
                await channel.send(f"👋 {member.mention} dołączył do serwera! Zaproszony przez {inviter.mention}.")
            else:
                print(f"❌ Could not find a channel named 'general' in {guild.name}.")
        else:
            print(f"❓ {member} dołączył, ale nie wiemy kto go zaprosił.")

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        
        guild = invite.guild
        invites = await guild.invites()
        self.invite_cache[guild.id] = invites
        print(f"📄 Nowa zaproszenia {invite.code} stworzona przez {invite.inviter}.")

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        
        guild = invite.guild
        invites = await guild.invites()
        self.invite_cache[guild.id] = invites
        print(f"❌ Zaproszenie {invite.code} zostało usunięte.")

    @commands.command(name="invites")
    async def invites(self, ctx, member: discord.Member = None):
        
        member = member or ctx.author
        invited_users = self.user_invite_map.get(member.id, [])
        await ctx.send(f"📨 {member.display_name} zaprosił {len(invited_users)} na serwer.")


async def setup(bot):
    await bot.add_cog(Invites(bot))
