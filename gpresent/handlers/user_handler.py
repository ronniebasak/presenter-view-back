# -*- coding: utf-8 -*-
from aiohttp import web
from ..models.user import User
import json
import pymongo.errors as MongoErrors
import bcrypt
import sys
import bson.json_util as json_util
import jwt
from datetime import datetime, timedelta
import os
from ..middleware.json_middleware import jsonify

async def index(request):
    return web.Response(text='Hello Aiohttp!')



async def get_by_uid(request):
    return web.Response(text='Hello {}'.format(request.match_info.get('uid')))


@jsonify
async def add_new_user(request):
    request_data = request.body
    
    password = request_data['password']
    salt = bcrypt.gensalt();
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt);

    try:
        user_inst = User(username=request_data['username'], password=hashed, email=request_data['email'], avatar=request_data['avatar']);
        await user_inst.insert();
        return web.Response(text='Sucess')

    except MongoErrors.DuplicateKeyError:
        print("::::::::ERROR::::::",sys.exc_info()[1])
        return {"status": "Duplicate Entry Rejected", 'statusCode': 401}


@jsonify
async def authenticate(request):
    request_data = request.body

    user_inst = await User.get(db_filter={'username': request_data['username']})
    print(user_inst)
    
    password = request_data['password'].encode('utf-8')
    if(not bcrypt.checkpw(password, user_inst.password.encode('utf-8'))):
        return web.Response(body=json.dumps({'status': "Auth fail"}), status=401)

    token=jwt.encode({
        'id': str(user_inst.id), 
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow()+timedelta(seconds=int(os.getenv('SESSION_TIMEOUT')))
    }, os.getenv('SECRET'))
    
    to_return = {'token': token.decode('ascii')}
    return web.Response(body=json.dumps(to_return))



__all__ = [
    "index",
    "get_by_uid",
    "add_new_user",
    "authenticate"
]