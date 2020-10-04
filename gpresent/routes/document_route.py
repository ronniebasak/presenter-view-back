from ..handlers.document_handler import *


def setup_routes(app):
    app.router.add_get('/documents/{did}', get_document_id)
    app.router.add_get('/documents', get_all_documents)
    app.router.add_post('/documents', add_new_document)
    app.router.add_get('/ws', websocket_handler)
