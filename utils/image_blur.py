import math
import requests
from PIL import Image, ImageFilter, ImageEnhance
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
from typing import Union

async def x_times_what_is_bigger_than_y(x: int, y: int) -> Union[int, float]:
    for num in range(100):
        if x * num > y:
            return num

async def find_scale_factor(width: int, height: int, goal_width: int, goal_height: int) -> Union[int, float]:
    for num in range(100):
        if (width * num >= goal_width) and (height * num >= goal_height):
            return num

# Find the best number of rows and columns for the grid
async def find_rows_and_cols(img_count: int):
    sqrt = math.sqrt(img_count)
    rows = math.floor(sqrt)
    cols = math.ceil(sqrt)
    return rows, cols

# Resize images while maintaining its aspect ratio
async def resize_image(image, cell_width, cell_height):
    width_ratio = cell_width / image.width
    height_ratio = cell_height / image.height
    resize_ratio = min(width_ratio, height_ratio)
    new_size = (int(image.width * resize_ratio), int(image.height * resize_ratio))
    return image.resize(new_size, Image.LANCZOS)

def download_image(url):
    for i in range(3):
        try:
            response = requests.get(url)
            return Image.open(BytesIO(response.content))
        except:
            pass

    return None

async def gen_images_from_urls(urls):
    with ThreadPoolExecutor() as executor:
        tasks = [executor.submit(download_image, url) for url in urls if url is not None]
        return [task.result() for task in tasks if task is not None]


async def combine_images(urls):
    # Load images
    images = await gen_images_from_urls(urls)
    print('finished downloading images')
    img_count = len(images)
    print(f'image count {img_count}')

    # Calculate rows and columns, as well as the canvas size (downscale if too big)
    rows, cols = await find_rows_and_cols(img_count)
    canvas_width, canvas_height = cols * max(img.width for img in images), rows * max(img.height for img in images)
    if canvas_width > 2048 or canvas_height > 2048:
        print('downscaling image')
        scale_factor = await find_scale_factor(canvas_width, canvas_height, 2048, 2048)
        canvas_width = int(canvas_width * scale_factor)
        canvas_height = int(canvas_height * scale_factor)

    # calc cell width and height
    cell_width = canvas_width // cols
    cell_height = canvas_height // rows

    # canvas_size = (cols * 350, rows * 350)
    # cell_width = 350
    # cell_height = 350

    # Initialize canvas
    canvas = Image.new('RGB', (canvas_width, canvas_height))

    # Paste images onto canvas
    for row in range(rows):
        for column in range(cols):
            if not images:
                break
            img = images.pop(0)

            # Rescale and blur small images
            if img.width < cell_width and img.height < cell_height:
                img_scale_factor = await find_scale_factor(img.width, img.height, cell_width, cell_height)

                bg = img.resize(
                    size=(
                        int(img.width * img_scale_factor),
                        int(img.height * img_scale_factor)
                    ),
                    resample=Image.Resampling.LANCZOS
                )
                bg = bg.filter(ImageFilter.GaussianBlur(radius=12))
                bg = ImageEnhance.Brightness(bg).enhance(0.5)
                bg = bg.crop((0, 0, cell_width, cell_height))
                paste_box = (column*cell_width, row*cell_height)
                canvas.paste(bg, paste_box)

            # Resize to cell size
            print('resize image to cell size')
            img = await resize_image(img, cell_width, cell_height)
            print('resized image to cell size')
            paste_box = (column*cell_width + (cell_width - img.width) // 2, row*cell_height + (cell_height - img.height) // 2)
            canvas.paste(img, paste_box)



    # Convert canvas to bytes
    try:
        _buffer = BytesIO()
        canvas.save(_buffer, 'png')
        return _buffer.getvalue()
    except:
        print('a')