import asyncio
import json
import bson.json_util as json_util
from aiohttp import web


def jsonify(func):
    async def handler(request):
        request.body = json.loads(await request.content.read())
        d = await func(request)
        if type(d) == dict:
            if('statusCode' in d and type(d['statusCode'])==int):
                return web.Response(body=json_util.dumps(d), headers=[('content-type', 'application/json')], status=d['statusCode'])
            return web.Response(body=json_util.dumps(d), headers=[('content-type', 'application/json')])
        elif type(d)==list:
            return web.Response(body=json_util.dumps(d), headers=[('content-type', 'application/json')])
        elif type(d) == web.Response:
            return d
        return web.Response(json.dumps({'status': "Internal Server Error"}), status=500, headers=[('content-type', 'application/json')])
    return handler