from typing import List, Optional

class Student:
    """
    מחלקה המייצגת סטודנט במערכת
    
    Attributes:
        id: מזהה ייחודי של הסטודנט
        name: שם הסטודנט
        department: המחלקה שאליה שייך הסטודנט (cs/math)
        courses: רשימת קורסים שהסטודנט רשום להם
        is_excellent: האם הסטודנט מצטיין
    """
    
    def __init__(self, 
                 id: str, 
                 name: str, 
                 department: str, 
                 courses: Optional[List[str]] = None, 
                 is_excellent: bool = False):
        """
        יצירת אובייקט סטודנט חדש
        
        Args:
            id: מזהה ייחודי של הסטודנט
            name: שם הסטודנט
            department: המחלקה (cs/math)
            courses: רשימת קודי קורסים שהסטודנט רשום להם (אופציונלי)
            is_excellent: האם הסטודנט מצטיין (ברירת מחדל: False)
        """
        self.id = id
        self.name = name
        self.department = department
        self.courses = courses if courses is not None else []
        self.is_excellent = is_excellent
    
    def add_course(self, course_id: str) -> bool:
        """
        הוסף קורס לרשימת הקורסים של הסטודנט
        
        Args:
            course_id: קוד הקורס להוספה
            
        Returns:
            True אם הקורס נוסף בהצלחה, False אם הקורס כבר קיים ברשימה
        """
        if course_id not in self.courses:
            self.courses.append(course_id)
            return True
        return False
    
    def remove_course(self, course_id: str) -> bool:
        """
        הסר קורס מרשימת הקורסים של הסטודנט
        
        Args:
            course_id: קוד הקורס להסרה
            
        Returns:
            True אם הקורס הוסר בהצלחה, False אם הקורס לא קיים ברשימה
        """
        if course_id in self.courses:
            self.courses.remove(course_id)
            return True
        return False
    
    def has_course(self, course_id: str) -> bool:
        """
        בדוק האם הסטודנט רשום לקורס מסוים
        
        Args:
            course_id: קוד הקורס לבדיקה
            
        Returns:
            True אם הסטודנט רשום לקורס, False אחרת
        """
        return course_id in self.courses
    
    def get_courses_count(self) -> int:
        """
        קבל את מספר הקורסים שהסטודנט רשום להם
        
        Returns:
            מספר קורסים
        """
        return len(self.courses)
    
    def set_excellence(self, is_excellent: bool) -> None:
        """
        עדכן את סטטוס ההצטיינות של הסטודנט
        
        Args:
            is_excellent: True אם הסטודנט מצטיין, False אחרת
        """
        self.is_excellent = is_excellent
    
    def to_dict(self) -> dict:
        """
        המרת אובייקט הסטודנט למילון
        
        Returns:
            מילון המייצג את הסטודנט
        """
        return {
            'id': self.id,
            'name': self.name,
            'department': self.department,
            'courses': self.courses,
            'is_excellent': self.is_excellent,
            'courses_count': self.get_courses_count()
        }
    
    def __str__(self) -> str:
        """
        ייצוג טקסטי של הסטודנט
        
        Returns:
            תיאור טקסטי של הסטודנט
        """
        excellence = "Excellent" if self.is_excellent else "Regular"
        return (f"Student: {self.name} (ID: {self.id}) | Dept: {self.department} | "
                f"Status: {excellence} | Courses: {self.get_courses_count()}")
    
    def __repr__(self) -> str:
        """
        ייצוג חוקי של הסטודנט
        
        Returns:
            ייצוג חוקי של הסטודנט
        """
        return f"Student(id='{self.id}', name='{self.name}', department='{self.department}', courses={self.courses}, is_excellent={self.is_excellent})"
