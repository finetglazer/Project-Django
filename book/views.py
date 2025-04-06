from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import logging
from django.shortcuts import render
from django.db.models import Q, Count
from django.utils import timezone

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
# Modify the search function in book/views.py
def search(request):
    keyword = request.GET.get('keyword', '')
    items = []

    try:
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
            try:
                recommended_items = RecommendationService.get_recommendations_for_user(
                    user=request.user,
                    limit=4
                )
            except Exception as e:
                logger.error(f"Error getting recommendations: {str(e)}")
                # Continue even if recommendations fail
                recommended_items = []

        return render(request, 'search.html', {
            'items': items,
            'recommended_items': recommended_items
        })

    except Exception as e:
        logger.error(f"Database error in search view: {str(e)}")
        messages.error(request, "Sorry, we encountered a problem connecting to our database. Please try again later.")
        return render(request, 'search.html', {
            'items': [],
            'recommended_items': [],
            'error': "Database connection error. Please try again later."
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

# Update this function in book/views.py
def recommendations(request):
    """View for displaying personalized recommendations"""
    try:
        # Get top-rated items as recommendations
        recommended_items = Item.objects.all().order_by('-average_rating')[:8]

        # Get trending items (most recently added)
        trending_items = Item.objects.all().order_by('-id')[:4]

        context = {
            'recommended_items': recommended_items,
            'trending_items': trending_items,
        }

        return render(request, 'book/recommendations.html', context)
    except Exception as e:
        logger.error(f"Error in recommendations view: {str(e)}")
        messages.error(request, "An error occurred while loading recommendations. Please try again later.")
        return redirect('accounts:index')  # Redirect to home page on error



# Add this function to book/views.py to check database connection
def db_health_check(request):
    """
    Simple view to check if the database connection is working.
    Access via /book/db-health/ after adding to urls.py
    """
    try:
        # Try to connect to the database
        conn = connections['default']
        conn.cursor()

        # Try a simple query
        test_query = Item.objects.first()

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
        'engine': connections['default'].settings_dict['ENGINE'],
        'name': connections['default'].settings_dict['NAME'],
        'timestamp': timezone.now().isoformat(),
    }, status=status_code)

# Add this to your urls.py:
# path('db-health/', views.db_health_check, name='db_health_check'),