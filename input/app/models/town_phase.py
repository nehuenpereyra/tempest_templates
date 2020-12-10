
import requests
from flask import current_app


class TownPhase:

    def __init__(self, id, title):
        self.id = id
        self.title = title

    def __repr__(self):
        return f"<{self.title}>"

    @staticmethod
    def all():
        api_url = current_app.config["REFERENCES_API_URL"] + "/fases"
        try:
            json_status = requests.get(api_url, params={"per_page": 0}).json()
            json_result = requests.get(
                api_url, params={"per_page": json_status["total"]}).json()
            return json_result["data"].collect(lambda each: TownPhase(each["id"], each["title"]))
        except:
            return None
