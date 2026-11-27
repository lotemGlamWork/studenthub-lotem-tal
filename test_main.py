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


# --- STU-302: סיכום העגלה ב-CLI ---

def test_cart_summary_empty_cart(monkeypatch, capsys):
    out = run_main_with_inputs(monkeypatch, capsys, ["1", "cart", "q"])
    assert "Your cart is empty." in out
    assert "Items in cart: 0" in out


def test_cart_summary_with_discount(monkeypatch, capsys):
    # Dana (cs), 10% הנחה: 101 (100) + 202 (150)
    out = run_main_with_inputs(
        monkeypatch, capsys,
        ["1", "cs", "101", "", "cs", "202", "", "cart", "q"],
    )
    assert "Items in cart: 2" in out
    assert "Subtotal: 250.00" in out
    assert "Savings: 25.00" in out
    assert "Total: 225.00" in out


def test_cart_summary_without_discount(monkeypatch, capsys):
    # לכל הסטודנטים המובנים יש הנחה, אז מחליפים את בחירת האסטרטגיה ב-DefaultStrategy
    from strategies import DefaultStrategy
    monkeypatch.setattr(main, "choose_pricing_strategy", lambda student, dept: DefaultStrategy())
    out = run_main_with_inputs(
        monkeypatch, capsys,
        ["1", "cs", "101", "", "math", "901", "", "cart", "q"],
    )
    assert "Items in cart: 2" in out
    assert "Subtotal: 220.00" in out
    assert "Savings: 0.00" in out
    assert "Total: 220.00" in out


# --- STU-303: ייצוא העגלה ב-CLI ---
from exporters import CsvExporter


def test_export_cart_to_csv_command(monkeypatch, capsys, tmp_path):
    monkeypatch.chdir(tmp_path)  # cart.csv נכתב לתיקייה זמנית
    out = run_main_with_inputs(
        monkeypatch, capsys,
        ["1", "cs", "101", "", "math", "901", "", "export csv", "q"],
    )
    assert "Cart exported to cart.csv (2 items)." in out
    content = (tmp_path / "cart.csv").read_text(encoding="utf-8")
    assert "101,Intro to CS\n" in content
    assert "901,Calculus 1\n" in content


def test_export_cart_to_html_command(monkeypatch, capsys, tmp_path):
    monkeypatch.chdir(tmp_path)
    out = run_main_with_inputs(
        monkeypatch, capsys, ["1", "cs", "202", "", "EXPORT HTML", "q"],
    )
    assert "Cart exported to cart.html (1 item)." in out
    content = (tmp_path / "cart.html").read_text(encoding="utf-8")
    assert "<tr><td>202</td><td>Data Structures</td></tr>" in content


def test_export_empty_cart_command(monkeypatch, capsys, tmp_path):
    monkeypatch.chdir(tmp_path)
    out = run_main_with_inputs(monkeypatch, capsys, ["1", "export csv", "q"])
    assert "Cart exported to cart.csv (0 items)." in out
    assert (tmp_path / "cart.csv").read_text(encoding="utf-8") == CsvExporter().export([])


def test_export_invalid_format_command(monkeypatch, capsys, tmp_path):
    monkeypatch.chdir(tmp_path)
    out = run_main_with_inputs(monkeypatch, capsys, ["1", "export pdf", "export", "q"])
    assert "Error: unknown export format 'pdf'. Usage: export <csv|html>" in out
    assert "Error: unknown export format ''. Usage: export <csv|html>" in out
    assert list(tmp_path.iterdir()) == []


# --- STU-304: ריקון העגלה ב-CLI ---

def test_clear_command_on_populated_cart(monkeypatch, capsys):
    out = run_main_with_inputs(
        monkeypatch, capsys,
        ["1", "cs", "101", "", "cs", "202", "", "clear", "cart", "q"],
    )
    assert "Cart cleared (2 items removed)." in out
    assert "Your cart is empty." in out
    assert "Items in cart: 0" in out


def test_clear_command_single_item(monkeypatch, capsys):
    out = run_main_with_inputs(monkeypatch, capsys, ["1", "cs", "101", "", "clear", "q"])
    assert "Cart cleared (1 item removed)." in out


def test_clear_command_on_empty_cart(monkeypatch, capsys):
    out = run_main_with_inputs(monkeypatch, capsys, ["1", "clear", "q"])
    assert "Your cart is already empty." in out


def test_cart_usable_after_clear_command(monkeypatch, capsys):
    out = run_main_with_inputs(
        monkeypatch, capsys,
        ["1", "cs", "101", "", "clear", "math", "901", "", "cart", "q"],
    )
    assert "Items in cart: 1" in out
    assert "Calculus 1" in out.split("--- Your cart ---")[-1]
    assert "Intro to CS, Price" not in out.split("--- Your cart ---")[-1]
