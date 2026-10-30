"""
Dataset Preparation Script for Phishing Website Detection System.

Builds a balanced, realistic, modern dataset of:
1. Legitimate URLs:
   - Sourced from Cisco OpenDNS top domains (root, subpages, blogs, search, docs)
   - Sourced from UNB CIC benign dataset
2. Phishing URLs:
   - Sourced from PhishTank verified active phishing database
   - Sourced from OpenPhish live intelligence feed
"""

import os
import csv
import random
import urllib.request
import io
import pandas as pd

random.seed(42)

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(DATA_DIR, "phishing_dataset.csv")

OPENDNS_URL = "https://raw.githubusercontent.com/opendns/public-domain-lists/master/opendns-top-domains.txt"
PHISHTANK_URL = "https://raw.githubusercontent.com/shreyagopal/Phishing-Website-Detection-by-Machine-Learning-Techniques/master/DataFiles/2.online-valid.csv"
OPENPHISH_URL = "https://openphish.com/feed.txt"
UNB_BENIGN_URL = "https://raw.githubusercontent.com/shreyagopal/Phishing-Website-Detection-by-Machine-Learning-Techniques/master/DataFiles/1.Benign_list_big_final.csv"

# Typical legitimate subpaths to represent real-world benign website navigation
BENIGN_PATH_TEMPLATES = [
    "",
    "/",
    "/about",
    "/about-us",
    "/contact",
    "/contact-us",
    "/products",
    "/services",
    "/solutions",
    "/pricing",
    "/features",
    "/documentation",
    "/docs/overview",
    "/docs/api/reference",
    "/blog",
    "/news/technology",
    "/articles/latest",
    "/help/center",
    "/support/knowledge-base",
    "/privacy-policy",
    "/terms-of-service",
    "/faq",
    "/careers",
    "/download/release",
    "/wiki/Main_Page",
    "/wiki/Computer_science",
    "/search?q=technology&page=1",
    "/search?query=documentation&lang=en",
    "/category/software/updates",
    "/projects/open-source",
    "/browse/popular"
]


def prepare_dataset(sample_per_class: int = 3500):
    print("=" * 65)
    print("PREPARING REALISTIC BALANCED DATASET (LEGITIMATE & PHISHING)")
    print("=" * 65)

    benign_urls = []
    phishing_urls = []

    # 1. Cisco OpenDNS Top Legitimate Domains
    print("[*] Fetching Cisco OpenDNS top domains...")
    try:
        req = urllib.request.Request(OPENDNS_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=12) as response:
            domains = [l.decode('utf-8', errors='ignore').strip() for l in response.readlines()]
            clean_domains = [d for d in domains if d and not d.startswith('#') and '.' in d][:2000]
            
            for i, d in enumerate(clean_domains):
                # Include root domains
                benign_urls.append(f"https://{d}")
                benign_urls.append(f"https://www.{d}")
                
                # Include realistic paths & subpages
                path_choice = BENIGN_PATH_TEMPLATES[i % len(BENIGN_PATH_TEMPLATES)]
                if path_choice and path_choice != "/":
                    benign_urls.append(f"https://{d}{path_choice}")
                    benign_urls.append(f"https://www.{d}{path_choice}")
                    
        print(f"[+] Generated {len(benign_urls)} modern legitimate URLs from OpenDNS.")
    except Exception as e:
        print(f"[!] Warning: OpenDNS download failed: {e}")

    # 2. Add UNB Benign URLs
    print("[*] Downloading UNB CIC benign dataset...")
    try:
        req = urllib.request.Request(UNB_BENIGN_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            lines = response.read(600000).decode('utf-8', errors='ignore').splitlines()
            for l in lines:
                u = l.strip().split(',')[0].strip('"\'')
                if u.startswith('http://') or u.startswith('https://'):
                    benign_urls.append(u)
                    # Also include https version for modern web representation
                    if u.startswith('http://'):
                        benign_urls.append('https://' + u[7:])
        print(f"[+] Total benign pool size: {len(benign_urls)}")
    except Exception as e:
        print(f"[!] Warning: UNB dataset fetch failed: {e}")

    # 3. PhishTank Phishing URLs
    print("[*] Downloading PhishTank verified phishing database...")
    try:
        req = urllib.request.Request(PHISHTANK_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8', errors='ignore')
            reader = csv.DictReader(io.StringIO(content))
            for row in reader:
                u = row.get('url', '').strip()
                if u.startswith('http://') or u.startswith('https://'):
                    phishing_urls.append(u)
        print(f"[+] Loaded {len(phishing_urls)} PhishTank phishing URLs.")
    except Exception as e:
        print(f"[!] Warning: PhishTank download failed: {e}")

    # 4. OpenPhish Live Phishing URLs
    print("[*] Downloading OpenPhish active live feed...")
    try:
        req = urllib.request.Request(OPENPHISH_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            lines = [l.strip() for l in response.read().decode('utf-8', errors='ignore').splitlines() if l.strip()]
            for u in lines:
                if u.startswith('http://') or u.startswith('https://'):
                    phishing_urls.append(u)
        print(f"[+] Total phishing pool size: {len(phishing_urls)}")
    except Exception as e:
        print(f"[!] Warning: OpenPhish download failed: {e}")

    # Deduplicate and shuffle
    benign_urls = list(dict.fromkeys(benign_urls))
    phishing_urls = list(dict.fromkeys(phishing_urls))
    random.shuffle(benign_urls)
    random.shuffle(phishing_urls)

    target_count = min(len(benign_urls), len(phishing_urls), sample_per_class)
    print(f"[*] Selecting balanced sample: {target_count} legitimate & {target_count} phishing...")

    final_rows = []
    for u in benign_urls[:target_count]:
        final_rows.append({"url": u, "label": 0})
    for u in phishing_urls[:target_count]:
        final_rows.append({"url": u, "label": 1})

    df = pd.DataFrame(final_rows)
    df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"[SUCCESS] Saved balanced dataset to {OUTPUT_FILE}")
    print(f"Total Rows: {len(df)} | Legitimate (0): {sum(df['label'] == 0)} | Phishing (1): {sum(df['label'] == 1)}")
    return df


if __name__ == "__main__":
    prepare_dataset(sample_per_class=3500)
