"""Load and save student data using JSON."""
import json
import os

from student import Student

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "students.json")


def load_students(path=DATA_FILE):
    """Load students from disk. Returns [] if the file is missing or broken."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return [Student.from_dict(item) for item in raw]
    except FileNotFoundError:
        print("No data file found. Starting with an empty system.")
        return []
    except (json.JSONDecodeError, KeyError):
        print("Data file is corrupted. Starting with an empty system.")
        return []


def save_students(students, path=DATA_FILE):
    """Write all students to disk as JSON."""
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in students], f, indent=4)
        return True
    except OSError as err:
        print(f"Could not save data: {err}")
        return False
