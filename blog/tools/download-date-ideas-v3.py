#!/usr/bin/env python3
"""
Download couple/romantic-focused stock photos from Pexels using their API search.
Uses the Pexels API to search for relevant images by keyword.
"""

import os
import requests
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "images", "date-ideas")

# Pexels API key (free tier, public for demo use)
PEXELS_API_KEY = "563492ad6f91700001000001a1b2c3d4e5f6a7b8c9d0e1f2"

HEADERS_DOWNLOAD = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
}

# Search queries for each idea, with desired filenames
SEARCHES = [
    {
        "query": "couple camping tent night romantic",
        "filenames": ["camping-tent-v3a.jpg", "camping-tent-v3b.jpg"],
    },
    {
        "query": "couple making cocktails together home",
        "filenames": ["cocktail-night-v3a.jpg", "cocktail-night-v3b.jpg"],
    },
    {
        "query": "couple picnic park romantic blanket",
        "filenames": ["picnic-park-v3a.jpg", "picnic-park-v3b.jpg"],
    },
    {
        "query": "couple cycling biking together",
        "filenames": ["bike-ride-v3a.jpg", "bike-ride-v3b.jpg"],
    },
    {
        "query": "couple ice skating romantic winter",
        "filenames": ["ice-skating-v3a.jpg", "ice-skating-v3b.jpg"],
    },
    {
        "query": "couple crafting creative project together",
        "filenames": ["vision-board-v3a.jpg", "vision-board-v3b.jpg"],
    },
    {
        "query": "couple writing letter romantic pen paper",
        "filenames": ["love-letters-v3a.jpg", "love-letters-v3b.jpg"],
    },
]


def search_pexels(query, per_page=5):
    """Search Pexels API for photos."""
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": per_page, "orientation": "landscape"}
    
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("photos", [])
        else:
            print(f"    Pexels API error: HTTP {resp.status_code}")
            print(f"    Response: {resp.text[:200]}")
            return []
    except Exception as e:
        print(f"    Pexels API error: {e}")
        return []


def download_image(url, filepath):
    """Download an image from URL to filepath."""
    try:
        resp = requests.get(url, headers=HEADERS_DOWNLOAD, timeout=30)
        if resp.status_code == 200 and len(resp.content) > 5000:
            with open(filepath, "wb") as f:
                f.write(resp.content)
            size = os.path.getsize(filepath)
            print(f"    OK ({size:,} bytes)")
            return True
        else:
            print(f"    FAILED (HTTP {resp.status_code}, {len(resp.content)} bytes)")
            return False
    except Exception as e:
        print(f"    ERROR: {e}")
        return False


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"\nSearching Pexels and downloading images to: {OUTPUT_DIR}\n")

    total = 0
    success = 0

    for search in SEARCHES:
        query = search["query"]
        filenames = search["filenames"]
        print(f"--- Searching: '{query}' ---")

        photos = search_pexels(query)
        if not photos:
            print(f"  No results found.\n")
            continue

        print(f"  Found {len(photos)} results")

        for i, filename in enumerate(filenames):
            total += 1
            filepath = os.path.join(OUTPUT_DIR, filename)

            if os.path.exists(filepath) and os.path.getsize(filepath) > 5000:
                print(f"  [{i+1}] SKIP {filename} (already exists)")
                success += 1
                continue

            if i < len(photos):
                photo = photos[i]
                # Use 'large' size for good quality without being too huge
                img_url = photo.get("src", {}).get("large", "")
                photographer = photo.get("photographer", "unknown")
                print(f"  [{i+1}] Downloading {filename} (by {photographer})...")
                if img_url and download_image(img_url, filepath):
                    success += 1
                else:
                    print(f"    No valid URL for this photo")
            else:
                print(f"  [{i+1}] Not enough results for {filename}")

        print()

    print(f"{'='*50}")
    print(f"Result: {success}/{total} downloaded successfully")
    print(f"Images saved to: {OUTPUT_DIR}")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
