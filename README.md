# Student Result Management System

A menu-driven Python application for managing student records, scores,
grades and reports. Built for the New Horizon *Introduction to Python* project.

## Features
- Add, view, search, update and delete students
- Record at least five subject scores per student (with the date entered)
- Automatic total, average and grade (A–F)
- Report cards, sorted result lists (by average or name), class statistics
- Export a text report to `data/`
- Data saved to `data/students.json` and loaded on startup

## How to run
Requires Python 3.8+ (no external libraries).

```bash
python main.py
```

## Project structure
```
student_result_system/
├── main.py        # Menu and program flow
├── student.py     # Student class + ID/date validation (regex, datetime)
├── results.py     # Totals, averages, grading, sorting, statistics
├── storage.py     # JSON load/save with error handling
├── reports.py     # Report card, table and text-file report
├── data/          # students.json and exported reports
└── README.md
```

## Grading scale
| Average | Grade |
|---------|-------|
| 70+     | A |
| 60–69   | B |
| 50–59   | C |
| 45–49   | D |
| below 45| F |

## Python concepts used
Variables and type conversion, if/elif/else, for/while loops, lists, tuples,
dictionaries, functions, sorting (`sorted` with `key`), exception handling
(`try/except/else`), JSON file handling, modules, OOP (`Student` class),
`datetime`, regular expressions, and the standard library (`os`, `json`, `re`).
