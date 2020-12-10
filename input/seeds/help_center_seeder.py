
from datetime import time

from flask_seeder import Seeder

from app.models.help_center import HelpCenter, HelpCenterType
from app.models.town import Town
from app.models.turn import Turn
from datetime import datetime


class HelpCenterSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    def run(self):

        print("[HelpCenterSeeder]")

        food_center_type = HelpCenterType(name="Centro de Alimentos")
        food_center_type.save()
        print(f" - {food_center_type.name} OK")

        clothing_center_type = HelpCenterType(name="Centro de Ropa")
        clothing_center_type.save()
        print(f" - {clothing_center_type.name} OK")

        blood_center_type = HelpCenterType(name="Centro de Sangre")
        blood_center_type.save()
        print(f" - {blood_center_type.name} OK")

        food_center_1 = HelpCenter(
            name="Centro el Arroz",
            address="Av 64 e40 y 41 nro 30",
            phone_number="+54 294 412-3456",
            opening_time=time(9),
            closing_time=time(16),
            center_type=food_center_type,
            town=Town.get(25),
            web_url="https://arroz.centro.org",
            email="arroz@centro.org"
        )
        food_center_1.save()
        print(f" - {food_center_1.name} OK")

        food_center_2 = HelpCenter(
            name="Centro la Papa",
            address="Av 80 e20 y 21 nro 90",
            phone_number="+54 294 410-2030",
            opening_time=time(9),
            closing_time=time(16),
            center_type=food_center_type,
            town=Town.get(1),
            web_url="https://papa.centro.org",
            email="papa@centro.org",
            request_status=True
        )
        food_center_2.save()
        print(f" - {food_center_2.name} OK")

        clothing_center = HelpCenter(
            name="Centro la Camisa",
            address="Av 20 e42 y 43 nro 64",
            phone_number="+54 294 420-2040",
            opening_time=time(9),
            closing_time=time(16),
            center_type=clothing_center_type,
            town=Town.get(25),
            web_url="https://camisa.centro.org",
            email="camisa@centro.org",
            request_status=False)
        clothing_center.save()
        print(f" - {clothing_center.name} OK")

        blood_center = HelpCenter(
            name="Centro la Gota",
            address="Av 46 e80 y 81 nro 70",
            phone_number="+54 294 440-2010",
            opening_time=time(9),
            closing_time=time(16),
            center_type=blood_center_type,
            town=Town.get(20),
            web_url="https://gota.centro.org",
            published=False,
            request_status=True)
        blood_center.save()
        print(f" - {blood_center.name} OK")

        print("[TurnSeeder]")

        turn_one = Turn(email="juan@gmail.com",
                        day_hour=datetime(2020, 11, 13, 12, 30, 00), donor_phone_number="2214053283", help_center=food_center_2)
        turn_one.save()
        print(f" - {turn_one.id} OK")

        turn_two = Turn(email="ramiro@gmail.com",
                        day_hour=datetime(2020, 11, 14, 9, 00, 00), donor_phone_number="2214053283", help_center=food_center_2)
        turn_two.save()
        print(f" - {turn_two.id} OK")

        turn_three = Turn(email="julieta@gmail.com",
                          day_hour=datetime(2020, 11, 13, 15, 30, 00), donor_phone_number="2214053283", help_center=food_center_2)
        turn_three.save()
        print(f" - {turn_three.id} OK")

        turn_four = Turn(email="marcela@gmail.com",
                         day_hour=datetime(2020, 11, 13, 10, 30, 00), donor_phone_number="2214053283", help_center=blood_center)
        turn_four.save()
        print(f" - {turn_four.id} OK")
