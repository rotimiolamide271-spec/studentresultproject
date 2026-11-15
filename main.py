"""Entry point: menu-driven Student Result Management System."""
from student import Student, is_valid_id, is_valid_dob
from results import (sort_by_average, sort_by_name, has_enough_subjects,
                     MIN_SUBJECTS)
from storage import load_students, save_students
import reports


def find_by_id(students, student_id):
    for s in students:
        if s.student_id == student_id.strip().upper():
            return s
    return None


def ask_student(students):
    """Prompt for an ID and return the matching student (or None)."""
    student = find_by_id(students, input("Student ID: "))
    if student is None:
        print("Student not found.")
    return student


# ---------- Student management ----------
def add_student(students):
    sid = input("Student ID (e.g. STU001): ").strip().upper()
    if not is_valid_id(sid):
        print("Invalid ID. Use letters followed by digits, e.g. STU001.")
        return
    if find_by_id(students, sid):
        print("A student with that ID already exists.")
        return
    name = input("Full name: ").strip()
    cls = input("Class/Form (e.g. SS2): ").strip()
    gender = input("Gender (M/F): ").strip().upper()
    dob = input("Date of birth (YYYY-MM-DD): ").strip()
    if not name or not cls or gender not in ("M", "F"):
        print("Name, class and gender (M/F) are required.")
        return
    if not is_valid_dob(dob):
        print("Invalid date. Use YYYY-MM-DD.")
        return
    students.append(Student(sid, name, cls, gender, dob))
    save_students(students)
    print("Student added.")


def view_students(students):
    if not students:
        print("No students registered yet.")
        return
    print(f"{'ID':<10} {'Name':<25} {'Class':<8} {'Gender':<7} DOB")
    for s in students:
        print(s)


def search_student(students):
    term = input("Enter ID or part of name: ").strip().lower()
    matches = [s for s in students
               if term == s.student_id.lower() or term in s.name.lower()]
    if matches:
        for s in matches:
            print(s)
    else:
        print("No match found.")


def update_student(students):
    s = ask_student(students)
    if not s:
        return
    print("Press Enter to keep the current value.")
    s.name = input(f"Name [{s.name}]: ").strip() or s.name
    s.student_class = input(f"Class [{s.student_class}]: ").strip() or s.student_class
    gender = input(f"Gender [{s.gender}]: ").strip().upper()
    if gender in ("M", "F"):
        s.gender = gender
    dob = input(f"DOB [{s.dob}]: ").strip()
    if dob:
        if is_valid_dob(dob):
            s.dob = dob
        else:
            print("Invalid date ignored.")
    save_students(students)
    print("Student updated.")


def delete_student(students):
    s = ask_student(students)
    if s and input(f"Delete {s.name}? (y/n): ").lower() == "y":
        students.remove(s)
        save_students(students)
        print("Student deleted.")


# ---------- Scores ----------
def record_scores(students):
    s = ask_student(students)
    if not s:
        return
    print(f"Enter at least {MIN_SUBJECTS} subjects. Type 'done' as subject to finish.")
    while True:
        subject = input("Subject: ").strip()
        if subject.lower() == "done":
            break
        if not subject:
            continue
        try:
            s.set_score(subject, input(f"Score for {subject} (0-100): "))
        except ValueError as err:
            print(f"Invalid score: {err}")
        else:
            print("Score saved.")
    if not has_enough_subjects(s):
        print(f"Warning: only {len(s.scores)} subject(s) recorded; {MIN_SUBJECTS} required.")
    save_students(students)


def update_score(students):
    s = ask_student(students)
    if not s:
        return
    if not s.scores:
        print("No scores recorded for this student.")
        return
    subject = input(f"Subject to update {list(s.scores)}: ").strip().title()
    if subject not in s.scores:
        print("Subject not found.")
        return
    try:
        s.set_score(subject, input("New score (0-100): "))
    except ValueError as err:
        print(f"Invalid score: {err}")
    else:
        save_students(students)
        print("Score updated.")


def show_report_card(students):
    s = ask_student(students)
    if s:
        if not s.scores:
            print("No scores recorded for this student.")
        else:
            print(reports.report_card(s))


# ---------- Reporting ----------
def list_results(students):
    scored = [s for s in students if s.scores]
    if not scored:
        print("No results to show.")
        return
    choice = input("Sort by (1) average or (2) name: ").strip()
    ordered = sort_by_name(scored) if choice == "2" else sort_by_average(scored)
    print(reports.results_table(ordered))


def show_statistics(students):
    print(reports.statistics_text(students))


def export_report(students):
    if not any(s.scores for s in students):
        print("Nothing to export yet.")
        return
    try:
        path = reports.save_report([s for s in students if s.scores])
    except OSError as err:
        print(f"Could not save report: {err}")
    else:
        print(f"Report saved to {path}")


MENU = """
===== STUDENT RESULT MANAGEMENT SYSTEM =====
 1. Add student              7. Show report card
 2. View all students        8. List results (sorted)
 3. Search student           9. Class statistics
 4. Update student          10. Export text report
 5. Delete student           0. Exit
 6. Record scores           11. Update a score
"""

ACTIONS = {
    "1": add_student, "2": view_students, "3": search_student,
    "4": update_student, "5": delete_student, "6": record_scores,
    "7": show_report_card, "8": list_results, "9": show_statistics,
    "10": export_report, "11": update_score,
}


def main():
    students = load_students()
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            save_students(students)
            print("Data saved. Goodbye!")
            break
        action = ACTIONS.get(choice)
        if action:
            action(students)
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
