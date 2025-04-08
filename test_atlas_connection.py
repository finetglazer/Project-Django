#!/usr/bin/env python
# Save this file in your project root

import os
import sys
import pymongo
import time

# Add the project to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings_docker')

def test_atlas_connection():
    print("Testing MongoDB Atlas connection...")

    # Atlas connection string
    atlas_uri = "mongodb+srv://tranhung10122003:OJw5AywNkq2TBQOw@cluster0.24wivb9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    max_retries = 5
    retry_interval = 3  # seconds

    for attempt in range(max_retries):
        try:
            client = pymongo.MongoClient(atlas_uri, serverSelectionTimeoutMS=5000)
            # The ismaster command is cheap and does not require auth
            client.admin.command('ismaster')

            # Get database name (ec2)
            db = client['ec2']

            print(f"✅ Successfully connected to MongoDB Atlas!")
            print(f"📊 Database: ec2")
            print(f"📋 Collections: {db.list_collection_names()}")
            return True

        except pymongo.errors.ServerSelectionTimeoutError as err:
            print(f"❌ Connection attempt {attempt + 1}/{max_retries} failed: {err}")
            if attempt < max_retries - 1:
                print(f"⏱️ Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
            else:
                print("❌ Failed to connect to MongoDB Atlas after multiple attempts")
                print("Please check your Atlas connection string, network settings, and IP whitelist")
                return False

        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}")
            return False

if __name__ == "__main__":
    test_atlas_connection()