"""
Pet Shop - Recommendation Engine
Provides product recommendations based on user preferences and behavior
"""

from typing import List, Dict, Optional
from collections import defaultdict


class RecommendationEngine:
    def __init__(self):
        self.user_preferences: Dict[int, dict] = {}
        self.purchase_history: Dict[int, List[int]] = defaultdict(list)
        self.product_categories: Dict[int, str] = {}
        self.similarity_scores: Dict[tuple, float] = {}

    def track_user_preference(self, user_id: int, preferences: dict):
        """Track user preferences for recommendations"""
        self.user_preferences[user_id] = preferences

    def track_purchase(self, user_id: int, product_id: int):
        """Track user purchase for recommendation history"""
        if product_id not in self.purchase_history[user_id]:
            self.purchase_history[user_id].append(product_id)

    def set_product_category(self, product_id: int, category: str):
        """Set product category for recommendations"""
        self.product_categories[product_id] = category

    def get_recommended_products(self, user_id: int, limit: int = 5) -> List[int]:
        """Get personalized product recommendations for user"""
        if user_id not in self.user_preferences:
            return self.get_popular_products(limit)
        
        preferences = self.user_preferences[user_id]
        purchased = self.purchase_history.get(user_id, [])
        
        # Get products based on preferences
        recommended = []
        
        # Recommend products in preferred categories
        preferred_category = preferences.get('preferred_species', '')
        for product_id, category in self.product_categories.items():
            if product_id not in purchased and category == preferred_category:
                recommended.append(product_id)
        
        # Add popular products if not enough recommendations
        if len(recommended) < limit:
            popular = self.get_popular_products(limit - len(recommended))
            for product_id in popular:
                if product_id not in recommended and product_id not in purchased:
                    recommended.append(product_id)
        
        return recommended[:limit]

    def get_similar_products(self, product_id: int, limit: int = 5) -> List[int]:
        """Get products similar to the given product"""
        if product_id not in self.product_categories:
            return []
        
        category = self.product_categories[product_id]
        similar = []
        
        for pid, cat in self.product_categories.items():
            if pid != product_id and cat == category:
                similar.append(pid)
        
        return similar[:limit]

    def get_frequently_bought_together(self, product_id: int, limit: int = 3) -> List[int]:
        """Get products frequently bought with this product"""
        co_purchased = defaultdict(int)
        
        # Find users who bought this product
        for user_id, purchases in self.purchase_history.items():
            if product_id in purchases:
                # Count other products they bought
                for pid in purchases:
                    if pid != product_id:
                        co_purchased[pid] += 1
        
        # Sort by frequency
        sorted_products = sorted(co_purchased.items(), 
                               key=lambda x: x[1], reverse=True)
        
        return [pid for pid, count in sorted_products[:limit]]

    def get_popular_products(self, limit: int = 10) -> List[int]:
        """Get most popular products based on purchase history"""
        product_counts = defaultdict(int)
        
        for purchases in self.purchase_history.values():
            for product_id in purchases:
                product_counts[product_id] += 1
        
        sorted_products = sorted(product_counts.items(), 
                               key=lambda x: x[1], reverse=True)
        
        return [pid for pid, count in sorted_products[:limit]]

    def get_trending_products(self, days: int = 7, limit: int = 5) -> List[int]:
        """Get trending products (placeholder - would use timestamps in real implementation)"""
        # In a real implementation, would filter by date
        return self.get_popular_products(limit)

    def get_recommendations_for_cart(self, cart_items: List[int], 
                                    limit: int = 3) -> List[int]:
        """Get recommendations based on current cart contents"""
        recommendations = set()
        
        for product_id in cart_items:
            similar = self.get_similar_products(product_id, limit)
            recommendations.update(similar)
            
            bought_together = self.get_frequently_bought_together(product_id, limit)
            recommendations.update(bought_together)
        
        # Remove items already in cart
        recommendations -= set(cart_items)
        
        return list(recommendations)[:limit]

    def calculate_product_similarity(self, product_id1: int, product_id2: int) -> float:
        """Calculate similarity score between two products"""
        key = tuple(sorted([product_id1, product_id2]))
        
        if key in self.similarity_scores:
            return self.similarity_scores[key]
        
        # Simple similarity based on category
        if product_id1 in self.product_categories and product_id2 in self.product_categories:
            cat1 = self.product_categories[product_id1]
            cat2 = self.product_categories[product_id2]
            
            if cat1 == cat2:
                score = 0.8
            else:
                score = 0.2
            
            self.similarity_scores[key] = score
            return score
        
        return 0.0

    def get_personalized_search_results(self, user_id: int, 
                                       search_results: List[int]) -> List[int]:
        """Reorder search results based on user preferences"""
        if user_id not in self.user_preferences:
            return search_results
        
        preferences = self.user_preferences[user_id]
        preferred_category = preferences.get('preferred_species', '')
        
        # Separate into preferred and other categories
        preferred = []
        other = []
        
        for product_id in search_results:
            category = self.product_categories.get(product_id, '')
            if category == preferred_category:
                preferred.append(product_id)
            else:
                other.append(product_id)
        
        # Return preferred items first
        return preferred + other
