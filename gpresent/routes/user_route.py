from ..handlers.user_handler import *


def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_get('/users/{uid}', get_by_uid)
    app.router.add_post('/users', add_new_user)
    app.router.add_post('/users/auth', authenticate)
