from tortoise import fields
from tortoise import Model
from tortoise import Type


class Discs(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=False)
    artist = fields.CharField(max_length=255, null=False)
    launched = fields.DateField(null=False)
    style = fields.CharField(max_length=255, null=False)
    quantity = fields.IntField(null=False)
    created = fields.DatetimeField(null=False)
    deleted = fields.DatetimeField(null=True)

    def __str__(self) -> str:
        obj = {}
        obj["id"] = f"{self.id}"
        obj["name"] = f"{self.name}"
        obj["artist"] = f"{self.artist}"
        obj["launched"] = f"{self.launched:%m/%d/%Y}"
        obj["style"] = f"{self.style}"
        obj["quantity"] = f"{self.quantity}"
        return f"{obj}"

class Clients(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=False)
    document = fields.CharField(max_length=255, null=False)
    birthdate = fields.DateField(null=False)
    email = fields.CharField(max_length=255, null=False)
    phone = fields.CharField(max_length=255, null=False)
    created = fields.DatetimeField(null=False)
    deleted = fields.DatetimeField(null=True)

    def __str__(self) -> str:
        obj = {}
        obj["id"] = f"{self.id}"
        obj["name"] = f"{self.name}"
        obj["document"] = f"{self.document}"
        obj["birthdate"] = f"{self.birthdate:%m/%d/%Y}"
        obj["email"] = f"{self.email}"
        obj["phone"] = f"{self.phone}"
        return f"{obj}"

class Orders(Model):
    id = fields.IntField(pk=True)
    client_id = fields.CharField(max_length=255, null=False)
    disc_id = fields.CharField(max_length=255, null=False)
    quantity = fields.IntField(null=False)
    created = fields.DatetimeField(null=False)
    deleted = fields.DatetimeField(null=True)

    def __str__(self) -> int:
        obj = {}
        obj["client_id"] = f"{self.client_id}"
        obj["disc_id"] = f"{self.disc_id}"
        obj["quantity"] = f"{self.quantity}"
        obj["created"] = f"{self.created:%m/%d/%Y}"
        return f"{obj}"


class Router:
    def db_for_read(self, model: Type[Model]):
        return "slave"

    def db_for_write(self, model: Type[Model]):
        return "master"