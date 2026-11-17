# exporters.py
from abc import ABC, abstractmethod

class BaseReportExporter(ABC):

    # 1. זהו ה-Template Method!
    def export(self, courses):
        report = ""
        # שלב 1: מוגדר כאן
        report += self._generate_header()

        # שלב 2: מוגדר כאן, עם קריאה לשלב אבסטרקטי
        for course in courses:
            report += self._format_course_line(course)

        # שלב 3: מוגדר כאן
        report += self._generate_footer()
        return report

    # 2. אלו הצעדים ה"חופשיים" שמשתנים
    @abstractmethod
    def _generate_header(self):
        pass

    @abstractmethod
    def _format_course_line(self, course):
        pass

    @abstractmethod
    def _generate_footer(self):
        pass

# 3. מימוש המחלקות שיודעות "לצבוע" את השלד
class HtmlExporter(BaseReportExporter):
    def _generate_header(self):
        return "<html><body><table>\n"

    def _format_course_line(self, course):
        return f"  <tr><td>{course['id']}</td><td>{course['name']}</td></tr>\n"

    def _generate_footer(self):
        return "</table></body></html>\n"

class CsvExporter(BaseReportExporter):
    def _generate_header(self):
        return "ID,Name\n"

    def _format_course_line(self, course):
        return f"{course['id']},{course['name']}\n"

    def _generate_footer(self):
        return "\n--- End of Report ---"