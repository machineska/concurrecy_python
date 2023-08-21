import time
from random import randint
import requests as requests
from flask import Flask


app = Flask(__name__)


def get_xkcd_image():
    random = randint(0, 300)
    response = requests.get(f'http://xkcd.com/{random}/info.0.json')
    return response.json()['img']


def get_multiple_images(number):
    return [get_xkcd_image() for _ in range(number)]


@app.get('/comic')
def hello():
    start = time.perf_counter()
    urls = get_multiple_images(5)
    end = time.perf_counter()

    markup = f"Time taken: {end-start}<br><br>"
    for url in urls:
        markup += f'<img src="{url}"></img><br><br>'

    return markup


if __name__ == '__main__':
    app.run(debug=True)
