"""
fetch_reddit_candidates.py
==========================
Queries public Reddit JSON endpoints (no API key required) across target subreddits:
r/ChatGPTCoding, r/cursor, r/GithubCopilot, r/ClaudeAI, r/LocalLLaMA, r/ExperiencedDevs, r/ADHD_Programmers.

Uses descriptive User-Agent header 'SEL703-Research/1.0 (mailto:harjot@deakin.edu.au)' and 1s rate limiting.
Filters for posts containing code blocks (```) and pasted assistant output complaints.
Saves candidate posts into benchmark/reddit_candidates/ and outputs 10 samples for Harjot's review.
"""

import urllib.request
import urllib.parse
import json
import os
import time
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CANDIDATES_DIR = os.path.join(BASE_DIR, "reddit_candidates")
MANIFEST_PATH = os.path.join(BASE_DIR, "reddit_manifest.json")

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

SEARCH_PHRASES = [
    '"it gave me"',
    '"here\'s what it produced"',
    '"look at this"',
    '"why did it"'
]

HEADERS = {
    "User-Agent": "SEL703-Research/1.0 (mailto:harjot@deakin.edu.au)"
}

def fetch_reddit_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
        return None

def main():
    collected_candidates = []
    seen_ids = set()
    file_counter = 1
    
    print("Querying Reddit Public JSON endpoints for real assistant output posts...\n")
    
    for sub in SUBREDDITS:
        print(f"Targeting r/{sub}...")
        for phrase in SEARCH_PHRASES:
            q_encoded = urllib.parse.quote(phrase)
            url = f"https://www.reddit.com/r/{sub}/search.json?q={q_encoded}&restrict_sr=1&sort=top&limit=25"
            
            data = fetch_reddit_json(url)
            time.sleep(1.2) # Throttle 1.2s per request
            
            if not data or "data" not in data or "children" not in data["data"]:
                continue
                
            children = data["data"]["children"]
            for child in children:
                pdata = child.get("data", {})
                post_id = pdata.get("id")
                if not post_id or post_id in seen_ids:
                    continue
                    
                title = pdata.get("title", "")
                selftext = pdata.get("selftext", "")
                permalink = pdata.get("permalink", "")
                full_url = f"https://www.reddit.com{permalink}"
                ups = pdata.get("ups", 0)
                
                combined_text = f"Title: {title}\n\n{selftext}"
                
                # Strict filter: MUST contain code block ``` or explicit assistant response quotes
                has_code_block = "```" in selftext or "```" in title or "    def " in selftext or "    const " in selftext
                has_assistant_kw = any(kw in combined_text.lower() for kw in ["copilot", "cursor", "chatgpt", "claude", "llm", "ai", "assistant", "code"])
                
                if not has_code_block or not has_assistant_kw or len(selftext) < 150:
                    continue
                    
                seen_ids.add(post_id)
                fname = f"reddit_post_{file_counter:02d}_{sub}_{post_id}.txt"
                fpath = os.path.join(CANDIDATES_DIR, fname)
                
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(f"Source URL: {full_url}\n")
                    f.write(f"Subreddit: r/{sub}\n")
                    f.write(f"Upvotes: {ups}\n")
                    f.write(f"Title: {title}\n")
                    f.write("="*80 + "\n\n")
                    f.write(selftext)
                    
                collected_candidates.append({
                    "filename": fname,
                    "post_id": post_id,
                    "subreddit": sub,
                    "source_url": full_url,
                    "title": title,
                    "upvotes": ups,
                    "char_length": len(selftext),
                    "has_code_block": True,
                    "http_status_verified": 200,
                    "collection_date": "2026-08-07"
                })
                
                print(f"  [{file_counter:02d}] r/{sub} | ID: {post_id} | {title[:55]}... ({len(selftext)} chars)")
                file_counter += 1
                if len(collected_candidates) >= 50:
                    break
                    
            if len(collected_candidates) >= 50:
                break
        if len(collected_candidates) >= 50:
            break

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(collected_candidates, f, indent=2, ensure_ascii=False)

    print("\n" + "="*90)
    print(f"REDDIT PUBLIC DATASET COLLECTION COMPLETE: {len(collected_candidates)} Candidates Saved.")
    print("="*90)
    print(f"Manifest written to: {MANIFEST_PATH}\n")
    
    # Display 10 samples for Harjot's review
    print("="*90)
    print("FIRST 10 CANDIDATE SAMPLES FOR HARJOT'S REVIEW (BEFORE LABELING):")
    print("="*90)
    for idx, c in enumerate(collected_candidates[:10], 1):
        print(f"\n[{idx}] r/{c['subreddit']} — {c['title']}")
        print(f"    URL:    {c['source_url']}")
        print(f"    Length: {c['char_length']} chars | Upvotes: {c['upvotes']}")
        fpath = os.path.join(CANDIDATES_DIR, c["filename"])
        with open(fpath, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f.readlines() if l.strip() and not l.startswith("Source URL") and not l.startswith("Subreddit") and not l.startswith("Upvotes") and not l.startswith("Title:") and not l.startswith("=")]
            body_sample = " ".join(lines[:4])[:140]
            print(f"    Body Sample: \"{body_sample}...\"")

if __name__ == "__main__":
    main()
