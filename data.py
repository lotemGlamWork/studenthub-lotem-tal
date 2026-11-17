# data.py - STU-202: לכל קורס יש מחיר משלו (בש"ח)
COURSES_DB = {
    "cs": [
        {"id": "101", "name": "Intro to CS", "prereqs": [], "price": 100},
        {"id": "202", "name": "Data Structures", "prereqs": ["101"], "price": 150},
        {"id": "303", "name": "Algorithms", "prereqs": ["202", "101"], "price": 200},
    ],
    "math": [
        {"id": "901", "name": "Calculus 1", "prereqs": [], "price": 120},
        {"id": "902", "name": "Calculus 2", "prereqs": ["901"], "price": 180},
    ]
}
