from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import logging
from django.shortcuts import render
from django.db.models import Q, Count
from .models import Item
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Avg
from .models import Item, Review
from .forms import ReviewForm
from .services.sentiment_service import SentimentService
from .services.recommendation_service import RecommendationService
from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError


logger = logging.getLogger('book')



# The search function you already have
def search(request):
    keyword = request.GET.get('keyword', '')
    if keyword:
        # Filter items by name or category that contain the keyword (case-insensitive)
        items = Item.objects.filter(
            Q(name__icontains=keyword) | Q(category__icontains=keyword)
        )
    else:
        # If no keyword provided, display all items
        items = Item.objects.all()

    # Add some recommended items if we have a user
    recommended_items = []
    if request.user.is_authenticated:
        recommended_items = RecommendationService.get_recommendations_for_user(
            user=request.user,
            limit=4
        )

    return render(request, 'search.html', {
        'items': items,
        'recommended_items': recommended_items
    })

def item_detail(request, item_id):
    """View for displaying item details and reviews"""
    item = get_object_or_404(Item, pk=item_id)
    reviews = item.reviews.all().order_by('-created_at')
    review_form = ReviewForm()

    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.item = item
            review.user = request.user

            # Analyze sentiment
            sentiment_score = SentimentService.analyze_sentiment(review.text)
            review.sentiment_score = sentiment_score

            review.save()

            # Update item's average rating
            item.average_rating = item.reviews.aggregate(Avg('rating'))['rating__avg']
            item.save()

            messages.success(request, "Thank you for your review!")
            return redirect('item_detail', item_id=item.id)

    # Get recommended items based on this item
    similar_items = Item.objects.filter(
        category=item.category
    ).exclude(
        id=item.id
    ).order_by('-average_rating')[:4]

    context = {
        'item': item,
        'reviews': reviews,
        'review_form': review_form,
        'similar_items': similar_items
    }

    return render(request, 'book/item_detail.html', context)


def recommendations(request):
    """View for displaying personalized recommendations"""
    try:
        # Get recommendations for current user
        recommended_items = RecommendationService.get_recommendations_for_user(
            user=request.user,
            limit=8
        )

        # Get trending items (most reviewed with positive sentiment)
        trending_items = Item.objects.annotate(
            review_count=Count('reviews'),
            avg_sentiment=Avg('reviews__sentiment_score')
        ).filter(
            review_count__gt=0
        ).order_by('-review_count', '-avg_sentiment')[:4]

        context = {
            'recommended_items': recommended_items,
            'trending_items': trending_items,
        }

        return render(request, 'book/recommendations.html', context)
    except Exception as e:
        logger.error(f"Error in recommendations view: {str(e)}")
        messages.error(request, "An error occurred while loading recommendations. Please try again later.")
        return redirect('accounts:index')  # Redirect to home page on error


def db_health_check(request):
    """
    Simple view to check if the database connection is working.
    Access via /db-health/ after adding to urls.py
    """
    try:
        # Try to connect to the database
        conn = connections['default']
        conn.cursor()
        db_status = "Database connection successful!"
        status_code = 200
    except OperationalError as e:
        # Handle database connection error
        db_status = f"Database connection failed: {str(e)}"
        status_code = 500
    except Exception as e:
        # Handle other exceptions
        db_status = f"Error checking database: {str(e)}"
        status_code = 500

    return JsonResponse({
        'status': db_status,
        'connection_settings': {
            'ENGINE': connections['default'].settings_dict['ENGINE'],
            'NAME': connections['default'].settings_dict['NAME'],
            # Don't include sensitive info like password in the response
        }
    }, status=status_code)

# Add to your urls.py:
# path('db-health/', db_health_check, name='db_health_check'),