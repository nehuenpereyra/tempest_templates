
from flask_seeder import Seeder

from app.models import Role, Permission


class RoleSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 2

    def run(self):
        print("[RoleSeeder]")
        permissions = {each.name: each for each in Permission.all()}

        cathedra_manager_permissions = [
            permissions["user_index"]
        ]

        admin_role = Role(name="Administrador", permissions=list(
            permissions.values()))
        admin_role.save()
        print(f" - {admin_role.name} Role OK")

        cathedra_manager_role = Role(
            name="Responsable de Catedra", permissions=cathedra_manager_permissions)
        cathedra_manager_role.save()
        print(f" - {cathedra_manager_role.name} Role OK")
