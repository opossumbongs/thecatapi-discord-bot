import discord
from discord.ext import commands
from utils import Cat

cat = Cat()

class Gif(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name = 'gif', description = 'Sends a cat gif.')
    async def gif(self, interaction: discord.Interaction):
        gif_obj = await cat.gif()
        gif = gif_obj[0]['url']


        embed=discord.Embed(title="Here's a cat gif:", color=discord.Colour(cat.embedColor))
        embed.set_image(url=gif)

        await interaction.response.send_message(embed=embed)

    async def gif_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message(f'An error occured: {error}')

async def setup(bot: commands.Bot):
    await bot.add_cog(Gif(bot))