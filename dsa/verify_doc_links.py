#!/usr/bin/env python3
import sys
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, '/home/dhruv/Desktop/dsa_new/dsa')
import curated_resources

def check_doc(day, res):
    doc = res.get('doc')
    if not doc:
        return (day, 'NONE', 'No doc link', '')
    url = doc.get('url', '')
    source = doc.get('source', '')
    title = doc.get('title', '')
    
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }
    )
    try:
        # Some servers return 403 to automated scripts (like Cloudflare / LeetCode / USENIX), but 200/301/302/403 means domain and path exist.
        # 404 means broken dead link.
        with urllib.request.urlopen(req, timeout=8) as response:
            return (day, 'VALID', f"[{source}] {title} (HTTP {response.status})", url)
    except urllib.error.HTTPError as e:
        if e.code in (403, 401, 429):
            # Anti-bot protection, URL is live
            return (day, 'LIVE_PROTECTED', f"[{source}] {title} (HTTP {e.code})", url)
        elif e.code == 404:
            return (day, 'DEAD_404', f"[{source}] {title} (HTTP 404)", url)
        else:
            return (day, 'HTTP_ERR', f"[{source}] {title} (HTTP {e.code})", url)
    except Exception as e:
        return (day, 'CONN_ERR', f"[{source}] {title} ({str(e)})", url)

def main():
    items = list(curated_resources.CURATED_RESOURCES.items())
    results = []
    with ThreadPoolExecutor(max_workers=25) as executor:
        futures = [executor.submit(check_doc, day, res) for day, res in items]
        for f in futures:
            results.append(f.result())
    
    results.sort(key=lambda x: x[0])
    
    valid = [r for r in results if r[1] in ('VALID', 'LIVE_PROTECTED')]
    dead = [r for r in results if r[1] == 'DEAD_404']
    none_ = [r for r in results if r[1] == 'NONE']
    other = [r for r in results if r[1] not in ('VALID', 'LIVE_PROTECTED', 'DEAD_404', 'NONE')]
    
    print(f"Total days: {len(results)}")
    print(f"Valid/Live docs: {len(valid)}")
    print(f"None (Diagnostic/Mock): {len(none_)}")
    print(f"Dead 404 docs: {len(dead)}")
    print(f"Other connection issues: {len(other)}")
    print("=" * 60)
    for d in dead:
        print(f"Day {d[0]:3d}: {d[2]} -> {d[3]}")
    for o in other:
        print(f"Day {o[0]:3d} [{o[1]}]: {o[2]} -> {o[3]}")

if __name__ == '__main__':
    main()
