# StudentHub — Course Search CLI

נקודת ההתחלה של **תרגיל 4** (הנדסת פיתוח מערכות, אריאל תשפ"ז).
זה הקוד שבו סיימנו את המעבדה: STU-201 (תיקון הקריסה) ו-STU-202 (מחיר לכל קורס).

## הרצה
```bash
uv venv
.venv\Scripts\activate        # Windows  (Linux/Mac: source .venv/bin/activate)
uv pip install -r requirements.txt
python main.py
pytest -q                      # 32 passed
```

## מבנה
| קובץ | אחריות |
|---|---|
| `data.py` | הנתונים (קורסים, מחירים, דרישות קדם) |
| `services.py` | `CourseService`: קטלוג הקורסים |
| `strategies.py` | אסטרטגיות תמחור (Strategy Pattern) |
| `exporters.py` | ייצוא CSV/HTML (Template Method Pattern) |
| `student.py` | מחלקת `Student` |
| `main.py` | ממשק שורת פקודה |
| `test_*.py` | בדיקות PyTest |

## תהליך העבודה
- **ענפים ו-PR**: כל משימה מפותחת בענף נפרד (`feature/STU-XXX-...`) ומתמזגת ל-`main` דרך Pull Request.
- **תבנית PR**: כל PR נפתח לפי `.github/pull_request_template.md` — קישור לכרטיס ב-Jira, תיאור מה בוצע, תיעוד הפרומפט והשינויים בעקבות Review, וצ'קליסט של Definition of Done.
- **CI אוטומטי**: ב-GitHub Actions (`.github/workflows/ci.yml`) מורץ `pytest` בכל `push` ו-`pull_request` לענף `main`, עם Python 3.11 והתקנת `requirements.txt`. מיזוג מתבצע רק כש-ה-CI ירוק.
- **Definition of Done**: הקוד עבר Review של בן/בת הזוג, הפרומפט ותהליך העבודה מתועדים ב-PR, וכל קריטריון קבלה מכוסה בבדיקה כש-`pytest` ירוק.

## מה נשאר בספרינט
- **STU-203**: עגלת קניות (`ShoppingService`)

הפרטים בקובץ התרגיל.
