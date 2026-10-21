#!/usr/bin/env python3
import sys
import os
import urllib.request
import urllib.parse
import json
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, '/home/dhruv/Desktop/dsa_new/dsa')
import curated_resources

def check_yt(day, res):
    yt = res.get('yt')
    if not yt:
        return (day, 'NONE', 'No YT link', '')
    url = yt.get('url', '')
    creator = yt.get('creator', '')
    title = yt.get('title', '')
    
    if 'results?search_query=' in url:
        return (day, 'SEARCH', f'[{creator}] {title}', url)
    if 'playlist?list=' in url:
        # Check playlist if possible or mark playlist
        return (day, 'PLAYLIST', f'[{creator}] {title}', url)
    
    if 'watch?v=' in url or 'youtu.be/' in url:
        oembed = f'https://www.youtube.com/oembed?url={urllib.parse.quote(url)}&format=json'
        req = urllib.request.Request(oembed, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        try:
            with urllib.request.urlopen(req, timeout=6) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    return (day, 'VALID', f"[{creator}] Real Title: {data.get('title')}", url)
                else:
                    return (day, 'BROKEN', f"[{creator}] {title} (HTTP {response.status})", url)
        except urllib.error.HTTPError as e:
            return (day, 'BROKEN', f"[{creator}] {title} (HTTP {e.code})", url)
        except Exception as e:
            return (day, 'BROKEN', f"[{creator}] {title} ({str(e)})", url)
    
    return (day, 'UNKNOWN', f"[{creator}] {title}", url)

def main():
    items = list(curated_resources.CURATED_RESOURCES.items())
    results = []
    with ThreadPoolExecutor(max_workers=25) as executor:
        futures = [executor.submit(check_yt, day, res) for day, res in items]
        for f in futures:
            results.append(f.result())
    
    results.sort(key=lambda x: x[0])
    
    valid = [r for r in results if r[1] == 'VALID']
    broken = [r for r in results if r[1] == 'BROKEN']
    search = [r for r in results if r[1] == 'SEARCH']
    playlist = [r for r in results if r[1] == 'PLAYLIST']
    none_ = [r for r in results if r[1] == 'NONE']
    
    print(f"Total: {len(results)}")
    print(f"VALID: {len(valid)}")
    print(f"PLAYLIST: {len(playlist)}")
    print(f"SEARCH: {len(search)}")
    print(f"NONE: {len(none_)}")
    print(f"BROKEN (Unavailable): {len(broken)}")
    print("=" * 60)
    for b in broken:
        print(f"Day {b[0]:3d}: {b[2]} -> {b[3]}")

if __name__ == '__main__':
    main()
