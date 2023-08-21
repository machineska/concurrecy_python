import asyncio
import time
import requests
from random import randint
import httpx
from flask import Flask


app = Flask(__name__)
img_count = 30

# function converted to coroutine
async def get_xkcd_image(session):
    random = randint(0, 300)
    result = await session.get(f'http://xkcd.com/{random}/info.0.json', follow_redirects=True) # dont wait for the response of API
    return result.json()['img']


def get_xkcd_image_single():
    random = randint(0, 300)
    response = requests.get(f'http://xkcd.com/{random}/info.0.json')
    return response.json()['img']


# function converted to coroutine
async def get_multiple_images(number):
    async with httpx.AsyncClient() as session: # async client used for async functions
        tasks = [get_xkcd_image(session) for _ in range(number)]
        result = await asyncio.gather(*tasks, return_exceptions=True) # gather used to collect all coroutines and run them using loop and get the ordered response
    return result


def get_xkcd_image_sync():
    random = randint(0, 300)
    response = requests.get(f'http://xkcd.com/{random}/info.0.json')
    return response.json()['img']


def get_multiple_images_sync(number):
    return [get_xkcd_image_sync() for _ in range(number)]




@app.get('/comic_async')
async def hello_async():
    start = time.perf_counter()
    urls = await get_multiple_images(img_count)
    end = time.perf_counter()
    markup = f"Time taken: {end-start}<br><br>"
    for url in urls:
        markup += f'<img src="{url}"></img><br><br>'

    return markup


@app.get('/comic_sync')
def hello_sync():
    start = time.perf_counter()
    urls = get_multiple_images_sync(img_count)
    end = time.perf_counter()

    markup = f"Time taken: {end-start}<br><br>"
    for url in urls:
        markup += f'<img src="{url}"></img><br><br>'

    return markup


@app.get('/comic_single')
def hello_single():
    start = time.perf_counter()
    url = get_xkcd_image_single()
    end = time.perf_counter()
    return f"""
        Time taken: {end-start}<br><br>
        <img src="{url}"></img>
    """



if __name__ == '__main__':
    app.run(debug=True)
