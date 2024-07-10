import json

def read_json(filename):
    try:
        with open(f"data/{filename}", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": [], "teams": [], "boards": [], "tasks": []}

def write_json(filename, data):
    with open(f"data/{filename}", "w") as file:
        json.dump(data, file, indent=4)
