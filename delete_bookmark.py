#!/usr/bin/env python3
"""Delete a bookmark from Raindrop.io by its ID."""

import requests


def delete_bookmark(api_token: str, bookmark_id: int) -> bool:
    """
    Delete a raindrop bookmark by ID.

    Returns True on success, False on failure.
    """
    url = f"https://api.raindrop.io/rest/v1/raindrop/{bookmark_id}"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Error deleting bookmark {bookmark_id}: {e}")
        return False
