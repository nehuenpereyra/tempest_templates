from app.models.help_center import HelpCenter


def is_in_accepted_state(id):
    return HelpCenter.query.get(id).is_in_accepted_state()
