
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(loader=FileSystemLoader(searchpath="templates"),
                  trim_blocks=True, block_start_string='[%', block_end_string='%]', variable_start_string='[[', variable_end_string=']]')


def render_template(template, **kwargs):
    return env.get_template(template).render(**kwargs)
