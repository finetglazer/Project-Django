# book/services/recommendation_service.py
from django.db.models import Avg, Count
from book.models import Item, Review

class RecommendationService:
    """Service for generating product recommendations based on sentiment analysis"""
    
    @staticmethod
    def get_top_rated_items(limit=5, category=None):
        """
        Get items with the highest average sentiment scores
        
        Args:
            limit: Number of items to return
            category: Optional category to filter by
        
        Returns:
            List of items sorted by average sentiment score
        """
        items_query = Item.objects.annotate(
            avg_sentiment=Avg('reviews__sentiment_score'),
            review_count=Count('reviews')
        ).filter(review_count__gt=0)
        
        if category:
            items_query = items_query.filter(category__iexact=category)
        
        return items_query.order_by('-avg_sentiment', '-review_count')[:limit]
    
    @staticmethod
    def get_recommendations_for_user(user, limit=5):
        """
        Get personalized recommendations for a user based on their past reviews
        
        Args:
            user: User object to get recommendations for
            limit: Number of items to recommend
            
        Returns:
            List of recommended items
        """
        if not user.is_authenticated:
            # Return top-rated items for anonymous users
            return RecommendationService.get_top_rated_items(limit)
        
        # Get categories the user has positively reviewed
        user_positive_categories = Review.objects.filter(
            user=user,
            sentiment_score__gt=0.3  # Consider scores > 0.3 as positive
        ).values_list('item__category', flat=True).distinct()
        
        if not user_positive_categories:
            # If no positive reviews, return top-rated items
            return RecommendationService.get_top_rated_items(limit)
        
        # Get items from categories the user likes that they haven't reviewed yet
        recommended_items = Item.objects.filter(
            category__in=user_positive_categories
        ).exclude(
            reviews__user=user
        ).annotate(
            avg_sentiment=Avg('reviews__sentiment_score'),
            review_count=Count('reviews')
        ).filter(
            review_count__gt=0,
            avg_sentiment__gt=0.3  # Only recommend items with positive sentiment
        ).order_by('-avg_sentiment', '-review_count')[:limit]
        
        # If we don't have enough recommendations, add some top-rated items
        if recommended_items.count() < limit:
            top_items = RecommendationService.get_top_rated_items(
                limit=limit - recommended_items.count()
            )
            # Combine the two querysets
            recommended_items = list(recommended_items) + list(top_items)
            # Remove duplicates
            seen_ids = set()
            unique_items = []
            for item in recommended_items:
                if item.id not in seen_ids:
                    seen_ids.add(item.id)
                    unique_items.append(item)
            return unique_items[:limit]
            
        return recommended_items