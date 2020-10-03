from aiohttp import web
import gpresent.routes.user_route as user_route


app = web.Application()


user_route.setup_routes(app)

web.run_app(app, host='127.0.0.1', port=8080)
