
from flask_seeder import Seeder

from app.models.user_permission import UserPermission


class PermissionSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    def run(self):
        print("[PermissionSeeder]")

        UserPermission(name="configuration_update").save()
        print(f" - Configuration Permission OK")

        UserPermission(name="user_index").save()
        UserPermission(name="user_create").save()
        UserPermission(name="user_update").save()
        UserPermission(name="user_delete").save()
        print(f" - User Permissions OK")

        UserPermission(name="help_center_index").save()
        UserPermission(name="help_center_show").save()
        UserPermission(name="help_center_create").save()
        UserPermission(name="help_center_update").save()
        UserPermission(name="help_center_delete").save()
        UserPermission(name="help_center_certify").save()
        print(f" - Help Center Permissions OK")

        UserPermission(name="turn_index").save()
        UserPermission(name="turn_create").save()
        UserPermission(name="turn_update").save()
        UserPermission(name="turn_delete").save()
        print(f" - Turn Permissions OK")
