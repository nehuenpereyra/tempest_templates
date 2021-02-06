
import os
import shutil

from app.helpers import load_json, render_template, write_file
from app.models import EntityBuilder


def run():

    main_json_path = os.environ.get("CONFIG_FILE")

    if not main_json_path:
        print("error: config file is not setted")
        return False

    main_json = load_json(main_json_path)
    builder = EntityBuilder()

    for entity_route in main_json["entities"]:
        builder.add_entity(load_json(os.path.join(os.path.dirname(main_json_path), entity_route)))

    entities = builder.build()

    generate_structure(main_json)
    generate_model(main_json, entities)
    generate_form(main_json, entities)
    generate_routes(main_json, entities)
    generate_views(main_json, entities)
    generate_resourse(main_json, entities)
    generate_seeds(main_json, entities)

    return True


def generate_structure(main_json):

    input_folder = main_json.get("input", None)
    output_folder = main_json["output"]["root"]

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    if input_folder:
        shutil.copytree(input_folder, output_folder)
    else:
        os.makedirs(output_folder, exist_ok=True)


def generate_model(main_json, entities):

    model_path = os.path.join(main_json["output"]["root"],
                              main_json["output"]["models"])

    os.makedirs(model_path, exist_ok=True)

    write_file(
        os.path.join(model_path, "__init__.py"),
        render_template("model_init", entities=entities)
    )

    entities.do(lambda each: write_file(
        os.path.join(model_path, each.get_name_delimited() + ".py"),
        render_template("model", entity=each)
    ))

    if entities.any_satisfy(lambda each: each.has_relationship_of_many_to_many()):
        database_links_path = os.path.join(model_path, "database_links")

        os.makedirs(database_links_path, exist_ok=True)

        relationship_attributes = []
        all_relationship_attributes = entities.flat_collect(
            lambda each: each.get_many_to_many_relationship_attributes()
        )

        for attribute in all_relationship_attributes:
            if not relationship_attributes.includes(attribute) and \
                    not relationship_attributes.includes(attribute.type.linked_attribute):
                relationship_attributes.add(attribute)

        write_file(
            os.path.join(database_links_path, "__init__.py"),
            render_template("link_table_init", link_names=relationship_attributes.collect(
                lambda each: each.type.get_import_link()
            ))
        )

        relationship_attributes.do(lambda each: write_file(
            os.path.join(
                database_links_path,
                each.type.get_import_link() + ".py"
            ),
            render_template(
                "link_table",
                table_name=each.type.get_import_link(),
                primary_entity_name=each.entity.get_name_delimited(),
                secondary_entity_name=each.type.linked_attribute.entity.get_name_delimited()
            )
        ))


def generate_form(main_json, entities):

    form_path = os.path.join(main_json["output"]["root"],
                             main_json["output"]["forms"])

    os.makedirs(form_path, exist_ok=True)

    write_file(
        os.path.join(form_path, "__init__.py"),
        render_template("form_init", entities=entities)
    )

    entities.do(lambda each: write_file(
        os.path.join(form_path, each.get_name_delimited() + ".py"),
        render_template("form", entity=each)
    ))


def generate_routes(main_json, entities):

    routes_path = os.path.join(main_json["output"]["root"],
                               main_json["output"]["routes"])

    os.makedirs(routes_path, exist_ok=True)

    write_file(
        os.path.join(routes_path, "__init__.py"),
        render_template("routes_init", modules=entities.collect(
            lambda each: each.get_name_delimited()
        ))
    )

    entities.do(lambda each: write_file(
        os.path.join(routes_path, each.get_name_delimited() + ".py"),
        render_template("routes", entity=each)
    ))


def generate_view_for(main_json, entity, path):

    entity_path = os.path.join(path, entity.get_name_delimited())

    os.makedirs(entity_path, exist_ok=True)

    ["show", "index", "new", "edit"].do(lambda each: write_file(
        os.path.join(entity_path, f"{each}.html"),
        render_template(
            f"view/{each}",
            entity=entity,
            extends=main_json["view"]["extends"],
            main_block=main_json["view"]["main_block"],
            messages=main_json["message"],
        )
    ))


def generate_views(main_json, entities):

    views_path = os.path.join(main_json["output"]["root"],
                              main_json["output"]["templates"])

    os.makedirs(views_path, exist_ok=True)

    entities.do(lambda each: generate_view_for(main_json, each, views_path))


def generate_resourse(main_json, entities):

    resource_path = os.path.join(main_json["output"]["root"],
                                 main_json["output"]["resources"])

    os.makedirs(resource_path, exist_ok=True)

    entities.do(lambda each: write_file(
        os.path.join(resource_path, each.get_name_delimited() + ".py"),
        render_template("resource", entity=each, main_json=main_json)
    ))


def generate_seeds(main_json, entities):

    seeds_path = os.path.join(main_json["output"]["root"],
                                 main_json["output"]["seeds"])

    os.makedirs(seeds_path, exist_ok=True)

    write_file(
        os.path.join(seeds_path, "permission.py"),
        render_template("seeds/permission", entities=entities)
    )
