# book/services/recommendation_service.py
from django.db.models import Avg, Count
from book.models import Item, Review

class RecommendationService:
    """Service for generating product recommendations based on sentiment analysis"""

    @staticmethod
    def get_top_rated_items(limit=5, category=None):
        """
        Get items with the highest average ratings

        Args:
            limit: Number of items to return
            category: Optional category to filter by

        Returns:
            List of items sorted by average rating
        """
        try:
            items_query = Item.objects.all()

            if category:
                items_query = items_query.filter(category__iexact=category)

            # Order by average_rating
            return items_query.order_by('-average_rating')[:limit]
        except Exception as e:
            # If anything goes wrong, return an empty list
            return []

    @staticmethod
    def get_recommendations_for_user(user, limit=5):
        """
        Get personalized recommendations for a user

        Args:
            user: User object to get recommendations for
            limit: Number of items to recommend

        Returns:
            List of recommended items
        """
        try:
            # For simplicity, just return top-rated items
            return RecommendationService.get_top_rated_items(limit)
        except Exception as e:
            # If anything goes wrong, return an empty list
            return []