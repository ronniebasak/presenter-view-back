from aiohttp import web
from aiohttp_middlewares import cors_middleware
from aiohttp_middlewares.cors import DEFAULT_ALLOW_HEADERS

import gpresent.routes.user_route as user_route
import gpresent.routes.document_route as document_route

import dotenv 
dotenv.load_dotenv()

app = web.Application(
    middlewares=[cors_middleware(allow_all=True)]
)


user_route.setup_routes(app)
document_route.setup_routes(app)

web.run_app(app, host='127.0.0.1', port=8080)
