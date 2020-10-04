from aiohttp import web, WSMessage, WSMsgType, WSCloseCode
from ..middleware.json_middleware import jsonify
from ..middleware.auth_middleware import authenticated
from ..models.document import GDocument
from bson import ObjectId, json_util

large_ds = {}

async def websocket_handler(request):
    global large_ds
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                data = json_util.loads(msg.data)
                if data['type'] == "INIT":
                    print("INIT");
                    print("DOCUMENT ID", data['did'])

                    if(data['did'] not in large_ds):
                        large_ds[data['did']] = {'users': [], 'ws_pool': []}

                    large_ds[data['did']]['users'].append(data['userInfo'])
                    print(type(ws))
                    large_ds[data['did']]['ws_pool'].append(ws)

                    print(large_ds)
                    await ws.send_json({'type': 'INIT_ACK'})
                    await ws.send_str(json_util.dumps({'type': 'USER_LIST', 'userList': large_ds[data['did']]['users']}))

                    for ws_inst in large_ds[data['did']]['ws_pool']:
                        if ws_inst != ws:
                            await ws_inst.send_str(json_util.dumps({'type': 'USER_LIST', 'userList': large_ds[data['did']]['users']}))

                elif data['type'] == "CLOSE":
                    print("CLOSE");

                    large_ds[data['did']]['ws_pool'].remove(ws);

                    idx = -1
                    for ui in range(len(large_ds[data['did']]['users'])):
                        user = large_ds[data['did']]['users'][ui]
                        if(user['id'] == data['userInfo']['id']):
                            idx = ui
                            break;

                    if idx>-1:
                        del large_ds[data['did']]['users'][idx]

                        
                    await ws.close()

                    for ws_inst in large_ds[data['did']]['ws_pool']:
                        await ws_inst.send_str(json_util.dumps({'type': 'USER_LIST', 'userList': large_ds[data['did']]['users']}))

                else:
                    ws.send_str(json_util.dumps({type: 'UNKNOWN'}))
                # await ws.send_str(msg.data + '/answer')
                
        elif msg.type == WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws



@jsonify
@authenticated
async def get_document_id(request): # document by id
    did = request.match_info.get('did');
    doc_inst = await GDocument.get(db_filter={'_id': ObjectId(did)});
    return doc_inst.dict()


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



