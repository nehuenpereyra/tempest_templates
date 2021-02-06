
from flask_seeder import Seeder

from app.models import Setting


class SettingSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    def run(self):
        Setting(
            title="Sistema Base",
            description="Sistema generado de forma automatica con Tempest Templates.",
            contact_email="admin@example",
            items_per_page=20,
            enabled_site=True
        ).save()
