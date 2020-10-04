from aiohttp import web, WSMessage, WSMsgType, WSCloseCode
from ..middleware.json_middleware import jsonify
from ..middleware.auth_middleware import authenticated
from ..models.document import GDocument



async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws



@jsonify
@authenticated
async def get_document_id(request): # document by id
    return {'result': 1}


@jsonify
@authenticated
async def get_all_documents(request):
    doc_list = GDocument.all(db_filter={});
    to_return = []
    async for doc in doc_list:
        to_return.append(doc.dict())
    
    return to_return


@jsonify
@authenticated
async def add_new_document(request):
    if not 'name' in request.body:
        return {'messaage': "Bad Request", 'statusCode': 400}

    content=""
    if 'content' in request.body:
        content=request.body['content']

    doc_inst = GDocument(created_by=request.session_data['id'], name=request.body['name'], content=content)
    await doc_inst.insert();
    
    return doc_inst.dict();



