#!/usr/bin/env python3
"""
Random Bookmark Fetcher for Raindrop.io

This script fetches a random bookmark from your Raindrop collection.
It's designed to be scalable even with large bookmark collections by using
pagination and efficient random selection.

Requirements:
- requests library
- Raindrop.io API token

Setup:
1. Create an app at https://app.raindrop.io/settings/integrations
2. Get your API token
3. Set the RAINDROP_TOKEN environment variable or update the script
"""

import os
import requests
import random
import sys
from typing import Dict, List, Optional
from dotenv import load_dotenv


class RaindropRandomizer:
    """Handles fetching random bookmarks from Raindrop.io"""
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.raindrop.io/rest/v1"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    def get_total_bookmarks(self, collection_id: int = 0) -> int:
        """
        Get the total number of bookmarks in a collection.
        
        Args:
            collection_id: Collection ID (0 for all bookmarks)
            
        Returns:
            Total number of bookmarks
        """
        url = f"{self.base_url}/raindrops/{collection_id}"
        params = {"perpage": 1}  # We only need the count
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("count", 0)
        except requests.RequestException as e:
            print(f"Error fetching bookmark count: {e}")
            return 0
    
    def get_bookmarks_page(self, page: int, per_page: int = 50,
                           collection_id: int = 0) -> List[Dict]:
        """
        Get a specific page of bookmarks.
        
        Args:
            page: Page number (0-indexed)
            per_page: Number of bookmarks per page (max 50)
            collection_id: Collection ID (0 for all bookmarks)
            
        Returns:
            List of bookmark dictionaries
        """
        url = f"{self.base_url}/raindrops/{collection_id}"
        params = {
            "page": page,
            "perpage": min(per_page, 50)  # API limit is 50
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("items", [])
        except requests.RequestException as e:
            print(f"Error fetching bookmarks page {page}: {e}")
            return []
    
    def get_random_bookmark(self, collection_id: int = 0) -> Optional[Dict]:
        """
        Get a random bookmark using efficient pagination.
        
        Args:
            collection_id: Collection ID (0 for all bookmarks)
            
        Returns:
            Random bookmark dictionary or None if no bookmarks found
        """
        total_bookmarks = self.get_total_bookmarks(collection_id)
        
        if total_bookmarks == 0:
            print("No bookmarks found in the collection.")
            return None
        
        print(f"Found {total_bookmarks} total bookmarks")
        
        # For scalability, pick a random page then a random bookmark
        # from that page
        per_page = 50  # Maximum allowed by API
        total_pages = (total_bookmarks + per_page - 1) // per_page
        
        # Pick a random page
        random_page = random.randint(0, total_pages - 1)
        
        # Get the bookmarks from that page
        bookmarks = self.get_bookmarks_page(
            random_page, per_page, collection_id
        )
        
        if not bookmarks:
            print(f"No bookmarks found on page {random_page}")
            return None
        
        # Pick a random bookmark from the page
        random_bookmark = random.choice(bookmarks)
        return random_bookmark
    
    def get_collections(self) -> List[Dict]:
        """
        Get all collections to help users choose which one to use.
        
        Returns:
            List of collection dictionaries
        """
        url = f"{self.base_url}/collections"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data.get("items", [])
        except requests.RequestException as e:
            print(f"Error fetching collections: {e}")
            return []
    
    def format_bookmark(self, bookmark: Dict) -> str:
        """
        Format a bookmark for display.
        
        Args:
            bookmark: Bookmark dictionary from API
            
        Returns:
            Formatted bookmark string
        """
        title = bookmark.get("title", "Untitled")
        url = bookmark.get("link", "")
        excerpt = bookmark.get("excerpt", "")
        tags = bookmark.get("tags", [])
        created = bookmark.get("created", "")
        
        formatted = f"""
📖 {title}
🔗 {url}
"""
        
        if excerpt:
            excerpt_text = excerpt[:200]
            if len(excerpt) > 200:
                excerpt_text += "..."
            formatted += f"📝 {excerpt_text}\n"
        
        if tags:
            formatted += f"🏷️  {', '.join(tags)}\n"
        
        if created:
            formatted += f"📅 Added: {created[:10]}\n"
        
        return formatted


def get_api_token() -> str:
    """Get API token from .env file, environment variable, or prompt user."""
    # Load environment variables from .env file
    load_dotenv()
    
    token = os.getenv("RAINDROP_TOKEN")
    
    if not token:
        print("Raindrop API token not found in .env file or "
              "environment variables.")
        print("Please set RAINDROP_TOKEN in .env file or "
              "environment variable.")
        print("Get your token from: "
              "https://app.raindrop.io/settings/integrations")
        token = input("Enter your Raindrop API token: ").strip()
    
    return token


def main():
    """Main function to run the random bookmark fetcher."""
    print("🌧️  Random Raindrop Bookmark Fetcher")
    print("=" * 40)
    
    # Get API token
    api_token = get_api_token()
    
    if not api_token:
        print("❌ No API token provided. Exiting.")
        sys.exit(1)
    
    # Initialize the randomizer
    randomizer = RaindropRandomizer(api_token)
    
    # Check if user wants to see collections first
    if len(sys.argv) > 1 and sys.argv[1] == "--collections":
        print("\n📁 Available Collections:")
        collections = randomizer.get_collections()
        print(f"{'ID':<10} {'Title':<30} {'Count':<10}")
        print("-" * 50)
        print(f"{'0':<10} {'All Bookmarks':<30} {'N/A':<10}")
        
        for collection in collections:
            cid = collection.get("_id", "Unknown")
            title = collection.get("title", "Untitled")[:30]
            count = collection.get("count", 0)
            print(f"{cid:<10} {title:<30} {count:<10}")
        
        print("\nUse: python random_bookmark.py [collection_id]")
        return
    
    # Get collection ID from command line argument
    collection_id = 0  # Default to all bookmarks
    if len(sys.argv) > 1:
        try:
            collection_id = int(sys.argv[1])
        except ValueError:
            print(f"❌ Invalid collection ID: {sys.argv[1]}")
            print("Use --collections to see available collections")
            sys.exit(1)
    
    # Get a random bookmark
    print(f"\n🎲 Fetching random bookmark from collection {collection_id}...")
    bookmark = randomizer.get_random_bookmark(collection_id)
    
    if bookmark:
        print("\n🎉 Here's your random bookmark:")
        print(randomizer.format_bookmark(bookmark))
        
        # Option to open in browser
        if input("\n🌐 Open in browser? (y/N): ").lower().strip() == 'y':
            import webbrowser
            webbrowser.open(bookmark.get("link", ""))
    else:
        print("❌ No bookmark found or error occurred.")


if __name__ == "__main__":
    main()