
from app.db import db


class HelpCenterType(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    help_centers = db.relationship("HelpCenter", back_populates="center_type")

    def public_dict(self):
        return {
            "id": self.id,
            "nombre": self.name,
            "cantidad_centros": self.help_centers.size()
        }

    @staticmethod
    def all():
        return HelpCenterType.query.all()

    @staticmethod
    def all_paginated(page=1, per_page=None):
        return HelpCenterType.query.paginate(page=page, per_page=per_page, error_out=False).items, \
            HelpCenterType.query.count()

    @staticmethod
    def get(id):
        return HelpCenterType.query.get(id)

    @staticmethod
    def get_by_name(name):
        return HelpCenterType.query.filter_by(name=name).first()

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
