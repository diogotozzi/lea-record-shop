from tortoise import Model
from tortoise import Type


class Router:
    def db_for_read(self, model: Type[Model]):
        return "replica"

    def db_for_write(self, model: Type[Model]):
        return "main"