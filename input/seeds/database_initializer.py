
import os
import shutil

from flask import current_app
from flask_seeder import Seeder

from app.db import db
from app.models.help_center import HelpCenter


class DatabaseInitializer(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 0

    def run(self):
        print("[DatabaseInitializer]")

        shutil.rmtree(current_app.config["UPLOAD_FOLDER"])
        os.makedirs(current_app.config["UPLOAD_FOLDER"])
        print(f" - upload folder restarted")

        db.drop_all()
        print(f" - database dropped")

        db.create_all()
        print(f" - database created")
