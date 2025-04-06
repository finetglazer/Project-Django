# book/services/sentiment_service.py
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class SentimentService:
    """Service for analyzing sentiment in text"""
    
    @staticmethod
    def initialize_nltk():
        """Download required NLTK data if not already present"""
        try:
            # Check if VADER lexicon is available
            nltk.data.find('sentiment/vader_lexicon.zip')
        except LookupError:
            # Download necessary NLTK data
            nltk.download('punkt')
            nltk.download('stopwords')
            nltk.download('vader_lexicon')
    
    @staticmethod
    def preprocess_text(text):
        """Clean and preprocess text for sentiment analysis"""
        if not text:
            return ""
            
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation and special characters
        text = re.sub(r'[^\w\s]', '', text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stop_words]
        
        # Rejoin tokens
        return " ".join(tokens)
    
    @staticmethod
    def analyze_sentiment(text):
        """
        Analyze sentiment of text and return a score between -1 and 1
        where -1 is very negative, 0 is neutral, and 1 is very positive
        """
        SentimentService.initialize_nltk()
        
        # Preprocess the text
        processed_text = SentimentService.preprocess_text(text)
        
        if not processed_text:
            return 0.0
        
        # Use VADER Sentiment Intensity Analyzer
        analyzer = SentimentIntensityAnalyzer()
        sentiment_scores = analyzer.polarity_scores(processed_text)
        
        # Return the compound score which is a normalized score between -1 and 1
        return sentiment_scores['compound']