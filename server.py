# pylint: disable=E0401,E0611
import logging
import json

from datetime import datetime

from models import Clients, Discs, Orders

from sanic import response
from sanic import Sanic
from sanic.request import Request
from tortoise.contrib.sanic import register_tortoise


app = Sanic("LeaRecordShopApp")

logging.basicConfig(level=logging.DEBUG)

register_tortoise(
    app,
    db_url="mysql://root:root@127.0.0.1/lea",
    modules={"models": ["models"]},
    generate_schemas=True
)

@app.get("/disc/<disc_id:int>")
async def disc(request: Request, disc_id: int) -> response.json:
    disc = await Discs.filter(id=disc_id, deleted=None).first()
    return response.json({"disc": str(disc)})

@app.get("/discs")
async def discs(request: Request) -> response.json:
    discs = await Discs.filter(deleted=None)
    return response.json({"discs": [str(disc) for disc in discs]})

@app.post("/disc")
async def add_disc(request: Request) -> response.json:
    data = json.loads(request.body)

    disc = await Discs.create(
        name=data["name"],
        artist=data["artist"],
        launched=data["lauched"],
        style=data["style"],
        quantity=data["quantity"],
        created=datetime.now(),
    )

    return response.json({"disc": str(disc)}, status=201)


@app.get("/client/<client_id:int>")
async def client(request: Request, client_id: int) -> response.json:
    client = await Clients.filter(id=client_id, deleted=None).first()
    return response.json({"client": str(client)})

@app.get("/clients")
async def clients(request: Request) -> response.json:
    clients = await Clients.filter(deleted=None)
    return response.json({"clients": [str(client) for client in clients]})

@app.post("/client")
async def add_client(request: Request) -> response.json:
    data = json.loads(request.body)

    client = await Clients.create(
        name=data["name"],
        document=data["document"],
        birthdate=datetime.strptime(data["birthdate"], '%m/%d/%Y'),
        email=data["email"],
        phone=data["phone"],
        created=datetime.now(),
    )

    return response.json({"client": str(client)}, status=201)

@app.delete("/client/<client_id:int>", ignore_body=False)
async def delete_client(request: Request, client_id: int) -> response.json:
    client = await Clients.filter(id=client_id).first()
    client.deleted=datetime.now()
    await client.save()
    return response.json({"client": str(client)})


@app.post("/order")
async def add_order(request: Request) -> response.json:

    data = json.loads(request.body)

    client = await Clients.filter(id=data["client_id"], deleted=None).first()
    if not client:
        return response.json({"order":"client does not exist"}, status=204)

    disc = await Discs.filter(id=data["disc_id"], deleted=None).first()
    if disc.quantity < data["quantity"]:
        return response.json({"order":"not enough discs"}, status=204)
    
    disc.quantity=int(disc.quantity) - 1
    await disc.save()

    order = await Orders.create(
        client_id=data["client_id"],
        disc_id=data["disc_id"],
        quantity=data["quantity"],
        created=datetime.now(),
    )

    return response.json({"order": str(order)})

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000)