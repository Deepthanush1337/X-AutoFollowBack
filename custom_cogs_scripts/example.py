from discord.ext import commands

class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def example(self, ctx):
        await ctx.message.delete()
        await ctx.send("ExampleCog Loaded")

async def setup(bot):
    await bot.add_cog(ExampleCog(bot))
