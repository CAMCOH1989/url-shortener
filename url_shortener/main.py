import json
from functools import partial
from http import HTTPStatus

import asyncpg
from aiohttp import web
from aiohttp.web_exceptions import HTTPNotFound
from aiohttp_validate import validate
from asyncpg.protocol.protocol import Record

from url_shortener.payload import convert
from url_shortener.utils import encode, decode

URL_DATA = {
    'short_url': 'http://goo.gl/hdyHd',
    'original_url': 'http://gogle.com/...',
    'created_at': '..',
    'url_id': '...'
}


def make_row_response(row: Record, base_url) -> dict:
    return{
        'url_id': row['url_id'],
        'short_url': base_url + encode(row['url_id']),
        'url': row['url'],
        'created_at': row['created_at'],
        'visited_at': row['visited_at']
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
            data['url'])
    return web.json_response(
        {'data': make_row_response(row)},
        dumps=partial(json.dumps, default=convert))


async def get_urls_handler(request: web.Request):
    async with request.app['postgres'].acquire() as conn:
        result = await conn.fetch('SELECT * FROM urls')
        return web.json_response(data={
            'data': [
                make_row_response(row)
                for row in result]},
            dumps=partial(json.dumps, default=convert))


async def get_url_handler(request: web.Request):
    async with request.app['postgres'].acquire() as conn:
        url_id = int(request.match_info.get("url_id"))
        row = await conn.fetchrow('SELECT * FROM urls WHERE url_id=$1', url_id)
        if row is None:
            raise HTTPNotFound()
        return web.json_response(data={
            'data': make_row_response(row)},
            dumps=partial(json.dumps, default=convert))


async def delete_url_handler(request: web.Request):
    async with request.app['postgres'].acquire() as conn:
        url_id = int(request.match_info.get("url_id"))
        row = await conn.fetchrow('DELETE FROM urls WHERE url_id=$1 RETURNING urls.*', url_id)
        if row is None:
            raise HTTPNotFound()
        return web.Response(status=HTTPStatus.NO_CONTENT)


async def get_redirect_handler(request: web.Request):
    url_id = decode(request.match_info.get("encoded_url_id"))
    async with request.app['postgres'].acquire() as conn:
        result = await conn.fetchrow('SELECT * FROM urls WHERE url_id=$1', url_id)
        if result is None:
            raise HTTPNotFound()

        return web.Response(status=HTTPStatus.FOUND, headers={
            "Location": result["url"]
        })


async def setup_db(app: web.Application):
    app['postgres'] = await asyncpg.create_pool('postgresql://api:hackme@0.0.0.0:5452/url_shortener')


def main():
    app = web.Application()
    app["base_url"]="http://0.0.0.0:8080"
    app.on_startup.append(setup_db)
    app.add_routes([web.post('/api/urls', create_url_handler),
                    web.get('/api/urls', get_urls_handler),
                    web.get('/api/urls/{url_id}', get_url_handler),
                    web.delete('/api/urls/{url_id}', delete_url_handler),
                    web.get('/r/{encoded_url_id}', get_redirect_handler)])

    web.run_app(app)


