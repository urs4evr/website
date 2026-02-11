#!/usr/bin/env python3
"""
Download better romantic/couple-focused stock photos for 7 date ideas.
2 alternatives per idea so we can pick the best.
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

IMAGES = [
    # --- Backyard / Tent Camping ---
    {
        "filename": "camping-tent-a.jpg",
        "url": "https://images.pexels.com/photos/6271625/pexels-photo-6271625.jpeg?auto=compress&cs=tinysrgb&w=1200",
    },
    {
        "filename": "camping-tent-b.jpg",
        "url": "https://images.pexels.com/photos/7363069/pexels-photo-7363069.jpeg?auto=compress&cs=tinysrgb&w=1200",
    },

    # --- DIY Cocktail Night ---
    {
        "filename": "cocktail-night-a.jpg",
        "url": "https://images.pexels.com/photos/5490965/pexels-photo-5490965.jpeg?auto=compress&cs=tinysrgb&w=1200",
    },
    {
        "filename": "cocktail-night-b.jpg",
        "url": "https://images.pexels.com/photos/3171815/pexels-photo-3171815.jpeg?auto=compress&cs=tinysrgb&w=1200",
    },

    # --- Picnic in a Park ---
    {
        "filename": "picnic-park-a.jpg",
        "url": "https://images.pexels.com/photos/1322185/pexels-photo-1322185.jpeg?auto=compress&cs=tinysrgb&w=1200",
    },
    {
        "filename": "picnic-park-b.jpg",
        "url": "https://images.pexels.com/photos/5765828/pexels-photo-5765828.jpeg?auto=compress&cs=tinysrgb&w=1200",
    },

    # --- Bike Ride Together ---
    {
        "filename": "bike-ride-a.jpg",
        "url": "https://images.pexels.com/photos/2549018/pexels-photo-2549018.jpeg?auto=compress&cs=tinysrgb&w=1200",
    },
    {
        "filename": "bike-ride-b.jpg",
        "url": "https://images.pexels.com/photos/1548771/pexels-photo-1548771.jpeg?auto=compress&cs=tinysrgb&w=1200",
    },

    # --- Roller or Ice Skating ---
    {
        "filename": "ice-skating-a.jpg",
        "url": "https://images.pexels.com/photos/1216544/pexels-photo-1216544.jpeg?auto=compress&cs=tinysrgb&w=1200",
    },
    {
        "filename": "ice-skating-b.jpg",
        "url": "https://images.pexels.com/photos/5858106/pexels-photo-5858106.jpeg?auto=compress&cs=tinysrgb&w=1200",
    },

    # --- Couple's Vision Board ---
    {
        "filename": "vision-board-a.jpg",
        "url": "https://images.pexels.com/photos/8112172/pexels-photo-8112172.jpeg?auto=compress&cs=tinysrgb&w=1200",
    },
    {
        "filename": "vision-board-b.jpg",
        "url": "https://images.pexels.com/photos/5428833/pexels-photo-5428833.jpeg?auto=compress&cs=tinysrgb&w=1200",
    },

    # --- Write Letters to Future Selves ---
    {
        "filename": "love-letters-a.jpg",
        "url": "https://images.pexels.com/photos/6205509/pexels-photo-6205509.jpeg?auto=compress&cs=tinysrgb&w=1200",
    },
    {
        "filename": "love-letters-b.jpg",
        "url": "https://images.pexels.com/photos/4226896/pexels-photo-4226896.jpeg?auto=compress&cs=tinysrgb&w=1200",
    },
]


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"\nDownloading {len(IMAGES)} images to: {OUTPUT_DIR}\n")

    success = 0
    failed = []
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
                failed.append(img["filename"])
        except Exception as e:
            print(f"           ERROR: {e}")
            failed.append(img["filename"])

    print(f"\nResult: {success}/{len(IMAGES)} downloaded successfully")
    if failed:
        print(f"Failed: {', '.join(failed)}")
    print(f"Images saved to: {OUTPUT_DIR}\n")


if __name__ == "__main__":
    main()
