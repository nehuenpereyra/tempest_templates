
from flask_seeder import Seeder

from app.models import Permission


class PermissionSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    def run(self):
        print("[PermissionSeeder]")

        Permission(name="configuration_update").save()
        print(f" - Configuration Permission OK")

        Permission(name="user_index").save()
        Permission(name="user_create").save()
        Permission(name="user_update").save()
        Permission(name="user_delete").save()
        print(f" - User Permissions OK")
