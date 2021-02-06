
from flask_seeder import Seeder
from werkzeug.security import generate_password_hash

from app.models import User, Role


class UserSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 3

    def run(self):
        roles = {each.name: each for each in Role.query.all()}

        User(
            name="Juan",
            surname="Lopez",
            username="admin",
            password=generate_password_hash("password"),
            roles=[roles["Administrador"]]
        ).save()
