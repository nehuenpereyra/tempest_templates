
from flask_seeder import Seeder

from app.models import Role, Permission


class RoleSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 2

    def run(self):
        permissions = {each.name: each for each in Permission.all()}

        Role(
            name="Administrador",
            permissions=list(permissions.values())
        ).save()
