
from flask_seeder import Seeder

from app.models.user_role import UserRole
from app.models.user_permission import UserPermission


class UserRoleSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 2

    def run(self):
        print("[UserRoleSeeder]")
        permissions = {each.name: each for each in UserPermission.query.all()}

        operator_permissions = [
            permissions["help_center_index"],
            permissions["help_center_show"],
            permissions["help_center_create"],
            permissions["help_center_update"],
            permissions["help_center_certify"],
            permissions["turn_index"],
            permissions["turn_create"],
            permissions["turn_update"],
        ]

        admin_role = UserRole(name="Administrador", permissions=list(
            permissions.values()))
        admin_role.save()
        print(f" - {admin_role.name} Role OK")

        operator_role = UserRole(
            name="Operador", permissions=operator_permissions)
        operator_role.save()
        print(f" - {operator_role.name} Role OK")
