#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tutorial_data.py
Curated YouTube creators and direct video search queries for all 35 tutorials
in the 24-Week Silicon-Aware DSA & AI-Infrastructure program.
Channels:
  - Striver (take U forward)
  - Aditya Verma
  - Love Babbar (CodeHelp)
  - Padho with Pratyush
  - NeetCode
  - Specialized: Abdul Bari, WilliamFiset, Errichto, Martin Thompson, etc.
"""

import urllib.parse

TUTORIAL_CREATORS = {
    1: {
        "primary": "Striver",
        "query": "striver time complexity analysis",
        "channels": [
            {"name": "Striver", "query": "striver time complexity analysis", "cls": "striver"},
            {"name": "Aditya Verma", "query": "aditya verma time complexity", "cls": "aditya"},
            {"name": "Love Babbar", "query": "love babbar time and space complexity", "cls": "babbar"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush time complexity", "cls": "pratyush"},
            {"name": "NeetCode", "query": "neetcode big o notation", "cls": "neetcode"},
            {"name": "Abdul Bari", "query": "abdul bari algorithm analysis time complexity", "cls": "other"}
        ]
    },
    3: {
        "primary": "Striver",
        "query": "striver subarray sum equals k prefix sum",
        "channels": [
            {"name": "Striver", "query": "striver subarray sum equals k prefix sum", "cls": "striver"},
            {"name": "Aditya Verma", "query": "aditya verma prefix sum subarray", "cls": "aditya"},
            {"name": "Love Babbar", "query": "love babbar prefix sum subarray", "cls": "babbar"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush prefix sum", "cls": "pratyush"},
            {"name": "NeetCode", "query": "neetcode subarray sum equals k", "cls": "neetcode"}
        ]
    },
    8: {
        "primary": "Striver",
        "query": "striver two pointers 3sum",
        "channels": [
            {"name": "Striver", "query": "striver two pointers 3sum", "cls": "striver"},
            {"name": "Aditya Verma", "query": "aditya verma two pointer approach", "cls": "aditya"},
            {"name": "Love Babbar", "query": "love babbar two pointer approach", "cls": "babbar"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush two pointers", "cls": "pratyush"},
            {"name": "NeetCode", "query": "neetcode two pointers 3sum", "cls": "neetcode"}
        ]
    },
    10: {
        "primary": "Aditya Verma",
        "query": "aditya verma sliding window playlist",
        "channels": [
            {"name": "Aditya Verma", "query": "aditya verma sliding window playlist", "cls": "aditya"},
            {"name": "Striver", "query": "striver sliding window playlist", "cls": "striver"},
            {"name": "Love Babbar", "query": "love babbar sliding window", "cls": "babbar"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush sliding window", "cls": "pratyush"},
            {"name": "NeetCode", "query": "neetcode sliding window", "cls": "neetcode"}
        ]
    },
    15: {
        "primary": "Aditya Verma",
        "query": "aditya verma binary search playlist",
        "channels": [
            {"name": "Aditya Verma", "query": "aditya verma binary search playlist", "cls": "aditya"},
            {"name": "Striver", "query": "striver binary search playlist", "cls": "striver"},
            {"name": "Love Babbar", "query": "love babbar binary search", "cls": "babbar"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush binary search", "cls": "pratyush"},
            {"name": "NeetCode", "query": "neetcode binary search", "cls": "neetcode"}
        ]
    },
    17: {
        "primary": "Striver",
        "query": "striver binary search on answers koko eating bananas",
        "channels": [
            {"name": "Striver", "query": "striver binary search on answers koko eating bananas", "cls": "striver"},
            {"name": "Aditya Verma", "query": "aditya verma allocate minimum number of pages binary search", "cls": "aditya"},
            {"name": "Love Babbar", "query": "love babbar book allocation painter partition binary search", "cls": "babbar"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush binary search on answers", "cls": "pratyush"},
            {"name": "NeetCode", "query": "neetcode koko eating bananas", "cls": "neetcode"}
        ]
    },
    23: {
        "primary": "Striver",
        "query": "striver meeting rooms merge intervals",
        "channels": [
            {"name": "Striver", "query": "striver meeting rooms merge intervals", "cls": "striver"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush line sweep intervals", "cls": "pratyush"},
            {"name": "Aditya Verma", "query": "aditya verma interval merge", "cls": "aditya"},
            {"name": "Love Babbar", "query": "love babbar merge intervals", "cls": "babbar"},
            {"name": "NeetCode", "query": "neetcode meeting rooms insert interval", "cls": "neetcode"}
        ]
    },
    24: {
        "primary": "Aditya Verma",
        "query": "aditya verma stack playlist nearest greater to right",
        "channels": [
            {"name": "Aditya Verma", "query": "aditya verma stack playlist nearest greater to right", "cls": "aditya"},
            {"name": "Striver", "query": "striver next greater element monotonic stack", "cls": "striver"},
            {"name": "Love Babbar", "query": "love babbar largest rectangle in histogram stack", "cls": "babbar"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush monotonic stack", "cls": "pratyush"},
            {"name": "NeetCode", "query": "neetcode daily temperatures monotonic stack", "cls": "neetcode"}
        ]
    },
    29: {
        "primary": "Aditya Verma",
        "query": "aditya verma heap playlist kth smallest element",
        "channels": [
            {"name": "Aditya Verma", "query": "aditya verma heap playlist kth smallest element", "cls": "aditya"},
            {"name": "Striver", "query": "striver heaps priority queue playlist", "cls": "striver"},
            {"name": "Love Babbar", "query": "love babbar heap data structure heapify", "cls": "babbar"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush heap priority queue", "cls": "pratyush"},
            {"name": "Abdul Bari", "query": "abdul bari heap sort heapify", "cls": "other"}
        ]
    },
    32: {
        "primary": "Striver",
        "query": "striver greedy algorithms playlist",
        "channels": [
            {"name": "Striver", "query": "striver greedy algorithms playlist", "cls": "striver"},
            {"name": "Aditya Verma", "query": "aditya verma greedy algorithms", "cls": "aditya"},
            {"name": "Love Babbar", "query": "love babbar greedy algorithm", "cls": "babbar"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush greedy exchange argument", "cls": "pratyush"},
            {"name": "Abdul Bari", "query": "abdul bari greedy method knapsack", "cls": "other"},
            {"name": "NeetCode", "query": "neetcode jump game gas station", "cls": "neetcode"}
        ]
    },
    37: {
        "primary": "Striver",
        "query": "striver lru cache implementation",
        "channels": [
            {"name": "Striver", "query": "striver lru cache implementation", "cls": "striver"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush lru cache", "cls": "pratyush"},
            {"name": "Love Babbar", "query": "love babbar lru cache", "cls": "babbar"},
            {"name": "Aditya Verma", "query": "aditya verma lru cache", "cls": "aditya"},
            {"name": "NeetCode", "query": "neetcode lru cache", "cls": "neetcode"}
        ]
    },
    39: {
        "primary": "Striver",
        "query": "striver bit manipulation playlist",
        "channels": [
            {"name": "Striver", "query": "striver bit manipulation playlist", "cls": "striver"},
            {"name": "Love Babbar", "query": "love babbar bitwise operators", "cls": "babbar"},
            {"name": "Aditya Verma", "query": "aditya verma bit manipulation", "cls": "aditya"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush bitmask", "cls": "pratyush"},
            {"name": "NeetCode", "query": "neetcode bit manipulation", "cls": "neetcode"}
        ]
    },
    43: {
        "primary": "Striver",
        "query": "striver binary tree series playlist",
        "channels": [
            {"name": "Striver", "query": "striver binary tree series playlist", "cls": "striver"},
            {"name": "Aditya Verma", "query": "aditya verma recursion playlist", "cls": "aditya"},
            {"name": "Love Babbar", "query": "love babbar binary tree recursion", "cls": "babbar"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush binary tree", "cls": "pratyush"},
            {"name": "NeetCode", "query": "neetcode binary tree maximum path sum", "cls": "neetcode"}
        ]
    },
    50: {
        "primary": "Striver",
        "query": "striver trie series playlist",
        "channels": [
            {"name": "Striver", "query": "striver trie series playlist", "cls": "striver"},
            {"name": "Love Babbar", "query": "love babbar trie implementation", "cls": "babbar"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush trie", "cls": "pratyush"},
            {"name": "Aditya Verma", "query": "aditya verma trie", "cls": "aditya"},
            {"name": "NeetCode", "query": "neetcode implement trie", "cls": "neetcode"}
        ]
    },
    57: {
        "primary": "Striver",
        "query": "striver graph series bfs dfs",
        "channels": [
            {"name": "Striver", "query": "striver graph series bfs dfs", "cls": "striver"},
            {"name": "Love Babbar", "query": "love babbar graph series bfs dfs", "cls": "babbar"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush graph", "cls": "pratyush"},
            {"name": "Aditya Verma", "query": "aditya verma graph bfs dfs", "cls": "aditya"},
            {"name": "WilliamFiset", "query": "williamfiset graph theory", "cls": "other"}
        ]
    },
    59: {
        "primary": "Striver",
        "query": "striver disjoint set union find",
        "channels": [
            {"name": "Striver", "query": "striver disjoint set union find", "cls": "striver"},
            {"name": "Love Babbar", "query": "love babbar kruskal disjoint set", "cls": "babbar"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush dsu", "cls": "pratyush"},
            {"name": "WilliamFiset", "query": "williamfiset disjoint set union find", "cls": "other"},
            {"name": "NeetCode", "query": "neetcode redundant connection union find", "cls": "neetcode"}
        ]
    },
    61: {
        "primary": "Striver",
        "query": "striver topological sort kahns algorithm",
        "channels": [
            {"name": "Striver", "query": "striver topological sort kahns algorithm", "cls": "striver"},
            {"name": "Love Babbar", "query": "love babbar topological sort kahn", "cls": "babbar"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush topological sort", "cls": "pratyush"},
            {"name": "Aditya Verma", "query": "aditya verma topological sort", "cls": "aditya"},
            {"name": "NeetCode", "query": "neetcode course schedule topological sort", "cls": "neetcode"}
        ]
    },
    65: {
        "primary": "Striver",
        "query": "striver word ladder bfs shortest path",
        "channels": [
            {"name": "Striver", "query": "striver word ladder bfs shortest path", "cls": "striver"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush state space search bfs", "cls": "pratyush"},
            {"name": "Love Babbar", "query": "love babbar word ladder shortest path bfs", "cls": "babbar"},
            {"name": "Aditya Verma", "query": "aditya verma bfs shortest path", "cls": "aditya"},
            {"name": "NeetCode", "query": "neetcode word ladder", "cls": "neetcode"}
        ]
    },
    66: {
        "primary": "Striver",
        "query": "striver dijkstra algorithm priority queue",
        "channels": [
            {"name": "Striver", "query": "striver dijkstra algorithm priority queue", "cls": "striver"},
            {"name": "Love Babbar", "query": "love babbar dijkstra shortest path", "cls": "babbar"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush dijkstra", "cls": "pratyush"},
            {"name": "Abdul Bari", "query": "abdul bari dijkstra algorithm", "cls": "other"},
            {"name": "WilliamFiset", "query": "williamfiset dijkstras shortest path", "cls": "other"}
        ]
    },
    71: {
        "primary": "Aditya Verma",
        "query": "aditya verma backtracking playlist",
        "channels": [
            {"name": "Aditya Verma", "query": "aditya verma backtracking playlist", "cls": "aditya"},
            {"name": "Striver", "query": "striver backtracking n queens subsets", "cls": "striver"},
            {"name": "Love Babbar", "query": "love babbar backtracking rat in a maze", "cls": "babbar"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush backtracking", "cls": "pratyush"},
            {"name": "NeetCode", "query": "neetcode subsets backtracking", "cls": "neetcode"}
        ]
    },
    76: {
        "primary": "Aditya Verma",
        "query": "aditya verma dynamic programming playlist intro memoization",
        "channels": [
            {"name": "Aditya Verma", "query": "aditya verma dp playlist memoization", "cls": "aditya"},
            {"name": "Striver", "query": "striver dp series introduction memoization", "cls": "striver"},
            {"name": "Love Babbar", "query": "love babbar dp playlist memoization", "cls": "babbar"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush dynamic programming", "cls": "pratyush"},
            {"name": "Abdul Bari", "query": "abdul bari dynamic programming", "cls": "other"}
        ]
    },
    78: {
        "primary": "Aditya Verma",
        "query": "aditya verma dp playlist",
        "channels": [
            {"name": "Aditya Verma", "query": "aditya verma dp playlist", "cls": "aditya"},
            {"name": "Striver", "query": "striver dp series playlist", "cls": "striver"},
            {"name": "Love Babbar", "query": "love babbar dynamic programming", "cls": "babbar"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush dp space optimization", "cls": "pratyush"},
            {"name": "Abdul Bari", "query": "abdul bari dynamic programming", "cls": "other"}
        ]
    },
    80: {
        "primary": "Aditya Verma",
        "query": "aditya verma 01 knapsack playlist",
        "channels": [
            {"name": "Aditya Verma", "query": "aditya verma 01 knapsack playlist", "cls": "aditya"},
            {"name": "Striver", "query": "striver 01 knapsack subset sum", "cls": "striver"},
            {"name": "Love Babbar", "query": "love babbar knapsack problem", "cls": "babbar"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush knapsack", "cls": "pratyush"},
            {"name": "NeetCode", "query": "neetcode coin change knapsack", "cls": "neetcode"}
        ]
    },
    85: {
        "primary": "Aditya Verma",
        "query": "aditya verma matrix chain multiplication mcm playlist",
        "channels": [
            {"name": "Aditya Verma", "query": "aditya verma matrix chain multiplication mcm playlist", "cls": "aditya"},
            {"name": "Striver", "query": "striver matrix chain multiplication burst balloons", "cls": "striver"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush interval dp", "cls": "pratyush"},
            {"name": "Love Babbar", "query": "love babbar matrix chain multiplication", "cls": "babbar"},
            {"name": "NeetCode", "query": "neetcode burst balloons", "cls": "neetcode"}
        ]
    },
    87: {
        "primary": "Striver",
        "query": "striver bitmask dp",
        "channels": [
            {"name": "Striver", "query": "striver bitmask dp", "cls": "striver"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush bitmask dp", "cls": "pratyush"},
            {"name": "Aditya Verma", "query": "aditya verma bitmask dp", "cls": "aditya"},
            {"name": "Love Babbar", "query": "love babbar bitmasking", "cls": "babbar"},
            {"name": "Errichto", "query": "errichto bitmask dynamic programming", "cls": "other"}
        ]
    },
    99: {
        "primary": "Striver",
        "query": "striver fenwick tree binary indexed tree",
        "channels": [
            {"name": "Striver", "query": "striver fenwick tree binary indexed tree", "cls": "striver"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush fenwick tree", "cls": "pratyush"},
            {"name": "Love Babbar", "query": "love babbar binary indexed tree fenwick", "cls": "babbar"},
            {"name": "WilliamFiset", "query": "williamfiset fenwick tree binary indexed tree", "cls": "other"},
            {"name": "Errichto", "query": "errichto fenwick tree", "cls": "other"}
        ]
    },
    100: {
        "primary": "Striver",
        "query": "striver segment tree playlist",
        "channels": [
            {"name": "Striver", "query": "striver segment tree playlist", "cls": "striver"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush segment tree", "cls": "pratyush"},
            {"name": "Love Babbar", "query": "love babbar segment tree", "cls": "babbar"},
            {"name": "WilliamFiset", "query": "williamfiset segment tree", "cls": "other"},
            {"name": "Errichto", "query": "errichto segment trees", "cls": "other"}
        ]
    },
    101: {
        "primary": "Striver",
        "query": "striver lazy propagation segment tree",
        "channels": [
            {"name": "Striver", "query": "striver lazy propagation segment tree", "cls": "striver"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush segment tree lazy propagation", "cls": "pratyush"},
            {"name": "Love Babbar", "query": "love babbar segment tree lazy propagation", "cls": "babbar"},
            {"name": "WilliamFiset", "query": "williamfiset segment tree lazy propagation", "cls": "other"},
            {"name": "Errichto", "query": "errichto lazy propagation", "cls": "other"}
        ]
    },
    106: {
        "primary": "Striver",
        "query": "striver bridges in graph tarjans algorithm",
        "channels": [
            {"name": "Striver", "query": "striver bridges in graph tarjans algorithm", "cls": "striver"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush tarjan bridges", "cls": "pratyush"},
            {"name": "Love Babbar", "query": "love babbar bridges in a graph", "cls": "babbar"},
            {"name": "WilliamFiset", "query": "williamfiset bridges and articulation points", "cls": "other"},
            {"name": "Abdul Bari", "query": "abdul bari tarjan strongly connected components", "cls": "other"}
        ]
    },
    109: {
        "primary": "WilliamFiset",
        "query": "williamfiset dinics algorithm max flow",
        "channels": [
            {"name": "WilliamFiset", "query": "williamfiset dinics algorithm max flow", "cls": "other"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush max flow", "cls": "pratyush"},
            {"name": "Striver", "query": "striver max flow dinic", "cls": "striver"},
            {"name": "Love Babbar", "query": "love babbar max flow", "cls": "babbar"},
            {"name": "Abdul Bari", "query": "abdul bari ford fulkerson max flow", "cls": "other"}
        ]
    },
    120: {
        "primary": "Abdul Bari",
        "query": "abdul bari kmp algorithm string matching",
        "channels": [
            {"name": "Abdul Bari", "query": "abdul bari kmp algorithm string matching", "cls": "other"},
            {"name": "Striver", "query": "striver kmp string matching algorithm", "cls": "striver"},
            {"name": "Love Babbar", "query": "love babbar kmp string matching", "cls": "babbar"},
            {"name": "Aditya Verma", "query": "aditya verma string algorithms", "cls": "aditya"},
            {"name": "Padho with Pratyush", "query": "padho with pratyush kmp", "cls": "pratyush"},
            {"name": "NeetCode", "query": "neetcode kmp algorithm", "cls": "neetcode"}
        ]
    },
    127: {
        "primary": "Padho with Pratyush",
        "query": "padho with pratyush lru arc cache buffer pool",
        "channels": [
            {"name": "Padho with Pratyush", "query": "padho with pratyush lru arc cache buffer pool", "cls": "pratyush"},
            {"name": "Striver", "query": "striver lru cache lfu cache design", "cls": "striver"},
            {"name": "Love Babbar", "query": "love babbar lru cache design", "cls": "babbar"},
            {"name": "CMU Database Group", "query": "cmu database buffer pool replacement arc", "cls": "other"},
            {"name": "NeetCode", "query": "neetcode lru lfu cache", "cls": "neetcode"}
        ]
    },
    134: {
        "primary": "Padho with Pratyush",
        "query": "padho with pratyush lock free queue ring buffer",
        "channels": [
            {"name": "Padho with Pratyush", "query": "padho with pratyush lock free queue ring buffer", "cls": "pratyush"},
            {"name": "Love Babbar", "query": "love babbar queue operating systems concurrency", "cls": "babbar"},
            {"name": "CppCon", "query": "cppcon lock free ring buffer spsc", "cls": "other"},
            {"name": "Martin Thompson", "query": "martin thompson mechanical sympathy lock free queue", "cls": "other"},
            {"name": "NeetCode", "query": "neetcode design bounded blocking queue", "cls": "neetcode"}
        ]
    },
    143: {
        "primary": "Padho with Pratyush",
        "query": "padho with pratyush hnsw vector search",
        "channels": [
            {"name": "Padho with Pratyush", "query": "padho with pratyush hnsw vector search", "cls": "pratyush"},
            {"name": "Pinecone", "query": "pinecone hnsw algorithm vector search", "cls": "other"},
            {"name": "James Briggs", "query": "james briggs hierarchical navigable small world hnsw", "cls": "other"},
            {"name": "Striver", "query": "striver k nearest neighbors graph", "cls": "striver"},
            {"name": "NeetCode", "query": "neetcode vector embeddings search", "cls": "neetcode"}
        ]
    },
    148: {
        "primary": "Padho with Pratyush",
        "query": "padho with pratyush dag scheduling critical path",
        "channels": [
            {"name": "Padho with Pratyush", "query": "padho with pratyush dag scheduling critical path", "cls": "pratyush"},
            {"name": "Abdul Bari", "query": "abdul bari critical path method dag", "cls": "other"},
            {"name": "Striver", "query": "striver topological sort dag scheduling", "cls": "striver"},
            {"name": "Love Babbar", "query": "love babbar dag topological sort", "cls": "babbar"},
            {"name": "MIT OpenCourseWare", "query": "mit 6.172 dag scheduling critical path", "cls": "other"}
        ]
    }
}

def get_tutorial_resource(day_num, topic):
    creator_info = TUTORIAL_CREATORS.get(day_num, {
        "primary": "Striver",
        "query": f"striver {topic}",
        "channels": [
            {"name": "Striver", "query": f"striver {topic}", "cls": "striver"},
            {"name": "Aditya Verma", "query": f"aditya verma {topic}", "cls": "aditya"},
            {"name": "Love Babbar", "query": f"love babbar {topic}", "cls": "babbar"},
            {"name": "Padho with Pratyush", "query": f"padho with pratyush {topic}", "cls": "pratyush"},
            {"name": "NeetCode", "query": f"neetcode {topic}", "cls": "neetcode"}
        ]
    })
    primary_yt_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(creator_info['query'])}"
    channel_links = []
    for ch in creator_info["channels"]:
        ch_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(ch['query'])}"
        channel_links.append({
            "name": ch["name"],
            "url": ch_url,
            "cls": ch.get("cls", "other"),
            "query": ch["query"]
        })
    return {
        "primary": creator_info["primary"],
        "primaryChannel": creator_info["primary"],
        "primary_url": primary_yt_url,
        "primaryUrl": primary_yt_url,
        "channels": channel_links,
        "query": creator_info["query"]
    }
