from fastapi import FastAPI, Query

app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Hello World'}


@app.get('/schedule')
async def get_schedule(arrival, departure, date):
    return {}


@app.get('/train/{train_id}')
async def get_train(train_id: int = Query(None)):
    if train_id is not None:
        return {'id': train_id, 'text': 'success'}
    else:
        return {'error': 'Code'}


@app.post('/train/{train_id}')
async def post_train(train_id: int = Query(None)):
    if train_id is not None:
        return {'id': train_id, 'text': 'success'}
    else:
        return {'error': 'Code'}


