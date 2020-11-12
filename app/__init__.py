
from app.helpers import load_json
from app.models import EntityBuilder


def run():

    main_json = load_json("own/main.json")
    builder = EntityBuilder()

    for entity_route in main_json["entities"]:
        builder.add_entity(load_json("own/" + entity_route))

    print("\n\n".join(builder.build().collect(lambda each: str(each))))
