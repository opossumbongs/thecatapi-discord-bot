import discord
from discord.ext import commands
from utils.api import Cat
from utils.image_blur import combine_images
from typing import Optional
from io import BytesIO

cat = Cat()

class Image(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name = 'image', description = 'Sends a cat image.')
    async def image(self, interaction: discord.Interaction, breed: Optional[str], amount: Optional[int] = 1):
        if not breed:
            if amount <= 10 and amount > 1:
                # Responding to the interaction so that it doesn't timeout
                embed = discord.Embed(title='Processing...', description='This may take a while.', color=discord.Colour(cat.embedColor))
                await interaction.response.send_message(embed=embed)

                # Fetch images and then combine them
                print('fetching list of images')
                images = await cat.image(amount=amount)
                print('fetched list of images now we\'re downloading each image and combining them')
                image = await combine_images([img.get('url', None) for img in images])
                print('image combined')

                # Convert the returned image to a BytesIO object, then create a discord.File object from it
                bytes_obj = BytesIO(image)
                _file = discord.File(fp=bytes_obj, filename='image.png')

                embed = discord.Embed(title="Here's some cat images", color=discord.Colour(cat.embedColor))

                await interaction.edit_original_response(attachments=[_file], embed=embed)

            elif amount == 1:
                await interaction.response.send_message('a')



            # embed = discord.Embed(title="Here's a cat image:", color=discord.Colour(cat.embedColor))
            # embed.set_image(url=img)
        else:
            breeds = await cat.get_breeds()
            breedIDs = [breed['id'] for breed in breeds]

            if breed in breedIDs:
                img_obj = await cat.image(breed=breed)
                breed_obj = await cat.get_breed_info(breed)
                img = img_obj[0]['url']
                breedname = breed_obj['name']

                embed = discord.Embed(title="Here's a cat image:", description = f'Breed: {breedname}', color=discord.Colour(cat.embedColor))
                embed.set_image(url=img)
            else:
                img_obj = await cat.image()
                img = img_obj[0]['url']

                embed = discord.Embed(title='Error', description = "This breed doesn't exist. Please check your spelling and try again.", color=discord.Colour.red())
                embed.set_image(url=img)

        # await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Image(bot))