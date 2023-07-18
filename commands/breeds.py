import discord
from discord.ext import commands
from utils import Cat

cat = Cat()
greenStar = ':green_square:'
blackStar = ':black_large_square:'

# Buttons for `/breeds list`
class Pages(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, pages: list):
        super().__init__(timeout=None)
        self.pages = pages
        self.interaction = interaction
        self.current_page = 0

    @discord.ui.button(label='Previous', style=discord.ButtonStyle.grey, disabled=True)
    async def previous(self, interaction: discord.Interaction, _button: discord.ui.Button):
        self.current_page -= 1

        if self.current_page == 0:
            for i in self.children:
                if i.label == 'Previous':
                    i.disabled = True
                elif i.label == 'Next':
                    i.disabled = False
        else:
            for i in self.children:
                if i.label == 'Previous':
                    i.disabled = False
                elif i.label == 'Next':
                    i.disabled = False

        await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)

    @discord.ui.button(label='Next', style=discord.ButtonStyle.grey)
    async def next(self, interaction: discord.Interaction, _button: discord.ui.Button):
        self.current_page += 1

        if self.current_page == len(self.pages) - 1:
            for i in self.children:
                if i.label == 'Next':
                    i.disabled = True
                elif i.label == 'Previous':
                    i.disabled = False
        else:
            for i in self.children:
                if i.label == 'Next':
                    i.disabled = False
                elif i.label == 'Previous':
                    i.disabled = False

        await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.interaction.user.id:
            img_obj = await cat.image()
            img = img_obj[0]['url']

            embed = discord.Embed(title='Error', description="You can't use this button because you didn't start the command. Try running </breeds:1> and selecting \"list\".", color=discord.Colour.red())
            embed.set_image(url=img)

            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        else:
            return True

async def getBreedInfo(interaction, breed):
    img_obj = await cat.image()
    breed_obj = await cat.get_breed_info(breed)
    img = img_obj[0]['url']

    embed = discord.Embed(title=breed_obj['name'], description=breed_obj['description'], color=discord.Colour(cat.embedColor))
    embed.add_field(name='Stats', value=f'''
**Weight**\n{breed_obj['weight']['imperial']} lbs / {breed_obj['weight']['metric']} kg\n
**Temperament**\n{breed_obj['temperament']}\n
**Origin**\n{breed_obj['origin']}\n
**Life Span**\n{breed_obj['life_span']} years\n
**Wikipedia URL**\n{breed_obj['wikipedia_url']}\n''', inline=True)
    embed.set_image(url=img)

    await interaction.response.send_message(embed=embed)

async def getBreedStats(interaction, breed):
    img_obj = await cat.image()
    breed_obj = await cat.get_breed_info(breed)
    img = img_obj[0]['url']


    embed=discord.Embed(title=breed_obj['name'], color=discord.Colour(cat.embedColor))
    embed.add_field(name='Adaptability', value=f'{greenStar * breed_obj["adaptability"]}{blackStar * (5 - breed_obj["adaptability"])}', inline=True)
    embed.add_field(name='Affection Level', value=f'{greenStar * breed_obj["affection_level"]}{blackStar * (5 - breed_obj["affection_level"])}', inline=True)
    embed.add_field(name='Child Friendly', value=f'{greenStar * breed_obj["child_friendly"]}{blackStar * (5 - breed_obj["child_friendly"])}', inline=True)
    embed.add_field(name='Dog Friendly', value=f'{greenStar * breed_obj["dog_friendly"]}{blackStar * (5 - breed_obj["dog_friendly"])}', inline=True)
    embed.add_field(name='Energy Level', value=f'{greenStar * breed_obj["energy_level"]}{blackStar * (5 - breed_obj["energy_level"])}', inline=True)
    embed.add_field(name='Grooming', value=f'{greenStar * breed_obj["grooming"]}{blackStar * (5 - breed_obj["grooming"])}', inline=True)
    embed.add_field(name='Health Issues', value=f'{greenStar * breed_obj["health_issues"]}{blackStar * (5 - breed_obj["health_issues"])}', inline=True)
    embed.add_field(name='Intelligence', value=f'{greenStar * breed_obj["intelligence"]}{blackStar * (5 - breed_obj["intelligence"])}', inline=True)
    embed.add_field(name='Shedding Level', value=f'{greenStar * breed_obj["shedding_level"]}{blackStar * (5 - breed_obj["shedding_level"])}', inline=True)
    embed.add_field(name='Social Needs', value=f'{greenStar * breed_obj["social_needs"]}{blackStar * (5 - breed_obj["social_needs"])}', inline=True)
    embed.add_field(name='Stranger Friendly', value=f'{greenStar * breed_obj["stranger_friendly"]}{blackStar * (5 - breed_obj["stranger_friendly"])}', inline=True)
    embed.add_field(name='Vocalisation', value=f'{greenStar * breed_obj["vocalisation"]}{blackStar * (5 - breed_obj["vocalisation"])}', inline=True)
    embed.set_image(url=img)

    await interaction.response.send_message(embed=embed)

async def handleError(interaction):
    img_obj = await cat.image()
    img = img_obj[0]['url']

    embed = discord.Embed(title='Error', description="This breed doesn't exist.\nPlease check you entered the corresponding 4 letter code for your chosen breed by running </breeds:1> and selecting \"list\".",color=discord.Colour.red())
    embed.set_image(url=img)

    await interaction.response.send_message(embed=embed)

class breeds(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name='breeds', description='Sends info on a cat breed.')
    @discord.app_commands.describe(breed='Your breed of choice that you want to know more about.')
    @discord.app_commands.choices(type=[
        discord.app_commands.Choice(name='information', value='Information'),
        discord.app_commands.Choice(name='stats', value='Stats'),
        discord.app_commands.Choice(name='list', value='List')
    ])

    async def breeds(self, interaction: discord.Interaction, type: discord.app_commands.Choice[str], breed: str = ''):
        breeds = await cat.get_breeds()
        breedIDs = [breed['id'] for breed in breeds]

        if type.value == 'Information':
            if breed in breedIDs:
                await getBreedInfo(interaction, breed)
            else:
                await handleError(interaction)

        elif type.value == 'Stats':
            if breed in breedIDs:
                await getBreedStats(interaction, breed)
            else:
                await handleError(interaction)

        elif type.value == 'List':
            embeds = []
            count = 0

            for num in range(0, len(breeds), 10):
                count += 1
                embed = discord.Embed(title='Breed List', description=f'The bot currently supports a total of {len(breeds)} breeds.\nTo get any information about the breeds listed below, you can run the </breeds:1> command and select either "information" or "statistics".', color=discord.Colour(cat.embedColor))

                for breed in breeds[num:num+10]:
                    embed.add_field(name=breed['name'], value=breed['id'], inline=True)

                embed.set_footer(text=f'Page {count} of {len(breeds) // 10 + 1}')
                embeds.append(embed)

            images = await cat.image(limit=len(embeds))

            for index in range(len(embeds)):
                embeds[index].set_image(url=images[index]['url'])

            await interaction.response.send_message(embed=embeds[0], view=Pages(interaction, embeds))

async def setup(bot: commands.Bot):
    await bot.add_cog(breeds(bot))