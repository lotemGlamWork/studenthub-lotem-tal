# test_shopping_service.py - STU-203: בדיקות עגלת הקניות
import pytest
from services import CourseService
from shopping_service import ShoppingService
from strategies import DefaultStrategy, FixedDiscountStrategy, PercentageDiscountStrategy

MOCK_DB = {
    "cs": [
        {"id": "101", "name": "Intro", "prereqs": [], "price": 100},
        {"id": "202", "name": "DS", "prereqs": ["101"], "price": 150},
    ],
    "math": [
        {"id": "901", "name": "Calculus", "prereqs": [], "price": 120},
    ],
}


@pytest.fixture
def cart():
    # DI: מזריקים CourseService עם DB מזויף
    return ShoppingService(course_service=CourseService(db=MOCK_DB))


# AC1: קורס קיים שלא בעגלה -> נוסף ומחזיר True
def test_add_existing_course_returns_true(cart):
    assert cart.add_to_cart("101") is True
    assert [c["id"] for c in cart.get_cart()] == ["101"]


# AC2: קורס שכבר בעגלה -> False, בלי כפילות
def test_add_duplicate_returns_false_without_duplicate(cart):
    cart.add_to_cart("101")
    assert cart.add_to_cart("101") is False
    assert len(cart.get_cart()) == 1


# AC3: מזהה לא קיים -> ValueError, העגלה לא משתנה
def test_add_unknown_course_raises_and_cart_unchanged(cart):
    cart.add_to_cart("101")
    with pytest.raises(ValueError):
        cart.add_to_cart("999")
    assert [c["id"] for c in cart.get_cart()] == ["101"]


# AC4: הסכום הכולל מחושב עם האסטרטגיה שהועברה
def test_total_with_default_strategy(cart):
    cart.add_to_cart("101")
    cart.add_to_cart("901")
    assert cart.calculate_total(DefaultStrategy()) == 220


def test_total_with_percentage_strategy(cart):
    cart.add_to_cart("101")
    cart.add_to_cart("202")
    assert cart.calculate_total(PercentageDiscountStrategy(10)) == pytest.approx(225)


def test_total_with_fixed_strategy_applies_per_course(cart):
    cart.add_to_cart("101")
    cart.add_to_cart("901")
    # 20 ש"ח הנחה על כל קורס: 80 + 100
    assert cart.calculate_total(FixedDiscountStrategy(20)) == 180


# AC5: עגלה ריקה -> סכום 0; ShoppingService משתמש ב-CourseService שהוזרק
def test_empty_cart_total_is_zero(cart):
    assert cart.calculate_total(DefaultStrategy()) == 0


def test_uses_injected_course_service():
    class FakeCourseService:
        def get_course_by_id(self, course_id):
            return {"id": course_id, "name": "Fake", "prereqs": [], "price": 50}

    cart = ShoppingService(course_service=FakeCourseService())
    assert cart.add_to_cart("anything") is True
    assert cart.calculate_total(DefaultStrategy()) == 50


def test_get_cart_returns_copy(cart):
    cart.add_to_cart("101")
    cart.get_cart().clear()
    assert len(cart.get_cart()) == 1


# --- STU-301: הסרה מהעגלה ---

def test_remove_existing_course_returns_true(cart):
    cart.add_to_cart("101")
    cart.add_to_cart("901")
    assert cart.remove_from_cart("101") is True
    assert [c["id"] for c in cart.get_cart()] == ["901"]


def test_remove_course_not_in_cart_returns_false(cart):
    cart.add_to_cart("101")
    # קורס קיים בקטלוג אבל לא בעגלה
    assert cart.remove_from_cart("202") is False
    assert [c["id"] for c in cart.get_cart()] == ["101"]


def test_remove_unknown_course_id_returns_false_without_error(cart):
    assert cart.remove_from_cart("999") is False
    assert cart.get_cart() == []


def test_total_updates_after_removal(cart):
    cart.add_to_cart("101")
    cart.add_to_cart("202")
    assert cart.calculate_total(DefaultStrategy()) == 250
    cart.remove_from_cart("202")
    assert cart.calculate_total(DefaultStrategy()) == 100
    cart.remove_from_cart("101")
    assert cart.calculate_total(DefaultStrategy()) == 0


def test_removed_course_can_be_added_again(cart):
    cart.add_to_cart("101")
    cart.remove_from_cart("101")
    assert cart.add_to_cart("101") is True


# --- STU-302: מספר פריטים וסיכום חיסכון ---

def test_empty_cart_summary(cart):
    assert cart.get_item_count() == 0
    assert cart.get_subtotal() == 0
    assert cart.calculate_savings(PercentageDiscountStrategy(10)) == 0


def test_item_count_tracks_add_and_remove(cart):
    cart.add_to_cart("101")
    cart.add_to_cart("202")
    cart.add_to_cart("101")  # כפילות - לא נספרת
    assert cart.get_item_count() == 2
    cart.remove_from_cart("101")
    assert cart.get_item_count() == 1


def test_savings_with_percentage_discount(cart):
    cart.add_to_cart("101")
    cart.add_to_cart("202")
    # 250 לפני, 225 אחרי 10%
    assert cart.get_subtotal() == 250
    assert cart.calculate_savings(PercentageDiscountStrategy(10)) == pytest.approx(25)


def test_savings_with_fixed_discount_per_course(cart):
    cart.add_to_cart("101")
    cart.add_to_cart("901")
    # 20 ש"ח על כל אחד מ-2 קורסים
    assert cart.calculate_savings(FixedDiscountStrategy(20)) == 40


def test_savings_with_fixed_discount_capped_at_course_price():
    class FakeCourseService:
        def get_course_by_id(self, course_id):
            return {"id": course_id, "name": "Cheap", "prereqs": [], "price": 15}

    cart = ShoppingService(course_service=FakeCourseService())
    cart.add_to_cart("1")
    # המחיר לא יורד מתחת ל-0, אז החיסכון הוא 15 ולא 20
    assert cart.calculate_savings(FixedDiscountStrategy(20)) == 15


def test_no_discount_means_zero_savings(cart):
    cart.add_to_cart("101")
    cart.add_to_cart("901")
    assert cart.calculate_savings(DefaultStrategy()) == 0
    assert cart.calculate_total(DefaultStrategy()) == cart.get_subtotal() == 220
