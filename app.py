import time
from random import randint
import requests as requests
from flask import Flask


app = Flask(__name__)


def get_xkcd_image():
    random = randint(0, 300)
    response = requests.get(f'http://xkcd.com/{random}/info.0.json')
    return response.json()['img']


@app.get('/comic')
def hello():
    start = time.perf_counter()
    url = get_xkcd_image()
    end = time.perf_counter()
    return f"""
        Time taken: {end-start}<br><br>
        <img src="{url}"></img>
    """


if __name__ == '__main__':
    app.run(debug=True)
