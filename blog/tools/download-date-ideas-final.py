#!/usr/bin/env python3
"""
Download couple/romantic-focused stock photos from Pexels.
Uses verified Pexels photo IDs found via web search.
URL pattern: https://images.pexels.com/photos/{ID}/pexels-photo-{ID}.jpeg?auto=compress&cs=tinysrgb&w=1200
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

def pexels_url(photo_id):
    return f"https://images.pexels.com/photos/{photo_id}/pexels-photo-{photo_id}.jpeg?auto=compress&cs=tinysrgb&w=1200"

# Verified Pexels photo IDs from web search results
IMAGES = [
    # --- Camping: couple in tent (Vanessa Garcia) ---
    {"filename": "camping-final-a.jpg", "url": pexels_url(6324452)},
    {"filename": "camping-final-b.jpg", "url": pexels_url(6324456)},

    # --- Cocktails: couple with drinks at home ---
    {"filename": "cocktail-final-a.jpg", "url": pexels_url(3859842)},
    {"filename": "cocktail-final-b.jpg", "url": pexels_url(3171815)},

    # --- Picnic: romantic couple on picnic blanket ---
    {"filename": "picnic-final-a.jpg", "url": pexels_url(5119609)},
    {"filename": "picnic-final-b.jpg", "url": pexels_url(19759639)},

    # --- Biking: couple riding bicycles ---
    {"filename": "bike-final-a.jpg", "url": pexels_url(10509678)},
    {"filename": "bike-final-b.jpg", "url": pexels_url(8350895)},

    # --- Ice skating: couple holding hands ---
    {"filename": "skating-final-a.jpg", "url": pexels_url(6712141)},
    # Second ice skating option - couple at ice rink
    {"filename": "skating-final-b.jpg", "url": pexels_url(6711948)},

    # --- Vision board / creative couple project ---
    {"filename": "vision-final-a.jpg", "url": pexels_url(6899260)},
    {"filename": "vision-final-b.jpg", "url": pexels_url(4348401)},

    # --- Love letters: writing / romantic letter ---
    {"filename": "letters-final-a.jpg", "url": pexels_url(1809347)},
    {"filename": "letters-final-b.jpg", "url": pexels_url(6205759)},
]


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"\nDownloading {len(IMAGES)} images to: {OUTPUT_DIR}\n")

    success = 0
    failed = []
    for i, img in enumerate(IMAGES, 1):
        filepath = os.path.join(OUTPUT_DIR, img["filename"])
        if os.path.exists(filepath) and os.path.getsize(filepath) > 5000:
            print(f"  [{i:2d}/{len(IMAGES)}] SKIP {img['filename']} (exists)")
            success += 1
            continue

        print(f"  [{i:2d}/{len(IMAGES)}] {img['filename']}...")
        try:
            resp = requests.get(img["url"], headers=HEADERS, timeout=30, allow_redirects=True)
            if resp.status_code == 200 and len(resp.content) > 5000:
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

    print(f"\n{'='*50}")
    print(f"Result: {success}/{len(IMAGES)} downloaded")
    if failed:
        print(f"Failed: {', '.join(failed)}")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
