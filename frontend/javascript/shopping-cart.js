// Pet Shop - Shopping Cart Manager
// Handles cart operations and calculations

class ShoppingCart {
    constructor() {
        this.items = [];
        this.taxRate = 0.08;
    }

    addItem(productId, quantity = 1) {
        const existingItem = this.items.find(item => item.productId === productId);
        
        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            this.items.push({
                productId,
                quantity,
                addedAt: new Date()
            });
        }
        
        this.saveCart();
        this.updateCartDisplay();
    }

    removeItem(productId) {
        this.items = this.items.filter(item => item.productId !== productId);
        this.saveCart();
        this.updateCartDisplay();
    }

    calculateTotal() {
        let subtotal = 0;
        this.items.forEach(item => {
            subtotal += item.price * item.quantity;
        });
        
        const tax = subtotal * this.taxRate;
        const total = subtotal + tax;
        
        return {
            subtotal,
            tax,
            total
        };
    }

    saveCart() {
        localStorage.setItem('petShopCart', JSON.stringify(this.items));
    }

    loadCart() {
        const saved = localStorage.getItem('petShopCart');
        if (saved) {
            this.items = JSON.parse(saved);
        }
    }

    updateCartDisplay() {
        const badge = document.getElementById('cart-badge');
        badge.textContent = this.items.length;
    }
}

const cart = new ShoppingCart();
cart.loadCart();
