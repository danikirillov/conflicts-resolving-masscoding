"""
Pet Shop - Pricing Calculator
Calculates prices with discounts, taxes, and promotions
"""

from typing import List, Dict, Optional
from datetime import datetime


class PricingCalculator:
    def __init__(self):
        self.tax_rate = 0.08
        self.base_discount = 0.0
        self.promotions: Dict[str, dict] = {}

    def calculate_item_price(self, base_price: float, quantity: int = 1) -> float:
        """Calculate price for a single item with quantity"""
        return base_price * quantity

    def apply_discount(self, price: float, discount_percent: float) -> float:
        """Apply discount percentage to price"""
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Discount must be between 0 and 100")
        
        discount_amount = price * (discount_percent / 100)
        return price - discount_amount

    def calculate_tax(self, subtotal: float) -> float:
        """Calculate tax on subtotal"""
        return subtotal * self.tax_rate

    def calculate_order_total(self, items: List[dict]) -> dict:
        """Calculate complete order total with tax"""
        subtotal = 0.0
        
        for item in items:
            price = item.get('price', 0.0)
            quantity = item.get('quantity', 1)
            discount = item.get('discount', 0.0)
            
            item_price = self.calculate_item_price(price, quantity)
            item_price = self.apply_discount(item_price, discount)
            subtotal += item_price
        
        tax = self.calculate_tax(subtotal)
        total = subtotal + tax
        
        return {
            'subtotal': round(subtotal, 2),
            'tax': round(tax, 2),
            'total': round(total, 2)
        }

    def add_promotion(self, promo_code: str, discount_percent: float, 
                     expiry_date: Optional[datetime] = None):
        """Add a promotional discount code"""
        self.promotions[promo_code] = {
            'discount': discount_percent,
            'expiry': expiry_date
        }

    def apply_promo_code(self, promo_code: str, subtotal: float) -> dict:
        """Apply promotional code to order"""
        if promo_code not in self.promotions:
            return {
                'success': False,
                'message': 'Invalid promo code',
                'discount': 0.0
            }
        
        promo = self.promotions[promo_code]
        
        # Check if promotion is expired
        if promo['expiry'] and datetime.now() > promo['expiry']:
            return {
                'success': False,
                'message': 'Promo code expired',
                'discount': 0.0
            }
        
        discount_amount = subtotal * (promo['discount'] / 100)
        
        return {
            'success': True,
            'message': 'Promo code applied',
            'discount': round(discount_amount, 2),
            'new_subtotal': round(subtotal - discount_amount, 2)
        }

    def calculate_bulk_discount(self, quantity: int, base_price: float) -> float:
        """Calculate bulk discount based on quantity"""
        if quantity >= 10:
            discount = 15.0
        elif quantity >= 5:
            discount = 10.0
        elif quantity >= 3:
            discount = 5.0
        else:
            discount = 0.0
        
        total = self.calculate_item_price(base_price, quantity)
        return self.apply_discount(total, discount)

    def calculate_loyalty_discount(self, subtotal: float, loyalty_points: int) -> float:
        """Calculate discount based on loyalty points"""
        # 100 points = $1 discount
        discount_amount = loyalty_points / 100
        return max(0, subtotal - discount_amount)

    def calculate_shipping(self, subtotal: float, shipping_method: str = 'standard') -> float:
        """Calculate shipping cost"""
        # Free shipping over $50
        if subtotal >= 50:
            return 0.0
        
        shipping_rates = {
            'standard': 5.99,
            'express': 12.99,
            'overnight': 24.99
        }
        
        return shipping_rates.get(shipping_method, 5.99)

    def get_final_price(self, items: List[dict], promo_code: Optional[str] = None,
                       loyalty_points: int = 0, shipping_method: str = 'standard') -> dict:
        """Calculate final price with all discounts and fees"""
        # Calculate base order total
        order_calc = self.calculate_order_total(items)
        subtotal = order_calc['subtotal']
        
        # Apply promo code if provided
        promo_discount = 0.0
        if promo_code:
            promo_result = self.apply_promo_code(promo_code, subtotal)
            if promo_result['success']:
                promo_discount = promo_result['discount']
                subtotal = promo_result['new_subtotal']
        
        # Apply loyalty discount
        subtotal = self.calculate_loyalty_discount(subtotal, loyalty_points)
        
        # Calculate shipping
        shipping = self.calculate_shipping(subtotal, shipping_method)
        
        # Recalculate tax on adjusted subtotal
        tax = self.calculate_tax(subtotal)
        
        # Final total
        total = subtotal + tax + shipping
        
        return {
            'subtotal': round(subtotal, 2),
            'promo_discount': round(promo_discount, 2),
            'tax': round(tax, 2),
            'shipping': round(shipping, 2),
            'total': round(total, 2)
        }
