"""Student class and helper functions for validation."""
import re
from datetime import datetime

ID_PATTERN = re.compile(r"^[A-Za-z]{2,4}/?\d{2,6}$")  # e.g. STU001, SRS/2026


def is_valid_id(student_id):
    """Return True if the ID looks like letters followed by digits."""
    return bool(ID_PATTERN.match(student_id))


def is_valid_dob(dob):
    """Return True if dob is a real date in YYYY-MM-DD format."""
    try:
        datetime.strptime(dob, "%Y-%m-%d")
        return True
    except ValueError:
        return False


class Student:
    """Represents one student and their subject scores."""

    def __init__(self, student_id, name, student_class, gender, dob,
                 scores=None, date_entered=None):
        self.student_id = student_id.upper()
        self.name = name
        self.student_class = student_class
        self.gender = gender
        self.dob = dob
        self.scores = scores if scores is not None else {}  # {subject: score}
        self.date_entered = date_entered  # when scores were last recorded

    def set_score(self, subject, score):
        """Store a score (0-100) and stamp the date it was entered."""
        score = float(score)
        if not 0 <= score <= 100:
            raise ValueError("Score must be between 0 and 100.")
        self.scores[subject.title()] = score
        self.date_entered = datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "student_class": self.student_class,
            "gender": self.gender,
            "dob": self.dob,
            "scores": self.scores,
            "date_entered": self.date_entered,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["student_id"], data["name"], data["student_class"],
            data["gender"], data["dob"],
            data.get("scores", {}), data.get("date_entered"),
        )

    def __str__(self):
        return (f"{self.student_id:<10} {self.name:<25} "
                f"{self.student_class:<8} {self.gender:<7} {self.dob}")
