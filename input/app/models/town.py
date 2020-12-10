
import requests

from flask import current_app

from app.models.town_phase import TownPhase


class Town():

    def __init__(self, id, name, phase):
        self.id = id
        self.name = name
        self.phase = phase

    def __repr__(self):
        return f"<{self.name}, {self.phase}>"

    @staticmethod
    def all():
        api_url = current_app.config["REFERENCES_API_URL"] + "/municipios"

        try:
            json_status = requests.get(api_url, params={"per_page": 0}).json()

            json_result = requests.get(
                api_url, params={"per_page": json_status["total"]}).json()

            phases = {value["id"]: TownPhase(value["id"], value["title"])
                      for value in json_result["data"]["Phase"].values()}

            return [Town(value["id"], value["name"], phases[value["phase"]])
                    for value in json_result["data"]["Town"].values()]
        except:
            return None

    @staticmethod
    def get(id):
        api_url = current_app.config["REFERENCES_API_URL"] + \
            "/municipios/" + str(id)

        try:
            json_result = requests.get(api_url).json()
            town_json = json_result["data"]["Town"][str(id)]
            phase_json = json_result["data"]["Phase"][str(town_json["phase"])]

            return Town(id=town_json["id"], name=town_json["name"],
                        phase=TownPhase(id=phase_json["id"], title=phase_json["title"]))
        except:
            return None

    @staticmethod
    def get_by_name(name):
        return Town.all().detect(lambda each: each.name == name)
