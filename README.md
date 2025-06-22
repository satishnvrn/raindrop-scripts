# Random Raindrop Bookmark Fetcher

A Python script to fetch random bookmarks from your Raindrop.io collection. Designed to be scalable even with large bookmark collections.

## Features

- 🎲 Fetch random bookmarks from your entire collection or specific collections
- 📊 Scalable design using pagination (works efficiently with thousands of bookmarks)
- 🏷️ Displays bookmark title, URL, excerpt, tags, and creation date
- 🌐 Optional browser opening
- 📁 List all your collections

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Your Raindrop API Token

1. Go to [Raindrop.io Integrations](https://app.raindrop.io/settings/integrations)
2. Create a new app or use an existing one
3. Copy your API token

### 3. Set Up Your API Token

**Option 1: Using .env file (Recommended)**

Create a `.env` file in the script directory:
```bash
echo 'RAINDROP_TOKEN=your_api_token_here' > .env
```

**Option 2: Environment Variable**

```bash
export RAINDROP_TOKEN="your_api_token_here"
```

Or add it to your shell profile:
```bash
echo 'export RAINDROP_TOKEN="your_api_token_here"' >> ~/.zshrc
source ~/.zshrc
```

## Usage

### Basic Usage (All Bookmarks)

```bash
python random_bookmark.py
```

### List Available Collections

```bash
python random_bookmark.py --collections
```

### Get Random Bookmark from Specific Collection

```bash
python random_bookmark.py 12345678
```

Replace `12345678` with the collection ID from the collections list.

## How It Works (Scalability)

The script uses an efficient approach for large collections:

1. **First**, it gets the total count of bookmarks in your collection
2. **Then**, it calculates how many pages exist (50 bookmarks per page, API limit)
3. **Next**, it randomly selects a page number
4. **Finally**, it fetches that single page and picks a random bookmark from it

This means:
- ✅ Only 2 API calls needed (count + one page)
- ✅ Works with 10 bookmarks or 100,000 bookmarks equally well
- ✅ No memory issues from loading large datasets
- ✅ Fast execution regardless of collection size

## Example Output

```
🌧️  Random Raindrop Bookmark Fetcher
========================================

🎲 Fetching random bookmark from collection 0...
Found 2,847 total bookmarks

🎉 Here's your random bookmark:

📖 How to Build Scalable Python Applications
🔗 https://example.com/python-scaling
📝 A comprehensive guide to building Python applications that can handle millions of users...
🏷️  python, programming, scalability, backend
📅 Added: 2024-12-15

🌐 Open in browser? (y/N):
```

## Error Handling

The script handles various scenarios:
- Invalid or missing API tokens
- Network connectivity issues
- Empty collections
- Invalid collection IDs
- API rate limits and errors

## Requirements

- Python 3.6+
- `requests` library
- Valid Raindrop.io account and API token
