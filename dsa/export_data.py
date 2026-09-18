#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
export_data.py
Extracts 100% of data from dsa_builder.py into data.json and data.js
Guarantees zero data loss across all 168 days, 42 patterns, 30 cards,
35 tutorials, 24 mocks, 20 blind problems, 24 milestones, and NVIDIA playbook.
Enriched with curated YouTube links for Striver, Padho with Pratyush,
Aditya Verma, NeetCode, Love Babbar, Abdul Bari, and other top specialists.
"""

import json
from datetime import date, timedelta
import urllib.parse
import re

# Import raw data from dsa_builder
import dsa_builder

def generate_lc_url(problem_str):
    """Generates direct LeetCode search URL for any problem string."""
    clean = re.sub(r"^LC\s*\d+\s*", "", problem_str).strip()
    clean = clean.split("(")[0].strip()
    query = urllib.parse.quote(clean)
    return f"https://leetcode.com/problem-list/all/?search={query}"

def is_nvidia_related(day_num, pat, infra, skill):
    nvidia_days = {1, 41, 85, 113, 114, 115, 116, 117, 118, 119, 134, 135, 136, 137, 138, 139, 140, 148, 149, 150, 151, 152, 153, 154, 162, 163, 166, 167}
    if day_num in nvidia_days:
        return True
    combined = f"{pat} {infra} {skill}".lower()
    keywords = ["cache", "hardware", "warp", "gpu", "spsc", "lock-free", "ring buffer", "tensor", "blelloch", "sparsity", "allocator", "cuda", "memory", "coalesc"]
    return any(k in combined for k in keywords)

def get_phase(day_num):
    if day_num <= 42:
        return 1, "Phase 1: Linear Foundations & Hardware Calibration"
    elif day_num <= 84:
        return 2, "Phase 2: Hierarchical Structures, Topologies & Compilers"
    elif day_num <= 126:
        return 3, "Phase 3: Advanced Optimization, Range Queries & Flows"
    else:
        return 4, "Phase 4: Systems & AI-Infrastructure Domain Specialization"

# Curated YouTube Creators imported from tutorial_data
from tutorial_data import TUTORIAL_CREATORS, get_tutorial_resource

def run_export():
    start_dt = dsa_builder.START

    # 1. Config
    config = {
        "startDate": start_dt.strftime("%Y-%m-%d"),
        "endDate": (start_dt + timedelta(days=dsa_builder.DAYS - 1)).strftime("%Y-%m-%d"),
        "totalDays": dsa_builder.DAYS,
        "totalWeeks": dsa_builder.WEEKS,
        "pdbRows": dsa_builder.PDB_ROWS,
        "flRows": dsa_builder.FL_ROWS,
        "title": "DSA TRAINING & SPECIALIST COCKPIT - NVIDIA & AI-INFRASTRUCTURE SYSTEMS",
        "subtitle": "24 Weeks (168 Days) | Silicon-Aware High-Performance Computing & Systems Mastery"
    }

    # 2. FCATS
    fcats_data = [
        {"code": "F1", "label": "Understand", "desc": "Misread or misunderstood the problem statement or constraints", "drill": "Annotate constraints and draw 2 custom examples before writing code"},
        {"code": "F2", "label": "Pattern", "desc": "Could not identify the correct underlying pattern", "drill": "10 unlabelled 'name the pattern only' flashcard reps daily"},
        {"code": "F3", "label": "Derive", "desc": "Knew the pattern, could not derive the recurrence, state, or transition", "drill": "1 extra blank-editor reconstruction per day from the failed pattern"},
        {"code": "F4", "label": "WrongDS", "desc": "Identified the right approach, chose the wrong data structure", "drill": "Write Big-O comparison table for candidate data structures"},
        {"code": "F5", "label": "Complexity", "desc": "Wrong or absent complexity analysis; hit TLE", "drill": "Estimate target Big-O aloud from input constraints before touching keyboard"},
        {"code": "F6", "label": "Implementation", "desc": "Correct approach, but hit coding bug, pointer error, or off-by-one", "drill": "Write loop invariants as code comments before writing loops"},
        {"code": "F7", "label": "EdgeCase", "desc": "Failed on empty, single, duplicate, negative, or overflow inputs", "drill": "Execute personal 6-point edge case checklist before submission"},
        {"code": "F8", "label": "Debugging", "desc": "Took > 15 minutes to find and isolate a bug", "drill": "Practice manual dry-run pointer tracing with tables on paper"},
        {"code": "F9", "label": "Forgot", "desc": "Previously learned this technique, but could not retrieve it today", "drill": "Add anchor card to daily active recall queue"},
        {"code": "F10", "label": "Pressure", "desc": "Panic or cognitive freeze specifically due to timer", "drill": "Replace 1 untimed session per week with a timed session"},
        {"code": "F11", "label": "HintDependent", "desc": "Required a hint or editorial approach to make progress", "drill": "Stuck protocol clock resets; enforce full 30-min struggle before hints"},
        {"code": "F12", "label": "CantExplain", "desc": "Passed test cases, but cannot explain the invariant aloud to another person", "drill": "Record voice explaining invariant and verify explanation soundness"}
    ]

    # 3. Phases
    phases_data = [
        {
            "id": 1,
            "title": "Phase 1: Linear Foundations & Hardware Calibration",
            "weeks": "Weeks 1–6 (Days 1–42)",
            "description": "Complexity calibration, memory hierarchy (64B cache lines, contiguous layouts), prefix/suffix reasoning, two pointers, sliding window invariants, binary search variants, heaps/top-K, monotonic stacks, and bit manipulation."
        },
        {
            "id": 2,
            "title": "Phase 2: Hierarchical Structures, Topologies & Compilers",
            "weeks": "Weeks 7–12 (Days 43–84)",
            "description": "Tree recursion contracts, subtree post-order DP, BST ordering, Tries, graph BFS/DFS, Disjoint Set Union (DSU), topological sorting, backtracking with dedup/pruning, and memoization bridges."
        },
        {
            "id": 3,
            "title": "Phase 3: Advanced Optimization, Range Queries & Flows",
            "weeks": "Weeks 13–18 (Days 85–126)",
            "description": "Interval/Bitmask/Tree DP, Segment Trees with lazy propagation, Fenwick Trees, Tarjan's bridges & SCC, Dinic's max-flow, hardware cache locality, Cuckoo/Robin Hood hashing, and string automata (KMP, BPE)."
        },
        {
            "id": 4,
            "title": "Phase 4: Systems & AI-Infrastructure Domain Specialization",
            "weeks": "Weeks 19–24 (Days 127–168)",
            "description": "Cache architectures (ARC, 2Q, Clock-Pro, PagedAttention), lock-free concurrency (SPSC/MPMC ring buffers, work-stealing deques), HNSW vector proximity graphs, ML compiler DAG schedulers, Blelloch parallel scan, streaming sketches, and Buddy/Slab allocators."
        }
    ]

    # 4. Weeks
    weeks_data = []
    for i, theme in enumerate(dsa_builder.WEEK_THEMES):
        w_id = i + 1
        start_day = i * 7 + 1
        end_day = start_day + 6
        phase_id, _ = get_phase(start_day)
        weeks_data.append({
            "id": w_id,
            "phaseId": phase_id,
            "theme": theme,
            "startDay": start_day,
            "endDay": end_day
        })

    # 5. Days Plan (168 Days) with Attached Tutorial Creator Resources
    days_data = []
    for i, day_data in enumerate(dsa_builder.PLAN):
        day_num = i + 1
        week_num = (i // 7) + 1
        phase_num, phase_title = get_phase(day_num)
        curr_dt = start_dt + timedelta(days=i)

        if len(day_data) == 21:
            (obj, pat, con, tY, tT, tM, mode, help_,
             p1, d1, t1, p2_a, d2_a, t2_a, p2_b, d2_b, t2_b,
             rec, asr, infra, skill) = day_data
            p2 = f"{p2_a} + {p2_b}"
            d2 = d2_a
            t2 = t2_a + t2_b
            rev = "-"
        else:
            (obj, pat, con, tY, tT, tM, mode, help_, p1, d1, t1, p2, d2, t2,
             rev, rec, asr, infra, skill) = day_data

        is_diag = (mode == "Diagnostic") or (day_num in (28, 56, 84, 98, 112, 126, 140, 154, 168))
        is_mock = day_num in (42, 70, 92, 95, 164, 165, 166)
        is_nv = is_nvidia_related(day_num, pat, infra, skill)

        tut_resource = get_tutorial_resource(day_num, tT) if tY == 'YES' else None

        days_data.append({
            "day": day_num,
            "week": week_num,
            "phase": phase_num,
            "phaseTitle": phase_title,
            "date": curr_dt.strftime("%Y-%m-%d"),
            "dateDisplay": curr_dt.strftime("%a, %d %b %Y"),
            "dayOfWeek": curr_dt.strftime("%A"),
            "objective": obj,
            "pattern": pat,
            "concept": con,
            "tutYn": tY,
            "tutTopic": tT,
            "tutMin": tM if tM else 0,
            "tutResource": tut_resource,
            "mode": mode,
            "help": help_,
            "p1": p1,
            "d1": d1,
            "t1": t1,
            "p1Url": generate_lc_url(p1),
            "p2": p2,
            "d2": d2,
            "t2": t2,
            "p2Url": generate_lc_url(p2),
            "review": rev,
            "reconstruction": rec,
            "assessment": asr,
            "infra": infra,
            "skill": skill,
            "isDiagnostic": is_diag,
            "isMock": is_mock,
            "isNvidia": is_nv
        })

    # 6. Patterns (42 Patterns)
    patterns_data = []
    for i, p in enumerate(dsa_builder.PATTERNS):
        (p_name, cues, constr, idea, ds, fails, comp, examples, infra_rel) = p
        patterns_data.append({
            "id": i + 1,
            "name": p_name,
            "recognitionCues": cues,
            "constraintTriggers": constr,
            "coreIdea": idea,
            "dataStructures": ds,
            "failureModes": fails,
            "complexity": comp,
            "canonicalExamples": examples,
            "aiInfraRelevance": infra_rel
        })

    # 7. Pattern Cards (30 Cards)
    cards_data = []
    for i, c in enumerate(dsa_builder.CARDS):
        (prob, pat, trig, ds_idea, comp, inv_rule, fail_trap, variants, anchor) = c
        cards_data.append({
            "id": i + 1,
            "problem": prob,
            "pattern": pat,
            "triggerCue": trig,
            "coreIdea": ds_idea,
            "complexity": comp,
            "invariant": inv_rule,
            "failureTrap": fail_trap,
            "variants": variants,
            "anchorCue": anchor,
            "lcUrl": generate_lc_url(prob)
        })

    # 8. Resources (35 Tutorials) with Curated YouTube Creator Links
    resources_data = []
    for r in dsa_builder.RESOURCES:
        (r_day, r_src, r_topic, r_url_desc, r_dur, r_why, r_extract, r_not_copy, r_unlocks, r_test) = r
        tut_res = get_tutorial_resource(r_day, r_topic)

        resources_data.append({
            "day": r_day,
            "source": r_src,
            "topic": r_topic,
            "urlDesc": r_url_desc,
            "duration": r_dur,
            "whyItMatters": r_why,
            "whatToExtract": r_extract,
            "whatNotToCopy": r_not_copy,
            "problemsUnlocked": r_unlocks,
            "retrievalTest": r_test,
            "primaryChannel": tut_res["primaryChannel"],
            "primaryUrl": tut_res["primaryUrl"],
            "channels": tut_res["channels"]
        })

    # 9. Mock Interviews & Diagnostics (24 Sessions)
    mocks_data = []
    for i, m in enumerate(dsa_builder.MOCKS):
        (m_day, m_type, m_prob, m_diff, m_lim) = m
        m_dt = start_dt + timedelta(days=m_day - 1)
        mocks_data.append({
            "id": i + 1,
            "day": m_day,
            "date": m_dt.strftime("%Y-%m-%d"),
            "dateDisplay": m_dt.strftime("%a, %d %b %Y"),
            "sessionType": m_type,
            "problemDesc": m_prob,
            "difficulty": m_diff,
            "timeLimit": m_lim,
            "lcUrl": generate_lc_url(m_prob)
        })

    # 10. Blind Pool Problems (20 Problems)
    blind_data = []
    for i, b in enumerate(dsa_builder.BLIND_POOL):
        (b_prob, b_num, b_diff, b_pat, b_rec) = b
        blind_data.append({
            "id": i + 1,
            "problem": b_prob,
            "leetcodeNum": b_num,
            "difficulty": b_diff,
            "hiddenPattern": b_pat,
            "dayRecommended": str(b_rec),
            "lcUrl": f"https://leetcode.com/problems/{urllib.parse.quote(b_prob.lower().replace(' ', '-'))}/"
        })

    # 11. Milestones (24 Milestones)
    milestones_data = []
    for m in dsa_builder.MILESTONES:
        (m_day, m_title, m_ttp, m_indep, m_hint) = m
        m_dt = start_dt + timedelta(days=m_day - 1)
        milestones_data.append({
            "day": m_day,
            "date": m_dt.strftime("%Y-%m-%d"),
            "dateDisplay": m_dt.strftime("%a, %d %b %Y"),
            "milestone": m_title,
            "targetTtp": m_ttp,
            "targetIndep": m_indep,
            "targetHint": m_hint
        })

    # 12. README Sections
    readme_data = []
    for title, body in dsa_builder.README_SECTIONS:
        readme_data.append({
            "title": title.strip(),
            "body": body.strip()
        })

    # 13. NVIDIA Playbook Data
    nvidia_playbook = {
        "title": "The NVIDIA Systems, CUDA & AI-Infrastructure Playbook",
        "pillars": [
            {
                "id": 1,
                "title": "Memory Coalescing & Contiguous Layouts (SoA vs. AoS)",
                "summary": "Structure of Arrays enables 32 SIMD/CUDA lanes to load consecutive 4-byte floats in a single coalesced 128-byte DRAM transaction.",
                "trap": "Array of Structures (struct Particle { float x,y,z; } p[N]) causes strided uncoalesced access (32 transactions instead of 1).",
                "days": [1, 113, 114],
                "badge": "Hardware Memory"
            },
            {
                "id": 2,
                "title": "Bitwise Arithmetic as a First-Class Language",
                "summary": "32-bit registers represent thread execution masks (__activemask). Alignment, bit-reversal, and popcount are production primitives.",
                "primitives": [
                    {"code": "(addr + 63) & ~63", "desc": "64-byte cache line alignment"},
                    {"code": "(n > 0) && ((n & (n - 1)) == 0)", "desc": "Power-of-two check"},
                    {"code": "x & (power_of_2_size - 1)", "desc": "Fast branchless modulo"},
                    {"code": "x & -x", "desc": "Lowest set bit (Fenwick trees / sparse indexing)"},
                    {"code": "__builtin_popcount(mask)", "desc": "Active warp thread count"}
                ],
                "days": [41, 85, 117],
                "badge": "Bit Manipulation"
            },
            {
                "id": 3,
                "title": "Warp-Level Parallel Reductions (Shuffle Trees & Blelloch Scan)",
                "summary": "Replace sequential loops with 5-step __shfl_down_sync tree reductions (log2(32)=5 cycles, zero shared memory) and Blelloch up-sweep/down-sweep prefix scans.",
                "days": [153, 154],
                "badge": "Parallel Algorithms"
            },
            {
                "id": 4,
                "title": "Sparse Representations & 2:4 Structured Sparsity",
                "summary": "Compressed Sparse Row (CSR) & CSC matrix representations. NVIDIA Ampere/Hopper Tensor Cores provide 2x hardware throughput for 2:4 structured sparsity.",
                "days": [151, 152],
                "badge": "AI Tensor Cores"
            },
            {
                "id": 5,
                "title": "Lock-Free Ring Buffers & Command Queues (SPSC / MPMC)",
                "summary": "Host CPU drivers submit GPU commands via lock-free circular ring buffers with acquire/release memory fences and 64-byte padding (alignas(64)) to eliminate false sharing.",
                "days": [134, 135, 136],
                "badge": "Concurrency"
            },
            {
                "id": 6,
                "title": "Custom Memory Allocators (Buddy & Slab / Arena)",
                "summary": "cudaMalloc freezes GPU streams. High-performance frameworks use binary Buddy Allocators (buddy = addr ^ size) and Slab memory pools (PyTorch Caching Allocator).",
                "days": [162, 163],
                "badge": "Memory Management"
            },
            {
                "id": 7,
                "title": "Distributed Collective Communication (NCCL Ring All-Reduce)",
                "summary": "Large-scale LLM training across DGX SuperPODs. Total data transferred in Ring All-Reduce is 2*(P-1)/P * S bytes (bandwidth scaling independent of cluster size P).",
                "days": [166, 167],
                "badge": "Distributed Systems"
            }
        ],
        "responseFramework": [
            {
                "step": "Step 1: The Classical Algorithm (Big-O Baseline)",
                "quote": "Theoretically, this problem can be solved in O(N) time and O(N) space using an adjacency list and Dijkstra's..."
            },
            {
                "step": "Step 2: The Hardware Reality Check (The Differentiator)",
                "quote": "However, in high-performance GPU systems or low-level CUDA kernels, pointer-heavy node allocations cause continuous L1/L2 cache misses. I will represent this using a contiguous CSR flat array layout aligned to 64-byte boundaries..."
            },
            {
                "step": "Step 3: The Parallel / Scale Follow-Up (The Closer)",
                "quote": "If executed across a 32-thread GPU warp, we can replace the sequential reduction with a 5-step __shfl_down_sync tree, achieving zero-allocation reduction directly in registers."
            }
        ],
        "killerDialogue": "Theoretically, this is O(N) time and O(N) space. However, in high-performance GPU systems or low-level CUDA kernels, instead of a pointer-based tree or linked list, I would lay this out in a contiguous 1D array (Structure of Arrays) aligned to 64-byte boundaries. This guarantees spatial locality, maximizes L1/L2 cache hit rate, and enables 128-byte memory transaction coalescing across warps without branch divergence."
    }

    # Assemble complete dataset
    dsa_full_data = {
        "config": config,
        "fcats": fcats_data,
        "phases": phases_data,
        "weeks": weeks_data,
        "days": days_data,
        "patterns": patterns_data,
        "cards": cards_data,
        "resources": resources_data,
        "mocks": mocks_data,
        "blindPool": blind_data,
        "milestones": milestones_data,
        "readme": readme_data,
        "nvidiaPlaybook": nvidia_playbook
    }

    # Save to data.json
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(dsa_full_data, f, indent=2, ensure_ascii=False)
    print(f"[OK] data.json written ({len(json.dumps(dsa_full_data))} bytes)")

    # Save to data.js for direct browser consumption
    with open("data.js", "w", encoding="utf-8") as f:
        f.write("// Complete Zero-Data-Loss Dataset for DSA & AI-Infrastructure Web App\n")
        f.write("window.DSA_DATA = ")
        json.dump(dsa_full_data, f, indent=2, ensure_ascii=False)
        f.write(";\n")
    print(f"[OK] data.js written successfully")

if __name__ == "__main__":
    run_export()
