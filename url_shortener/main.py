import json
from http import HTTPStatus

import asyncpg
from aiohttp import web
from aiohttp_validate import validate

URL_DATA = {
    'short_url': 'http://goo.gl/hdyHd',
    'original_url': 'http://gogle.com/...',
    'created_at': '..',
    'url_id': '...'
}


@validate(
    request_schema={
        "type": "object",
        "properties": {
            "url": {"type": "string"},
        },
        "required": ["url"],
        "additionalProperties": False
    },
)
async def create_url_handler(data, request: web.Request):
    async with request.app['postgres'].acquire() as conn:
        row = await conn.fetchrow(
            'INSERT INTO urls (url) VALUES ($1) RETURNING urls.*',
            data['url']
        )
    return web.Response(
        status=HTTPStatus.CREATED, text=json.dumps({
            'url_id':row['url_id']
        }), headers={"Content-Type": "application/json"})


async def get_urls_handler(request: web.Request):
    async with request.app['postgres'].acquire() as conn:
        async with conn.transaction():
            result = await conn.fetchval('select 2 ^ $1', 5)
            return web.json_response(data={
                'example': result
            })


async def get_url_handler(request: web.Request):
    return web.json_response(data=URL_DATA)


async def delete_url_handler(request: web.Request):
    return web.Response(status=HTTPStatus.NO_CONTENT)


async def get_redirect_handler(request: web.Request):
    redirectedLink = "http://ya.ru/"
    async with request.app['postgres'].acquire() as conn:
        async with conn.transaction():
            try:
                result = await conn.fetchval('select 2 ^ $1', 5)
                return web.HTTPFound(redirectedLink + "/" + str(result))
            except:
                return web.Response(status=HTTPStatus.NO_CONTENT)
    # raise web.HTTPFound(redirectedLink)


async def setup_db(app: web.Application):
    app['postgres'] = await asyncpg.create_pool('postgresql://api:hackme@0.0.0.0:5452/url_shortener')


def main():
    app = web.Application()
    app.on_startup.append(setup_db)
    app.add_routes([web.post('/urls', create_url_handler),
                    web.get('/urls', get_urls_handler),
                    web.get('/urls/{id}', get_url_handler),
                    web.delete('/urls/{id}', delete_url_handler),
                    web.get('/{shortLink}', get_redirect_handler)])

    web.run_app(app)


