from sanic import Sanic
from sanic.response import json
import asyncpg
import asyncio
import uvloop
from signal import signal, SIGINT
app = Sanic()

app.db_pool = None
DATABASE = {
    'DB_NAME': 'zhengshi',
    'DB_USER': 'yuan',
    'DB_USER_PASSWORD': 'qq111111',
    'DB_HOST': '127.0.0.1',
    'DB_PORT': '5432',
}


async def init_db() -> 'asyncpg.pool.Pool':
    app.db_pool = await asyncpg.create_pool(max_size=50,
                                            user=DATABASE['DB_USER'],
                                            password=DATABASE['DB_USER_PASSWORD'],
                                            database=DATABASE['DB_NAME'],
                                            host=DATABASE['DB_HOST'])

@app.route('/get/sale/order/line/<order_name>')
async def order_name(request, order_name):
    async with app.db_pool.acquire() as conn:
        result = await conn.fetchrow("""SELECT sol.name,sol.product_uom_qty,sol.price_unit
                                              FROM sale_order_line sol LEFT JOIN sale_order so ON sol.order_id=so.id
                                               WHERE so.name=$1 """, order_name)
        result = dict(result)
        return json({'result': {
            'name': result.get('name'),
            'product_uom_qty': float(result.get('product_uom_qty')),
            'price_unit': float(result.get('price_unit'))
        }})

if __name__ == '__main__':
    asyncio.set_event_loop(uvloop.new_event_loop())
    loop = asyncio.get_event_loop()
    task = loop.create_task(init_db())
    loop.run_until_complete(task)
    server = app.create_server(host="0.0.0.0", port=8000)
    task = asyncio.ensure_future(server)
    signal(SIGINT, lambda s, f: loop.stop())
    try:
        loop.run_forever()
    except:
        loop.stop()
