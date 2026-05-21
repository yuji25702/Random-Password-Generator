import json
import os

FILE_NAME = "passwords.json"


def load_history():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError:
        return []


def save_history(history):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)