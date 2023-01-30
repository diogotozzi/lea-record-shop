from tortoise import fields
from tortoise import Model


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
        return f"{self.name}"

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
        return f"{self.name}"

class Orders(Model):
    id = fields.IntField(pk=True)
    client_id = fields.CharField(max_length=255, null=False)
    disc_id = fields.CharField(max_length=255, null=False)
    quantity = fields.IntField(null=False)
    created = fields.DatetimeField(null=False)
    deleted = fields.DatetimeField(null=True)

    def __str__(self) -> int:
        return f"{self.id}"
