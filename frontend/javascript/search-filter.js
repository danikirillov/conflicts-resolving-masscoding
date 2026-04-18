// Pet Shop - Search and Filter Functionality
// Provides advanced search and filtering for pets and products

class SearchFilter {
    constructor() {
        this.filters = {
            category: 'all',
            minPrice: 0,
            maxPrice: 10000,
            species: [],
            age: 'all'
        };
        this.sortBy = 'price_low';
    }

    applyFilters(products) {
        let filtered = [...products];
        
        // Filter by category
        if (this.filters.category !== 'all') {
            filtered = filtered.filter(p => p.category === this.filters.category);
        }
        
        // Filter by price range
        filtered = filtered.filter(p => 
            p.price >= this.filters.minPrice && 
            p.price <= this.filters.maxPrice
        );
        
        // Filter by species
        if (this.filters.species.length > 0) {
            filtered = filtered.filter(p => 
                this.filters.species.includes(p.species)
            );
        }
        
        // Filter by age
        if (this.filters.age !== 'all') {
            filtered = filtered.filter(p => this.matchesAgeFilter(p));
        }
        
        return this.sortProducts(filtered);
    }

    sortProducts(products) {
        const sorted = [...products];
        
        switch(this.sortBy) {
            case 'name':
                return sorted.sort((a, b) => a.name.localeCompare(b.name));
            case 'price_low':
                return sorted.sort((a, b) => a.price - b.price);
            case 'price_high':
                return sorted.sort((a, b) => b.price - a.price);
            case 'newest':
                return sorted.sort((a, b) => new Date(b.addedDate) - new Date(a.addedDate));
            default:
                return sorted;
        }
    }

    matchesAgeFilter(product) {
        const age = product.age;
        switch(this.filters.age) {
            case 'puppy':
                return age < 12;
            case 'adult':
                return age >= 12 && age < 84;
            case 'senior':
                return age >= 84;
            default:
                return true;
        }
    }

    updateFilter(filterName, value) {
        this.filters[filterName] = value;
    }

    resetFilters() {
        this.filters = {
            category: 'all',
            minPrice: 0,
            maxPrice: 10000,
            species: [],
            age: 'all'
        };
        this.sortBy = 'price_low';
    }
}

const searchFilter = new SearchFilter();
