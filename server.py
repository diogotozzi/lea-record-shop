# pylint: disable=E0401,E0611
import logging
import json
import redis

from datetime import datetime
from sanic import response
from sanic import Sanic
from sanic.request import Request
from tortoise.contrib.sanic import register_tortoise

from models.models import Clients, Discs, Orders


app = Sanic("LeaRecordShopApp")

logging.basicConfig(level=logging.ERROR)

register_tortoise(
    app,
    config_file="./tortoise.json",
    generate_schemas=True
)

# =====

class CacheAdapter:
    conn: None

    def __init__(self):
        self.conn = redis.Redis(
            host="redis",
            port=6379,
            decode_responses=True
        )

    async def get(self, key: str) -> str:
        return self.conn.get(key)

    async def set(self, key: str, value: str, expiration: int = 3600) -> str:
        return self.conn.setex(key, expiration, value)

    async def delete(self, key: str) -> str:
        return self.conn.delete(key)


@app.before_server_start
async def setup_cache(app, _):
    cache = CacheAdapter()
    app.ext.dependency(cache)

# =====

@app.get("/")
async def discs(request: Request, cache: CacheAdapter) -> response.json:
    discs = await cache.get("discs")
    if not discs:
        discs = await Discs.filter(deleted=None)
        discs = json.dumps([str(disc) for disc in discs])
        await cache.set("discs", discs)

    return response.json(discs)

@app.get("/disc/<disc_id:int>")
async def disc(request: Request, disc_id: int, cache: CacheAdapter) -> response.json:
    disc = await cache.get("disc_"+str(disc_id))
    if not disc:
        disc = await Discs.filter(id=disc_id, deleted=None).first()
        disc = json.dumps(str(disc))
        await cache.set("disc_"+str(disc_id), disc)

    if "None" in disc:
        return response.json(
            body={"disc":"disc does not exist"},
            status=404,
        )

    return response.json(disc)

@app.post("/disc")
async def add_disc(request: Request, cache: CacheAdapter) -> response.json:
    data = json.loads(request.body)

    disc = await Discs.create(
        name=data["name"],
        artist=data["artist"],
        launched=data["lauched"],
        style=data["style"],
        quantity=data["quantity"],
        created=datetime.now(),
    )

    await cache.delete("discs")

    return response.json({"disc": str(disc)}, status=201)

@app.delete("/disc/<disc_id:int>", ignore_body=False)
async def delete_disc(request: Request, disc_id: int, cache: CacheAdapter) -> response.json:
    disc = await Discs.filter(id=disc_id, deleted=None).first()

    if not disc:
        return response.json(
            body={"disc":"disc does not exist"},
            status=404,
        )

    disc.deleted=datetime.now()
    await disc.save()

    await cache.delete("disc_"+str(disc_id))
    await cache.delete("discs")

    return response.json(str(disc))

# =====

@app.get("/client/<client_id:int>")
async def client(request: Request, client_id: int, cache: CacheAdapter) -> response.json:
    client = await cache.get("client_"+str(client_id))
    if not client:
        client = await Clients.filter(id=client_id, deleted=None).first()
        client = json.dumps(str(client))
        await cache.set("client_"+str(client_id), client)

    if "None" in client:
        return response.json(
            body={"client":"client does not exist"},
            status=404,
        )

    return response.json(client)

@app.get("/clients")
async def clients(request: Request, cache: CacheAdapter) -> response.json:
    clients = await cache.get("clients")
    if not clients:
        clients = await Clients.filter(deleted=None)
        clients = json.dumps([str(client) for client in clients])
        await cache.set("clients", clients)

    return response.json(clients)

@app.post("/client")
async def add_client(request: Request, cache: CacheAdapter) -> response.json:
    data = json.loads(request.body)

    client = await Clients.create(
        name=data["name"],
        document=data["document"],
        birthdate=datetime.strptime(data["birthdate"], "%m/%d/%Y"),
        email=data["email"],
        phone=data["phone"],
        created=datetime.now(),
    )

    await cache.delete("clients")

    return response.json(str(client), status=201)

@app.delete("/client/<client_id:int>", ignore_body=False)
async def delete_client(request: Request, client_id: int, cache: CacheAdapter) -> response.json:
    client = await Clients.filter(id=client_id, deleted=None).first()

    if not client:
        return response.json(
            body={"client":"client does not exist"},
            status=404,
        )

    client.deleted=datetime.now()
    await client.save()

    await cache.delete("client_"+str(client_id))

    return response.json(str(client))

# =====

@app.post("/order")
async def add_order(request: Request, cache: CacheAdapter) -> response.json:

    data = json.loads(request.body)

    client = await Clients.filter(id=data["client_id"], deleted=None).first()
    if not client:
        return response.json(
            body={"order":"client does not exist"},
            status=404,
        )

    disc = await Discs.filter(id=data["disc_id"], deleted=None).first()
    if disc.quantity < int(data["quantity"]):
        return response.json(
            body={"order":"no discs available at stock"},
            status=404,
        )

    disc.quantity=int(disc.quantity) - 1
    await disc.save()

    order = await Orders.create(
        client_id=data["client_id"],
        disc_id=data["disc_id"],
        quantity=data["quantity"],
        created=datetime.now(),
    )

    await cache.delete("disc_"+str(data["disc_id"]))
    await cache.delete("discs")

    return response.json(str(order), status=201)

# =====

if __name__ == '__main__':
    app.run()