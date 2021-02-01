
from sqlalchemy import event

from app.db import db


class Setting(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), nullable=False)
    description = db.Column(db.Text, nullable=False)
    contact_email = db.Column(db.String(32), unique=True, nullable=False)
    items_per_page = db.Column(db.Integer, nullable=False)
    enabled_site = db.Column(db.Boolean, nullable=False)


    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get():
        return Setting.query.first()

    @staticmethod
    def update(title, description, contact_email, items_per_page, enabled_site):
        settings = Setting.get()
        settings.title = title
        settings.description = description
        settings.contact_email = contact_email
        settings.items_per_page = items_per_page
        settings.enabled_site = enabled_site
        settings.save()
