#!/usr/bin/env python3
"""
Blog-Produktbilder Downloader
=============================
Wiederverwendbares Skript zum Herunterladen von Amazon-Produktbildern
für Blog-Artikel auf anni.

Nutzung:
  1. JSON-Datei:   python3 download-product-images.py products.json
  2. Inline:       PRODUCTS-Liste unten bearbeiten, dann: python3 download-product-images.py

Beispiel JSON-Datei (products.json):
{
  "output_dir": "images",
  "products": [
    {
      "url": "https://www.amazon.com/dp/B0CGY4X222",
      "filename": "lego-roses.jpg"
    }
  ]
}
"""

import os
import sys
import json
import re
import requests
from bs4 import BeautifulSoup

# =============================================================================
# KONFIGURATION - Nur diesen Block anpassen!
# =============================================================================

OUTPUT_DIR = "images"  # Relativer Ordner (wird neben diesem Skript erstellt)

PRODUCTS = [
    # {"url": "https://www.amazon.com/dp/ASIN", "filename": "dein-dateiname.jpg"},
]

# =============================================================================
# AB HIER NICHTS ÄNDERN
# =============================================================================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}


def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"  Ordner erstellt: {path}")


def try_highres_url(img_url):
    """
    Versucht aus einer Amazon-Thumbnail-URL eine hochaufgeloeste Version zu machen.
    Amazon-Bild-URLs enthalten Groessen-Parameter wie ._SX38_ oder ._SS40_.
    Wir ersetzen diese durch ._SL1500_ fuer maximale Aufloesung.
    """
    # Pattern: ._XXNNN_ wobei XX = Buchstaben, NNN = Zahlen
    highres = re.sub(r'\._[A-Z]{2}\d+_', '._SL1500_', img_url)
    if highres != img_url:
        return highres

    # Alternativ: ._SCLZZZZZZZ_SXNNN_ Pattern
    highres = re.sub(r'\._SCL[Z]+_SX\d+_', '._SL1500_', img_url)
    if highres != img_url:
        return highres

    return None


def find_image_url(soup):
    """
    Sucht die Produktbild-URL mit mehreren Strategien (in Prioritaetsreihenfolge).
    """
    strategies = []

    # Strategie 1: Amazon landingImage (zuverlaessigstes Element)
    img = soup.find('img', {'id': 'landingImage'})
    if img:
        # data-old-hires hat oft die hoechste Aufloesung
        if img.get('data-old-hires'):
            strategies.append(('landingImage[data-old-hires]', img['data-old-hires']))
        if img.get('src'):
            strategies.append(('landingImage[src]', img['src']))

    # Strategie 2: hiRes aus dem JavaScript-Daten-Block
    scripts = soup.find_all('script', string=re.compile(r'"hiRes"\s*:'))
    for script in scripts:
        matches = re.findall(r'"hiRes"\s*:\s*"([^"]+)"', script.string or '')
        for match in matches:
            if 'm.media-amazon.com' in match or 'images-na.ssl-images-amazon.com' in match:
                strategies.append(('hiRes-script', match))
                break
        if strategies:
            break

    # Strategie 3: Open Graph meta tag (funktioniert auch auf nicht-Amazon-Seiten)
    meta = soup.find('meta', property='og:image')
    if meta and meta.get('content'):
        strategies.append(('og:image', meta['content']))

    # Strategie 4: Erstes grosses Amazon-CDN-Bild im HTML
    for img in soup.find_all('img'):
        src = img.get('src', '') or ''
        if 'm.media-amazon.com/images/I/' in src:
            strategies.append(('media-amazon-scan', src))
            break

    return strategies


def download_image(product, save_dir):
    """Laedt ein einzelnes Produktbild herunter."""
    filepath = os.path.join(save_dir, product['filename'])

    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        if size > 100:  # Platzhalter-GIFs sind ~43 Bytes
            print(f"  SKIP  {product['filename']} (existiert bereits, {size:,} bytes)")
            return True

    print(f"  LOAD  {product['filename']}")

    try:
        response = requests.get(product['url'], headers=HEADERS, timeout=20)
        if response.status_code != 200:
            print(f"        HTTP {response.status_code} - Seite nicht erreichbar")
            return False

        soup = BeautifulSoup(response.content, 'html.parser')
        strategies = find_image_url(soup)

        if not strategies:
            title = soup.find('title')
            title_text = (title.text.strip()[:60] + '...') if title else 'unbekannt'
            print(f"        FEHLER: Kein Bild gefunden (Seite: {title_text})")
            return False

        # Beste Strategie nehmen
        strategy_name, img_url = strategies[0]
        print(f"        Quelle: {strategy_name}")

        # Hochaufgeloeste Version versuchen
        highres_url = try_highres_url(img_url)
        if highres_url:
            try:
                hr_resp = requests.get(highres_url, headers=HEADERS, timeout=15)
                if hr_resp.status_code == 200 and len(hr_resp.content) > 1000:
                    img_url = highres_url
                    print(f"        Hochaufgeloest: ja")
            except Exception:
                pass  # Fallback auf Original-URL

        # Bild herunterladen
        img_resp = requests.get(img_url, headers=HEADERS, timeout=15)
        if img_resp.status_code != 200 or len(img_resp.content) < 100:
            print(f"        FEHLER: Bild-Download fehlgeschlagen")
            return False

        with open(filepath, 'wb') as f:
            f.write(img_resp.content)

        size = os.path.getsize(filepath)
        print(f"        OK ({size:,} bytes)")
        return True

    except requests.Timeout:
        print(f"        FEHLER: Timeout")
        return False
    except Exception as e:
        print(f"        FEHLER: {e}")
        return False


def main():
    products = PRODUCTS
    output_dir = OUTPUT_DIR

    # JSON-Datei als Argument?
    if len(sys.argv) > 1:
        json_path = sys.argv[1]
        if not os.path.exists(json_path):
            print(f"Datei nicht gefunden: {json_path}")
            sys.exit(1)
        with open(json_path, 'r') as f:
            config = json.load(f)
        products = config.get('products', [])
        output_dir = config.get('output_dir', OUTPUT_DIR)

    if not products:
        print("Keine Produkte definiert!")
        print("Entweder PRODUCTS-Liste im Skript fuellen oder JSON-Datei uebergeben.")
        print(f"Nutzung: python3 {os.path.basename(__file__)} [products.json]")
        sys.exit(1)

    # Ausgabe-Ordner relativ zum Skript-Verzeichnis
    save_dir = os.path.join(get_script_dir(), output_dir)
    ensure_dir(save_dir)

    print(f"\n{'='*60}")
    print(f"Blog-Produktbilder Downloader")
    print(f"{'='*60}")
    print(f"Zielordner: {save_dir}")
    print(f"Produkte:   {len(products)}")
    print(f"{'='*60}\n")

    success = 0
    failed = []

    for i, product in enumerate(products, 1):
        print(f"[{i}/{len(products)}] {product.get('filename', '???')}")
        if download_image(product, save_dir):
            success += 1
        else:
            failed.append(product['filename'])
        print()

    print(f"{'='*60}")
    print(f"ERGEBNIS: {success}/{len(products)} erfolgreich")
    if failed:
        print(f"FEHLGESCHLAGEN:")
        for f in failed:
            print(f"  - {f}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
