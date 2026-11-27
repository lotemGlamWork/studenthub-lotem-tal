# services.py


from strategies import IPricingStrategy


class CourseService:
    
    def __init__(self, db):
        """
        המחלקה מקבלת את הדאטהבייס שלה מבחוץ.
        היא לא יודעת או דואגת מאיפה הוא הגיע.
        """
        self.db = db

    def _get_course_details(self, course_id):
        """פונקציית עזר פנימית (private)"""
        for dept_courses in self.db.values():
            for course in dept_courses:
                if course["id"] == course_id:
                    return course["name"]
        return "Unknown Course"

    def get_course_by_id(self, course_id):
        """STU-203: מחזיר את הקורס (dict) לפי מזהה, או None אם לא קיים."""
        for dept_courses in self.db.values():
            for course in dept_courses:
                if course["id"] == course_id:
                    return course
        return None

    def find_courses_by_dept(self, dept):
        if dept not in self.db:
            return None 
        return self.db[dept]

    def get_formatted_prereqs(self, course):
        prereq_names = []
        if course["prereqs"]:
            for prereq_id in course["prereqs"]:
                prereq_name = self._get_course_details(prereq_id)
                prereq_names.append(f"{prereq_name} ({prereq_id})")
        return ", ".join(prereq_names) if prereq_names else "None"



    
    def calculate_price(self, strategy: IPricingStrategy, base_price):
        return strategy.calculate_price(base_price)

