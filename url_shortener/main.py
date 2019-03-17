import json
from http import HTTPStatus

from aiohttp import web


URL_DATA = {
    'short_url': 'http://goo.gl/hdyHd',
    'original_url': 'http://gogle.com/...',
    'created_at': '..',
    'url_id': '...'
}


async def create_url_handler(request: web.Request):

    return web.Response(
        status=HTTPStatus.CREATED, text=json.dumps(URL_DATA), headers={"Content-Type": "application/json"})


async def get_urls_handler(request: web.Request):
    return web.json_response(data=[URL_DATA])


async def get_url_handler(request: web.Request):
    return web.json_response(data=URL_DATA)


async def delete_url_handler(request: web.Request):
    return web.Response(status=HTTPStatus.NO_CONTENT)


def main():
    app = web.Application()
    app.add_routes([web.post('/urls', create_url_handler),
                    web.get('/urls', get_urls_handler),
                    web.get('/urls/{id}', get_url_handler),
                    web.delete('/urls/{id}', delete_url_handler)])

    web.run_app(app)
