"""Score calculation and grading logic."""

MIN_SUBJECTS = 5


def total_score(student):
    return sum(student.scores.values())


def average_score(student):
    if not student.scores:
        return 0.0
    return total_score(student) / len(student.scores)


def get_grade(average):
    """Convert an average score to a letter grade."""
    if average >= 70:
        return "A"
    elif average >= 60:
        return "B"
    elif average >= 50:
        return "C"
    elif average >= 45:
        return "D"
    return "F"


def has_enough_subjects(student):
    return len(student.scores) >= MIN_SUBJECTS


def class_statistics(students):
    """Return highest/lowest student average and the class average."""
    graded = [s for s in students if s.scores]
    if not graded:
        return None
    averages = {s.name: average_score(s) for s in graded}
    best = max(averages, key=averages.get)
    worst = min(averages, key=averages.get)
    all_scores = [sc for s in graded for sc in s.scores.values()]
    return {
        "highest_name": best,
        "highest_avg": averages[best],
        "lowest_name": worst,
        "lowest_avg": averages[worst],
        "class_average": sum(averages.values()) / len(averages),
        "highest_single_score": max(all_scores),
        "lowest_single_score": min(all_scores),
    }


def sort_by_average(students):
    """Highest to lowest average."""
    return sorted(students, key=average_score, reverse=True)


def sort_by_name(students):
    return sorted(students, key=lambda s: s.name.lower())
