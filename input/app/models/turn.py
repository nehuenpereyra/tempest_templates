import json
import phonenumbers
from datetime import datetime, date, time, timedelta
from sqlalchemy import Date, DateTime, Time, cast, and_

from app.db import db
from app.models.help_center import HelpCenter


class Turn(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), nullable=False)
    day_hour = db.Column(db.DateTime, nullable=False, unique=False)
    _donor_phone_number = db.Column(
        "donor_phone_number", db.String(16), nullable=True)
    help_center = db.relationship(
        "HelpCenter", back_populates="turns")
    help_center_id = db.Column(
        db.Integer, db.ForeignKey('help_center.id'), nullable=False)

    @property
    def donor_phone_number(self):
        return self._donor_phone_number

    @donor_phone_number.setter
    def donor_phone_number(self, phone):
        if phone:
            self._donor_phone_number = phonenumbers.format_number(
                phonenumbers.parse(phone, "AR"), phonenumbers.PhoneNumberFormat.INTERNATIONAL)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def remove(self):
        if self.id:
            db.session.delete(self)
            db.session.commit()

    @staticmethod
    def all_reserved(center_id):
        return Turn.query.filter(Turn.help_center_id == center_id).all()

    @staticmethod
    def all_reserved_date(center_id, in_date):
        return Turn.query.filter(and_(cast(Turn.day_hour, Date) == in_date), (Turn.help_center_id == center_id)).all()

    @staticmethod
    def all_free_time(center_id, in_date):

        turns = []
        turn_date = datetime(in_date.year, in_date.month,
                             in_date.day, 9, 0, 0, 0)
        for x in range(14):
            if turn_date > datetime.today():
                turns.append(turn_date)
            turn_date = turn_date + timedelta(minutes=30)

        return turns.match_all(Turn.all_reserved_date(center_id, in_date), lambda each1,
                               each2: each1 != each2.day_hour)

    @staticmethod
    def update(id, id_center, email, donor_phone_number, day_hour):
        turn = Turn.query.get(id)
        if turn:
            turn.id_center = id_center
            turn.email = email
            turn.donor_phone_number = donor_phone_number
            turn.day_hour = day_hour
            turn.save()
            return turn
        return None

    @staticmethod
    def delete(id):
        turn = Turn.query.get(id)
        if turn:
            turn.remove()
            return turn
        return None

    @staticmethod
    def search(id_center, email, page, per_page):
        query = Turn.query
        query = query.filter(Turn.help_center_id == id_center)
        if (email and email != "Elija alguno de los siguientes emails"):
            query = query.filter_by(email=email)
        query = query.order_by(
            cast(Turn.day_hour, Date).desc(), cast(Turn.day_hour, Time).asc())
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def all_free_time_json(id_center, search_date):
        array_json = []
        turns = Turn.all_free_time(id_center, search_date)
        for turn in turns:
            array_json.append({
                'centro_id': str(id_center),
                'horario_inicio': turn.strftime('%H:%M'),
                'horario_fin': (turn + timedelta(minutes=30)).strftime('%H:%M'),
                'fecha': turn.strftime('%Y/%m/%d')
            })
        return json.dumps({'turnos': array_json})

    @staticmethod
    def get_next_tuns(search_query, email, page, per_page):
        query = Turn.query
        today = datetime.today()

        if (search_query):
            query = query.join(HelpCenter.turns).filter(
                HelpCenter.name.like(f"%{search_query}%"))

        if (email and email != "Elija alguno de los siguientes emails"):
            query = query.filter_by(email=email)

        query = query.filter(cast(Turn.day_hour, DateTime).between(
            today, today + timedelta(hours=48)))

        query = query.order_by(
            cast(Turn.day_hour, Date).asc(), cast(Turn.day_hour, Time).asc())

        return query.paginate(page=page, per_page=per_page, error_out=False)

    @ staticmethod
    def get_all_emails():
        return Turn.query.with_entities(Turn.email).distinct().all().collect(
            lambda each: each[0])

    @staticmethod
    def get_quantity_turns_last(total_days=7):
        array_json = []
        query = Turn.query
        today = datetime.today() - timedelta(total_days)

        for x in range(total_days):
            today = today + timedelta(days=1)
            array_json.append({
                'fecha': today.strftime("%d/%m/%Y"),
                'cantidad': query.filter((cast(Turn.day_hour, Date) == today.date())).all().size(),
            })

        return array_json