
from datetime import datetime, date
import calendar

from flask import url_for, escape

from app.helpers.permission import verify_permission


def show_field(field, attribute=None, link=None):
    if field is not None:
        return __show_field_not_none(field, attribute, link)
    else:
        return '<small class="ml-2">No tiene</small>'

def __show_field_not_none(field, attribute, link):

    if not isinstance(field, list):
        content = '<small class="ml-2">{}</small>'.format(
            escape(__get_string_field(field if attribute is None else getattr(field, attribute)))
        )

        if link and verify_permission(link):
            content = '<a href="{}" style="text-decoration: none">{}</a>'.format(
                url_for(link, id=field.id),
                content
            )

        return content
    else:
        return __show_list_field(field, attribute, link)

def __get_string_field(field):
    if type(field) is bool:
        return "Si" if field else "No"
    elif type(field) is datetime or type(field) is date:
        return "{} de {} del {}".format(
            field.day,
            calendar.month_name[field.month].capitalize(),
            field.year
        )
    return field

def __show_list_field(field, attribute, link):
    if field:
        if link and verify_permission(link):
            return __show_list_field_with_links(field, attribute, link)
        else:
            return __show_list_field_without_links(field, attribute)
    else:
        return '<small class="ml-2">Sin elementos</small>'

def __show_list_field_with_links(field, attribute, link):
    return '<div class="list-group">{}</div>'.format(
        field.inject(lambda each, result: '{}<a class="list-group-item list-group-item-action" href="{}">{}</a>'.format(
            result,
            url_for(link, id=each.id),
            escape(__get_string_field(getattr(each, attribute)))
        ), "")
    )

def __show_list_field_without_links(field, attribute):
    return '<ul class="list-group">{}</ul>'.format(
        field.inject(lambda each, result: '{}<li class="list-group-item">{}</li>'.format(
            result,
            escape(__get_string_field(getattr(each, attribute)))
        ), "")
    )
