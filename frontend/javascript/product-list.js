// Pet Shop - Product List Manager
// Displays and filters available pets and products

class ProductList {
    constructor() {
        this.products = [];
        this.itemsPerPage = 12;
    }

    loadProducts() {
        // Fetch products from API
        fetch('/api/products')
            .then(response => response.json())
            .then(data => {
                this.products = data;
                this.displayProducts();
            });
    }

    displayProducts() {
        const container = document.getElementById('product-grid');
        container.innerHTML = '';
        
        this.products.forEach(product => {
            const card = this.createProductCard(product);
            container.appendChild(card);
        });
    }

    createProductCard(product) {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.innerHTML = `
            <img src="${product.image}" alt="${product.name}">
            <h3>${product.name}</h3>
            <p>${product.description}</p>
            <p class="price">$${product.price}</p>
            <button onclick="addToCart(${product.id})">Add to Cart</button>
        `;
        return card;
    }

    filterByCategory(category) {
        const filtered = this.products.filter(p => p.category === category);
        return filtered;
    }
}

const productList = new ProductList();
productList.loadProducts();
