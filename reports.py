"""Report generation functions."""
import os
from datetime import datetime

from results import (total_score, average_score, get_grade,
                     class_statistics, sort_by_average)


def report_card(student):
    """Return a formatted report card string for one student."""
    lines = [
        "=" * 50,
        "STUDENT REPORT CARD".center(50),
        "=" * 50,
        f"Name  : {student.name}",
        f"ID    : {student.student_id}",
        f"Class : {student.student_class}",
        f"Gender: {student.gender}    DOB: {student.dob}",
        "-" * 50,
    ]
    for subject, score in student.scores.items():
        lines.append(f"{subject:<30}{score:>6.1f}")
    avg = average_score(student)
    lines += [
        "-" * 50,
        f"Total   : {total_score(student):.1f}",
        f"Average : {avg:.2f}",
        f"Grade   : {get_grade(avg)}",
        f"Result entered: {student.date_entered or 'N/A'}",
        "=" * 50,
    ]
    return "\n".join(lines)


def results_table(students):
    """Return a table of every student with total, average and grade."""
    header = f"{'ID':<10}{'Name':<25}{'Total':>8}{'Average':>9}{'Grade':>7}"
    lines = [header, "-" * len(header)]
    for s in students:
        avg = average_score(s)
        lines.append(f"{s.student_id:<10}{s.name:<25}"
                     f"{total_score(s):>8.1f}{avg:>9.2f}{get_grade(avg):>7}")
    return "\n".join(lines)


def statistics_text(students):
    stats = class_statistics(students)
    if stats is None:
        return "No scores recorded yet."
    return "\n".join([
        f"Top student      : {stats['highest_name']} ({stats['highest_avg']:.2f})",
        f"Lowest student   : {stats['lowest_name']} ({stats['lowest_avg']:.2f})",
        f"Class average    : {stats['class_average']:.2f}",
        f"Highest score    : {stats['highest_single_score']:.1f}",
        f"Lowest score     : {stats['lowest_single_score']:.1f}",
    ])


def save_report(students, folder="data"):
    """Write a full class report to a timestamped text file."""
    os.makedirs(folder, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(folder, f"class_report_{stamp}.txt")
    ranked = sort_by_average(students)
    with open(path, "w", encoding="utf-8") as f:
        f.write("CLASS RESULT REPORT\n")
        f.write(f"Generated: {datetime.now():%Y-%m-%d %H:%M}\n\n")
        f.write(results_table(ranked) + "\n\n")
        f.write("CLASS STATISTICS\n")
        f.write(statistics_text(students) + "\n")
    return path
