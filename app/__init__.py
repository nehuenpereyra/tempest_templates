
import os
import shutil

from app.helpers import load_json, render_template, write_file
from app.models import EntityBuilder


def run():

    main_json = load_json("own/main.json")
    builder = EntityBuilder()

    for entity_route in main_json["entities"]:
        builder.add_entity(load_json("own/" + entity_route))

    entities = builder.build()

    if os.path.exists(main_json["output"]["root"]):
        shutil.rmtree(main_json["output"]["root"])

    os.mkdir(main_json["output"]["root"])

    generate_model(main_json, entities)

    # print("\n\n".join(builder.build().collect(lambda each: str(each))))


def generate_model(main_json, entities):

    model_path = os.path.join(main_json["output"]["root"],
                              main_json["output"]["models"])

    os.mkdir(model_path)

    entities.do(lambda each: write_file(
        os.path.join(model_path, each.get_name_delimited() + ".py"),
        render_template("model", entity=each)
    ))

    # print(render_template("example", value="user.name"))
