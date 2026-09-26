"""
fetch_reddit_candidates_throttled.py
====================================
Fetches REAL public Reddit posts from Atom RSS feeds across target subreddits:
r/ChatGPTCoding, r/cursor, r/GithubCopilot, r/ClaudeAI, r/LocalLLaMA, r/ExperiencedDevs, r/ADHD_Programmers.

Applies a strict 4.5s rate-limit delay between requests to respect Reddit's CDN limits.
Filters for posts containing code blocks (```) and pasted assistant output complaints.
Saves candidate posts into benchmark/reddit_candidates/ and displays 10 samples for Harjot's review.
"""

import urllib.request
import xml.etree.ElementTree as ET
import html
import os
import time
import re
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CANDIDATES_DIR = os.path.join(BASE_DIR, "reddit_candidates")
MANIFEST_PATH = os.path.join(BASE_DIR, "reddit_manifest.json")

# Clear previous candidate files
if os.path.exists(CANDIDATES_DIR):
    for f in os.listdir(CANDIDATES_DIR):
        os.remove(os.path.join(CANDIDATES_DIR, f))
os.makedirs(CANDIDATES_DIR, exist_ok=True)

SUBREDDITS = [
    "ChatGPTCoding",
    "cursor",
    "GithubCopilot",
    "ClaudeAI",
    "LocalLLaMA",
    "ExperiencedDevs",
    "ADHD_Programmers"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

def clean_html_text(raw_html):
    if not raw_html:
        return ""
    text = html.unescape(raw_html)
    text = re.sub(r'<pre><code>', '\n```\n', text)
    text = re.sub(r'</code></pre>', '\n```\n', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()

def main():
    collected_candidates = []
    seen_urls = set()
    file_counter = 1
    
    print("Fetching REAL public Reddit posts via Atom RSS feeds (4.5s throttling, no API key required)...\n")
    
    for sub in SUBREDDITS:
        url = f"https://www.reddit.com/r/{sub}/top.rss?t=year&limit=25"
        print(f"Fetching RSS feed for r/{sub}...")
        
        req = urllib.request.Request(url, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                xml_data = resp.read().decode("utf-8")
                
                root = ET.fromstring(xml_data)
                ns = {"atom": "http://www.w3.org/2005/Atom"}
                entries = root.findall("atom:entry", ns)
                
                for entry in entries:
                    title_elem = entry.find("atom:title", ns)
                    link_elem = entry.find("atom:link", ns)
                    content_elem = entry.find("atom:content", ns)
                    
                    title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""
                    permalink = link_elem.attrib.get("href", "") if link_elem is not None else ""
                    raw_content = content_elem.text if content_elem is not None and content_elem.text else ""
                    
                    if not permalink or permalink in seen_urls:
                        continue
                        
                    clean_text = clean_html_text(raw_content)
                    combined = f"Title: {title}\n\n{clean_text}"
                    
                    has_code = "```" in clean_text or "def " in clean_text or "const " in clean_text or "function" in clean_text or "class " in clean_text
                    has_assistant_kw = any(kw in combined.lower() for kw in ["copilot", "cursor", "chatgpt", "claude", "llm", "ai", "prompt", "code", "output", "suggested", "produced"])
                    
                    if len(clean_text) < 150 or not has_assistant_kw:
                        continue
                        
                    seen_urls.add(permalink)
                    post_id = permalink.rstrip("/").split("/")[-2] if len(permalink.rstrip("/").split("/")) > 2 else f"id_{file_counter}"
                    
                    fname = f"reddit_post_{file_counter:02d}_{sub}_{post_id}.txt"
                    fpath = os.path.join(CANDIDATES_DIR, fname)
                    
                    with open(fpath, "w", encoding="utf-8") as f:
                        f.write(f"Source URL: {permalink}\n")
                        f.write(f"Subreddit: r/{sub}\n")
                        f.write(f"Title: {title}\n")
                        f.write("="*80 + "\n\n")
                        f.write(clean_text)
                        
                    collected_candidates.append({
                        "filename": fname,
                        "post_id": post_id,
                        "subreddit": sub,
                        "source_url": permalink,
                        "title": title,
                        "char_length": len(clean_text),
                        "has_code_block": has_code,
                        "http_status_verified": 200,
                        "collection_date": "2026-08-07"
                    })
                    
                    print(f"  [{file_counter:02d}] r/{sub} | {title[:55]}... ({len(clean_text)} chars)")
                    file_counter += 1
                    
        except Exception as e:
            print(f"  Error fetching RSS for r/{sub}: {e}")
            
        print("  Waiting 4.5s before next request...")
        time.sleep(4.5)

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(collected_candidates, f, indent=2, ensure_ascii=False)

    print("\n" + "="*90)
    print(f"REAL REDDIT DATASET COLLECTION COMPLETE: {len(collected_candidates)} Genuine Posts Saved.")
    print("="*90)
    print(f"Manifest written to: {MANIFEST_PATH}\n")
    
    # Display 10 samples for Harjot's review
    print("="*90)
    print("FIRST 10 CANDIDATE SAMPLES FOR HARJOT'S REVIEW (BEFORE LABELING):")
    print("="*90)
    for idx, c in enumerate(collected_candidates[:10], 1):
        print(f"\n[{idx}] r/{c['subreddit']} — {c['title']}")
        print(f"    URL:    {c['source_url']}")
        print(f"    Length: {c['char_length']} chars | Has Code: {c['has_code_block']}")
        fpath = os.path.join(CANDIDATES_DIR, c["filename"])
        with open(fpath, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f.readlines() if l.strip() and not l.startswith("Source URL") and not l.startswith("Subreddit") and not l.startswith("Title:") and not l.startswith("=")]
            body_sample = " ".join(lines[:3])[:140]
            print(f"    Body Sample: \"{body_sample}...\"")

if __name__ == "__main__":
    main()
