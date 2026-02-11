#!/usr/bin/env python3
"""
Download free stock photos from Pexels for the Valentine's Day Date Ideas blog article.
Uses the Pexels API-free direct image URLs.
"""

import os
import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "images", "date-ideas")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
}

# Free Pexels photos (direct image URLs, free to use)
IMAGES = [
    {
        "filename": "spa-thermal-baths.jpg",
        "url": "https://images.pexels.com/photos/3188/love-romantic-bath-candlelight.jpg?auto=compress&cs=tinysrgb&w=1200",
        "alt": "Spa day at thermal baths"
    },
    {
        "filename": "love-letters.jpg",
        "url": "https://images.pexels.com/photos/745045/pexels-photo-745045.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "alt": "Writing love letters"
    },
    {
        "filename": "vision-board.jpg",
        "url": "https://images.pexels.com/photos/7176026/pexels-photo-7176026.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "alt": "Couple creating a vision board"
    },
    {
        "filename": "ice-skating.jpg",
        "url": "https://images.pexels.com/photos/1839151/pexels-photo-1839151.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "alt": "Couple ice skating"
    },
    {
        "filename": "bike-ride.jpg",
        "url": "https://images.pexels.com/photos/1578750/pexels-photo-1578750.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "alt": "Couple bike riding together"
    },
    {
        "filename": "picnic-park.jpg",
        "url": "https://images.pexels.com/photos/1656579/pexels-photo-1656579.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "alt": "Couple having a picnic in a park"
    },
    {
        "filename": "board-games.jpg",
        "url": "https://images.pexels.com/photos/4691567/pexels-photo-4691567.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "alt": "Board game night"
    },
    {
        "filename": "restaurant-date.jpg",
        "url": "https://images.pexels.com/photos/1267320/pexels-photo-1267320.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "alt": "Couple at a restaurant"
    },
    {
        "filename": "cocktail-night.jpg",
        "url": "https://images.pexels.com/photos/5947019/pexels-photo-5947019.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "alt": "DIY cocktail making"
    },
    {
        "filename": "camping-tent.jpg",
        "url": "https://images.pexels.com/photos/2398220/pexels-photo-2398220.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "alt": "Backyard camping with tent"
    },
]


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"\nDownloading {len(IMAGES)} images to: {OUTPUT_DIR}\n")

    success = 0
    for i, img in enumerate(IMAGES, 1):
        filepath = os.path.join(OUTPUT_DIR, img["filename"])
        if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
            print(f"  [{i}/{len(IMAGES)}] SKIP {img['filename']} (already exists)")
            success += 1
            continue

        print(f"  [{i}/{len(IMAGES)}] Downloading {img['filename']}...")
        try:
            resp = requests.get(img["url"], headers=HEADERS, timeout=30)
            if resp.status_code == 200 and len(resp.content) > 1000:
                with open(filepath, "wb") as f:
                    f.write(resp.content)
                size = os.path.getsize(filepath)
                print(f"           OK ({size:,} bytes)")
                success += 1
            else:
                print(f"           FAILED (HTTP {resp.status_code}, {len(resp.content)} bytes)")
        except Exception as e:
            print(f"           ERROR: {e}")

    print(f"\nResult: {success}/{len(IMAGES)} downloaded successfully")
    print(f"Images saved to: {OUTPUT_DIR}\n")


if __name__ == "__main__":
    main()
