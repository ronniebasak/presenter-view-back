import asyncio
import json
import bson.json_util as json_util
from aiohttp import web


headers = [
('Content-Type', 'application/json'),
('Access-Control-Allow-Origin', '*')
]

def jsonify(func):
    async def handler(request):
        f = await request.content.read()
        try: 
            request.body = json_util.loads(f)
        except:
            request.body = {}
            
        d = await func(request)
        print (type(d))
        if type(d) == dict:
            if('statusCode' in d and type(d['statusCode'])==int):
                return web.Response(body=json_util.dumps(d), headers=headers, status=d['statusCode'])
            return web.Response(body=json_util.dumps(d), headers=headers)
        elif type(d)==list:
            return web.Response(body=json_util.dumps(d), headers=headers)
        elif type(d) == web.Response:
            return d
        return web.Response(json_util.dumps({'status': "Internal Server Error"}), status=500, headers=headers)
    return handler