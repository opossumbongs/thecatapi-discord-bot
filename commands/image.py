import discord
from discord.ext import commands
from utils import Cat

cat = Cat()

class Image(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name = 'image', description = 'Sends a cat image.')
    async def image(self, interaction: discord.Interaction, breed: str = None):
        if not breed:
            img_obj = await cat.image()
            print(img_obj)
            image = img_obj[0]['url']
            print(image)

            embed = discord.Embed(title="Here's a cat image:", color=discord.Colour(cat.embedColor))
            embed.set_image(url=image)
        else:
            breeds = await cat.get_breeds()
            breedIDs = [breed['id'] for breed in breeds]

            if breed in breedIDs:
                image = await cat.image(breed=breed)[0]['url']
                breedname = await cat.get_breed_info(breed)['name']

                embed = discord.Embed(title="Here's a cat image:", description = f'Breed: {breedname}', color=discord.Colour(cat.embedColor))
                embed.set_image(url=image)
            else:
                image = await cat.image()[0]['url']

                embed = discord.Embed(title='Error', description = "This breed doesn't exist. Please check your spelling and try again.", color=discord.Colour.red())
                embed.set_image(url=image)

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Image(bot))