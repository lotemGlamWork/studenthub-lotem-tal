
from abc import ABC, abstractmethod

class IPricingStrategy(ABC):
    @abstractmethod
    def calculate_price(self, base_price):
        """מחשב את המחיר הסופי"""
        pass

# 2. מימוש האסטרטגיות
class PercentageDiscountStrategy(IPricingStrategy):
    def __init__(self, percentage):
        self.percentage = percentage

    def calculate_price(self, base_price):
        return base_price * (1 - self.percentage / 100)

class FixedDiscountStrategy(IPricingStrategy):
    def __init__(self, amount):
        self.amount = amount

    def calculate_price(self, base_price):
        return max(0, base_price - self.amount) # לוודא שלא יורד מתחת ל-0

class DefaultStrategy(IPricingStrategy):
    def calculate_price(self, base_price):
        return base_price
