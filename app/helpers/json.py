
import json

def load_json(filename):
    with open(filename, "r") as file:
        result = json.load(file)
    return result