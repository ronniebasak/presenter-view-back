import asyncio
from aiohttp import web
import jwt
import os

def authenticated(func):
    async def handler(request):
        if('Authorization' in request.headers):
            # try:
                udata = jwt.decode(request.headers['Authorization'], os.getenv('SECRET'))
                request.session_data = udata;
                return await func(request)
            # except:
            #     print("AHA")
            #     return {'status': "Error", 'message': "Authorization Failed", 'statusCode': 401}

        print("AHI")
        return {'status': "Error", 'message': "Authorization Failed", 'statusCode': 401}
    return handler