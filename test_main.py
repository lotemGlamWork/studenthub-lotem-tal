# test_main.py - STU-201: בדיקת Smoke מקצה לקצה
#
# הרעיון: לפני שמתקנים באג, כותבים בדיקה ש*משחזרת* אותו (היא חייבת להיכשל!).
# רק אחרי שראינו אותה אדומה - מתקנים, ורואים אותה הופכת לירוקה.
# מעכשיו הבאג הזה לא יוכל לחזור בלי שנדע (Regression Test).
#
# איך בודקים תוכנית שקוראת ל-input()? מחליפים את input בפונקציה מזויפת
# שמחזירה תשובות מוכנות מראש - בעזרת ה-fixture המובנה של PyTest: monkeypatch.
import builtins

import main


def run_main_with_inputs(monkeypatch, capsys, answers):
    """מריץ את main() כאילו משתמש הקליד את answers, ומחזיר את כל מה שהודפס."""
    answers_iter = iter(answers)
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(answers_iter))
    main.main()
    return capsys.readouterr().out


def test_quit_immediately_does_not_crash(monkeypatch, capsys):
    # סטודנט 1, ומיד יציאה. זה בדיוק התרחיש שקרס ב-step-0
    out = run_main_with_inputs(monkeypatch, capsys, ["1", "q"])
    assert "Goodbye!" in out


def test_search_then_quit(monkeypatch, capsys):
    # סטודנט 1 (Dana, cs) -> מחלקה cs -> בלי ייצוא -> יציאה
    out = run_main_with_inputs(monkeypatch, capsys, ["1", "cs", "", "", "q"])
    assert "Intro to CS" in out
    assert "Goodbye!" in out


def test_unknown_department_shows_error(monkeypatch, capsys):
    out = run_main_with_inputs(monkeypatch, capsys, ["1", "physics", "q"])
    assert "Department 'physics' not found" in out


# --- STU-202: קריטריוני הקבלה (Acceptance Criteria) הפכו לבדיקות ---

def test_cs_student_sees_real_price_with_10_percent_discount(monkeypatch, capsys):
    # Given: Dana, סטודנטית רגילה למדמ"ח
    # When:  היא מחפשת קורסים ב-cs
    # Then:  Data Structures (150) מוצג במחיר 135.00
    out = run_main_with_inputs(monkeypatch, capsys, ["1", "cs", "", "", "q"])
    assert "Name: Data Structures, Prereqs: Intro to CS (101), Price: 135.00" in out


def test_math_student_sees_real_price_with_fixed_discount(monkeypatch, capsys):
    # Given: Yossi, סטודנט למתמטיקה
    # When:  הוא מחפש קורסים ב-math
    # Then:  Calculus 2 (180) מוצג במחיר 160.00
    out = run_main_with_inputs(monkeypatch, capsys, ["2", "math", "", "", "q"])
    assert "Name: Calculus 2" in out
    assert "Price: 160.00" in out


# --- STU-203: עגלת קניות ב-CLI ---

def test_add_course_to_cart_and_show_total(monkeypatch, capsys):
    # Dana (cs): 101 (100) + 202 (150) עם 10% הנחה -> 225
    out = run_main_with_inputs(
        monkeypatch, capsys,
        ["1", "cs", "101", "", "cs", "202", "", "cart", "q"],
    )
    assert "Course 101 added to cart." in out
    assert "Course 202 added to cart." in out
    assert "--- Your cart ---" in out
    assert "Total: 225.00" in out


def test_add_duplicate_course_to_cart(monkeypatch, capsys):
    out = run_main_with_inputs(
        monkeypatch, capsys,
        ["1", "cs", "101", "", "cs", "101", "", "q"],
    )
    assert "Course 101 is already in the cart." in out


def test_add_unknown_course_shows_error(monkeypatch, capsys):
    out = run_main_with_inputs(monkeypatch, capsys, ["1", "cs", "999", "", "cart", "q"])
    assert "Error: Course '999' not found" in out
    assert "Your cart is empty." in out


# --- STU-301: הסרה מהעגלה ב-CLI ---

def test_remove_command_removes_course_and_updates_total(monkeypatch, capsys):
    # Dana (cs), 10% הנחה: 101 + 202 = 225; אחרי הסרת 202 -> 90
    out = run_main_with_inputs(
        monkeypatch, capsys,
        ["1", "cs", "101", "", "cs", "202", "", "remove 202", "cart", "q"],
    )
    assert "Course 202 removed from cart." in out
    assert "Total: 90.00" in out


def test_remove_command_course_not_in_cart(monkeypatch, capsys):
    out = run_main_with_inputs(monkeypatch, capsys, ["1", "remove 101", "q"])
    assert "Course 101 is not in the cart." in out


def test_remove_command_without_id_asks_for_it(monkeypatch, capsys):
    out = run_main_with_inputs(
        monkeypatch, capsys,
        ["1", "cs", "101", "", "remove", "101", "cart", "q"],
    )
    assert "Course 101 removed from cart." in out
    assert "Your cart is empty." in out
