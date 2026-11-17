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

## מה נשאר בספרינט
- **STU-203**: עגלת קניות (`ShoppingService`)
- **STU-204**: CI ב-GitHub Actions, תבנית PR ו-Definition of Done

הפרטים בקובץ התרגיל.
