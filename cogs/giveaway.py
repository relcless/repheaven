import discord
from discord.ext import commands
import random
import asyncio

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="giveaway")
    @commands.has_permissions(administrator=True)
    async def giveaway(self, ctx, duration: str, *, prize: str):
        try:
            duration = int(duration)
        except ValueError:
            await ctx.send("Błąd: Czas trwania musi być liczbą całkowitą w sekundach.")
            return
        
        embed = discord.Embed(title="🎉 Giveaway! 🎉", description=f"Nagroda: {prize}\nZareaguj z 🎉, aby wziąć udział!", color=discord.Color.red())
        embed.add_field(name="Czas trwania", value=f"{duration} sekund", inline=False)
        embed.set_footer(text="Giveaway zakończy się po określonym czasie.")
        
        giveaway_message = await ctx.send(embed=embed)
        await giveaway_message.add_reaction("🎉")
        
        start_time = asyncio.get_event_loop().time()
        quarter_time = duration / 2
        last_ping_time = 0

        while True:
            if asyncio.get_event_loop().time() - start_time >= duration:
                break

            if giveaway_message.reactions:
                reaction = giveaway_message.reactions[0]
                users = []

                async for user in reaction.users():
                    if user != self.bot.user:
                        users.append(user)

                num_participants = len(users)

                embed.set_field_at(1, name="Liczba uczestników", value=f"{num_participants}", inline=False)
                await giveaway_message.edit(embed=embed)
            
            if asyncio.get_event_loop().time() - start_time >= last_ping_time + quarter_time:
                await ctx.send("@here Pamiętajcie, że giveaway trwa! Reagujcie z 🎉, aby wziąć udział!")
                last_ping_time = asyncio.get_event_loop().time()
            
            await asyncio.sleep(5)

        if giveaway_message.reactions:
            reaction = giveaway_message.reactions[0]
            users = []

            async for user in reaction.users():
                if user != self.bot.user:
                    users.append(user)

            num_participants = len(users)

            embed.set_field_at(1, name="Liczba uczestników", value=f"{num_participants}", inline=False)
            await giveaway_message.edit(embed=embed)

            if users:
                winner = random.choice(users)
                await ctx.send(f"🎉 Gratulacje {winner.mention}! Wygrałeś **{prize}**!")
            else:
                await ctx.send("Niestety, nikt nie wziął udziału w giveaway.")
            
    @giveaway.error
    async def giveaway_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Nie masz uprawnień do używania tej komendy. Wymagane są uprawnienia administratora.")
        else:
            raise error

async def setup(bot):
    await bot.add_cog(Giveaway(bot))
