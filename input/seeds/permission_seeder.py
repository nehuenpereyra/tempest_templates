
from flask_seeder import Seeder

from app.models import Permission


class PermissionSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    def run(self):
        Permission(name="setting_update").save()

        Permission(name="user_index").save()
        Permission(name="user_show").save()
        Permission(name="user_create").save()
        Permission(name="user_update").save()
        Permission(name="user_delete").save()

        Permission(name="role_index").save()
        Permission(name="role_show").save()
        Permission(name="role_create").save()
        Permission(name="role_update").save()
        Permission(name="role_delete").save()

        Permission(name="permission_index").save()
        Permission(name="permission_show").save()
        Permission(name="permission_create").save()
        Permission(name="permission_update").save()
        Permission(name="permission_delete").save()
