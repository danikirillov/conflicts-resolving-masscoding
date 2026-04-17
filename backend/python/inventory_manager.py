"""
Pet Shop - Inventory Manager
Manages inventory tracking and stock levels
"""

from datetime import datetime
from typing import Dict, List, Optional


class InventoryManager:
    def __init__(self):
        self.inventory: Dict[int, dict] = {}
        self.transaction_history: List[dict] = []
        self.reorder_threshold = 15

    def add_product(self, product_id: int, name: str, quantity: int, cost: float) -> bool:
        """Add a new product to inventory"""
        if product_id in self.inventory:
            return False
        
        self.inventory[product_id] = {
            'product_id': product_id,
            'name': name,
            'quantity': quantity,
            'cost': cost,
            'last_updated': datetime.now()
        }
        
        self._log_transaction('ADD', product_id, quantity)
        return True

    def update_quantity(self, product_id: int, quantity: int) -> bool:
        """Update product quantity"""
        if product_id not in self.inventory:
            return False
        
        old_quantity = self.inventory[product_id]['quantity']
        self.inventory[product_id]['quantity'] = quantity
        self.inventory[product_id]['last_updated'] = datetime.now()
        
        change = quantity - old_quantity
        transaction_type = 'RESTOCK' if change > 0 else 'ADJUST'
        self._log_transaction(transaction_type, product_id, abs(change))
        
        return True

    def reduce_stock(self, product_id: int, quantity: int) -> bool:
        """Reduce stock when item is sold"""
        if product_id not in self.inventory:
            return False
        
        current_quantity = self.inventory[product_id]['quantity']
        if current_quantity < quantity:
            return False
        
        self.inventory[product_id]['quantity'] -= quantity
        self.inventory[product_id]['last_updated'] = datetime.now()
        
        self._log_transaction('SALE', product_id, quantity)
        return True

    def restock_product(self, product_id: int, quantity: int) -> bool:
        """Add stock to existing product"""
        if product_id not in self.inventory:
            return False
        
        self.inventory[product_id]['quantity'] += quantity
        self.inventory[product_id]['last_updated'] = datetime.now()
        
        self._log_transaction('RESTOCK', product_id, quantity)
        return True

    def get_product_info(self, product_id: int) -> Optional[dict]:
        """Get information about a specific product"""
        return self.inventory.get(product_id)

    def check_stock(self, product_id: int) -> int:
        """Check current stock level"""
        if product_id in self.inventory:
            return self.inventory[product_id]['quantity']
        return 0

    def get_low_stock_items(self) -> List[dict]:
        """Get list of products with low stock"""
        low_stock = []
        for product_id, info in self.inventory.items():
            if info['quantity'] < self.reorder_threshold:
                low_stock.append(info)
        return low_stock

    def get_all_products(self) -> List[dict]:
        """Get all products in inventory"""
        return list(self.inventory.values())

    def remove_product(self, product_id: int) -> bool:
        """Remove product from inventory"""
        if product_id in self.inventory:
            self._log_transaction('REMOVE', product_id, 
                                self.inventory[product_id]['quantity'])
            del self.inventory[product_id]
            return True
        return False

    def calculate_total_value(self) -> float:
        """Calculate total inventory value"""
        total = 0.0
        for info in self.inventory.values():
            total += info['quantity'] * info['cost']
        return total

    def _log_transaction(self, transaction_type: str, product_id: int, quantity: int):
        """Log inventory transaction"""
        self.transaction_history.append({
            'timestamp': datetime.now(),
            'type': transaction_type,
            'product_id': product_id,
            'quantity': quantity
        })

    def get_transaction_history(self, product_id: Optional[int] = None) -> List[dict]:
        """Get transaction history, optionally filtered by product"""
        if product_id is None:
            return self.transaction_history
        
        return [t for t in self.transaction_history if t['product_id'] == product_id]
