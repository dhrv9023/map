#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dsa_builder.py   -   DSA  ->  AI-Infra Training Workbook (improved)
Sheets:
  Dashboard | README | DayPlan | PatternLibrary | PatternCards |
  ProblemDB | FailureLog | ReviewQueue | WeeklyAssessment |
  MockInterviews | ResourcePlan | ProgressionCurve | BlindProblemPool
"""

from datetime import date, timedelta
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import (
    CellIsRule, ColorScaleRule, FormulaRule, DataBarRule
)
import urllib.parse
from tutorial_data import TUTORIAL_CREATORS, get_tutorial_resource

# --- CONFIG --------------------------------------------------------------------
START    = date(2026, 10, 1)
OUT      = "DSA_AI_Infra_Training.xlsx"
WEEKS    = 24
DAYS     = WEEKS * 7   # 168 days (24 weeks)
PDB_ROWS = 750         # ProblemDB data rows
FL_ROWS  = 500         # FailureLog data rows

# --- PALETTE -------------------------------------------------------------------
NAVY   = "1A2F5A"
BLUE   = "2563EB"
TEAL   = "0D9488"
PURPLE = "7C3AED"
LIGHT  = "EFF6FF"
GREY   = "F8FAFC"
DGREY  = "E2E8F0"
WHITE  = "FFFFFF"
GREEN  = "BBF7D0";  GREEN_D  = "16A34A"
AMBER  = "FEF9C3";  AMBER_D  = "CA8A04"
RED    = "FEE2E2";  RED_D    = "DC2626"
ORANGE = "FFEDD5"

# --- SHARED STYLES -------------------------------------------------------------
def _side(c="CBD5E1"): return Side(style="thin", color=c)
BORDER    = Border(left=_side(), right=_side(), top=_side(), bottom=_side())
BORDER_H  = Border(left=_side(NAVY), right=_side(NAVY),
                   top=_side(NAVY),  bottom=_side(NAVY))

WRAP  = Alignment(wrap_text=True,  vertical="top",    horizontal="left")
CTR   = Alignment(wrap_text=False, vertical="center", horizontal="center")
WRAPC = Alignment(wrap_text=True,  vertical="center", horizontal="center")

def fnt(bold=False, sz=10, color=NAVY, italic=False, underline=None):
    return Font(bold=bold, size=sz, color=color, italic=italic,
                underline=underline, name="Arial")

def fill(color): return PatternFill("solid", fgColor=color)

# --- HELPERS -------------------------------------------------------------------
def write_header(ws, headers, widths, freeze="B2", row=1, bg=BLUE):
    for c, (h, w) in enumerate(zip(headers, widths), 1):
        cell = ws.cell(row=row, column=c, value=h)
        cell.font      = fnt(bold=True, sz=9, color=WHITE)
        cell.fill      = fill(bg)
        cell.alignment = WRAPC
        cell.border    = BORDER_H
        ws.column_dimensions[get_column_letter(c)].width = w
    ws.row_dimensions[row].height = 28
    if freeze:
        ws.freeze_panes = freeze

def put(ws, r, c, v, fmt=None, bold=False, bg=None, color=NAVY,
        align=None, sz=10):
    cell = ws.cell(row=r, column=c, value=v)
    cell.border    = BORDER
    cell.alignment = align if align else WRAP
    cell.font      = fnt(bold=bold, sz=sz, color=color)
    if bg:   cell.fill = fill(bg)
    if fmt:  cell.number_format = fmt
    return cell

def dv(ws, options, rng, title="Choose"):
    d = DataValidation(type="list",
                       formula1='"%s"' % ",".join(options),
                       allow_blank=True, showDropDown=False)
    d.promptTitle = title
    ws.add_data_validation(d)
    d.add(rng)
    return d

DIFF_VALS  = ["E","M","H"]
YN_VALS    = ["Yes","No"]
SCORE_VALS = ["1","2","3","4","5"]
FCATS = [
    "F1-Understand","F2-Pattern","F3-Derive","F4-WrongDS",
    "F5-Complexity","F6-Implementation","F7-EdgeCase","F8-Debugging",
    "F9-Forgot","F10-Pressure","F11-HintDependent","F12-CantExplain"
]
MODE_VALS  = ["Untimed","Timed-30","Timed-45","Timed-60","Timed-75","Timed-90","Diagnostic"]
HELP_VALS  = ["None","1 hint @10min","1 hint @20min","1 hint @30min","2 hints","Hints allowed","Tutorial only"]

wb = Workbook()

# ==============================================================================
# SHEET 1  -  README  (rules + protocols)
# ==============================================================================
ws_r = wb.active
ws_r.title = "README"
ws_r.sheet_view.showGridLines = False
ws_r.column_dimensions["A"].width = 30
ws_r.column_dimensions["B"].width = 120

# Title banner
ws_r.merge_cells("A1:B1")
for col in ("A", "B"):
    ws_r[f"{col}1"].fill = fill(NAVY)
t = ws_r["A1"]
t.value = "DSA TRAINING SYSTEM - AI INFRASTRUCTURE (168 DAYS / 24 WEEKS)"
t.font  = fnt(bold=True, sz=13, color=WHITE)
t.alignment = Alignment(horizontal="center", vertical="center")
ws_r.row_dimensions[1].height = 36

ws_r.merge_cells("A2:B2")
for col in ("A", "B"):
    ws_r[f"{col}2"].fill = fill(LIGHT)
s = ws_r["A2"]
s.value = "The real metric: how fast you turn an unfamiliar problem into a correct, efficient algorithm. Not how many problems you have solved."
s.font  = fnt(italic=True, sz=9, color="475569")
s.alignment = Alignment(horizontal="center", vertical="center")
ws_r.row_dimensions[2].height = 24

README_SECTIONS = [
# (TITLE, BODY)
("THE ONLY METRIC THAT MATTERS",
"""Problem count is a lagging metric and a vanity number.
The metric that predicts interview success:
  * Time-to-pattern on UNLABELLED problems (target: <5 min for Medium by week 10)
  * Independent-solve rate (target: >70% by week 12)
  * Hint-dependency rate (target: <20% by week 10)
  * Ability to reconstruct any solved problem from memory 3 days later
Dashboard tracks all four. Fill it honestly or it becomes useless."""),

("DAILY BLOCK STRUCTURE  (1-2 hours total)",
"""A) RETRIEVAL  [10-15 min]
   From memory, no notes: state yesterday's pattern trigger + invariant + complexity.
   If you cannot, add it to ReviewQueue immediately.

B) CONCEPT / TUTORIAL  [0-25 min  -  ONLY if DayPlan says YES]
   Read the DayPlan tutorial column. If it says NO, do not watch anything.
   The urge to watch a tutorial instead of struggling is a productivity trap.

C) DEEP SOLVING  [45-70 min  -  the real training block]
   Obey the STUCK PROTOCOL below. No shortcuts.

D) RECONSTRUCTION  [10 min]
   Close your solution. Open a blank file. Rebuild it from memory.
   If you cannot reconstruct it, you did not learn it.

E) FAILURE ANALYSIS  [5 min]
   Log every failure in FailureLog with an honest category + one preventive rule.

F) REVIEW  [10 min]
   Top item from ReviewQueue. Retrieval only  -  no re-reading."""),

("THE STUCK PROTOCOL  (non-negotiable, enforced in DayPlan column)",
"""0-10 min   ->  NO help. Restate the problem in your own words.
              Write constraints. Write brute-force + its TC. Write target TC.
              Write 2-3 candidate approaches.

10-20 min  ->  ONE conceptual hint only. No code. No data-structure name if avoidable.
              Hint = a question that points you toward the right abstraction.

20-30 min  ->  Stronger hint: name the pattern or the key invariant.
              Still no implementation.

30+ min    ->  Read ONLY the core approach (2-3 sentences). Then close it.
              Implement entirely from scratch  -  never copy code.

If you read code  ->  problem is auto-logged as "Solution Viewed = Yes" and re-queued at +1 day.
If you solve with hints  ->  re-queued at +3 days, not +7.
The goal: "I understand WHY this solution exists." NOT "I understood it after being shown." """),

("PHASE SEQUENCE FOR EVERY IMPORTANT PROBLEM",
"""1. UNDERSTAND   -  What is asked? What are constraints? What changes? What is reusable?
2. PREDICT       -  Write target TC from constraints. List 2-3 approaches. Name the bottleneck.
3. DERIVE        -  Attempt yourself. Use stuck protocol if needed.
4. IMPLEMENT     -  Write clean code.
5. ATTACK        -  Test: empty input, single element, all duplicates, max n, negatives, overflow, adversarial order.
6. OPTIMIZE      -  Can TC improve? If no, can SC improve? Is there a hidden invariant?
7. RECONSTRUCT   -  Close everything. Rebuild from memory and explain aloud.
8. SCHEDULE      -  ProblemDB auto-computes review dates based on your performance."""),

("TUTORIAL RULES  (35 curated tutorials across 168 days)",
"""Watch BEFORE a problem only when the mental model is genuinely new (DayPlan marks these explicitly).
Do NOT watch because a specific problem is hard. Struggle first.
Watch AFTER only when you failed to recognise the SAME pattern twice.
Rewatch only if you cannot reconstruct the concept from memory.

For every tutorial, extract:
  * The TRIGGER (what wording in a problem should activate this pattern?)
  * The INVARIANT (what remains true throughout the algorithm?)
  * The COMPLEXITY ARGUMENT (why is it O(n)? O(n log n)?  -  derive it, do not accept it)

Do NOT memorise the presenter's code. That is passive consumption, not learning."""),

("FAILURE CATEGORIES  -  USE THESE CODES EVERYWHERE",
"""F1-Understand    : misread or misunderstood the problem statement
F2-Pattern       : could not identify the correct pattern
F3-Derive        : knew the pattern, could not derive the approach
F4-WrongDS       : identified the right approach, chose the wrong data structure
F5-Complexity    : wrong or absent complexity analysis
F6-Implementation: correct approach, coding bug
F7-EdgeCase      : correct solution, missed an edge case
F8-Debugging     : took too long to find the bug
F9-Forgot        : knew this technique previously, forgot it
F10-Pressure     : failed specifically because of time pressure (fine in untimed)
F11-HintDependent: required a hint to make progress
F12-CantExplain  : could implement but could not explain the solution"""),

("AUTO-ESCALATION RULES  (the plan adjusts to your failures)",
"""If any category appears 3+ times in one week:
  F2 (Pattern)      ->  next week's 2 blind days must target that pattern family
                     + do 10 "name the pattern only" reps daily (5 min, no coding)
  F3 (Derive)       ->  add 1 extra reconstruction per day from the failed pattern
  F5 (Complexity)   ->  estimate TC out loud BEFORE every single problem  -  no exceptions
  F6 (Implement)    ->  write the invariant as a comment before every loop
  F7 (EdgeCase)     ->  run your personal edge-case checklist before every submission
  F10 (Pressure)    ->  replace one untimed day per week with a timed session
  F11 (HintDep)     ->  the stuck-protocol clock resets to 0  -  you must wait the full 30 min

If F2 or F3 each appear 5+ times in a single week: run a pattern-recognition drill session
(20 problems, no coding, just write "pattern: X" for each) before continuing the plan."""),

("MISSED DAYS  (no restarts, ever)",
"""1 day missed      ->  resume exactly where you left off. Nothing special.
2-3 days missed   ->  RECOVERY SESSION: 15 min retrieval of last 3 patterns +
                    2 problems from top of ReviewQueue + nothing new.
1+ week missed    ->  MINI-DIAGNOSTIC: 3 unlabelled problems from the pool (60 min).
                    Re-enter the plan at the week whose patterns you failed.
                    Do NOT go back to Day 1. Do NOT do a multi-day catch-up pile.
                    Catch-up piles produce shallow results and break motivation."""),

("PRODUCTIVITY TRAPS  (re-read every Sunday)",
"""* Watching tutorials instead of struggling
* Solving only easy problems
* Solving problems already labelled with the pattern (defeats the whole purpose)
* Reading the solution before 30 minutes are up
* Memorising templates instead of understanding invariants
* Copying code from solutions
* Doing 10 shallow solves instead of 3 deep ones
* Never revisiting problems (mastery requires forgetting and re-retrieving)
* Confusing recognition with mastery
* Confusing "I understood when shown" with "I could derive it"
* Micro-optimising code whose algorithm you cannot explain
* Avoiding hard problems (they teach 5x more per minute)
* Switching resources mid-plan (new resource = new procrastination)
* Spending hours on beautiful notes instead of solving problems
* Tracking problem counts instead of solve quality
* Random LeetCode grinding with no failure analysis"""),

("SECOND-SOLUTION RULE",
"""For every problem marked [2-SOL] in DayPlan, find a fundamentally different approach:
  HashMap  <->  Sorting     |  DFS  <->  BFS          |  Greedy  <->  DP
  Heap  <->  Sorting        |  Binary Search  <->  Math|  Recursion  <->  Iteration+Stack

This kills problem -> template reflexes. Template-locked candidates fail on variants.
Write both approaches, compare TC/SC, and state when each is preferable."""),

("DIAGNOSTICS SCHEDULE",
"""Day 28  (90 min)  Pool A: LC 918, LC 795, LC 581         -  unlabelled, no hints
Day 56  (100 min) Pool B: LC 315, LC 1110, LC 1396        -  unlabelled, no hints
Day 84  (110 min) Pool C: LC 1383, LC 1326, LC 2092       -  unlabelled, no hints
Day 98  (110 min) Final:  LC 1751, LC 2421, LC 1463       -  unlabelled, no hints

Metric to track across all four: time-to-pattern, hint dependency, TC/SC accuracy, explanation quality.
A diagnostic where you improve on all four metrics = the plan is working.
A diagnostic where you stagnate = the plan must change, not the effort."""),

("MOCK INTERVIEW SCHEDULE",
"""Day 42  Mock #1  -  2 hints allowed, generous time, narrate aloud
Day 70  Mock #2  -  1 hint, 45 min, state TC/SC unprompted, one follow-up
Day 92  Mock #3  -  no hints, verbal reasoning required throughout
Day 95  Mock #4  -  unfamiliar hard problem, 45 min, follow-up required
Day 98  Final    -  included in final diagnostic

Every mock: narrate every decision aloud. State TC/SC before coding.
Answer one infra follow-up: "What if input is streaming / distributed / 10^9 elements?" """),

("AI-INFRA LENS  (use only where it genuinely adds clarity)",
"""Caching/eviction       ->  LRU, LFU, ARC (hashmap + ordered structure)
Scheduling             ->  heaps, topological order, priority queues
Dependency resolution  ->  DAG + Kahn's algorithm
Rate limiting          ->  sliding window, token bucket
Load balancing         ->  binary search on answer + greedy
Streaming metrics      ->  two heaps, monotonic deque, reservoir sampling
Sharding/partitioning  ->  hashing, consistent hashing, Union-Find
Indexing / search      ->  binary search, tries, sorted structures
Memory management      ->  knapsack, bin packing (intuition)
Log merging            ->  k-way merge, interval merging
Distributed connect.   ->  offline graph algorithms, DSU over streams

Do NOT force an infra analogy into every problem. Use it when it genuinely deepens understanding.
The interview DSA / infra DSA overlap is strongest in: heaps, hashing, graphs/DAGs,
binary search on answer, and O(1) structure design."""),

("THE NVIDIA & GPU-SYSTEMS INTERVIEW STANDARD",
"""NVIDIA does NOT interview like standard web/app Big Tech.
Interviewers in CUDA, TensorRT, Triton, NCCL, Tegra, Drivers, and AI Infrastructure
test whether your mental model matches the underlying SILICON.

1. HARDWARE-AWARE COMPLEXITY (Big-O in a vacuum is rejected):
   * Cache Lines: CPU/GPU memory moves in 64-byte or 128-byte chunks.
     A pointer-chasing O(N) linked-list is 50x slower than a contiguous O(N) array due to cache misses.
   * Memory Coalescing & Bank Conflicts: Consecutive threads must access consecutive
     memory addresses. Strided access serializes memory transactions into separate bus requests.
   * Branch Divergence: If threads in a 32-thread warp take different branches (if/else),
     both execution paths are serialized. Write branchless / bit-predicated logic where possible.

2. BITWISE ARITHMETIC AS A NATIVE LANGUAGE:
   * Thread & Warp Masks: __activemask(), __ballot_sync(), popcount (__builtin_popcount).
   * Memory Alignment: Aligning address X to 64 bytes: (X + 63) & ~63.
   * Fast Power-of-Two: (n & (n - 1)) == 0, modulo mask (x & (2^k - 1)).
   * Bit-reversal and lowest set bit (x & -x) for Fenwick trees and parallel FFTs.

3. PARALLEL REDUCTIONS & WARP PRIMITIVES:
   * Never stop at a sequential loop. Always be prepared to answer:
     "How does this run across 32 parallel threads in a warp?"
   * Master Blelloch work-efficient parallel scan (up-sweep / down-sweep tree reduction).
   * Master warp-shuffle reductions (__shfl_down_sync) for sum, min, max without shared memory.

4. DATA LAYOUT: SoA vs AoS:
   * Structure of Arrays (SoA: x[N], y[N], z[N]) allows SIMD/GPU coalesced vector loads.
   * Array of Structures (AoS: struct Point{x,y,z} pts[N]) causes strided, uncoalesced memory fetches.

5. LOCK-FREE COMMAND QUEUES & PRODUCER-CONSUMER:
   * SPSC (Single-Producer Single-Consumer) ring buffers with acquire/release memory fences.
   * Power-of-two buffer sizing for branchless index wrapping.
   * Avoid false sharing by padding cache lines (alignas(64)).

6. SPARSE MATRICES & TENSOR STRIDES:
   * Compressed Sparse Row (CSR: values, column_indices, row_pointers) and CSC.
   * 2:4 Structured Sparsity (NVIDIA Ampere/Hopper Tensor Core 2x throughput).
   * Strided indexing (offset = sum(coord[i] * stride[i])) and in-place tensor transposition.

7. NCCL & DISTRIBUTED COLLECTIVES:
   * Ring All-Reduce vs Tree All-Reduce: bandwidth vs latency trade-offs.
   * Ring All-Reduce: 2*(P-1)/P * S transfer size (constant bandwidth scaling as cluster size P grows)."""),

("COMPLEXITY TRAINING  (first-class skill)",
"""For EVERY problem, answer these before writing a single line of code:
  1. What is the brute-force TC and why?
  2. What makes it slow? (which step is repeated unnecessarily?)
  3. What is the target TC? (derived from n in the constraints)
  4. What is the likely lower bound? (can we prove nothing faster exists?)
  5. What is the SC?
  6. What happens at maximum input size? (n=10^5, n=10^9)

n <= 20        ->  O(2^n) or O(n!) acceptable (backtracking, bitmask DP)
n <= 500       ->  O(n^2) or O(n^2 log n) acceptable
n <= 5,000     ->  O(n^2) tight
n <= 100,000   ->  O(n log n) required
n <= 1,000,000 ->  O(n) strongly preferred
n <= 10^9      ->  O(log n) or O(1) only"""),

("RESOURCE DISCIPLINE & CURATED YOUTUBE CREATORS",
"""Curated tutorial channels:
  - Striver (take U forward) - algorithmic patterns & technical interview rigor
  - Aditya Verma - intuition & recurrence templates (DP, Stack, Sliding Window, BS)
  - Love Babbar (CodeHelp) - clear structural breakdowns & Hindi explanations
  - Padho with Pratyush - deep systems intuition, cache/concurrency & advanced DSA
  - NeetCode (neetcode.io) - concise visual problem walkthroughs & clean code
  - Specialized channels: Abdul Bari (algorithms), WilliamFiset (graphs), Errichto (range trees), Martin Thompson (lock-free), CMU DB (paging)

See the dedicated 'YouTubeChannels' sheet tab in this workbook for direct 1-click links to master playlists and channel URLs."""),
]

r = 4
for title, body in README_SECTIONS:
    # Section title
    ws_r.merge_cells(f"A{r}:B{r}")
    for col_l in ("A", "B"):
        ws_r[f"{col_l}{r}"].fill = fill(BLUE)
        ws_r[f"{col_l}{r}"].border = BORDER_H
    tc = ws_r[f"A{r}"]
    tc.value     = f"  {title}"
    tc.font      = fnt(bold=True, sz=10, color=WHITE)
    tc.alignment = Alignment(vertical="center", horizontal="left")
    ws_r.row_dimensions[r].height = 26
    r += 1
    # Body
    ws_r.merge_cells(f"A{r}:B{r}")
    for col_l in ("A", "B"):
        ws_r[f"{col_l}{r}"].fill = fill(GREY)
        ws_r[f"{col_l}{r}"].border = BORDER
    bc = ws_r[f"A{r}"]
    bc.value     = body.strip()
    bc.font      = fnt(sz=9, color="1E293B")
    bc.alignment = Alignment(wrap_text=True, vertical="top", horizontal="left")
    lines = body.strip().count("\n") + 1
    ws_r.row_dimensions[r].height = max(14 * lines, 30)
    r += 2

print("[OK] Part 1 done: README sheet built")

# ==============================================================================
# PART 2  -  98-DAY PLAN DATA
# ==============================================================================
# Tuple fields (19 per day):
# 0  objective       -  session goal
# 1  pattern         -  main pattern
# 2  concept         -  what to understand/internalize
# 3  tut_yn          -  YES/NO tutorial today
# 4  tut_topic       -  tutorial topic
# 5  tut_min         -  tutorial duration
# 6  mode            -  Untimed / Timed-XX / Diagnostic
# 7  help            -  stuck protocol variant
# 8  p1              -  problem 1
# 9  d1              -  difficulty E/M/H
# 10 t1              -  target minutes
# 11 p2              -  problem 2 (or task)
# 12 d2              -  difficulty
# 13 t2              -  target minutes
# 14 review          -  problem to review
# 15 reconstruction  -  what to rebuild from memory
# 16 assessment      -  one honest question
# 17 infra           -  AI-infra connection
# 18 skill           -  skill gained

PLAN = [

# --- WEEK 1: Constraints, Counting, Hashing, Prefix ---------------------------

("Build constraint -> complexity map; learn to target TC before writing code",
 "Complexity calibration","Map n to feasible TC; O(n^2) failure at n=10^5; recursion/hash constants",
 "YES","Big-O calibration + n -> TC mapping",25,
 "Untimed","Tutorial only",
 "LC 1 Two Sum","E",12,
 "LC 121 Best Time to Buy & Sell Stock","E",15,
 "-",
 "Write from memory: n -> max-feasible-TC table (20/500/5k/100k/1M/1B) + your 6-step pre-code checklist",
 "Did you state a target TC before writing a single line? Yes/No  -  be honest.",
 "Latency budgets: algorithm choice is a function of input scale, not taste",
 "Constraint-first thinking"),

("Turn counting into O(1) lookups; design the hash KEY deliberately",
 "Frequency/counting + hashing","Hash map as an index, not just storage; bucket counting vs sorting",
 "NO","-",0,
 "Untimed","1 hint @20min",
 "LC 49 Group Anagrams","M",25,
 "LC 347 Top K Frequent Elements","M",25,
 "LC 1 Two Sum",
 "Rederive bucket-sort top-K with no notes; state why it is O(n) not O(n log n)",
 "Was your hash KEY chosen from the invariant, or guessed by trial?",
 "Hot-key detection, metric counters, hash-based sharding in distributed systems",
 "Key design + counting"),

("Reuse computed sums instead of recomputing; prefix+hash is the unlock",
 "Prefix/suffix reasoning","Prefix sums; prefix+hashmap for subarray conditions; why count map != seen set",
 "YES","Prefix sum & prefix-hash pattern",20,
 "Untimed","1 hint @20min",
 "LC 560 Subarray Sum Equals K","M",30,
 "LC 238 Product of Array Except Self","M",25,
 "LC 49 Group Anagrams",
 "Explain why prefix+hash needs a COUNT map and why prefix 0 is seeded before any element",
 "Can you state the loop invariant of the prefix map in one sentence without notes?",
 "Cumulative counters, rolling aggregation over event logs, prefix histograms",
 "Reuse of partial results"),

("Encode a condition as a prefix value  -  problem transformation",
 "Prefix/suffix (encoding)","Rewrite equal-count as prefix equality; 2D prefix sums inclusion-exclusion",
 "NO","-",0,
 "Untimed","1 hint @20min",
 "LC 525 Contiguous Array","M",30,
 "LC 304 Range Sum Query 2D - Immutable","M",25,
 "LC 560 Subarray Sum Equals K",
 "Explain the +1/-1 transformation and the first-occurrence rule; derive 2D inclusion-exclusion formula",
 "Did you invent the encoding yourself? That determines your real review date.",
 "Region aggregation queries over tiled/sharded data, 2D coverage metrics",
 "Problem transformation"),

("Interleave week-1 patterns; first blind session  -  no pattern labels",
 "Blind (mixed W1 patterns)","Pattern discrimination under ambiguity; hashing invariants",
 "NO","-",0,
 "Untimed","No hints before 20min",
 "LC 128 Longest Consecutive Sequence","M",30,
 "LC 724 Find Pivot Index","E",12,
 "LC 238 Product of Array Except Self",
 "For both problems write a PatternCards entry: Trigger + Core Insight + Recognition Cue",
 "Time-to-pattern for each problem (record the number). Target: <6 min.",
 "Set membership/dedup at scale; pivot-based load distribution",
 "Pattern recognition without labels"),

("[2-SOL] First timed session  -  2 unlabelled problems; also find second solution for LC 380",
 "Blind + O(1) design","Working under a clock; index-map + swap-with-last deletion invariant",
 "NO","-",0,
 "Timed-60","None",
 "LC 380 Insert Delete GetRandom O(1)","M",25,
 "LC 36 Valid Sudoku","M",25,
 "LC 525 Contiguous Array",
 "State the swap-with-last deletion invariant and why element order in the array does not matter",
 "Did the clock reduce your decision quality? Identify exactly which decision suffered.",
 "Uniform random sampling from a live set; validation pipelines in data-quality systems",
 "Timed execution + O(1) design"),

("Week 1 assessment + full reconstruction. Zero new patterns.",
 "Review/audit","Retention without notes  -  the only real test of week 1",
 "NO","-",0,
 "Untimed","Notes forbidden",
 "Rederive: prefix+hash (LC 560), bucket top-K (LC 347), prefix-0 seed reason","M",45,
 "Fill WeeklyAssessment row + cluster FailureLog by category","-",20,
 "All week-1 rows with Mastered=No",
 "Rebuild prefix+hash and bucket top-K from a blank editor; diff your version against your first solution",
 "Score pattern recognition 1-5 HONESTLY. Cannot rebuild = was never learned.",
 "-",
 "Retention + self-audit"),

# --- WEEK 2: Two Pointers, Sliding Window -------------------------------------

("Learn WHY two pointers is valid  -  the monotonic movement proof",
 "Two pointers (opposite ends)","Convergence argument; proof no pair is skipped; duplicate handling",
 "YES","Two pointers: the validity argument (not just the template)",20,
 "Untimed","1 hint @20min",
 "LC 167 Two Sum II","E",12,
 "LC 15 3Sum","M",35,
 "LC 347 Top K Frequent Elements",
 "Prove why skipping duplicates in 3Sum cannot lose any valid solution",
 "Can you justify each pointer move with a logical argument, or are you pattern-matching?",
 "Merging two sorted streams; sorted shard scans in distributed databases",
 "Monotonic pointer proof"),

("Same-direction pointers; in-place rewriting; greedy discard argument",
 "Two pointers (read/write index)","Write-index vs read-index; discard step must be justified not assumed",
 "NO","-",0,
 "Untimed","1 hint @20min",
 "LC 11 Container With Most Water","M",30,
 "LC 75 Sort Colors (Dutch flag)","M",20,
 "LC 15 3Sum",
 "Write the exchange argument for discarding the shorter wall; state Sort Colors' 3-region invariant",
 "Did you PROVE the discard step, or just accept it as obvious?",
 "In-place buffer compaction; zero-copy stream rewriting",
 "Invariant-based greedy"),

("Variable-size sliding window: learn the shrink condition and its validity proof",
 "Sliding window (variable)","Monotone feasibility: growing never repairs a violation; shrink until valid",
 "YES","Sliding window: expand/shrink + when it FAILS (negatives, non-monotone)",25,
 "Untimed","Tutorial before; no solution reading",
 "LC 3 Longest Substring Without Repeating Characters","M",25,
 "LC 209 Minimum Size Subarray Sum","M",25,
 "LC 75 Sort Colors",
 "Write your window's loop invariant; then construct one problem where sliding window is INVALID",
 "Do you know the VALIDITY CONDITION, or only the template? They are not the same thing.",
 "Rate limiting over time windows; token bucket implementation",
 "Window invariants + validity condition"),

("Windows with a counting constraint; the atMost(K) subtraction trick",
 "Sliding window + frequency","exactly(K) = atMost(K) - atMost(K-1); frequency maps inside windows",
 "NO","-",0,
 "Untimed","1 hint @25min only",
 "LC 424 Longest Repeating Character Replacement","M",35,
 "LC 992 Subarrays with K Different Integers","H",40,
 "LC 3 Longest Substring Without Repeating Characters",
 "Derive the subtraction identity yourself; explain why maxFreq need not be recomputed on shrink in LC 424",
 "Did you reach the subtraction trick independently? If not  ->  F3, review at +2 days.",
 "Cardinality-bounded caches; distinct-key windows in streaming analytics",
 "Counting inside windows"),

("Fixed windows and the hardest window bookkeeping  -  need/have counters",
 "Sliding window (fixed/need-have)","Fixed-size window state; need/have counters; when 'have' increments",
 "NO","-",0,
 "Untimed","No hints before 30min",
 "LC 567 Permutation in String","M",25,
 "LC 76 Minimum Window Substring","H",40,
 "LC 424 Longest Repeating Character Replacement",
 "Rebuild the have/need counter logic of LC 76 from memory with no notes",
 "Was your bug in the LOGIC or the CODE? Different failure category, completely different fix.",
 "Pattern matching over log streams; sequence detection in telemetry pipelines",
 "Careful state maintenance under constraints"),

("Blind mix: two pointers vs window vs prefix  -  discriminate without labels",
 "Blind (W1+W2 mix)","Choosing between near-neighbour patterns from problem wording alone",
 "NO","-",0,
 "Untimed","None",
 "LC 904 Fruit Into Baskets","M",25,
 "LC 1004 Max Consecutive Ones III","M",25,
 "LC 76 Minimum Window Substring",
 "Write a 3-question decision tree: prefix vs window vs two-pointers (use it from today onwards)",
 "Correct pattern on first guess for both? Log the misread cue if wrong.",
 "Sliding aggregates over time-series telemetry data",
 "Pattern discrimination"),

("Week 2 assessment + timed retest of failures",
 "Review/audit","Retention under time pressure; failure clustering",
 "NO","-",0,
 "Timed-40","None",
 "Retest your 2 worst W2 problems, timed","M",40,
 "WeeklyAssessment + failure clustering","-",25,
 "ReviewQueue top 3",
 "Rederive the window shrink rule and the atMost(K) identity from memory",
 "Which failure category repeated from W1? It drives next week's blind days.",
 "-",
 "Self-diagnosis"),

# --- WEEK 3: Binary Search -----------------------------------------------------

("Binary search correctness from invariants, not from memory of a template",
 "Binary search (index)","Half-open invariant; lower_bound vs upper_bound; off-by-one elimination",
 "YES","Binary search boundaries: invariant-first approach",25,
 "Untimed","Tutorial before",
 "LC 704 Binary Search","E",10,
 "LC 34 Find First and Last Position","M",25,
 "LC 1004 Max Consecutive Ones III",
 "Write lower_bound AND upper_bound from memory with NO template; state the invariant of each",
 "Bug-free without a template? If no, that is F6 and it costs you in every future BS problem.",
 "Index lookups in sorted on-disk structures (SSTables, sorted file offsets)",
 "Boundary reasoning from invariants"),

("Binary search on broken monotonicity  -  rotated array",
 "Binary search (rotated)","Detect the sorted half; prove the test is correct; handle duplicates",
 "NO","-",0,
 "Untimed","1 hint @20min",
 "LC 33 Search in Rotated Sorted Array","M",30,
 "LC 153 Find Minimum in Rotated Sorted Array","M",20,
 "LC 34 Find First and Last Position",
 "Explain which half is sorted, why the test is correct, and what breaks with duplicates (LC 81)",
 "Did you enumerate the 4 cases before coding, or debug into a solution?",
 "Circular buffers; ring-index math in lock-free queues",
 "Partial-order search"),

("Binary search ON THE ANSWER  -  the single highest-leverage pattern in this program",
 "Binary search on answer","Monotone predicate feasible(x); search value space not index space",
 "YES","Binary search on answer / parametric search",25,
 "Untimed","Tutorial before, then solve alone with no help",
 "LC 875 Koko Eating Bananas","M",25,
 "LC 1011 Capacity to Ship Packages Within D Days","M",25,
 "LC 33 Search in Rotated Sorted Array",
 "Write the 3 validity conditions for BS-on-answer: answer space bounded, predicate monotone, predicate fast",
 "Do 'minimize the maximum' and 'maximize the minimum' now trigger this pattern instantly?",
 "Capacity planning, autoscaling thresholds, batch-size selection, quota fitting, SLO optimization",
 "Parametric search"),

("[2-SOL] Harder predicate design  -  construct feasible() when it is not obvious",
 "Binary search on answer (hard predicates)","feasible() construction; proving monotonicity",
 "NO","-",0,
 "Untimed","1 hint @25min",
 "LC 410 Split Array Largest Sum","H",40,
 "LC 1482 Minimum Number of Days to Make m Bouquets","M",25,
 "LC 875 Koko Eating Bananas",
 "Rederive feasible() for LC 410 with no notes; prove its monotonicity; find the DP alternative O(kn^2)",
 "Was your predicate actually monotone? Prove it  -  unproven predicates are guesses.",
 "Sharding load across workers under a max-per-worker bound; SLO-constrained batching",
 "Predicate construction + second solution (DP)"),

("Binary search where input is not a flat array; second solutions required",
 "Binary search (abstract) + partition","count(<=x) counting search; binary search over a 2D structure",
 "NO","-",0,
 "Untimed","1 hint @30min",
 "LC 378 Kth Smallest in a Sorted Matrix","M",35,
 "LC 4 Median of Two Sorted Arrays","H",45,
 "LC 410 Split Array Largest Sum",
 "Explain BOTH: count(<=x) search and the O(log(min(m,n))) partition method for LC 4",
 "Two genuinely different solutions found? If only one, you are template-locked.",
 "Quantile estimation over sorted shards; distributed k-th element queries",
 "Second-solution habit"),

("Blind mix: sort, window, or binary search  -  eliminate from constraints first",
 "Blind (W1-W3)","Approach elimination from constraint reading; recognition speed",
 "NO","-",0,
 "Timed-50","None",
 "LC 162 Find Peak Element","M",20,
 "LC 2300 Successful Pairs of Spells and Potions","M",25,
 "LC 4 Median of Two Sorted Arrays",
 "For each: write the single constraint clue that revealed the pattern",
 "Time-to-pattern < 4 min for both? Record both numbers in MockInterviews.",
 "Threshold queries over sorted metric arrays in monitoring systems",
 "Fast elimination from constraint reading"),

("Week 3  -  complexity drilling as a first-class skill (10 reps, no coding)",
 "Review/complexity","Estimate TC/SC BEFORE coding; lower bounds; 10 targeted dreps",
 "NO","-",0,
 "Untimed","None",
 "10 complexity drills: read problem  ->  brute TC  ->  target TC  ->  SC  ->  lower bound. No coding.","-",30,
 "Retest your 2 worst W3 problems","M",40,
 "ReviewQueue top 3",
 "Rederive the 3 BS-on-answer validity conditions; write 3 problems where it does NOT apply",
 "Complexity accuracy /10. Below 7 means F5 is your bottleneck, not algorithms.",
 "-",
 "Complexity fluency"),

# --- WEEK 4: Sorting, Intervals, Monotonic Structures + Diagnostic -------------

("Sorting as preprocessing: what invariant does the sort create?",
 "Sort + linear scan","Sort manufactures monotonicity you can exploit greedily; sort KEY matters",
 "NO","-",0,
 "Untimed","1 hint @20min",
 "LC 56 Merge Intervals","M",25,
 "LC 435 Non-Overlapping Intervals","M",25,
 "LC 2300 Successful Pairs of Spells and Potions",
 "State exactly what invariant the sort created in each problem, and why the sort key (start vs end) matters",
 "Did you justify the sort key, or try both until tests passed?",
 "Log compaction ordering; dedup windows; merging of sorted shard outputs in LSM-trees",
 "Preprocessing mindset"),

("Interval reasoning and sweep line  -  two equivalent views",
 "Intervals/sweep line","Events +1/-1; heap-of-end-times as equivalent model",
 "YES","Sweep line and event counting",20,
 "Untimed","Tutorial before",
 "LC 253 Meeting Rooms II","M",30,
 "LC 1094 Car Pooling","M",20,
 "LC 56 Merge Intervals",
 "Prove heap-of-ends and sweep-line give identical answers; state both complexities; derive the tie-breaking rule",
 "Two solutions for one problem  -  that is the target habit from today forward.",
 "Concurrent resource counting (GPU slots, DB connections); admission control",
 "Sweep-line modelling"),

("Monotonic stack from first principles  -  the amortized argument is everything",
 "Monotonic stack","A pop resolves one answer; total pops <= n  ->  amortized O(n); stack holds invariant",
 "YES","Monotonic stack from first principles (amortized)",25,
 "Untimed","Tutorial before",
 "LC 739 Daily Temperatures","M",25,
 "LC 503 Next Greater Element II (circular)","M",20,
 "LC 253 Meeting Rooms II",
 "Explain the amortized bound out loud; state what the stack contains at any moment (the invariant)",
 "Could you explain the amortization to an interviewer in 60 seconds? Practise aloud.",
 "Detecting monotone breaks in metric streams (backpressure onset, latency spikes)",
 "Amortized analysis"),

("Monotonic stack on spans and areas  -  boundary-span thinking",
 "Monotonic stack (boundaries)","previous-smaller / next-smaller  ->  span formula; equal-element handling",
 "NO","-",0,
 "Untimed","1 hint @30min",
 "LC 84 Largest Rectangle in Histogram","H",40,
 "LC 907 Sum of Subarray Minimums","M",35,
 "LC 739 Daily Temperatures",
 "Derive width = right - left - 1 yourself; explain the equal-element double-counting fix for LC 907",
 "Did you handle equal elements correctly BY DESIGN, or by trial and error?",
 "Peak-utilization rectangles over time-series capacity graphs; histogram-based alerting",
 "Boundary-span thinking"),

("[2-SOL] Monotonic deque + solve LC 42 Trapping Rain Water three ways",
 "Monotonic deque","Deque holds only viable candidates in decreasing order; window max in O(n)",
 "NO","-",0,
 "Untimed","1 hint @25min",
 "LC 239 Sliding Window Maximum","H",30,
 "LC 42 Trapping Rain Water (3 solutions)","M",30,
 "LC 84 Largest Rectangle in Histogram",
 "Solve LC 42 three ways: prefix-max arrays, two pointers, monotonic stack. Compare TC/SC for each.",
 "How many of the three did you find WITHOUT help? That is your second-solution score.",
 "Rolling max latency over stream windows; watermarking in streaming pipelines",
 "Multi-solution flexibility"),

("Blind mix across weeks 1-4  -  cross-pattern discrimination under time",
 "Blind (W1-W4 cross)","Speed of pattern recognition; avoiding false pattern matches",
 "NO","-",0,
 "Timed-55","None",
 "LC 621 Task Scheduler","M",30,
 "LC 452 Minimum Number of Arrows to Burst Balloons","M",20,
 "LC 239 Sliding Window Maximum",
 "Write one-line recognition cues for ALL patterns from weeks 1-4 (~14 cues total)",
 "First-try correct pattern rate this week. Below 60%  ->  recognition, not knowledge, is the gap.",
 "Cooldown-constrained job scheduling = real scheduler behaviour in ML training systems",
 "Recognition speed"),

("MONTH 1 DIAGNOSTIC  -  3 unlabelled, 90 min, zero hints, verbal explanation required",
 "Diagnostic","Measure, do not learn. No pattern labels. No hints.",
 "NO","-",0,
 "Diagnostic","None",
 "LC 918 Max Sum Circular Subarray","M",30,
 "LC 795 Number of Subarrays with Bounded Max","M",30,
 "LC 581 Shortest Unsorted Continuous Subarray (unlabelled)","M",30,
 "For each: log time-to-pattern, final TC/SC, correctness, hint-free, explanation quality",
 "Fill MockInterviews rows now. This is your baseline  -  do not soften any score.",
 "-",
 "Baseline measurement"),

# --- WEEK 5: Heaps, Streaming, Greedy -----------------------------------------

("Heap mental model: partial order is enough; when to use heap vs sort",
 "Heap/top-K","Why heap beats full sort when k<<n; heapify is O(n); min-heap vs max-heap",
 "YES","Heaps: sift-up/down, heapify, cost comparison",25,
 "Untimed","Tutorial before",
 "LC 215 Kth Largest Element in Array","M",25,
 "LC 973 K Closest Points to Origin","M",20,
 "LC 621 Task Scheduler",
 "State when sorting beats a heap and vice versa, with both complexities written out explicitly",
 "Can you compute and compare both costs, including constants? That is the skill.",
 "Top-K hot keys, request prioritisation, eviction candidate selection in caches",
 "Cost comparison reasoning"),

("Two-heap invariants for streaming statistics",
 "Heap (streaming/online)","Balanced max-heap/min-heap invariant; maintain the balance on every insert",
 "NO","-",0,
 "Untimed","1 hint @25min",
 "LC 295 Find Median from Data Stream","H",35,
 "LC 1046 Last Stone Weight","E",15,
 "LC 215 Kth Largest Element",
 "Write the two-heap invariant and rebalance rule BEFORE writing any code",
 "Did you define the invariant FIRST? That is the whole skill in streaming structure design.",
 "Online p50/p99 latency estimation without storing all samples; streaming quantiles",
 "Streaming state design"),

("Heap for k-way merging and greedy scheduling",
 "Heap (k-way merge)","k-way merge; heap of active cursors; where the log k factor comes from",
 "NO","-",0,
 "Untimed","1 hint @20min",
 "LC 23 Merge k Sorted Lists","H",30,
 "LC 767 Reorganize String","M",25,
 "LC 295 Find Median from Data Stream",
 "Explain where log k comes from; give the divide-and-conquer merge alternative and its TC",
 "Correct TC derived, not guessed? Two algorithms compared?",
 "LSM-tree compaction; merging sorted shard outputs in distributed ML data pipelines",
 "Merge algorithms"),

("Greedy: the exchange argument  -  proof, not vibes",
 "Greedy invariants","Exchange argument and staying-ahead argument; constructing counterexamples",
 "YES","Proving greedy correctness: exchange and staying-ahead",20,
 "Untimed","Tutorial before",
 "LC 45 Jump Game II","M",30,
 "LC 134 Gas Station","M",25,
 "LC 23 Merge k Sorted Lists",
 "Write a full exchange-argument proof for LC 45; write the unique-start argument for LC 134",
 "Did you PROVE it or trust it? Unproven greedy is the most common hard-interview failure.",
 "Chunked transfer decisions; admission control; retry budget allocation in ML serving",
 "Greedy proof technique"),

("Greedy vs DP  -  find where greedy breaks by constructing a counterexample",
 "Greedy vs DP","Counterexample construction as a design discipline",
 "NO","-",0,
 "Untimed","1 hint @30min",
 "LC 763 Partition Labels","M",20,
 "LC 871 Minimum Number of Refueling Stops","H",40,
 "LC 45 Jump Game II",
 "Construct an input where a plausible greedy fails on LC 871; state why the heap-greedy is correct",
 "Can you break your own solution? If you cannot, you cannot trust it.",
 "Checkpoint placement in long ML training runs; spot-instance restart strategy",
 "Adversarial self-testing"),

("Blind mix: heap vs sort vs greedy vs simulation",
 "Blind (W5 mix)","Cost-based structure selection under time pressure",
 "NO","-",0,
 "Timed-60","None",
 "LC 2402 Meeting Rooms III","H",40,
 "LC 1834 Single-Threaded CPU","M",30,
 "LC 871 Minimum Number of Refueling Stops",
 "Name the invariant each heap maintains in these problems and why two heaps are needed",
 "Simulation bugs count as F6, not F2  -  the pattern is correct, the implementation failed.",
 "This IS a real scheduler: ready-queue + busy-resource queue with release events",
 "Simulation discipline"),

("Week 5 assessment: weakness-targeted retest",
 "Review/targeted repair","Attack your dominant failure category directly",
 "NO","-",0,
 "Untimed","Hints allowed",
 "3 problems from your most frequent failure category this week","M",45,
 "WeeklyAssessment + write preventive rules","-",20,
 "ReviewQueue top 4",
 "Rebuild two-heap median and k-way merge from a blank file",
 "Is your top failure category shrinking week over week? If not, the plan changes.",
 "-",
 "Targeted repair"),

# --- WEEK 6: Design, Pointers, Bits -------------------------------------------

("Pointer surgery: linked-list invariants  -  reason before running, no debugger",
 "Linked list pointers","Dummy head; prev/curr discipline; draw state transitions before coding",
 "NO","-",0,
 "Untimed","1 hint @20min",
 "LC 206 Reverse Linked List","E",12,
 "LC 143 Reorder List","M",25,
 "LC 1834 Single-Threaded CPU",
 "Draw pointer states before/after EACH statement for LC 143  -  no debugger allowed",
 "Did you reason through it, or print-debug your way into a solution?",
 "Free lists and intrusive linked lists in memory allocators",
 "Precise state mutation"),

("[2-SOL] O(1) cache design: compose hashmap + doubly linked list",
 "Design (LRU)","Composing two structures for O(1) on all ops; API drives structure choice",
 "YES","LRU cache design: structure composition from requirements",20,
 "Untimed","Tutorial before",
 "LC 146 LRU Cache","M",35,
 "LC 142 Linked List Cycle II","M",25,
 "LC 143 Reorder List",
 "Rebuild LRU from an empty file with no notes; then explain Floyd's cycle detection proof",
 "Can you write a clean LRU in under 20 minutes? This is a baseline infra expectation.",
 "Page cache eviction; KV-store eviction; embedding/feature cache in ML serving",
 "Structure composition from API requirements"),

("Frequency-aware eviction: LFU  -  minFreq pointer invariant",
 "Design (LFU)","Bucketing by frequency; minFreq can only increase by 1 on access",
 "NO","-",0,
 "Untimed","1 hint @30min",
 "LC 460 LFU Cache","H",45,
 "LC 362 Design Hit Counter","M",20,
 "LC 146 LRU Cache",
 "Explain the minFreq invariant and why it increases by at most 1 on any access",
 "For an ML feature cache: LRU or LFU? Defend with an access-pattern argument.",
 "Feature-store caching; embedding cache eviction; hot-shard detection in key-value systems",
 "Advanced structure design"),

("Bit manipulation as set/state encoding",
 "Bit manipulation","Masks as tiny sets; XOR invariants; popcount; iterate subsets",
 "YES","Bit tricks that actually recur in interviews",20,
 "Untimed","Tutorial before",
 "LC 137 Single Number II","M",25,
 "LC 371 Sum of Two Integers","M",20,
 "LC 460 LFU Cache",
 "Explain XOR/counting-bits invariant; write mask ops for add/remove/test/iterate-all-subsets",
 "Do you now see bitmask=tiny-set automatically? You will need this in week 13.",
 "Bitmaps; feature flags; GPU lane masks; bloom-filter bit operations",
 "State compression"),

("Design under constraints: iterators, lazy evaluation, rate limits",
 "Design/simulation","Amortized design; lazy vs eager work; iterator cost analysis",
 "NO","-",0,
 "Untimed","1 hint @20min",
 "LC 341 Flatten Nested List Iterator","M",25,
 "LC 359 Logger Rate Limiter","M",20,
 "LC 137 Single Number II",
 "State the amortized cost of your iterator and why worst-case next() is not O(1)",
 "Was amortized reasoning explicit and stated, or hand-waved?",
 "API rate limiting; streaming iterators; data-loader prefetch in ML training",
 "Amortized design"),

("Blind mix: pick structures from API requirements, not from habit",
 "Blind (design)","Requirement -> structure mapping; API analysis",
 "NO","-",0,
 "Timed-60","None",
 "LC 981 Time Based Key-Value Store","M",25,
 "LC 355 Design Twitter","H",40,
 "LC 460 LFU Cache",
 "Write the requirement -> structure -> complexity table you used for each design",
 "Did each structure choice come from a stated API requirement? If not, that is F4.",
 "Versioned KV store = MVCC; social feed fanout = merge of k sorted streams",
 "API-driven design"),

("Week 6 assessment + MOCK INTERVIEW #1 (2 hints allowed, narrate everything)",
 "Mock interview #1","Verbal reasoning under observation; explanation quality",
 "NO","-",0,
 "Timed-45","2 hints max",
 "Mock #1: 1 medium problem, narrate every decision aloud, state TC/SC unprompted","M",45,
 "WeeklyAssessment + MockInterviews row","-",20,
 "ReviewQueue top 3",
 "Explain LRU aloud in 3 minutes with no notes; record yourself and listen back once",
 "Score explanation quality 1-5. Silent thinking during a mock is a failure mode.",
 "-",
 "Communication under pressure"),

# --- WEEK 7: Recursion & Trees -------------------------------------------------

("Recursion contracts: write exactly what your function returns, before coding",
 "Tree recursion (contract)","Write the contract; trust the recursion; call stack mental model",
 "YES","Recursion as contract + call stack",25,
 "Untimed","Tutorial before",
 "LC 104 Maximum Depth of Binary Tree","E",10,
 "LC 110 Balanced Binary Tree","E",20,
 "LC 981 Time Based Key-Value Store",
 "Write the exact return contract (in plain English) for every recursive function today",
 "Contract before code, or code until tests pass? Be honest.",
 "Recursive dependency evaluation; nested config resolution in ML pipeline systems",
 "Recursive decomposition"),

("The return-more-than-the-answer trick  -  post-order aggregation",
 "Tree DP (post-order)","Return value upward vs answer updated AT the node  -  these are different",
 "NO","-",0,
 "Untimed","1 hint @25min",
 "LC 543 Diameter of Binary Tree","E",25,
 "LC 124 Binary Tree Maximum Path Sum","H",35,
 "LC 110 Balanced Binary Tree",
 "Explain the difference between 'best path through this node' and 'best downward path from this node'",
 "Did you separate the two quantities BEFORE coding?",
 "Aggregating metrics up a topology/ownership tree in a distributed system",
 "Post-order aggregation"),

("BST invariant: the ordering IS the information",
 "BST/ordering","Range constraints propagated top-down; in-order traversal is sorted",
 "NO","-",0,
 "Untimed","1 hint",
 "LC 98 Validate Binary Search Tree","M",25,
 "LC 230 Kth Smallest Element in a BST","M",20,
 "LC 124 Binary Tree Maximum Path Sum",
 "State the (low, high) range-invariant proof; construct the input that breaks parent-child comparison alone",
 "Did you exploit the ordering property, or brute-force with a set?",
 "Ordered indexes; range scans; B-tree node invariants",
 "Invariant exploitation"),

("Tree construction and structural identity",
 "Tree recursion (construct)","Split by root; index map removes linear search; O(n) construction",
 "NO","-",0,
 "Untimed","1 hint @25min",
 "LC 105 Construct Tree from Preorder and Inorder","M",35,
 "LC 572 Subtree of Another Tree","E",20,
 "LC 98 Validate BST",
 "State TC before and after adding the inorder index map; verify correctness on an example",
 "Did you find the O(n) version yourself, or need a hint?",
 "Serialization formats; tree/config diffing; AST construction in compilers",
 "Recursive construction"),

("BFS on trees; designing an encoding for serialization",
 "BFS levels/serialization","Level-order state; null markers as an encoding decision; grammar first",
 "NO","-",0,
 "Untimed","1 hint @25min",
 "LC 199 Binary Tree Right Side View","M",20,
 "LC 297 Serialize and Deserialize Binary Tree","H",35,
 "LC 105 Construct Tree from Preorder and Inorder",
 "Rebuild serialize/deserialize from memory; define the encoding grammar BEFORE coding",
 "Did you define the encoding format before writing any code, or improvise?",
 "Wire formats; checkpoint serialization; graph snapshotting in ML systems",
 "Encoding design"),

("Blind tree mix: DFS or BFS, and why  -  state your reason before implementing",
 "Blind (trees)","Traversal choice driven by what information you need",
 "NO","-",0,
 "Timed-50","None",
 "LC 236 Lowest Common Ancestor","M",25,
 "LC 1448 Count Good Nodes in Binary Tree","M",20,
 "LC 297 Serialize and Deserialize Binary Tree",
 "Write a 3-line DFS-vs-BFS decision rule you will actually use from today",
 "First-try correctness on both? Log time-to-pattern.",
 "Ancestor/ownership queries in dependency trees; LCA in job-graph analysis",
 "Traversal selection"),

("Week 7 assessment  -  tree retention with zero notes",
 "Review/audit","Deep tree retention check",
 "NO","-",0,
 "Untimed","None",
 "Retest 3 tree problems from W7, no notes","M",45,
 "WeeklyAssessment","-",20,
 "ReviewQueue top 3",
 "Rederive diameter (LC 543) and max-path-sum (LC 124) from scratch; write both contracts first",
 "Has the 'write the contract first' habit actually formed? Show evidence.",
 "-",
 "Retention"),

# --- WEEK 8: Tries, Cross-Pattern Fusion, Diagnostic 2 ------------------------

("Tries: exploit shared prefixes; know when a trie is NOT worth it",
 "Trie","Character-indexed tree; memory vs lookup trade-off vs hashset",
 "YES","Trie construction and use",20,
 "Untimed","Tutorial before",
 "LC 208 Implement Trie (Prefix Tree)","M",25,
 "LC 139 Word Break","M",30,
 "LC 236 Lowest Common Ancestor",
 "Compare trie vs hashset on memory and lookup TC; name a concrete case where hashset wins",
 "Do you know the TRADE-OFF, or just that tries exist?",
 "Autocomplete; tokenizer vocabularies; longest-prefix-match routing in networking",
 "Structure trade-offs"),

("Trie + DFS: pruning is the entire point",
 "Trie + backtracking","Prune the search space using shared prefix structure",
 "NO","-",0,
 "Untimed","1 hint @30min",
 "LC 212 Word Search II","H",45,
 "LC 211 Design Add and Search Words Data Structure","M",25,
 "LC 208 Implement Trie",
 "Explain precisely how the trie prunes DFS branches and what the TC bound becomes with pruning",
 "Did you see pruning as the PURPOSE of the trie, or bolt it on afterwards?",
 "Prefix routing tables; vocabulary matching in tokenizers and NLP pipelines",
 "Search pruning"),

("Cross-pattern fusion: trees + prefix hashing (week-1 reappears in trees)",
 "Tree recursion + prefix-hash","Prefix sums along root-to-node path; undo the count on backtrack",
 "NO","-",0,
 "Untimed","1 hint @25min",
 "LC 437 Path Sum III","M",35,
 "LC 337 House Robber III","M",30,
 "LC 212 Word Search II",
 "Explain the path-prefix map and why you must DECREMENT on the way back up the recursion",
 "Did you connect week-1 prefix hashing to trees ON YOUR OWN?",
 "Hierarchical cost accounting; per-path aggregation in distributed tracing",
 "Cross-pattern fusion"),

("Interleaving weeks 1-7, hard-leaning, unlabelled, timed",
 "Blind (W1-W7 cross)","Full-range transfer recognition; unfamiliar problem structure",
 "NO","-",0,
 "Timed-60","None",
 "LC 549 Binary Tree Longest Consecutive Sequence II","M",30,
 "LC 987 Vertical Order Traversal of a Binary Tree","H",35,
 "LC 437 Path Sum III",
 "For each: which EARLIER pattern did it reuse? Name it explicitly.",
 "Cross-week transfer is the real test of retention vs surface memorisation.",
 "-",
 "Transfer"),

("Explanation training: compress 5 patterns to 90 seconds each  -  verbal clarity",
 "Communication","Compression forces genuine understanding; verbal explanation tests mastery",
 "NO","-",0,
 "Timed-40","None",
 "Explain 5 patterns aloud, recorded, 90s each (trigger, insight, invariant, TC)","-",30,
 "Retest 1 hard problem while narrating continuously","H",40,
 "ReviewQueue top 3",
 "No-notes verbal explanation of monotonic-stack amortization and BS-on-answer validity",
 "Would a sceptical interviewer follow your explanation? Listen to the recording once.",
 "Design reviews; RFC defence; on-call handover documentation",
 "Verbal clarity"),

("Failure-driven repair day  -  repair, do not explore new territory",
 "Targeted repair","Fix the failure category, not a new pattern",
 "NO","-",0,
 "Untimed","Hints allowed",
 "3 problems from your worst 2 failure categories","M",50,
 "Write/refresh preventive rules in FailureLog","-",20,
 "All Mastered=No from W5-W7",
 "Restate your 5 preventive rules from memory; verify they fired during today's solving",
 "Did the rules actually prevent the mistake? Rules that never fire are decoration.",
 "-",
 "Error correction"),

("MONTH 2 DIAGNOSTIC  -  3 unlabelled, 100 min, verbal + complexity required",
 "Diagnostic","Measure against Month 1. No pattern labels. No hints.",
 "NO","-",0,
 "Diagnostic","None",
 "LC 315 Count of Smaller Numbers After Self","H",34,
 "LC 1110 Delete Nodes and Return Forest","M",33,
 "LC 1396 Design Underground System (unlabelled)","M",33,
 "Log time-to-pattern, TC/SC, hints used, explanation quality for each",
 "Compare ALL numbers to Month 1. Time-to-pattern must be dropping. If not, recognition training increases.",
 "-",
 "Progress measurement"),

# --- WEEK 9: Graphs + Union Find ----------------------------------------------

("Graph modelling: what are the nodes and edges  -  model FIRST, algorithm second",
 "Graph traversal","Grid-as-graph; visited discipline  -  mark on PUSH, not on pop",
 "YES","Graph representations + BFS/DFS; visited discipline",25,
 "Untimed","Tutorial before",
 "LC 200 Number of Islands","M",25,
 "LC 133 Clone Graph","M",25,
 "LC 437 Path Sum III",
 "State when to mark visited (push vs pop); construct the input that causes exponential blowup if wrong",
 "Did you avoid revisit bugs by design, or by luck?",
 "Topology discovery; cluster membership; service-graph crawling in MLOps",
 "Graph modelling"),

("Multi-source BFS and reversing the direction of thought",
 "BFS (multi-source/reverse)","Seed all sources at level 0; think from the boundary inward",
 "NO","-",0,
 "Untimed","1 hint @20min",
 "LC 994 Rotting Oranges","M",25,
 "LC 417 Pacific Atlantic Water Flow","M",30,
 "LC 200 Number of Islands",
 "Explain why multi-source BFS is still O(V+E); why reverse traversal simplifies LC 417",
 "Did you reverse the direction yourself, or brute-force per cell?",
 "Failure propagation / blast-radius analysis in a distributed cluster",
 "Direction inversion"),

("Union-Find: connectivity without full traversal  -  write it cold in 5 minutes",
 "Union Find","Path compression + union by size; near-O(1) amortized; write it from memory",
 "YES","DSU with both optimizations (path compression + union by size)",25,
 "Untimed","Tutorial before",
 "LC 547 Number of Provinces","M",20,
 "LC 684 Redundant Connection","M",25,
 "LC 994 Rotting Oranges",
 "Write DSU from memory in under 5 minutes; state amortized complexity; why compression alone is insufficient",
 "Can you write DSU cold? It reappears in weeks 10 and 13.",
 "Cluster membership; shard grouping; entity dedup; dynamic connectivity under edge streams",
 "Near-O(1) connectivity"),

("DSU for grouping and incremental connectivity  -  when DSU beats repeated BFS",
 "Union Find (advanced)","DSU with labels; offline/incremental processing; streaming edge sets",
 "NO","-",0,
 "Untimed","1 hint @30min",
 "LC 721 Accounts Merge","M",35,
 "LC 827 Making a Large Island","H",40,
 "LC 547 Number of Provinces",
 "Explain why DSU beats repeated BFS when edges ARRIVE over time",
 "Right structure for a streaming edge set? Distinguish this from F4.",
 "Incremental cluster formation; dynamic membership in ML job schedulers",
 "Incremental algorithms"),

("Topological order: dependency resolution  -  know TWO implementations",
 "Topological sort","Kahn's in-degree invariant; DFS colours for cycle detection",
 "YES","Topo sort: Kahn + DFS colours; cycle detection in both",20,
 "Untimed","Tutorial before",
 "LC 207 Course Schedule","M",25,
 "LC 210 Course Schedule II","M",25,
 "LC 721 Accounts Merge",
 "State the in-degree invariant; explain cycle detection in BOTH Kahn and DFS-colours",
 "Do you know two implementations, or one memorised loop?",
 "DAG job scheduling; build systems; ML pipeline orchestration (Airflow-style DAGs)",
 "Dependency reasoning"),

("Blind graph mix: traversal vs DSU vs topological  -  from problem shape only",
 "Blind (graphs)","Selecting the graph tool from the structure of the question",
 "NO","-",0,
 "Timed-60","None",
 "LC 269 Alien Dictionary","H",45,
 "LC 310 Minimum Height Trees","M",30,
 "LC 210 Course Schedule II",
 "Which exact signal told you 'topological'? Which told you 'peel leaves layer by layer'?",
 "Recognition speed on graphs  -  log both times.",
 "Version-ordering inference; dependency inference from build observations",
 "Recognition"),

("Week 9 assessment  -  graph retention",
 "Review/audit","Graph retention without notes",
 "NO","-",0,
 "Untimed","None",
 "Retest 3 graph problems, no notes","M",45,
 "WeeklyAssessment","-",20,
 "ReviewQueue top 3",
 "Rebuild Kahn's algorithm and DSU from a blank file; both under 10 minutes total",
 "Score graph modelling 1-5. Modelling errors cause more graph failures than algorithm errors.",
 "-",
 "Retention"),

# --- WEEK 10: Shortest Paths + State-Space -------------------------------------

("Unweighted shortest path = BFS  -  prove why first-visit is final",
 "BFS shortest path","Layered distances; first-visit optimality argument; state-graph edge count",
 "NO","-",0,
 "Untimed","1 hint @25min",
 "LC 127 Word Ladder","H",40,
 "LC 752 Open the Lock","M",30,
 "LC 269 Alien Dictionary",
 "Explain why the first time BFS reaches a node the distance is final; state the implicit-graph edge count",
 "Was your bottleneck the modelling (edges) or the search algorithm?",
 "Network hop counts; dependency depth; minimum transformation steps in config migration",
 "State-graph modelling"),

("State-space search: state is more than position",
 "State-space BFS","Compound state encoding; visited MUST be keyed on the FULL state",
 "YES","State-space search and encoding",20,
 "Untimed","Tutorial before",
 "LC 1293 Shortest Path in Grid with Obstacles Elimination","H",40,
 "LC 433 Minimum Genetic Mutation","M",25,
 "LC 127 Word Ladder",
 "Write your state tuple, count the state space size, and derive TC from the count",
 "Was visited keyed on the FULL state? This single mistake invalidates most attempts.",
 "Scheduler/config state exploration; rollout planning in deployment systems",
 "State design"),

("Dijkstra: greedy + priority queue  -  know the correctness proof",
 "Dijkstra","Relaxation; popped distance is final (requires non-negative weights)",
 "YES","Dijkstra: correctness proof and implementation",25,
 "Untimed","Tutorial before",
 "LC 743 Network Delay Time","M",30,
 "LC 1514 Path with Maximum Probability","M",25,
 "LC 752 Open the Lock",
 "Prove the popped-node invariant; construct a negative-weight counterexample",
 "Do you know WHY negative edges break Dijkstra? If not, you memorised an implementation.",
 "Latency-aware routing; cost-based placement; weighted service-dependency graphs",
 "Weighted shortest path"),

("[2-SOL] Dijkstra variants: change the objective  -  min-max, 0-1 BFS",
 "Dijkstra variants/0-1 BFS","Min-max objectives; deque BFS for 0/1 weights; binary-search + BFS alternative",
 "NO","-",0,
 "Untimed","1 hint @30min",
 "LC 778 Swim in Rising Water","H",40,
 "LC 1631 Path with Minimum Effort","M",30,
 "LC 743 Network Delay Time",
 "Contrast sum-objective vs min-max objective; give binary-search+BFS alternative and its TC",
 "Did you find the second solution (BS + BFS) as well?",
 "Bottleneck-bandwidth routing; worst-link-aware placement in distributed ML clusters",
 "Objective transformation"),

("Constrained shortest paths: layers = DP over rounds",
 "Shortest path (constrained)","Bellman-Ford rounds; k-stop constraint as a DP dimension",
 "NO","-",0,
 "Untimed","1 hint @25min",
 "LC 787 Cheapest Flights Within K Stops","M",35,
 "LC 332 Reconstruct Itinerary","H",35,
 "LC 778 Swim in Rising Water",
 "Explain why exactly k+1 relaxation rounds solve the k-stop constraint; state the full DP state",
 "Did you see it as DP over layers rather than 'Dijkstra with a hack'?",
 "Multi-hop routing under hop limits; bounded-retry path planning",
 "DP-graph bridge"),

("Blind hard mix: graphs + earlier patterns, hard-leaning",
 "Blind (hard W1-W10)","Full-range recognition under time; composure on hards",
 "NO","-",0,
 "Timed-60","None",
 "LC 773 Sliding Puzzle","H",45,
 "LC 802 Find Eventual Safe States","M",25,
 "LC 787 Cheapest Flights Within K Stops",
 "For each: name the invariant the solution depends on, in one sentence",
 "Independent solve rate on hard problems  -  this is now tracked.",
 "-",
 "Hard-problem composure"),

("Week 10 assessment + MOCK INTERVIEW #2 (1 hint, 45 min)",
 "Mock interview #2","Medium-hard under pressure with narration",
 "NO","-",0,
 "Timed-45","1 hint max",
 "Mock #2: 1 medium-hard problem, narrate everything, state TC/SC, answer 1 follow-up","H",45,
 "WeeklyAssessment + failure clustering","-",25,
 "ReviewQueue top 3",
 "Explain Dijkstra in 2 minutes including why a priority queue is required",
 "Score TC/SC accuracy under pressure. Pressure-only errors are F10  -  they need mock reps, not theory.",
 "-",
 "Pressure performance"),

# --- WEEK 11: Backtracking -----------------------------------------------------

("Backtracking skeleton: choose/explore/unchoose  -  count the leaves for TC",
 "Backtracking","Decision tree; state restoration; count tree leaves to derive TC",
 "YES","Backtracking template + complexity counting",25,
 "Untimed","Tutorial before",
 "LC 78 Subsets","M",20,
 "LC 39 Combination Sum","M",25,
 "LC 802 Find Eventual Safe States",
 "Draw the recursion tree for a small input; count nodes/leaves; derive TC from the count",
 "Can you compute backtracking complexity? Writing 'exponential' and hoping is not enough.",
 "Config/hyperparameter enumeration; feasible-placement search in resource allocators",
 "Enumeration control"),

("Duplicate handling and canonical order in backtracking",
 "Backtracking (dedup)","Sort + skip-equal-at-same-depth rule; prove no distinct result is lost",
 "NO","-",0,
 "Untimed","1 hint",
 "LC 90 Subsets II","M",25,
 "LC 47 Permutations II","M",25,
 "LC 39 Combination Sum",
 "State the dedup rule precisely and argue no distinct result is lost",
 "Did you DERIVE the skip rule, or copy it from memory? Copied rules fail on variants.",
 "Deduplicating equivalent job configs; canonical representation of equivalent placements",
 "Canonical enumeration"),

("Pruning: the actual skill in backtracking  -  design it up front",
 "Backtracking (pruning)","Constraint propagation; ordering heuristics; early exit conditions",
 "NO","-",0,
 "Untimed","1 hint @25min",
 "LC 51 N-Queens","H",35,
 "LC 131 Palindrome Partitioning","M",30,
 "LC 90 Subsets II",
 "List every pruning rule and estimate its effect on the search-tree size",
 "Was pruning designed up front, or added reactively after a timeout?",
 "Constraint solvers; packing/placement with conflict constraints in cluster schedulers",
 "Pruning design"),

("Grid backtracking + bitmask constraint tracking",
 "Backtracking (grid)","Row/col/box bitmasks for O(1) legality checks; TC bound estimation",
 "NO","-",0,
 "Untimed","1 hint @30min",
 "LC 37 Sudoku Solver","H",45,
 "LC 79 Word Search","M",25,
 "LC 51 N-Queens",
 "Explain bitmask constraint tracking; give a defensible TC bound with pruning factored in",
 "Did you reuse week-6 bitmask thinking here WITHOUT being told to?",
 "Resource placement under conflict constraints; topology-aware scheduling in ML clusters",
 "Constraint encoding"),

("Blind mix: exponential backtracking vs polynomial DP vs greedy",
 "Blind (paradigm choice)","Deciding the PARADIGM before the algorithm; recognise when memo helps",
 "NO","-",0,
 "Timed-60","None",
 "LC 698 Partition to K Equal Sum Subsets","M",40,
 "LC 17 Letter Combinations of a Phone Number","M",20,
 "LC 37 Sudoku Solver",
 "Explain why memoization helps one of these problems and not the other",
 "Correct paradigm chosen FIRST, or did you thrash between two options?",
 "Bin packing for GPU/memory allocation; NP-hard scheduling approximations",
 "Paradigm selection"),

("The recursion -> memoization bridge: overlapping subproblems + state identification",
 "Memoization/state identification","Spot overlapping subproblems; name the state; count distinct states",
 "YES","From recursion to memo: state identification (the entry gate to all DP)",20,
 "Untimed","Tutorial before",
 "LC 140 Word Break II","H",35,
 "LC 494 Target Sum","M",25,
 "LC 698 Partition to K Equal Sum Subsets",
 "For each: write the state, count distinct states, derive memoized TC",
 "How quickly do you spot overlapping subproblems? This skill gates all of DP.",
 "Compilation/plan caches; memoizing expensive model inferences",
 "State identification"),

("Week 11 assessment  -  backtracking retention",
 "Review/audit","Backtracking retention check",
 "NO","-",0,
 "Untimed","None",
 "Retest N-Queens + 2 others from W11, no notes","H",50,
 "WeeklyAssessment","-",20,
 "ReviewQueue top 3",
 "Rebuild the backtracking skeleton and the dedup rule from memory",
 "Is pruning reasoning present in your retests, or did you regress to brute enumeration?",
 "-",
 "Retention"),

# --- WEEK 12: DP First Principles + Diagnostic 3 ------------------------------

("DP as a graph of states: the 5-step method before any code",
 "DP (1D)","State, transition, base case, evaluation order, answer location  -  in that ORDER",
 "YES","DP state design (5-step method, not templates)",30,
 "Untimed","Tutorial before",
 "LC 70 Climbing Stairs + LC 198 House Robber","E",25,
 "LC 91 Decode Ways","M",30,
 "LC 494 Target Sum",
 "Write the 5-step form for ALL THREE problems before coding any of them",
 "Did you define the STATE before the transition? Reversing causes most DP failures.",
 "Cost-optimal pipeline/config selection over stages; stage-wise optimisation",
 "DP formalism"),

("Subsequence DP and the O(n log n) upgrade  -  two solutions required",
 "DP (LIS family)","O(n^2) DP  ->  patience/tails + binary search; what tails[i] means",
 "NO","-",0,
 "Untimed","1 hint @30min",
 "LC 300 Longest Increasing Subsequence","M",35,
 "LC 354 Russian Doll Envelopes","H",40,
 "LC 91 Decode Ways",
 "Explain the tails array, what tails[i] MEANS, and why binary search is valid",
 "Two solutions with different complexities? Both must be explainable.",
 "Version/compatibility chains; monotone scheduling sequences",
 "DP optimization"),

("Knapsack family: capacity as a dimension  -  understand loop order",
 "DP (knapsack)","0/1 vs unbounded; what iteration direction MEANS; 1D rolling array",
 "YES","Knapsack variants and loop order (not the formula  -  the reasoning)",25,
 "Untimed","Tutorial before",
 "LC 416 Partition Equal Subset Sum","M",30,
 "LC 322 Coin Change","M",25,
 "LC 300 Longest Increasing Subsequence",
 "Explain why 1D 0/1 knapsack iterates capacity DESCENDING, using a concrete failing example",
 "Understanding of loop order, or memorised direction? Construct the failing test.",
 "Memory/GPU packing; budget and quota allocation across multiple dimensions",
 "Dimension design"),

("Knapsack in disguise: reduction practice",
 "DP (knapsack variants)","Rewrite the problem as: items, weights, capacity, value, objective",
 "NO","-",0,
 "Untimed","1 hint @25min",
 "LC 518 Coin Change II","M",25,
 "LC 474 Ones and Zeroes","M",30,
 "LC 322 Coin Change",
 "Write the explicit mapping for BOTH problems: items / weights / capacity / value / objective",
 "Did you spot the disguise independently, or start from scratch?",
 "Multi-resource quota allocation (CPU+RAM+GPU as two capacity dimensions)",
 "Problem reduction"),

("Two-sequence DP: alignment states over prefixes of both inputs",
 "DP (2 sequences)","dp[i][j] over prefixes of both sequences; derive transitions from the definition",
 "NO","-",0,
 "Untimed","1 hint @25min",
 "LC 1143 Longest Common Subsequence","M",25,
 "LC 72 Edit Distance","M",35,
 "LC 518 Coin Change II",
 "Explain each Edit Distance transition in words; DERIVE them from the definition, do not recall them",
 "Could you rebuild the transitions from the problem definition alone?",
 "Diffing; log alignment; tokenizer/sequence alignment in NLP systems",
 "2D state design"),

("Space optimization in DP  -  which previous states does the transition need?",
 "DP (space optimization)","Rolling arrays; dependency direction determines what rows you can drop",
 "NO","-",0,
 "Untimed","1 hint",
 "Rewrite LC 72 Edit Distance in O(min(m,n)) space","M",25,
 "LC 63 Unique Paths II + LC 64 Minimum Path Sum","M",25,
 "LC 72 Edit Distance",
 "State exactly which previous states each transition needs; then justify the rolling array",
 "SC reduced without breaking correctness? Verify on the maximum-size test case.",
 "Memory-bound kernels; buffer reuse; activation checkpointing intuition in training",
 "Space optimization"),

("MONTH 3 DIAGNOSTIC  -  3 unlabelled, 110 min, full interview conditions",
 "Diagnostic","Full interview conditions. No labels. No hints. Verbal + TC/SC required.",
 "NO","-",0,
 "Diagnostic","None",
 "LC 1383 Maximum Performance of a Team","H",37,
 "LC 1326 Minimum Taps to Water a Garden","H",37,
 "LC 2092 Find All People With Secret (unlabelled)","H",36,
 "Log every metric; compare Months 1, 2, 3 side by side in MockInterviews",
 "Use results to choose weak-pattern targets for weeks 13-14. Follow the data, not the plan blindly.",
 "-",
 "Measurement"),

# --- WEEK 13: Advanced DP ------------------------------------------------------

("Interval DP: build answers from small ranges  -  choose the LAST operation",
 "DP (interval)","Iterate by LENGTH; pick the LAST operation to keep subproblems independent",
 "YES","Interval DP: why last operation, not first",20,
 "Untimed","1 hint @30min",
 "LC 312 Burst Balloons","H",45,
 "LC 516 Longest Palindromic Subsequence","M",25,
 "LC 63 Unique Paths II",
 "Explain why we iterate by length AND why 'last balloon burst' makes subproblems independent",
 "Did you find the reversal insight yourself? That insight IS the entire problem.",
 "Optimal chunking / merge ordering; compaction cost minimisation in storage systems",
 "Interval reasoning"),

("DP on trees and DAGs  -  memoisation is valid exactly when the state graph is acyclic",
 "DP (tree/DAG)","Memoisation valid on DAGs; acyclicity must be verified, not assumed",
 "NO","-",0,
 "Untimed","1 hint @25min",
 "LC 329 Longest Increasing Path in a Matrix","H",35,
 "LC 979 Distribute Coins in Binary Tree","H",35,
 "LC 312 Burst Balloons",
 "Explain why memoisation works on a DAG but not on a general graph; verify acyclicity in LC 329",
 "Did you CHECK acyclicity, or assume it?",
 "Critical-path computation in ML pipeline DAGs; longest-path scheduling",
 "DP-graph fusion"),

("Bitmask DP: subsets as states  -  n<=20 is the signal",
 "DP (bitmask)","2^n states; (mask, position) state; transition over bits",
 "YES","Bitmask DP: state design and TC derivation",20,
 "Untimed","1 hint @30min",
 "LC 847 Shortest Path Visiting All Nodes","H",45,
 "LC 473 Matchsticks to Square","M",30,
 "LC 329 Longest Increasing Path in Matrix",
 "Compute the exact state count and TC; explain the (mask, position) state for LC 847",
 "Did n<=20 immediately suggest bitmask? Constraint-reading is the entire skill here.",
 "Job-to-machine assignment; small-scale optimal placement in resource schedulers",
 "Constraint-driven recognition"),

("DP optimization: monotonic deque inside a DP transition  -  week-2 reappears",
 "DP + monotonic deque","Sliding-window maximum hidden inside a DP recurrence; O(nk) -> O(n)",
 "NO","-",0,
 "Untimed","1 hint @30min",
 "LC 1696 Jump Game VI","M",30,
 "LC 1425 Constrained Subsequence Sum","H",40,
 "LC 847 Shortest Path Visiting All Nodes",
 "Write naive O(nk) transition first, then deque-optimised O(n) version; prove equivalence",
 "Did you see the sliding window HIDDEN inside the DP? That is week-2 reappearing in week-13.",
 "Streaming DP with bounded lookback; windowed online decisions in scheduling",
 "Transition optimization"),

("Counting DP and bounding the state space",
 "DP (counting)","Count configurations; prune impossible states; modular arithmetic",
 "NO","-",0,
 "Untimed","1 hint @25min",
 "LC 1269 Number of Ways to Stay in Same Place","H",35,
 "LC 1220 Count Vowels Permutation","H",30,
 "LC 1425 Constrained Subsequence Sum",
 "Explain the state bound (why positions beyond steps/2 are unreachable) and the modular arithmetic",
 "Did you bound the state space, or allocate a giant table and hope?",
 "Counting valid configurations / reachable states in a job scheduler or planner",
 "State bounding"),

("Blind HARD mix: full range, 90 minutes  -  peak capability test",
 "Blind (hard W1-W13)","Maximum capability test; no labels; no hints",
 "NO","-",0,
 "Timed-90","None",
 "LC 1235 Maximum Profit in Job Scheduling (unlabelled)","H",45,
 "LC 862 Shortest Subarray with Sum at Least K (unlabelled)","H",45,
 "LC 312 Burst Balloons",
 "Time-to-pattern for both; write PatternCards entries for any pattern you failed to recognise",
 "Independent solve on a hard, unlabelled, timed problem  -  the actual target behaviour.",
 "-",
 "Peak capability"),

("Week 13 assessment + reconstruction marathon  -  consolidation",
 "Review/consolidation","Deep retention audit across all 13 weeks",
 "NO","-",0,
 "Untimed","None",
 "Reconstruct 6 anchor problems from memory  -  code, no notes","H",60,
 "WeeklyAssessment + update PatternLibrary mastery honestly","-",25,
 "ReviewQueue top 5",
 "Fill PatternCards for every pattern rated below mastery 4",
 "Which patterns are still fragile? Those, and ONLY those, get week-14 repair time.",
 "-",
 "Consolidation"),

# --- WEEK 14: Interview Simulation --------------------------------------------

("MOCK INTERVIEW #3  -  no hints, verbal reasoning required throughout",
 "Mock interview #3","Full simulation with follow-up; narrate every decision",
 "NO","-",0,
 "Timed-50","None",
 "Mock #3: 1 medium + 1 hard follow-up question, narrated","H",50,
 "Self-review the recording against a rubric","-",20,
 "ReviewQueue top 3",
 "Rewrite the solution cleanly after the mock; note every place you stalled verbally",
 "Where did communication break down: restatement, approach pitch, or complexity explanation?",
 "-",
 "Interview execution"),

("Weak-pattern repair using mock + diagnostic data  -  repair, not exploration",
 "Targeted repair (W14)","Repair the weakest pattern; evidence-driven, not intuition-driven",
 "NO","-",0,
 "Untimed","Hints allowed",
 "2 problems in your single weakest pattern from diagnostics","H",50,
 "Update preventive rules in FailureLog","-",15,
 "All Mastered=No rows",
 "Explain the weak pattern aloud for 2 minutes with no notes",
 "Did the repair hold on the SECOND problem? One success is noise.",
 "-",
 "Targeted repair"),

("Infra-flavoured design + algorithm session: build real systems",
 "Design + algorithms","Algorithms living inside production systems; bottleneck analysis at scale",
 "NO","-",0,
 "Untimed","None",
 "Design: in-memory feature cache with TTL + LRU eviction + metrics  -  implement core ops","H",45,
 "Design: DAG task scheduler with priorities + worker limits  -  implement the ready-queue core","H",40,
 "LC 146 LRU Cache",
 "For each design: list every data structure, its purpose, and the TC of each operation",
 "Could you defend these under 10x scale in an ML-infra systems interview?",
 "This IS the overlap between DSA and AI-infra engineering",
 "Systems-algorithm bridge"),

("MOCK INTERVIEW #4  -  unfamiliar hard, no hints, 45 min, follow-up required",
 "Mock interview #4","Unfamiliar problem under full pressure; decision timeline analysis",
 "NO","-",0,
 "Timed-45","None",
 "Mock #4: 1 unfamiliar hard from README pool","H",45,
 "Post-mortem: minute-by-minute decision timeline","-",25,
 "ReviewQueue top 3",
 "Write the decision timeline: what you thought at minutes 2, 5, 10, 20, 35",
 "Where did you waste minutes? Time allocation is a trainable interview skill.",
 "-",
 "Time allocation"),

("[2-SOL] Second-solution day  -  force fundamentally different paradigms",
 "Multi-solution flexibility","Prevent template lock; conditions favouring each approach",
 "NO","-",0,
 "Untimed","None",
 "Solve 2 previously-solved problems using a DIFFERENT paradigm (heap -> sort, DFS -> BFS, greedy -> DP, BS -> math)","H",45,
 "Compare TC/SC of both approaches and state when each is preferable","-",20,
 "ReviewQueue top 3",
 "Explain both solutions for both problems and the conditions favouring each",
 "Flexible, or template-locked? Template-locked candidates fail on variants.",
 "Trade-off analysis is core to ML system design documents",
 "Approach flexibility"),

("Pressure day: 3 problems in 75 minutes  -  endurance without accuracy collapse",
 "Blind (timed volume)","Throughput without correctness collapse; triage decisions",
 "NO","-",0,
 "Timed-75","None",
 "3 unlabelled problems (E/M/H) from hard pool  -  75 min total","H",75,
 "Failure clustering after","-",15,
 "-",
 "Rank by speed of pattern recognition; explain the fastest one's recognition cue",
 "Where did speed cost correctness? That is your real interview risk profile.",
 "-",
 "Endurance"),

("FINAL DIAGNOSTIC + design your own next 4-week cycle",
 "Diagnostic/planning","Exit measurement and self-directed plan v2",
 "NO","-",0,
 "Diagnostic","None",
 "Final diagnostic: LC 1751, LC 2421, LC 1463  -  110 min, unlabelled, no hints","H",110,
 "Write your own next 4-week plan driven purely by weakness data","-",30,
 "-",
 "Fill dashboard; compare all 4 diagnostics on time-to-pattern, hint-dependency, TC accuracy",
 "Are you at the 'derive unfamiliar problems' level? Cite concrete evidence.",
 "-",
 "Self-directed training"),


# --- WEEKS 15-24: Systems & AI-Infrastructure Specialization ---------
('Fenwick Tree (Binary Indexed Tree / BIT): point updates & prefix range sums',
 'Fenwick Tree (BIT)', 'Lowest set bit (i & -i); 1-indexed tree array; partial sum decomposition in O(log n)',
 'YES', 'Fenwick Tree (Binary Indexed Tree) from scratch', 25,
 'Untimed', '1 hint @20min',
 'LC 307 Range Sum Query - Mutable', 'M', 25,
 'LC 315 Count of Smaller Numbers After Self', 'H', 35,
 'LC 304 Range Sum Query 2D - Immutable',
 'Write BIT add(i, delta) and query(i) from memory in 6 lines of code; explain the (i & -i) math',
 'Did you prove why (i & -i) isolates the lowest set bit?',
 'Cumulative billing meters; live request frequency counters over rolling numeric IDs',
 'Logarithmic prefix tracking'),

('Segment Tree: arbitrary associative range queries (min, max, gcd, sum)',
 'Segment Tree (point update)', 'Binary tree over array ranges; node 2i and 2i+1; tree size 4n; divide-and-conquer range intersection',
 'YES', 'Segment Tree: point update and range query', 25,
 'Untimed', '1 hint @20min',
 'LC 307 Range Sum Query - Mutable (Segment Tree solution)', 'M', 25,
 'LC 732 My Calendar III', 'H', 35,
 'LC 307 Range Sum Query - Mutable',
 'Implement SegmentTree.build(), update(), query() from memory with 0 syntax errors',
 'Why is the array representation size 4n instead of 2n? Derive it.',
 'Distributed SLA monitoring; finding max latency spike in arbitrary time intervals',
 'Associative range aggregation'),

('Segment Tree with Lazy Propagation: range update and range query in O(log n)',
 'Segment Tree (lazy propagation)', 'Deferring updates to children using a lazy tag; push-down before recursing; range addition',
 'YES', 'Lazy Propagation in Segment Trees explained', 25,
 'Untimed', '1 hint @20min',
 'LC 218 The Skyline Problem', 'H', 40,
 'LC 699 Falling Squares', 'H', 35,
 'LC 732 My Calendar III',
 'Write the push_down(node, l, r) invariant: what must hold before visiting child nodes?',
 'Did you trace push_down on a pen-and-paper interval tree before coding?',
 'Dynamic memory allocation tracking; continuous physical page range reservation',
 'Deferred range modification'),

('Disjoint Interval Maintenance & Coordinate Compression',
 'Interval / TreeMap composition', 'TreeMap / Balanced BST for non-overlapping interval ranges; merge adjacent; coordinate mapping',
 'NO', '-', 0,
 'Untimed', '1 hint @20min',
 'LC 715 Range Module', 'H', 40,
 'LC 352 Data Stream as Disjoint Intervals', 'M', 25,
 'LC 218 The Skyline Problem',
 'Explain why TreeMap.floorEntry() and subMap() make interval removal O(k log n)',
 'Can you state the boundary invariants when removing a range [left, right) cleanly?',
 'Virtual memory mapping (VMA) merging and splitting in kernel memory managers',
 'Dynamic range tracking'),

('Interleave range patterns: Blind session on mutable range operations',
 'Blind (range queries & trees)', 'Deciding between Fenwick, Segment Tree, Sweep Line, or TreeMap under ambiguity',
 'NO', '-', 0,
 'Untimed', 'No hints before 20min',
 'LC 1649 Create Sorted Array through Instructions', 'H', 35,
 'LC 327 Count of Range Sum', 'H', 40,
 'LC 715 Range Module',
 'For both problems, state whether Fenwick Tree or Merge Sort is asymptotically better and why',
 'Time-to-pattern on both problems (record minutes). Target: <7 min.',
 'Stream deduplication across numeric ranges; out-of-order packet ranking',
 'Range structure selection'),

('[2-SOL] Inversion counting & ranking: Segment Tree vs Fenwick Tree vs Divide & Conquer',
 'Multi-solution comparison', 'Comparing coordinate compression + BIT against Merge Sort divide-and-conquer',
 'NO', '-', 0,
 'Timed-60', 'None',
 'LC 493 Reverse Pairs', 'H', 35,
 'Find 2nd solution for LC 493 (Merge Sort vs BIT)', 'H', 25,
 'LC 315 Count of Smaller Numbers After Self',
 'Code both Merge Sort and BIT solutions for LC 493 from memory; compare cache efficiency',
 'Why does Merge Sort have better cache locality than a BIT on large coordinate spaces?',
 'Sorting algorithms for tensor strides; parallel rank reduction',
 'Dual-derivation fluency'),

('Week 15 audit: complete blank-editor reconstruction of BIT and Segment Tree',
 'Review/audit', 'Zero-notes retention of logarithmic range structures',
 'NO', '-', 0,
 'Untimed', 'Notes forbidden',
 'Rederive: BIT point-update + prefix-query cold', 'M', 25,
 'Rederive: Segment Tree build + query + lazy update cold', 'H', 35,
 'LC 1649 Create Sorted Array through Instructions',
 'Rebuild both data structures from scratch in raw code with complete test harness',
 'Can you implement a Segment Tree in an interview without looking at reference code?',
 'Self-contained systems data structures',
 'Core range mechanics'),

("Tarjan's Algorithm: Bridges, Articulation Points & Critical Connections",
 "Tarjan's DFS (tin / low)", 'Discovery time tin[u] vs lowest reachable ancestor low[u]; back-edge detection; bridge condition low[v] > tin[u]',
 'YES', "Tarjan's Algorithm for Bridges and Cut Vertices", 25,
 'Untimed', '1 hint @20min',
 'LC 1192 Critical Connections in a Network', 'H', 35,
 'LC 1568 Minimum Number of Days to Disconnect Island', 'H', 35,
 'LC 2092 Find All People With Secret',
 'Write the bridge condition from memory. Explain why parent edge is excluded from low[u] update',
 'Did you derive the difference between bridge condition (low[v] > tin[u]) and articulation condition (low[v] >= tin[u])?',
 'Single-point-of-failure (SPOF) detection in distributed microservice topologies',
 'Critical topology discovery'),

("Strongly Connected Components (SCC): Tarjan's & Kosaraju's Algorithm",
 'Graph SCC decomposition', 'Condensation DAG; two-pass Kosaraju (transpose graph) vs one-pass Tarjan with stack; component contracts',
 'YES', 'Strongly Connected Components: Tarjan & Kosaraju', 25,
 'Untimed', '1 hint @20min',
 'LC 1489 Find Critical and Pseudo-Critical Edges in MST', 'H', 40,
 'Condensation graph construction on directed graph', 'M', 25,
 'LC 1192 Critical Connections in a Network',
 'Explain how condensing a directed graph into an SCC DAG enables topological scheduling',
 'Can you explain why the condensation of any directed graph is always a DAG?',
 'Deadlock detection in distributed locking systems; circular dependency elimination in build graphs',
 'Cycle decomposition'),

("Eulerian Path & Circuit: Hierholzer's Algorithm",
 'Eulerian traversal', "Degree balance (in-degree == out-degree); Hierholzer's post-order DFS splice; visiting every edge exactly once",
 'YES', "Hierholzer's Algorithm for Eulerian Paths", 20,
 'Untimed', '1 hint @20min',
 'LC 332 Reconstruct Itinerary', 'H', 35,
 'LC 753 Cracking the Safe (De Bruijn sequence)', 'H', 35,
 'LC 1489 Find Critical and Pseudo-Critical Edges in MST',
 "Explain why Hierholzer's adds edges in reverse post-order to handle dead-end loops",
 'Did you explain the De Bruijn sequence graph model out loud?',
 'Complete network trace logging; memory bus traversal with zero redundant packet copies',
 'Edge-exhaustive routing'),

("Network Flows: Ford-Fulkerson, Edmonds-Karp & Dinic's Algorithm",
 'Max-Flow / Min-Cut', 'Residual graph; augmenting paths via BFS; max-flow min-cut theorem; bipartite matching equivalence',
 'YES', "Max Flow Min Cut: Edmonds-Karp & Dinic's", 25,
 'Untimed', '1 hint @20min',
 'LC 1349 Maximum Students Taking Exam (Bipartite matching / Max Flow formulation)', 'H', 40,
 'LC 1970 Last Day Where You Can Still Cross', 'H', 35,
 'LC 332 Reconstruct Itinerary',
 'State the Max-Flow Min-Cut theorem; derive why the capacity of the minimum cut equals max flow',
 'Can you transform a bipartite matching problem into a max-flow problem with source/sink?',
 'Cluster resource allocation; optimal network throughput routing across switch bisection bandwidth',
 'Capacity-constrained routing'),

('Blind Graph Topology Session: Bridges vs Flows vs DAGs',
 'Blind (advanced graphs)', 'Discriminating between structural decomposition and flow optimization',
 'NO', '-', 0,
 'Untimed', 'No hints before 20min',
 'LC 2127 Maximum Employees to Be Invited to a Meeting', 'H', 40,
 'LC 839 Similar String Groups', 'H', 30,
 'LC 1349 Maximum Students Taking Exam',
 'Write PatternCards entry for functional graphs (nodes with out-degree 1: cycle + trees)',
 'Time-to-pattern on LC 2127. Did you immediately spot the cycle + forest decomposition?',
 'Cluster leader election ring topologies; consensus quorum validation',
 'Complex graph decomposition'),

('Systems Simulation: Fault domains, network partition cuts, cluster failover graphs',
 'Systems graph modeling', 'Modeling datacenter racks, switches, and nodes as a graph; evaluating min-cut partition resilience',
 'NO', '-', 0,
 'Timed-45', 'None',
 'LC 924 Minimize Malware Spread', 'H', 35,
 'LC 928 Minimize Malware Spread II', 'H', 35,
 'LC 2127 Maximum Employees to Be Invited to a Meeting',
 'Explain the difference in removal impact between LC 924 and 928; state the connected component invariant',
 'Can you explain why node removal requires finding component unique-infectors?',
 'Fault blast-radius containment; blast-radius analysis in multi-region Kubernetes clusters',
 'Resilience topology modeling'),

('Milestone Diagnostic #4: Advanced Range Queries & Graph Topologies (3 unlabelled problems)',
 'Diagnostic', 'Performance under strict time limit on high-complexity problems',
 'NO', '-', 0,
 'Diagnostic', 'None',
 'Diagnostic 4: LC 315, LC 1192, LC 715 (unlabelled, 105 min)', 'H', 105,
 'Error log + weakness classification in FailureLog', '-', 25,
 '-',
 'Fill diagnostic score in MockInterviews; record time-to-pattern for each problem',
 'Did you identify the Tarjan / BIT / Interval invariants in under 6 minutes each?',
 'Systems interview diagnostic',
 'High-pressure synthesis'),

('Hardware Reality: Memory hierarchy, CPU cache lines (64 bytes), spatial vs temporal locality',
 'Hardware / Cache calibration', 'L1/L2/L3 cache latency vs RAM; cache-miss penalties; why B-Trees beat BSTs on modern CPUs; contiguous arrays',
 'YES', 'What Every Programmer Should Know About Memory (Algorithmic Summary)', 25,
 'Untimed', 'Tutorial only',
 'LC 498 Diagonal Traverse (Cache locality benchmark: row-major vs strided)', 'M', 25,
 'LC 566 Reshape the Matrix', 'E', 15,
 'LC 1192 Critical Connections in a Network',
 'Write down the latency hierarchy table: L1 (1ns), L2 (4ns), L3 (12ns), DRAM (60ns), SSD (10us), Network (1ms)',
 'Can you explain why traversing a 2D array column-by-column is 10x slower than row-by-row?',
 'Tensor memory strides, GPU shared-memory bank conflicts, cache-line bouncing',
 'Hardware-aware derivation'),

('Robin Hood Hashing & Cuckoo Hashing: Eliminating tail latency in hash tables',
 'High-performance hashing', 'Linear probing variance; Robin Hood displacement; Cuckoo two-hash constant O(1) worst-case lookups',
 'YES', 'Robin Hood & Cuckoo Hashing explained', 25,
 'Untimed', '1 hint @20min',
 'Design a Robin Hood Hash Map simulator with collision shift', 'M', 35,
 'LC 706 Design HashMap', 'E', 15,
 'LC 498 Diagonal Traverse',
 "Explain the 'take from the rich, give to the poor' probe length invariant",
 'Why does Robin Hood hashing dramatically reduce variance in query latency?',
 'High-throughput in-memory key-value caches (Memcached, Redis, RocksDB block cache)',
 'Collision minimization'),

('Radix Trees & Compressed Tries: Memory-efficient prefix lookups',
 'Radix tree / Patricia', 'Edge compression; path merging; space reduction from O(|alphabet| * N) to O(N); bitwise radix indexing',
 'YES', 'Radix Trees (Patricia Tries) in Linux Kernel & IP routing', 20,
 'Untimed', '1 hint @20min',
 'LC 421 Maximum XOR of Two Numbers in an Array', 'M', 30,
 'LC 1803 Count Pairs With XOR in a Range', 'H', 35,
 'LC 706 Design HashMap',
 'Explain how a 32-bit binary radix tree allows O(1) word-length XOR prefix queries',
 'Can you draw a compressed radix tree node vs standard trie node?',
 'Linux kernel page table lookups, CIDR network routing tables, subword vocabularies',
 'Prefix compression'),

('Bitsets & Bloom Filters: Probabilistic set membership with zero memory footprint',
 'Bloom filter / Bit manipulation', 'm-bit array with k independent hash functions; false positive rate formula (1 - e^(-kn/m))^k; no false negatives',
 'YES', 'Bloom Filters: Math, Mechanics & Applications in Big Data', 25,
 'Untimed', '1 hint @20min',
 'Implement a Bloom Filter with optimal k = (m/n) * ln(2)', 'M', 30,
 'LC 187 Repeated DNA Sequences (Bitmask hashing)', 'M', 25,
 'LC 421 Maximum XOR of Two Numbers in an Array',
 'Derive the optimal number of hash functions k for a Bloom filter given bit size m and element count n',
 'Why can a Bloom filter never yield a false negative? Explain the bitwise proof.',
 'SSTable disk-read avoidance in Cassandra/BigTable, web-crawler URL dedup, prompt cache filtering',
 'Probabilistic filtering'),

('Blind Cache-Conscious Session: Memory layout vs Pointer structures',
 'Blind (memory & search)', 'Evaluating pointer overhead (64-bit pointers) vs dense array representations',
 'NO', '-', 0,
 'Untimed', 'No hints before 20min',
 'LC 381 Insert Delete GetRandom O(1) - Duplicates allowed', 'H', 35,
 'LC 432 All O`one Data Structure', 'H', 40,
 'LC 187 Repeated DNA Sequences',
 'Write PatternCards entry for O(1) double-ended bucket structures',
 'Time-to-pattern on LC 432. Did you immediately recognize the doubly-linked bucket list + map?',
 'L1/L2 cache-friendly lookup tables; allocation-free collections',
 'Space-optimal design'),

('Systems Simulation: Designing a 10M QPS In-Memory Key-Value Index',
 'Systems algorithm design', 'Combining hash table, compact bitset, and contiguous page buffers for zero-copy lookups',
 'NO', '-', 0,
 'Timed-60', 'None',
 'LC 588 Design In-Memory File System', 'H', 35,
 'LC 1166 Design File System', 'M', 20,
 'LC 432 All O`one Data Structure',
 'Explain how trie-based paths map to inode structures in a distributed filesystem',
 'Did you analyze the lock granularity for path traversal vs leaf write?',
 'In-memory metadata servers (HDFS NameNode, Ceph MDS, Lustre MDT)',
 'Filesystem hierarchy modeling'),

('Week 17 audit: implement Bloom Filter and Radix XOR Tree cold with no reference',
 'Review/audit', 'Complete command of hardware-aligned and space-efficient structures',
 'NO', '-', 0,
 'Untimed', 'Notes forbidden',
 'Rederive: Bloom Filter class with bitarray & murmurhash simulation cold', 'M', 30,
 'Rederive: Binary Radix Tree for maximum XOR query cold', 'H', 35,
 'LC 588 Design In-Memory File System',
 'Write both classes in clean code; verify edge cases (empty input, full bitset saturation)',
 'Can you explain cache-locality tradeoffs to an infra architect convincingly?',
 'Hardware-aware algorithm mastery',
 'Systems memory fluency'),

('KMP (Knuth-Morris-Pratt): Prefix function pi and linear string matching',
 'KMP pattern matching', 'Longest proper prefix that is also suffix; deterministic state transitions; never backtracking the text pointer',
 'YES', 'KMP Algorithm: Prefix function and linear matching proof', 25,
 'Untimed', '1 hint @20min',
 'LC 28 Find the Index of the First Occurrence in a String', 'E', 15,
 'LC 214 Shortest Palindrome', 'H', 35,
 'LC 381 Insert Delete GetRandom O(1) - Duplicates',
 'Derive the prefix function pi computation loop from memory; explain the amortized O(n) argument',
 'Why does the j = pi[j-1] fallback guarantee we never decrement the main text pointer i?',
 'Deep packet inspection in networking switches; streaming sequence filtering in data ingestion',
 'Linear automaton matching'),

('Z-Algorithm & Polynomial Rolling Hash (Rabin-Karp)',
 'Z-algorithm / Rolling hash', 'Z-box [l, r] maintenance; segment matching; hash collisions; double hashing mod (10^9+7, 10^9+9)',
 'YES', 'Z-Algorithm and Rolling Hashes explained', 25,
 'Untimed', '1 hint @20min',
 'LC 1392 Longest Happy Prefix', 'H', 30,
 'LC 1044 Longest Duplicate Substring', 'H', 40,
 'LC 214 Shortest Palindrome',
 'Write polynomial rolling hash function with base and modulo from memory; explain sliding window hash update',
 'How do you remove the oldest character hash in O(1) when sliding the window?',
 'Content-defined chunking (Rabin fingerprints) in distributed deduplication storage',
 'Subquadratic sequence search'),

('Aho-Corasick Multi-Pattern Automaton: Matching dictionary of patterns in single pass',
 'Aho-Corasick automaton', 'Trie + BFS-constructed failure links and output links; generalized KMP on a tree; O(text + matches)',
 'YES', 'Aho-Corasick Multi-String Search Algorithm', 25,
 'Untimed', '1 hint @20min',
 'LC 1032 Stream of Characters', 'H', 35,
 'LC 1408 String Matching in an Array', 'E', 15,
 'LC 1392 Longest Happy Prefix',
 'Explain the failure link invariant: what does the failure link of node u point to?',
 'Why is Aho-Corasick optimal for matching 10,000 bad words against a streaming prompt?',
 'Prompt safety guardrails, regex engine compilation, intrusion detection packet matchers',
 'Multi-pattern automaton'),

('Byte-Pair Encoding (BPE) Algorithmic Mechanics: Subword Tokenization',
 'Tokenizer algorithms', 'Greedy pair-frequency counts; min-heap/priority queue of merge candidates; linked-list token merging',
 'YES', 'How GPT Tokenizers Work: The Byte-Pair Encoding Algorithm', 25,
 'Untimed', '1 hint @20min',
 'Implement a minimal BPE Tokenizer training loop with pair counting', 'M', 35,
 'LC 1163 Last Substring in Lexicographical Order', 'H', 35,
 'LC 1032 Stream of Characters',
 'Explain the algorithmic complexity of training BPE with V merges on text of length N',
 'Can you write the doubly-linked-list node merging logic for BPE without index corruption?',
 'LLM tokenization throughput, vocabulary compression, input token pre-processing pipelines',
 'Subword sequence modeling'),

("Suffix Arrays & Longest Common Prefix (LCP) Array (Kasai's Algorithm)",
 'Suffix array / LCP', "Sorted suffixes of string; Kasai's O(n) height array derivation; range minimum query on LCP",
 'YES', "Suffix Arrays & Kasai's LCP Algorithm", 25,
 'Untimed', '1 hint @20min',
 'LC 1754 Largest Merge Of Two Strings', 'M', 25,
 'LC 745 Prefix and Suffix Search', 'H', 35,
 'LC 1163 Last Substring in Lexicographical Order',
 "Explain why Kasai's algorithm computes LCPs in O(n) by demonstrating h >= h_prev - 1",
 'Did you prove why the LCP between any two suffixes is the range minimum in the LCP array?',
 'Genomic sequence alignment, code duplicate detection across repository scale',
 'Suffix permutation analytics'),

('Blind Sequence & String Matching Session',
 'Blind (string algorithms)', 'Identifying whether a problem requires KMP, Z-Algorithm, Rolling Hash, or Trie',
 'NO', '-', 0,
 'Untimed', 'No hints before 20min',
 'LC 686 Repeated String Match', 'M', 25,
 'LC 472 Concatenated Words', 'H', 35,
 'LC 745 Prefix and Suffix Search',
 'Write PatternCards entry for multi-pattern search vs single-pattern search',
 'Time-to-pattern on LC 472. Did you use Trie + DFS with memoization?',
 'String dedup in distributed datasets',
 'Sequence matching fluency'),

('Milestone Diagnostic #5: Strings, Automata & Hardware Structures',
 'Diagnostic', 'Rigorous unlabelled diagnostic covering Weeks 15 to 18',
 'NO', '-', 0,
 'Diagnostic', 'None',
 'Diagnostic 5: LC 214, LC 1044, LC 1032 (unlabelled, 110 min)', 'H', 110,
 'Error log + weakness classification in FailureLog', '-', 25,
 '-',
 'Log performance in MockInterviews; update ProgressionCurve actuals',
 'Did you derive all string matches without falling back to naive O(n^2) quadratic scanning?',
 'Systems interview diagnostic',
 'High-pressure synthesis'),

('Adaptive Replacement Cache (ARC): Self-tuning recency vs frequency with ghost caches',
 'Adaptive Cache (ARC)', 'Four lists: T1 (recent), T2 (frequent), B1 (ghost recent), B2 (ghost frequent); learning parameter p adaptation',
 'YES', 'The Adaptive Replacement Cache (ARC) Paper & Mechanics', 25,
 'Untimed', '1 hint @20min',
 'Simulate ARC Cache policy with target capacity c and learning parameter p', 'H', 45,
 'LC 146 LRU Cache (Review with Doubly Linked List)', 'M', 20,
 'LC 472 Concatenated Words',
 'Write down the ARC adaptation rule: how does p change when a hit occurs in B1 vs B2?',
 'Why does ARC outperform both LRU and LFU across mixed sequential-scan and looping workloads?',
 'Storage engine page caches (ZFS ARC), high-performance database buffer pools',
 'Self-tuning cache design'),

('2Q (Two-Queue) & SLRU (Segmented LRU): Eliminating scan pollution',
 'Segmented cache', 'A1in (FIFO queue for new pages) and Am (LRU for frequent pages); defending against one-hit wonders',
 'YES', '2Q Cache Algorithm: Low Overhead High Performance Buffer Management', 20,
 'Untimed', '1 hint @20min',
 'Implement 2Q Cache simulator: FIFO queue + LRU queue + Ghost list', 'H', 40,
 'LC 460 LFU Cache (Review with O(1) frequency buckets)', 'H', 30,
 'LC 146 LRU Cache',
 'Explain why a single huge sequential scan completely destroys a standard LRU cache but fails to corrupt 2Q',
 'Can you state the eviction decision flow when A1in exceeds its capacity quota?',
 'PostgreSQL shared buffers, Linux buffer cache page reclamation',
 'Scan-resistant caching'),

('Clock / Second-Chance Eviction & Clock-Pro: Lock-free page replacement',
 'Clock eviction', 'Circular buffer with a moving hand; access bit / referenced bit; clearing reference bit on rotation',
 'YES', 'Clock & Clock-Pro Page Replacement Algorithms', 20,
 'Untimed', '1 hint @20min',
 'Implement Clock eviction algorithm on a circular buffer with referenced bits', 'M', 30,
 'LC 146 LRU Cache (implement using circular array + reference bits)', 'M', 25,
 'LC 460 LFU Cache',
 'Why does Clock approximate LRU with O(1) space per entry and near-zero lock contention?',
 'How does Clock eliminate the need to move nodes around in a doubly linked list on every cache hit?',
 'Operating system virtual memory page eviction, GPU memory managers',
 'Lock-minimized eviction'),

('Tiered Caching & Time-To-Live (TTL) with Min-Heap & Hierarchical Timing Wheels',
 'Expiring cache / Timing wheel', 'Combining size-bounded eviction with timestamp-based expiration; O(1) timing wheels vs O(log n) min-heap',
 'YES', 'Hashed and Hierarchical Timing Wheels for Network Timers', 25,
 'Untimed', '1 hint @20min',
 'LC 981 Time Based Key-Value Store', 'M', 25,
 'Design a Cache with TTL and O(1) lazy expiration on read + active sweep', 'M', 35,
 'LC 146 LRU Cache',
 'Explain how a timing wheel achieves O(1) timer insertion and cancellation compared to a priority queue',
 'Did you analyze memory leaks in caches with TTL when keys are written once and never read again?',
 'Distributed session caches, API rate-limiting token replenishment, RPC timeout tracking',
 'Temporal cache mechanics'),

('Blind Cache Architecture Session: Selecting the optimal cache for workload signatures',
 'Blind (cache systems)', 'Matching workload access patterns (Zipfian, scan-heavy, looping, temporal burst) to cache algorithms',
 'NO', '-', 0,
 'Untimed', 'No hints before 20min',
 'LC 359 Logger Rate Limiter', 'E', 15,
 'LC 1797 Design Authentication Manager', 'M', 20,
 'LC 981 Time Based Key-Value Store',
 'Write a comparison matrix of LRU vs LFU vs ARC vs 2Q vs Clock across 5 criteria',
 'Which cache policy would you select for LLM embedding retrieval and why?',
 'Embedding vector cache, KV-cache in multi-turn conversational agents',
 'Cache topology selection'),

('Systems Simulation: KV-Cache Eviction & PagedAttention in LLM Inference Engines',
 'AI-infra systems modeling', 'PagedAttention: virtual memory paging for transformer KV-cache; eliminating external memory fragmentation',
 'YES', 'vLLM & PagedAttention: How KV Cache Memory is Managed in Modern LLM Serving', 25,
 'Untimed', 'Tutorial only',
 'Simulate a Block Table Manager for PagedAttention: allocate, map, copy-on-write', 'H', 45,
 'LC 146 LRU Cache', 'M', 20,
 'LC 1797 Design Authentication Manager',
 'Explain why standard contiguous allocation wastes up to 60-80% of GPU memory in LLM serving',
 'Can you explain the Copy-on-Write (CoW) mechanism in PagedAttention for parallel sampling?',
 'vLLM, TensorRT-LLM, HuggingFace TGI, GPU memory utilization',
 'Transformer KV-cache management'),

('Week 19 audit: complete implementation of ARC and Clock eviction policies cold',
 'Review/audit', 'Demonstrating mastery of industrial-grade caching algorithms',
 'NO', '-', 0,
 'Untimed', 'Notes forbidden',
 'Rederive: ARC Cache complete state transition machine cold', 'H', 45,
 'Rederive: Clock eviction algorithm with second chance cold', 'M', 25,
 'LC 359 Logger Rate Limiter',
 'Write both classes with clean API: get(key), put(key, val); test against sequential scan',
 'Can you defend the choice of ARC vs LRU in a senior systems interview whiteboard session?',
 'Systems cache mastery',
 'Eviction architecture fluency'),

('Lock-Free Ring Buffer: Single-Producer Single-Consumer (SPSC)',
 'Lock-free ring buffer', 'Head and tail indices; power-of-two capacity mask; memory barriers / acquire-release semantics; cache line padding',
 'YES', 'Lock-Free Single Producer Single Consumer Queue from scratch in C++/Rust', 25,
 'Untimed', '1 hint @20min',
 'LC 622 Design Circular Queue', 'M', 20,
 'LC 641 Design Circular Deque', 'M', 25,
 'LC 146 LRU Cache',
 'Explain why head and tail pointers must be padded to separate 64-byte cache lines to prevent false sharing',
 'Why is an SPSC queue completely lock-free without requiring any atomic CAS (Compare-And-Swap) instructions?',
 'Inter-thread messaging, LMAX Disruptor, high-frequency telemetry streaming',
 'Lock-free queue mechanics'),

('Multi-Producer Multi-Consumer (MPMC) Bounded Queue',
 'MPMC queue', 'Array of cell slots; sequence number per slot; atomic CAS on head and tail; turnaround generation invariant',
 'YES', "Dmitry Vyukov's MPMC Bounded Queue Algorithm", 25,
 'Untimed', '1 hint @20min',
 "Simulate Dmitry Vyukov's MPMC queue state machine with sequence counters", 'H', 45,
 'LC 1188 Design Bounded Blocking Queue', 'M', 25,
 'LC 622 Design Circular Queue',
 'Explain the cell sequence number invariant: when is a cell safe to write vs safe to read?',
 'How does the sequence counter prevent the ABA problem without a garbage collector?',
 'Thread-pool task submission queues, network socket event distribution',
 'Atomic sequence coordination'),

('Chase-Lev Work-Stealing Deque: Core of modern task runtimes',
 'Work-stealing deque', 'Private LIFO bottom for owner thread; concurrent FIFO top for worker thief threads; lock-free steal CAS',
 'YES', 'The Chase-Lev Work-Stealing Deque Paper & Architecture', 25,
 'Untimed', '1 hint @20min',
 'Simulate Chase-Lev Deque operations: push_bottom, pop_bottom, steal_top', 'H', 45,
 'LC 239 Sliding Window Maximum (Monotonic deque comparison)', 'H', 30,
 'LC 1188 Design Bounded Blocking Queue',
 'Explain why the worker steals from the TOP (oldest tasks) while owner pops from BOTTOM (newest tasks)',
 'Why does stealing from the top minimize contention with the owner thread?',
 'Go runtime goroutine scheduler, Tokio async executor, Ray distributed task scheduler',
 'Work-stealing runtime design'),

('Read-Copy-Update (RCU) & Hazard Pointers: Lock-free read scalability',
 'Read-Copy-Update (RCU)', 'Wait-free reader threads; copy on write; grace periods; deferred memory reclamation',
 'YES', 'Read-Copy-Update (RCU) in the Linux Kernel: Concepts & Mechanics', 20,
 'Untimed', '1 hint @20min',
 'Implement an RCU-style immutable config snapshot manager with atomic pointer swap', 'M', 30,
 'LC 380 Insert Delete GetRandom O(1)', 'M', 20,
 'LC 239 Sliding Window Maximum',
 'Explain what a grace period is in RCU: when is it guaranteed safe to free the old copy?',
 'Can you explain why RCU readers have zero lock overhead and zero atomic write operations?',
 'Routing tables in network proxies (Envoy), live feature flags in distributed microservices',
 'Zero-overhead read concurrency'),

('Consistent Hashing with Virtual Nodes: Bounded redistribution under cluster churn',
 'Consistent hashing', 'Hash ring [0, 2^32-1]; virtual nodes for balanced load; binary search (bisect) for partition owner lookup',
 'YES', 'Consistent Hashing: System Design & Algorithmic Mechanics', 20,
 'Untimed', '1 hint @20min',
 'Implement a ConsistentHashRing with virtual nodes, add_node(), remove_node(), get_node()', 'M', 35,
 'LC 535 Encode and Decode TinyURL', 'M', 15,
 'LC 380 Insert Delete GetRandom O(1)',
 'Prove that adding or removing a node re-shards only K/N keys on average, where K is total keys',
 'Why are virtual nodes necessary? What happens to variance in load if you have only 1 point per node?',
 'DynamoDB, Cassandra partitioner, Memcached client-side routing, distributed cache sharding',
 'Distributed topology hashing'),

('Blind Concurrency & Synchronization Session',
 'Blind (concurrency & queues)', 'Choosing the right synchronization primitive: Mutex vs Spinlock vs Ring Buffer vs RCU',
 'NO', '-', 0,
 'Untimed', 'No hints before 20min',
 'LC 1114 Print in Order', 'E', 15,
 'LC 1115 Print FooBar Alternately', 'M', 20,
 'LC 641 Design Circular Deque',
 'Write PatternCards entry for Lock-free SPSC Ring Buffer vs Bounded MPMC Queue',
 'Time-to-pattern on LC 1115. Can you write it using condition variables and semaphores cleanly?',
 'Inter-thread synchronization in high-performance engines',
 'Synchronization fluency'),

('Milestone Diagnostic #6: Concurrency Primitives, Caches & Work-Stealing',
 'Diagnostic', 'Unlabelled diagnostic testing systems data structures under strict time pressure',
 'NO', '-', 0,
 'Diagnostic', 'None',
 'Diagnostic 6: SPSC Ring Buffer, Consistent Hash Ring, 2Q Cache (unlabelled, 110 min)', 'H', 110,
 'Error log + weakness classification in FailureLog', '-', 25,
 '-',
 'Fill diagnostic scores in MockInterviews; record time-to-pattern and test correctness',
 'Did you implement the power-of-two mask in the ring buffer without modulo operator overhead?',
 'Systems interview diagnostic',
 'High-pressure synthesis'),

('Vector Search Foundations: KD-Tree & Ball-Tree Mechanics',
 'KD-Tree / Ball-Tree', 'Alternating dimension splitting; bounding box pruning; nearest neighbor search branch discard',
 'YES', 'KD-Trees and Ball Trees: High-Dimensional Spatial Indexing', 25,
 'Untimed', '1 hint @20min',
 'Implement a 2D KD-Tree: build from points and nearest_neighbor(q)', 'M', 35,
 'LC 973 K Closest Points to Origin (Heap baseline vs Spatial index)', 'M', 25,
 'LC 1115 Print FooBar Alternately',
 'Explain why KD-Trees degrade to O(N) linear scans when dimensionality D exceeds ~20 (curse of dimensionality)',
 'Why do vector databases use approximate nearest neighbors (ANN) instead of exact KD-trees for d=1536?',
 'Spatial databases, geometric indexing, low-dimensional coordinate search',
 'Spatial partition modeling'),

('Inverted File Index (IVF) & Voronoi Cells',
 'IVF Indexing', 'Coarse quantization via K-means clustering; Voronoi partition assignment; probe count nprobe trade-off',
 'YES', 'FAISS Internals: Inverted File Index (IVF) and Voronoi Cells', 25,
 'Untimed', '1 hint @20min',
 'Simulate an IVF index: assign vectors to clusters, query top-nprobe clusters', 'M', 35,
 'LC 215 Kth Largest Element in an Array (Quickselect baseline)', 'M', 25,
 'LC 973 K Closest Points to Origin',
 'Explain the trade-off between nlist (number of centroids) and nprobe (clusters searched during query)',
 'Why does IVF achieve sub-linear query time while sacrificing 1-2% in recall?',
 'Milvus, Pinecone, FAISS IVF index, vector database partitioners',
 'Clustered vector indexing'),

('Hierarchical Navigable Small World (HNSW) Graphs: Core of Modern Vector DBs',
 'HNSW graph search', 'Multi-layer proximity graph (skip-list on graphs); greedy routing at top layers, beam search at layer 0',
 'YES', 'HNSW Algorithm: The Paper, Mathematics, and Graph Navigation', 25,
 'Untimed', '1 hint @20min',
 'Simulate HNSW greedy entry routing and Layer-0 Beam Search on a proximity graph', 'H', 45,
 'LC 743 Network Delay Time (Dijkstra graph search comparison)', 'M', 25,
 'LC 215 Kth Largest Element in an Array',
 'Explain the probability distribution of assigning a vector to layer l in HNSW: l = floor(-ln(uniform) * m_L)',
 'Can you explain why HNSW achieves logarithmic search time on high-dimensional vectors?',
 'Weaviate, Qdrant, Chroma, FAISS HNSW, vector embedding retrieval engines',
 'Proximity graph navigation'),

('Product Quantization (PQ) & Asymmetric Distance Computation (ADC)',
 'Vector quantization', 'Splitting D-dimensional vector into M sub-vectors; codebook generation; precomputed distance lookup tables',
 'YES', 'Product Quantization (PQ) & Fast Distance Computation in FAISS', 25,
 'Untimed', '1 hint @20min',
 'Simulate Product Quantization: compress vectors to M byte codes; compute ADC distance table', 'H', 45,
 'LC 1396 Design Underground System', 'M', 20,
 'LC 743 Network Delay Time',
 'Explain how Product Quantization compresses a 1536-dimensional FP32 vector (6144 bytes) down to 64 bytes',
 'Why does Asymmetric Distance Computation (query uncompressed, database vectors quantized) beat Symmetric distance?',
 'Memory-constrained vector search at billion-scale, embedding index compression',
 'Vector compression analytics'),

('Random Projection Trees & Annoy (Approximate Nearest Neighbors Oh Yeah)',
 'Random projection trees', 'Splitting space with random hyperplanes; cosine similarity partitions; multi-tree forest voting',
 'YES', 'Annoy & Random Projection Trees for Spotify-Scale Recommendation', 20,
 'Untimed', '1 hint @20min',
 'Implement a Random Projection Tree: split points by hyperplane dot-product', 'M', 35,
 'LC 300 Longest Increasing Subsequence (Review patience sorting)', 'M', 20,
 'LC 1396 Design Underground System',
 'Explain why querying multiple independent random trees increases recall exponentially',
 'How does cosine distance reduce to dot product on normalized unit vectors?',
 'Spotify recommendation search, read-only memory-mapped embedding indexes',
 'Hyperplane partition search'),

('Blind Vector Retrieval Session: IVF vs HNSW vs Quantization Trade-offs',
 'Blind (vector algorithms)', 'Analyzing index build time, memory footprint, QPS latency, and Recall@K across vector indices',
 'NO', '-', 0,
 'Untimed', 'No hints before 20min',
 'LC 149 Max Points on a Line (Geometric slope mapping)', 'H', 35,
 'LC 347 Top K Frequent Elements (Review bucket vs heap)', 'M', 20,
 'LC 300 Longest Increasing Subsequence',
 'Write PatternCards entry for HNSW vs IVF-PQ indexing tradeoffs',
 'If an interviewer asks you to build a vector database for 10M embeddings on a single 32GB RAM instance, what index do you choose?',
 'Vector infrastructure capacity planning',
 'Vector index architectural design'),

('Week 21 audit: implement HNSW Layer-0 Beam Search cold with no notes',
 'Review/audit', 'Total command over proximity graph navigation mechanics',
 'NO', '-', 0,
 'Untimed', 'Notes forbidden',
 'Rederive: HNSW Layer-0 Beam Search with visited set and candidate min-heap cold', 'H', 45,
 'Rederive: Vector cosine similarity and Euclidean distance SIMD simulation cold', 'M', 20,
 'LC 149 Max Points on a Line',
 'Code the complete HNSW search algorithm in raw Python/C++; explain the efSearch parameter',
 'Can you explain how HNSW guarantees no infinite loops in cyclic proximity graphs?',
 'Vector database algorithmic mastery',
 'Proximity graph fluency'),

('Heterogeneous DAG Task Scheduling: ASAP, ALAP & Critical Path Method',
 'DAG scheduling', 'Earliest Start Time (EST), Latest Start Time (LST), task slack / float; critical path identification in ML compute graphs',
 'YES', 'DAG Task Scheduling & Critical Path Method in ML Compilers', 25,
 'Untimed', '1 hint @20min',
 'LC 2050 Parallel Courses III (Critical Path DAG)', 'H', 35,
 'LC 207 Course Schedule (Topological baseline)', 'M', 20,
 'LC 149 Max Points on a Line',
 'Write down the dynamic programming formula for critical path duration on a DAG: dist[v] = max(dist[u] + time[v])',
 'How do you identify tasks with zero slack (the critical path) from EST and LST arrays?',
 'PyTorch 2.0 Inductor graph lowering, XLA compiler fusion scheduling, distributed pipeline parallelism',
 'Pipeline latency minimization'),

('Memory-Bounded Topological Scheduling: Minimizing peak activation memory',
 'Memory-constrained DAG', 'Scheduling operator execution order to minimize peak live tensor memory; activation recomputation (checkpointing)',
 'YES', 'Memory-Efficient DAG Scheduling & Activation Checkpointing', 25,
 'Untimed', '1 hint @20min',
 'Simulate a topological scheduler that minimizes live peak memory using a greedy min-heap', 'H', 45,
 'LC 210 Course Schedule II (Topological order)', 'M', 20,
 'LC 2050 Parallel Courses III',
 'Explain why standard BFS topological sort causes maximum peak memory while DFS causes minimum peak memory',
 'Can you explain the trade-off between peak live memory and parallel operator execution concurrency?',
 'Megatron-LM activation checkpointing, GPU out-of-memory (OOM) avoidance in large model training',
 'Memory-bounded scheduling'),

('Tensor Strided Indexing, Memory Layouts (Row-Major vs Col-Major) & In-Place Transpose',
 'Strided index arithmetic', 'Multi-dimensional offset formula: index = sum(coords[i] * strides[i]); contiguous vs non-contiguous views; cycle-following transpose',
 'YES', 'Tensor Strides, Contiguity & In-Place Transposition Algorithms', 25,
 'Untimed', '1 hint @20min',
 'Implement Tensor strided indexing class: view, transpose, permute without copying data', 'M', 35,
 'LC 48 Rotate Image (In-place 2D matrix transpose)', 'M', 25,
 'LC 210 Course Schedule II',
 'Derive new strides after a transpose(dim1, dim2) operation without allocating new memory',
 'What condition must be satisfied for a tensor to be considered C-contiguous?',
 'PyTorch Tensor internals, Triton kernel memory layouts, FlashAttention tiled SRAM loading',
 'Zero-copy tensor math'),

('Parallel Prefix Scan (Blelloch Algorithm): Work-efficient parallel scan',
 'Parallel prefix scan', 'Up-sweep (reduce) tree and down-sweep tree; work efficiency O(n) additions vs naive O(n log n); parallel scan in GPU thread blocks',
 'YES', 'The Blelloch Work-Efficient Parallel Scan Algorithm', 25,
 'Untimed', '1 hint @20min',
 'Implement Blelloch parallel scan simulator in Python: up-sweep and down-sweep passes', 'H', 40,
 'LC 303 Range Sum Query - Immutable (Prefix baseline)', 'E', 15,
 'LC 48 Rotate Image',
 'Explain the down-sweep step: why does root set to 0, and what are left_child and right_child updated to?',
 'Can you explain why Blelloch scan is work-efficient (O(n) operations) compared to Hillis-Steele (O(n log n))?',
 'CUDA Thrust scan primitives, parallel token position index generation, stream compaction',
 'Parallel tree reduction'),

('Sparse Matrix Formats (COO, CSR, CSC) & Sparse-Dense Matrix Multiplication (SpMM)',
 'Sparse matrix formats', 'Coordinate format (COO), Compressed Sparse Row (CSR: values, col_indices, row_ptrs); O(nnz) operations',
 'YES', 'Sparse Matrix Representations (CSR, CSC) & SpMM Algorithm', 25,
 'Untimed', '1 hint @20min',
 'Implement CSR Matrix class: from_dense(), to_dense(), and spmm_vector_multiply()', 'M', 35,
 'LC 311 Sparse Matrix Multiplication', 'M', 25,
 'LC 303 Range Sum Query - Immutable',
 'Explain why row_ptrs array in CSR has length num_rows + 1; how do you find row non-zero elements in O(1)?',
 'Why is CSR optimal for row-slicing and matrix-vector product, while CSC is optimal for column operations?',
 'Graph Neural Networks (PyG), sparse mixture-of-experts (MoE) routing, sparse attention kernels',
 'Sparse linear algebra data structures'),

('Blind ML Systems Algorithmic Session',
 'Blind (ML algorithms)', 'Synthesizing DAG scheduling, sparse matrix representations, and tensor layouts',
 'NO', '-', 0,
 'Untimed', 'No hints before 20min',
 'LC 847 Shortest Path Visiting All Nodes (State-space bitmask graph)', 'H', 40,
 'LC 133 Clone Graph', 'M', 20,
 'LC 311 Sparse Matrix Multiplication',
 'Write PatternCards entry for Memory-Bounded Topological Sort vs Critical Path DAG',
 'Time-to-pattern on LC 847. Did you immediately recognize the BFS on (node, mask) state-space?',
 'Compiler pass optimization, graph kernel scheduling',
 'ML systems algorithmic fluency'),

('Milestone Diagnostic #7: ML Compilers, DAG Scheduling & Tensor Algorithms',
 'Diagnostic', 'Unlabelled diagnostic testing ML infrastructure algorithms under time constraints',
 'NO', '-', 0,
 'Diagnostic', 'None',
 'Diagnostic 7: LC 2050, Blelloch Scan Simulator, CSR SpMM (unlabelled, 110 min)', 'H', 110,
 'Error log + weakness classification in FailureLog', '-', 25,
 '-',
 'Log performance in MockInterviews; update ProgressionCurve actuals',
 'Did you prove work-efficiency of the parallel scan and DAG schedule latency bounds?',
 'Systems interview diagnostic',
 'High-pressure synthesis'),

('Reservoir Sampling (Uniform & Weighted): Fair streaming sampling with bounded memory',
 'Reservoir sampling', 'Algorithm R: keep first k, replace item i with probability k/i; A-Res weighted sampling with key u^(1/w)',
 'YES', 'Reservoir Sampling: Mathematical Proof & Weighted Extensions', 25,
 'Untimed', '1 hint @20min',
 'LC 382 Linked List Random Node', 'M', 25,
 'LC 398 Random Pick Index', 'M', 25,
 'LC 847 Shortest Path Visiting All Nodes',
 'Write the induction proof that every item in a stream of length N has probability exactly k/N of being in reservoir',
 'Why does reservoir sampling require zero knowledge of the total stream length N beforehand?',
 'Distributed dataset shuffling in PyTorch DataLoader, online telemetry metric sampling',
 'Fair streaming sampling'),

('Count-Min Sketch & Conservative Update: Frequency estimation over high-volume streams',
 'Count-Min Sketch', 'd x w 2D array of counters with d hash functions; point query takes min across rows; error bound eps = e/w, delta = 1/e^d',
 'YES', 'Count-Min Sketch: Approximating Stream Frequencies in Sub-Linear Space', 25,
 'Untimed', '1 hint @20min',
 'Implement Count-Min Sketch with conservative update: add(item), estimate(item)', 'M', 35,
 'LC 1497 Check If Array Pairs Are Divisible by k (Remainder counting)', 'M', 20,
 'LC 382 Linked List Random Node',
 'Explain why Count-Min Sketch always overestimates and never underestimates the true frequency',
 'What does the conservative update optimization do to reduce overestimation error?',
 'Network DDoS detection, live trending hashtag counters, distributed token frequency monitoring',
 'Sublinear frequency estimation'),

('HyperLogLog (HLL): Cardinality estimation of billions of unique keys',
 'HyperLogLog (HLL)', 'Register bucket assignment from hash prefix; counting leading zeros of hash suffix; harmonic mean aggregation',
 'YES', 'HyperLogLog: How Redis & Google Count Billions of Unique Elements in 1.5KB', 25,
 'Untimed', '1 hint @20min',
 'Implement minimal HyperLogLog simulator with 64 registers and leading zero count', 'M', 35,
 'LC 128 Longest Consecutive Sequence (Review unique sets)', 'M', 20,
 'LC 1497 Check If Array Pairs Are Divisible by k',
 'Explain why harmonic mean is used across registers instead of geometric or arithmetic mean (outlier resistance)',
 'Why does a 12KB HyperLogLog estimate cardinality up to 10^9 unique items with standard error ~1%?',
 'Unique visitor counts in BigQuery/Snowflake, distinct token counts across petabyte LLM training corpora',
 'Logarithmic cardinality estimation'),

('Heavy Hitters & Misra-Gries Algorithm: Finding top-K frequent elements in streaming data',
 'Misra-Gries / Majority', 'Maintaining at most k-1 candidate keys with decrement counters; generalisation of Boyer-Moore majority algorithm',
 'YES', 'The Misra-Gries Heavy Hitters Algorithm: Streaming Top-K in O(k) space', 25,
 'Untimed', '1 hint @20min',
 'LC 169 Majority Element (Boyer-Moore 1-candidate baseline)', 'E', 15,
 'LC 229 Majority Element II (Misra-Gries 2-candidate implementation)', 'M', 25,
 'LC 128 Longest Consecutive Sequence',
 'Explain why decrementing all k counters when an unfamiliar element arrives preserves the heavy hitter invariant',
 'Did you state the formal guarantee: any element with frequency > N/k is guaranteed to remain in the candidate set?',
 'Hot-key detection in caching proxies, toxic query identification in search infrastructure',
 'Streaming frequency filtering'),

('Quantization Algorithms: Symmetric / Asymmetric Uniform Quantization & Block Floating Point (FP8)',
 'Quantization algorithms', 'Scale factor S and zero-point Z; affine mapping q = round(x / S) + Z; clipping range [-128, 127]; outlier-preserving block quantization',
 'YES', 'Quantization for Deep Learning: INT8, FP8 & Block Float Algorithms', 25,
 'Untimed', '1 hint @20min',
 'Implement Symmetric & Asymmetric INT8 Quantizer/Dequantizer functions with dynamic scale calculation', 'M', 35,
 'LC 89 Gray Code (Bitwise representations)', 'M', 25,
 'LC 229 Majority Element II',
 'Derive the scale S and zero-point Z formulas given floating point range [x_min, x_max]',
 'Why is symmetric quantization (Z=0) faster on GPU tensor cores than asymmetric quantization?',
 'Post-training quantization (PTQ), AWQ, bitsandbytes, TensorRT FP8 kernel acceleration',
 'Numerical precision compression'),

('Blind Probabilistic & Streaming Session',
 'Blind (probabilistic algorithms)', 'Identifying whether a streaming problem needs Reservoir Sampling, Misra-Gries, or a Sketch',
 'NO', '-', 0,
 'Untimed', 'No hints before 20min',
 'LC 470 Implement Rand10() Using Rand7() (Rejection sampling)', 'M', 25,
 'LC 528 Random Pick with Weight (Prefix sum + Binary search)', 'M', 25,
 'LC 89 Gray Code',
 'Write PatternCards entry for Count-Min Sketch vs Misra-Gries streaming',
 'Time-to-pattern on LC 470. Did you immediately recognize the rejection sampling coordinate grid?',
 'Probabilistic data pipeline analytics',
 'Probabilistic algorithm fluency'),

('Week 23 audit: implement Count-Min Sketch and Misra-Gries cold with no notes',
 'Review/audit', 'Demonstrating command over streaming and probabilistic algorithms',
 'NO', '-', 0,
 'Untimed', 'Notes forbidden',
 'Rederive: Count-Min Sketch class with conservative update cold', 'M', 35,
 'Rederive: Misra-Gries top-K streaming candidate tracker cold', 'M', 30,
 'LC 528 Random Pick with Weight',
 'Write both algorithms from memory; state the mathematical error bounds for each without consulting references',
 'Can you explain the trade-offs of streaming sketches to a principal data engineer?',
 'Streaming algorithms mastery',
 'Streaming data structures'),

('Memory Allocator Mechanics: Buddy Allocator',
 'Buddy allocator', 'Power-of-two block splitting; bitwise XOR address buddy calculation (addr ^ (1 << order)); free lists per order',
 'YES', 'The Buddy Memory Allocator: Concepts, Bitwise Math & Implementation', 25,
 'Untimed', '1 hint @20min',
 'Implement a Buddy Allocator simulator: allocate(size), free(addr) with recursive coalescing', 'H', 45,
 'LC 41 First Missing Positive (In-place array allocation mapping)', 'H', 30,
 'LC 528 Random Pick with Weight',
 'Explain why the buddy of a block at address A with order K is computed as A ^ (1 << K)',
 'How does the Buddy Allocator eliminate external fragmentation while trading internal fragmentation?',
 'Linux kernel page allocator, GPU device memory allocators, jemalloc size classes',
 'Physical memory management'),

('Memory Allocator Mechanics: Slab Allocator & Arena Pooling',
 'Slab / Arena allocator', 'Pre-allocated fixed-size object caches; free-list pointers embedded in unallocated chunks; bump-pointer arena reset',
 'YES', 'The Slab Allocator & Arena Allocators in High-Performance Systems', 20,
 'Untimed', '1 hint @20min',
 'Implement a Bump-Pointer Arena Allocator with fast reset() and Slab Cache for fixed structs', 'M', 35,
 'LC 23 Merge k Sorted Lists (Review k-way merge)', 'H', 25,
 'LC 41 First Missing Positive',
 'Explain why an Arena allocator with bump-pointer allocation has O(1) allocation cost and zero deallocation overhead',
 'Why do game engines and web servers allocate per-request state inside an Arena rather than calling malloc()?',
 'Apache Arrow memory pools, Rust arena allocators, C++ custom STL allocators',
 'Zero-fragmentation memory design'),

('Capstone Mock Interview #1: Tier-1 Distributed Storage & Cache Algorithm (Full verbal, unlabelled)',
 'Mock interview', 'End-to-end interview simulation: Problem understanding, constraint derivation, algorithm design, coding, edge cases',
 'NO', '-', 0,
 'Timed-45', 'None',
 'Mock #1: Complex LRU/LFU cache eviction with TTL and concurrency constraints', 'H', 45,
 'Debrief + failure classification in FailureLog', '-', 20,
 'LC 460 LFU Cache',
 'Record Mock score in MockInterviews; identify the single most critical communication or technical bottleneck',
 'Did you speak continuously throughout your derivation without going silent for more than 45 seconds?',
 'Tier-1 storage algorithm interview',
 'High-stakes communication'),

('Capstone Mock Interview #2: Tier-1 ML Infra / Scheduling Algorithm (Full verbal, unlabelled)',
 'Mock interview', 'Memory-bounded DAG operator scheduling and tensor placement under accelerator constraints',
 'NO', '-', 0,
 'Timed-45', 'None',
 'Mock #2: Memory-bounded topological DAG scheduling with live tensor lifecycle tracking', 'H', 45,
 'Debrief + failure classification in FailureLog', '-', 20,
 'LC 2050 Parallel Courses III',
 'Record Mock score in MockInterviews; compare score progression vs previous mock',
 'Did you state the loop invariants and time/space complexity before writing a line of code?',
 'Tier-1 ML infra algorithm interview',
 'Systems problem derivation'),

('Capstone Mock Interview #3: Tier-1 High-Dimensional Vector Search & Indexing (Full verbal, unlabelled)',
 'Mock interview', 'Proximity graph navigation and vector index selection under strict memory and latency budgets',
 'NO', '-', 0,
 'Timed-45', 'None',
 'Mock #3: HNSW beam search navigation with dynamic pruning and distance metric optimization', 'H', 45,
 'Debrief + failure classification in FailureLog', '-', 20,
 'LC 743 Network Delay Time',
 'Record Mock score in MockInterviews; note any residual conceptual gaps in vector indexing',
 'Did you clearly articulate trade-offs between memory footprint, recall percentage, and QPS throughput?',
 'Tier-1 vector database algorithm interview',
 'Architectural algorithmic synthesis'),

('Final Spaced-Repetition Clearance: Clear the top 15 items in ReviewQueue to 0',
 'Comprehensive review', 'Total elimination of accumulated fragility across all 168 days',
 'NO', '-', 0,
 'Untimed', 'None',
 'Solve top 3 highest-priority problems from ReviewQueue', 'H', 45,
 'Solve next 3 highest-priority problems from ReviewQueue', 'M', 40,
 'ReviewQueue Rank 1-6',
 "Mark reviewed problems as 'Mastered = Yes' in ProblemDB; observe ReviewQueue repopulation",
 'Is every single high-priority problem in your ReviewQueue now cleared?',
 'Zero-backlog operational discipline',
 'Retention mastery'),

('Final Grand Diagnostic & Program Certification: 3 Unlabelled Multi-Domain Hard Problems',
 'Diagnostic', 'The ultimate test: 120 minutes, 3 unfamiliar hard problems spanning Classical, Systems & AI Infra DSA',
 'NO', '-', 0,
 'Diagnostic', 'None',
 'Final Diagnostic: 3 Unlabelled Hard Problems from BlindProblemPool (120 min)', 'H', 120,
 'Program completion reflection & Final Interview Readiness Score certification', '-', 30,
 '-',
 'Fill final diagnostic row in MockInterviews; view completed Dashboard with 100% progress',
 'Do you have concrete, data-backed evidence that you can derive any unfamiliar problem in <5 minutes?',
 'Tier-1 AI Infrastructure & Systems Algorithmic Specialist Certification',
 'Specialist algorithmic mastery'),

]

assert len(PLAN) == DAYS, f"Expected {DAYS} days, got {len(PLAN)}"
print(f"[OK] Part 2 done: {len(PLAN)}-day plan data validated")


# ==============================================================================
# PART 3  -  BUILD ALL SHEETS
# ==============================================================================

# --- SHEET: DayPlan -----------------------------------------------------------
ws_dp = wb.create_sheet("DayPlan")
ws_dp.sheet_view.showGridLines = False

DP_HEADERS = [
    "Day","Week","Date","Objective","Pattern","Concept",
    "Tutorial?","Tutorial Topic","Tut min","Mode","Help / Stuck Protocol",
    "Problem 1","P1 Diff","P1 Target min",
    "Problem 2","P2 Diff","P2 Target min",
    "Review Problem","Reconstruction Task","Assessment Question",
    "AI-Infra Connection","Skill Gained",
    "Completed?","Actual min","Notes","Failure Category","2nd-Sol?",
    "YouTube Tutorial ↗",
]
DP_WIDTHS = [5,5,12,46,24,36,9,30,6,11,18,38,6,8,38,6,8,34,46,44,40,22,10,8,34,18,8,22]
write_header(ws_dp, DP_HEADERS, DP_WIDTHS, freeze="D2")

WEEK_THEMES = [
    "Constraints + Counting + Hashing + Prefix",
    "Two Pointers + Sliding Window",
    "Binary Search (index + answer)",
    "Intervals + Monotonic Stack/Deque + Diagnostic 1",
    "Heaps + Streaming + Greedy",
    "Design (LRU/LFU) + Pointers + Bits",
    "Trees + Recursion + BST",
    "Tries + Cross-Fusion + Diagnostic 2",
    "Graphs + Union Find + Topo Sort",
    "Shortest Paths + State-Space + Mock 2",
    "Backtracking + Pruning + Memo Bridge",
    "DP: 1D/LIS/Knapsack/2-Seq + Diagnostic 3",
    "Advanced DP: Interval/Bitmask/Optimization",
    "Mid-Program Review + Diagnostic 4",
    "Range Queries: Fenwick Trees & Segment Trees",
    "Advanced Graphs: Bridges, SCC & Flows",
    "Hardware Reality: Cache-Conscious Structures",
    "Strings & Automata: KMP, Z-Algorithm, BPE",
    "Cache Architectures: ARC, 2Q & PagedAttention",
    "Concurrency: SPSC Ring Buffers & Work-Stealing",
    "Vector Search: KD-Trees, IVF & HNSW Graphs",
    "ML Compiler: DAG Scheduling & Tensor Strides",
    "Streaming & Probabilistic: Sketches & Quantization",
    "Capstone Systems Simulation & Final Diagnostic",
]

for i, day_data in enumerate(PLAN):
    r = i + 2
    day = i + 1
    week = (i // 7) + 1
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

    dt = START + timedelta(days=i)
    wk_fill = GREY if week % 2 == 0 else WHITE

    if tY == "YES" and tT:
        tut = get_tutorial_resource(day, tT)
        tT_val = f'=HYPERLINK("{tut["primary_url"]}", "{tT}")'
        yt_btn_val = f'=HYPERLINK("{tut["primary_url"]}", "▶ Watch ({tut["primary"]}) ↗")'
    else:
        tT_val = tT if tT else ""
        yt_btn_val = "—"

    vals = [
        day, week, dt, obj, pat, con,
        tY, tT_val, (tM if tM else ""), mode, help_,
        p1, d1, t1, p2, d2, t2,
        rev, rec, asr, infra, skill,
        None, None, None, None, None,
        yt_btn_val
    ]
    for c, v in enumerate(vals, 1):
        cell = put(ws_dp, r, c, v, bg=wk_fill if wk_fill != WHITE else None)
        if c == 3:  cell.number_format = "ddd dd-mmm-yy"
        if c in (1,2,9,13,14,16,17,23,24,27,28): cell.alignment = CTR
        if c == 8 and tY == "YES":
            cell.font = fnt(color=BLUE, underline="single", bold=True)
        if c == 28:
            if tY == "YES":
                cell.font = fnt(color=GREEN_D, underline="single", bold=True)
            else:
                cell.font = fnt(color="94A3B8")

    ws_dp.row_dimensions[r].height = 56

# Dropdowns
dv(ws_dp, YN_VALS,   f"G2:G{DAYS+1}", "Tutorial?")
dv(ws_dp, MODE_VALS, f"J2:J{DAYS+1}", "Mode")
dv(ws_dp, YN_VALS,   f"W2:W{DAYS+1}", "Completed?")
dv(ws_dp, FCATS,     f"Z2:Z{DAYS+1}", "Failure category")
dv(ws_dp, YN_VALS,   f"AA2:AA{DAYS+1}", "Found 2nd solution?")
dv(ws_dp, DIFF_VALS, f"M2:M{DAYS+1}", "P1 Diff")
dv(ws_dp, DIFF_VALS, f"P2:P{DAYS+1}", "P2 Diff")

last = DAYS + 1
# Conditional formatting
ws_dp.conditional_formatting.add(f"W2:W{last}",
    CellIsRule("equal", ['"Yes"'], fill=fill(GREEN)))
ws_dp.conditional_formatting.add(f"W2:W{last}",
    CellIsRule("equal", ['"No"'],  fill=fill(RED)))
for col in ("M","P"):
    ws_dp.conditional_formatting.add(f"{col}2:{col}{last}",
        CellIsRule("equal", ['"H"'], fill=fill(RED)))
    ws_dp.conditional_formatting.add(f"{col}2:{col}{last}",
        CellIsRule("equal", ['"M"'], fill=fill(AMBER)))
    ws_dp.conditional_formatting.add(f"{col}2:{col}{last}",
        CellIsRule("equal", ['"E"'], fill=fill(GREEN)))
ws_dp.conditional_formatting.add(f"G2:G{last}",
    CellIsRule("equal", ['"YES"'], fill=fill(ORANGE)))
ws_dp.conditional_formatting.add(f"E2:E{last}",
    CellIsRule("equal", ['"Diagnostic"'], fill=fill("FFF2CC")))
ws_dp.conditional_formatting.add(f"E2:E{last}",
    CellIsRule("containsText" if False else "equal", ['"Blind"'],
               fill=fill("F3E8FF")))

ws_dp.auto_filter.ref = f"A1:AB{last}"
print("[OK] DayPlan sheet built")

# --- SHEET: PatternLibrary -----------------------------------------------------
ws_pl = wb.create_sheet("PatternLibrary")
ws_pl.sheet_view.showGridLines = False

PL_H = ["Pattern","Recognition Cues","Typical Constraints","Core Idea",
        "Key Data Structures","Common Traps","Complexity Target",
        "Example Problem Types","AI-Infra Relevance","Mastery (1-5)",
        "# times it appeared in plan","Last practiced"]
PL_W = [26,44,22,44,24,40,18,34,38,10,10,12]
write_header(ws_pl, PL_H, PL_W, freeze="B2")

PATTERNS = [
("Complexity calibration",
 "Any problem with 'efficient' + a large n stated",
 "n in constraints",
 "Derive acceptable TC from n BEFORE designing anything; eliminate approaches that cannot fit",
 "None  -  pure reasoning",
 "Assuming O(n^2) passes at n=10^5; ignoring hash/recursion constants; never doing this step",
 "Pre-code decision",
 "Every single problem",
 "Latency budgets; SLO thresholds; batch-size selection"),

("Frequency/counting + hashing",
 "'anagram','k most frequent','duplicates','count of','appears more than once'",
 "values bounded or hashable; n up to 10^6",
 "Replace repeated scans with one pass building counts; hash the KEY that captures the invariant",
 "hash map, count array, bucket array",
 "Counting when positions matter; wrong key granularity; using set when count needed",
 "O(n) time, O(k) space",
 "Group anagrams, top-K, majority element, first unique character",
 "Hot-key detection, metric counters, histogram-based alerting"),

("Prefix/suffix reasoning",
 "'subarray sum','range query','product except self','subarrays satisfying condition'",
 "static array, multiple queries, O(n) target",
 "Precompute cumulative info so any range is O(1); prefix+hash converts a condition into a lookup",
 "prefix array, hash map (prefix -> count or prefix -> first-index)",
 "Forgetting prefix[0]=0; using seen-set instead of count-map; applying to non-additive functions",
 "O(n) build, O(1) query",
 "Range sums, balanced subarrays, product except self, 2D regions",
 "Rolling aggregates, cumulative metrics, event-log windows"),

("Two pointers (opposite ends)",
 "sorted or sortable input; 'pair/triplet sums to'; 'maximum area between'",
 "sorted or O(n log n) sort acceptable",
 "Move the pointer that provably cannot improve the answer; prove no valid pair is skipped",
 "two indices into the same array",
 "Moving the wrong pointer; skipping duplicates incorrectly; not proving the discard",
 "O(n) after sort",
 "Two Sum II, 3Sum, Container With Most Water",
 "Merging sorted shard scans; two-way join on sorted data"),

("Two pointers (same direction / read-write)",
 "'in place','remove elements','partition','k-th from end'",
 "O(1) extra space required; array mutation allowed",
 "Separate a slow write-index from a fast read-index; maintain a region invariant",
 "two indices, optional dummy node for lists",
 "Overwriting needed elements; not stating the region invariant; off-by-one",
 "O(n) time, O(1) space",
 "Remove duplicates, Sort Colors, move zeros, linked-list operations",
 "In-place buffer compaction; zero-copy stream rewriting"),

("Sliding window (variable)",
 "'longest/shortest subarray/substring satisfying condition'; contiguous required",
 "monotone feasibility must hold; n up to 10^5",
 "Grow right pointer; shrink left while invalid. ONLY valid when extending cannot repair a violation.",
 "hash map or count array for window contents, two indices",
 "Applying to non-monotone conditions (e.g. sum>=k with negatives); wrong shrink condition",
 "O(n)",
 "Longest unique substring, minimum size subarray sum, fruit into baskets",
 "Rate limiting, windowed quotas, token bucket"),

("Sliding window + counting",
 "'at most K distinct','replace at most k characters','subarrays with exactly k'",
 "alphabet/cardinality bounded; n up to 10^5",
 "Track frequency inside the window; exactly(K) = atMost(K) - atMost(K-1)",
 "hash map, freq array, maxFreq variable",
 "Recomputing maxFreq on every shrink; wrong atMost monotonicity assumption",
 "O(n) or O(n | |alphabet|)",
 "Longest repeating character replacement, K different integers, permutation in string",
 "Cardinality-bounded caches; distinct-key windows in streaming analytics"),

("Binary search (index)",
 "sorted array; 'first/last position'; 'O(log n) required'",
 "sorted, or search space has a monotone property; n up to 10^7",
 "Maintain a half-open invariant (lo<=answer<hi); shrink systematically; no templates",
 "sorted array (or implicit sorted space)",
 "Off-by-one errors; lo<hi vs lo<=hi confusion; infinite loops; wrong mid formula",
 "O(log n)",
 "Binary search, first/last position, find minimum in rotated array",
 "SSTable lookups, sorted offset indexes, version search"),

("Binary search on answer",
 "'minimize the maximum','maximize the minimum','minimum capacity/speed/time'; large answer range",
 "answer <= 10^9, predicate check is O(n) or O(n log n)",
 "Search the ANSWER SPACE with a monotone feasible(x) predicate; 3 validity conditions must hold",
 "feasibility predicate function + binary search loop",
 "Non-monotone predicate; wrong search bounds; predicate accidentally O(n^2)",
 "O(n log(answer_range))",
 "Koko eating bananas, ship packages, split array, min days for bouquets",
 "Capacity planning, autoscaling, SLO fitting, quota allocation"),

("Sort + linear scan (preprocessing)",
 "'intervals','pairs','sorted input assumed'; O(n log n) acceptable",
 "n up to 10^5, no online queries",
 "Sorting creates a monotonicity you can then exploit with a single greedy pass",
 "sort + one or two pointers or a heap",
 "Wrong sort key (start vs end vs value); assuming stability; sorting when a heap suffices",
 "O(n log n)",
 "Merge intervals, non-overlapping intervals, sort colors, meeting rooms",
 "Log compaction ordering, sorted shard merging, LSM-tree compaction"),

("Interval / sweep line",
 "'overlapping intervals','maximum concurrent events','resources needed at peak'",
 "intervals, events with timestamps; n up to 10^5",
 "Convert intervals to +1/-1 events and sweep; or maintain a min-heap of active end times",
 "sorted events array, min-heap of end times",
 "Tie-breaking between end and start at the same time; off-by-one on closed intervals",
 "O(n log n)",
 "Meeting rooms II, car pooling, calendar, task scheduler",
 "Concurrent resource counting (GPU/CPU slots), admission control"),

("Monotonic stack",
 "'next greater/smaller element','previous smaller','span','largest rectangle'",
 "array; n up to 10^5",
 "Keep a monotone stack; each pop resolves one answer; total pops <= n  ->  amortized O(n)",
 "stack of indices (not values)",
 "Storing values not indices; equal-element double counting; missing sentinel flush at end",
 "O(n) amortized",
 "Daily temperatures, next greater element, largest rectangle in histogram, subarray minimums",
 "Monotone-break detection in metric streams, backpressure onset"),

("Monotonic deque",
 "'maximum/minimum of every window of size k','sliding extremum','windowed DP'",
 "fixed or bounded window; n up to 10^6",
 "Maintain a deque of indices in monotone order; evict out-of-window and dominated candidates",
 "deque of indices",
 "Not evicting expired indices; storing values not indices; wrong eviction order",
 "O(n)",
 "Sliding window maximum, jump game VI, constrained subsequence sum",
 "Rolling max latency, watermarks, windowed DP in schedulers"),

("Heap / top-K / streaming extremum",
 "'k largest/smallest','median of stream','schedule next available resource'",
 "k<<n or online data; n up to 10^6",
 "Partial order is enough; a heap gives the extreme in O(log n); heapify is O(n)",
 "min-heap or max-heap; two heaps for median; heap of (key, cursor) for merge",
 "Full sort when k is tiny; wrong polarity; not using lazy deletion for stale entries",
 "O(n log k) or O(log n) per operation",
 "Kth largest, k closest, find median from stream, merge k sorted lists, task scheduler",
 "Top-K hot keys, p99 estimation, eviction candidate selection, priority scheduling"),

("Greedy invariants",
 "'maximum number of','minimum steps','locally safe choice'; often after sorting",
 "exchange argument must hold; usually O(n log n)",
 "Prove by exchange or staying-ahead that the local choice is in some optimal solution",
 "sort + counters, heap, or simple scan",
 "Unproven greedy; missing a counterexample that breaks it; using greedy where DP is required",
 "O(n log n) typically",
 "Jump game II, gas station, partition labels, refueling stops",
 "Admission control, retry budgets, checkpoint placement"),

("Design / structure composition",
 "'implement X with O(1) get/put/delete','LRU','LFU','getRandom'",
 "operation TC is the spec; n up to 10^5 ops",
 "Compose two structures so each required operation is O(1)/O(log n); API dictates structures",
 "hash map + doubly linked list (LRU), freq buckets + maps (LFU), array + index map (getRandom)",
 "Choosing structures by habit not by API; forgetting to keep both structures in sync on every path",
 "O(1) per operation",
 "LRU cache, LFU cache, RandomizedSet, TimeMap, hit counter",
 "Page/feature/embedding caches, KV stores, rate limiters, versioned stores"),

("Bit manipulation",
 "'subset of at most 20 items','XOR','without extra space','count bits','feature flags'",
 "n<=20 for subset enumeration; 32/64-bit word for bit tricks",
 "A bitmask is a tiny set with O(1) set operations; XOR cancels pairs; use popcount for size",
 "integer masks, popcount, __builtin_ctz",
 "Signed right-shifts; operator precedence bugs (use parentheses); overflow on mask<<1",
 "O(1) per mask op; O(2^n) for full enumeration",
 "Single number II, sum without +, missing number, subset enumeration",
 "Bitmaps, feature flags, GPU lane/warp masks, bloom filter ops"),

("Tree recursion (contract-first)",
 "'depth','balanced','path sum','subtree property','lowest common ancestor'",
 "n up to 10^5; beware recursion depth on skewed trees",
 "Define exactly what the function returns for a subtree; write it in English before coding; then trust it",
 "recursion, call stack, optional memoisation",
 "Vague contracts; mixing 'answer' with 'return value'; stack overflow on skewed trees",
 "O(n)",
 "Depth, balanced, diameter, max path sum, LCA, validate BST",
 "Recursive dependency evaluation, nested config resolution"),

("Tree DP (post-order)",
 "'max path','rob houses in tree','distribute coins','max sum with no adjacent'",
 "tree, single-pass wanted",
 "Combine children's return values at the parent; return one value upward; update global answer separately",
 "recursion + tuple return (gain upward, answer updated)",
 "Returning the global answer upward; double-counting the root node; forgetting to clamp negatives",
 "O(n)",
 "Diameter, max path sum, house robber III, distribute coins",
 "Aggregating metrics up a topology/ownership tree"),

("BST ordering",
 "'validate BST','k-th smallest in BST','BST range queries'",
 "BST given, may be unbalanced",
 "In-order traversal is sorted; propagate valid range (lo, hi) top-down instead of comparing parent-child",
 "recursion with range bounds, iterative inorder stack",
 "Comparing only parent-child (misses deep violations); ignoring duplicate policy",
 "O(h) per operation",
 "Validate BST, kth smallest, insert/delete, range queries",
 "Ordered indexes, range scans, B-tree node invariants"),

("BFS levels / shortest hops",
 "'minimum steps','level order','nearest X','spread from source'",
 "unweighted graph or grid; n up to 10^5",
 "First visit = shortest distance; seed all sources at level 0 for multi-source; expand in layers",
 "queue, visited set/array",
 "Marking visited on pop (causes exponential blowup); mixing level boundaries",
 "O(V+E)",
 "Rotting oranges, word ladder, open the lock, right side view, 01-matrix",
 "Hop counts, blast-radius analysis, BFS-based propagation"),

("Graph DFS / components",
 "'islands','connected components','clone graph','cycle detection','safe states'",
 "grid or adjacency list; n up to 10^5",
 "Explore exhaustively; component identity or cycle colour (white/grey/black) is the output",
 "recursion or explicit stack, visited array, colour array for directed cycles",
 "Recursion depth on large grids; not handling multiple components; directed vs undirected cycle logic",
 "O(V+E)",
 "Number of islands, clone graph, find eventual safe states, course schedule",
 "Topology discovery, cluster membership, service-graph crawling"),

("Union Find (DSU)",
 "'connected components that grow','merge groups','edges arrive incrementally','redundant edge'",
 "n up to 10^6; many merges and find queries",
 "Maintain disjoint sets with path compression + union by size for near-O(1) amortized ops",
 "parent array + size array",
 "Forgetting BOTH optimizations; using DSU where order of nodes matters; O(n) find without compression",
 "O(alpha(n)) amortized per op",
 "Number of provinces, accounts merge, redundant connection, dynamic connectivity",
 "Cluster membership, shard grouping, entity dedup, dynamic edge-stream connectivity"),

("Topological sorting",
 "'prerequisites','build order','dependency resolution','detect cycle in directed graph'",
 "DAG (or detect if not); V+E up to 10^5",
 "Remove in-degree-0 nodes repeatedly (Kahn); or DFS with 3 colours; cycle = fewer than n emitted",
 "in-degree array + queue (Kahn), or recursion + colour array (DFS)",
 "Not detecting cycles; assuming a unique ordering exists; skipping isolated nodes",
 "O(V+E)",
 "Course schedule I/II, alien dictionary, task order, build systems",
 "DAG job scheduling, ML pipeline orchestration, build dependency resolution"),

("Dijkstra / weighted shortest path",
 "'minimum cost/time path','non-negative edge weights','network delay'",
 "weights >= 0; E up to 10^5",
 "Greedily finalize the closest unfinished node; the popped distance is final (non-negative weights only)",
 "min-heap of (distance, node) + dist array",
 "Using on negative weights; not skipping stale heap entries; wrong objective (min-max vs min-sum)",
 "O(E log V)",
 "Network delay, path with max probability, min effort, cheapest flights",
 "Latency-aware routing, cost-based placement, weighted service graphs"),

("State-space BFS/Dijkstra",
 "'minimum moves with a resource budget','compound state','configuration reachability'",
 "state space bounded and enumerable; states up to ~10^6",
 "Nodes are FULL STATES (not just position); encode the state tuple; visited keyed on the complete state",
 "queue or min-heap, visited set of encoded state tuples",
 "Visited keyed on partial state (silent wrong answer); unbounded state space; expensive encoding",
 "O(states * transitions)",
 "Sliding puzzle, obstacle elimination, open the lock, minimum genetic mutation",
 "Scheduler/config state exploration, rollout planning, deployment state machines"),

("Backtracking + pruning",
 "'all combinations/permutations/partitions','place N items with constraints'",
 "n small (<=20) or with heavy pruning; exponential in theory",
 "Choose, explore, unchoose; the real skill is pruning branches that cannot lead to valid solutions",
 "recursion, path array, bitmasks for O(1) constraint checks",
 "No pruning; incorrect dedup; mutating shared state without restoring it",
 "Exponential with pruning factor",
 "Subsets, permutations, N-Queens, sudoku, palindrome partitioning, word search",
 "Config search, placement under conflict constraints, hyperparameter enumeration"),

("Trie / prefix tree",
 "'prefix queries','dictionary of words','autocomplete','search with wildcards'",
 "alphabet size small (<=26); many words/queries",
 "Share prefixes to make prefix queries proportional to word length; enables DFS pruning",
 "trie nodes (array or hash map per node) with end flags",
 "Memory blowup on large alphabets; using a trie where a hashset is simpler and sufficient",
 "O(L) per operation (L = word length)",
 "Implement trie, word search II, add and search words, longest prefix match",
 "Autocomplete, tokenizer vocabularies, longest-prefix-match routing"),

("DP (1D state design)",
 "'number of ways','min/max cost','can we reach target','decisions at each step'",
 "n up to 10^5; clear stages or positions",
 "Define state  ->  transition  ->  base case  ->  evaluation order  ->  answer location (in that exact order)",
 "1D array or hash map",
 "Defining transition before state; wrong evaluation order; reading answer from wrong position",
 "O(n * states_per_position)",
 "Climbing stairs, house robber, decode ways, jump game, coin change",
 "Stage-wise cost optimisation, pipeline configuration selection"),

("DP (knapsack family)",
 "'subset sum','choose items under capacity budget','coin change','ways to make amount'",
 "capacity/sum bounded (pseudo-polynomial); n * capacity <= 10^7",
 "Capacity is a DP dimension; loop order encodes 0/1 (descending) vs unbounded (ascending)",
 "1D or 2D DP arrays",
 "Wrong loop order; counting permutations vs combinations; not handling 0-capacity base case",
 "O(n * capacity)",
 "Partition equal subset, coin change I/II, ones and zeroes, target sum",
 "Memory/GPU packing, multi-resource quota allocation"),

("DP (two sequences)",
 "'two strings','edit distance','common subsequence','interleaving'",
 "m, n up to ~1000",
 "dp[i][j] over prefixes of both sequences; derive transitions from the problem definition",
 "2D array or rolling 1D for space optimization",
 "Index confusion (i=0 means empty prefix); wrong base cases; optimizing space before correctness",
 "O(mn) time, O(min(m,n)) space with rolling",
 "LCS, edit distance, interleaving strings, distinct subsequences",
 "Diffing, log/sequence alignment, tokenizer alignment"),

("DP (interval)",
 "'optimal order of operations on a range','merge/burst/remove from a subarray'",
 "n up to ~500 (O(n^3) acceptable)",
 "Solve shorter ranges first; pick the LAST operation (not first) to keep subproblems independent",
 "2D DP array dp[left][right]",
 "Picking the first operation instead of the last; wrong iteration order (must go by length)",
 "O(n^3)",
 "Burst balloons, longest palindromic subsequence, matrix chain, minimum cost to merge stones",
 "Optimal chunking, merge ordering, compaction cost minimisation"),

("DP (bitmask)",
 "'n<=20','visit all nodes','assign items to groups','travelling salesman variant'",
 "n<=20 (2^n states must fit in memory)",
 "State includes a subset bitmask; transition adds one element; (mask, position) is the full state",
 "dp[mask][...] arrays",
 "Not recognising the n<=20 signal; state explosion; recomputing popcount in the inner loop",
 "O(2^n | n) or O(2^n | n^2)",
 "Shortest path visiting all nodes, matchsticks to square, assignment, TSP-variants",
 "Job-to-machine assignment, small-scale optimal placement"),

("DP optimization (deque/heap in transition)",
 "naive DP transition is O(nk) or O(n^2) and n>10^3",
 "tight time limit + large n",
 "Optimize the transition by hiding a sliding-window maximum/minimum (monotonic deque) inside it",
 "DP array + monotonic deque or heap or prefix max array",
 "Optimizing before the naive recurrence is correct and verified; breaking the window bound",
 "O(n) or O(n log n)",
 "Jump game VI, constrained subsequence sum, LIS in O(n log n)",
 "Streaming DP with bounded lookback; windowed online decisions"),

("Fenwick Tree (BIT)",
 "'mutable range sum','inversion count','point update + prefix query'",
 "values coordinate-compressed; n up to 10^6",
 "Lowest set bit (i & -i) tree decomposition; O(log n) update and query with tiny constant factor",
 "1D array (1-indexed)",
 "0-indexing off-by-one; using when range updates needed without difference array",
 "O(log n) update/query",
 "Range sum query, smaller numbers after self, reverse pairs",
 "High-frequency telemetry counters, rolling latency meters"),

("Segment Tree (range query)",
 "'range min/max/sum/gcd query','point or range updates'; associative function",
 "array size n up to 5 * 10^5, associative operator",
 "Divide-and-conquer binary tree over array intervals; 4n array representation; lazy propagation",
 "tree array, lazy array",
 "Size 2n instead of 4n; forgetting push_down before inspecting children; non-associative ops",
 "O(n) build, O(log n) update/query",
 "Skyline, falling squares, range module, calendar booking",
 "Distributed SLA monitoring, physical memory reservation maps"),

("Tarjan's DFS (bridges & SCC)",
 "'critical connections','single point of failure','strongly connected components'",
 "directed or undirected graph, O(V + E) target",
 "Discovery time tin[u] and lowest ancestor low[u]; back-edge detection; condensation DAG",
 "tin array, low array, visited stack",
 "Updating low[u] from parent edge in undirected graph; not popping stack up to u in SCC",
 "O(V + E)",
 "Critical connections, graph disconnect, condensation DAG",
 "Fault-domain isolation, deadlock detection, build dependency validation"),

("Hardware / Cache calibration",
 "high throughput, 10M+ QPS, low latency SLO, memory-constrained traversal",
 "CPU cache line 64 bytes, DRAM access 60ns vs L1 1ns",
 "Structure data contiguously (AOS vs SOA); eliminate pointer chasing; size blocks to L1/L2 cache",
 "flat contiguous buffers, cyclic arrays",
 "Using linked lists / pointer trees in hot paths; ignoring false sharing and cache-line bouncing",
 "O(n) with 10x lower constant factor",
 "Matrix transposition, ring buffers, flat hash tables",
 "Tensor memory layouts, GPU shared memory tiling, low-latency trading"),

("High-performance hashing",
 "zero tail-latency, low collision variance, predictable lookup time",
 "in-memory key-value store, load factor 0.8 - 0.9",
 "Robin Hood displacement or Cuckoo two-table hashing; bounded worst-case probe lengths",
 "flat key/value array + probe count byte",
 "Infinite loops during cuckoo cycles without stash; bad hash functions",
 "O(1) average and worst-case",
 "In-memory KV store, RocksDB cache, Swiss table",
 "Storage engine block caches, Memcached, Redis hash tables"),

("Adaptive Cache (ARC)",
 "dynamic workload with mixed scans and recurring loops; hit ratio optimization",
 "fixed cache memory budget c",
 "Balance recency (T1) and frequency (T2) dynamically using ghost history lists (B1, B2)",
 "4 LRU lists (T1, T2, B1, B2) + hash map",
 "Losing ghost entries on eviction; incorrect target size p boundary clipping [0, c]",
 "O(1) per lookup and update",
 "ZFS storage ARC, buffer pool management, LLM prompt cache",
 "Database buffer managers, kernel page caches, multi-tenant AI caching"),

("Lock-free ring buffer",
 "high-speed inter-thread message passing; zero lock contention; producer-consumer",
 "single producer single consumer (SPSC) or MPMC; power-of-two size",
 "Head and tail indices advancing monotonically; masking with (size - 1); cache line padding (64 bytes)",
 "atomic size_t head, tail; contiguous array buffer",
 "False sharing between head and tail; missing memory barriers (acquire/release); ABA problem in MPMC",
 "O(1) wait-free SPSC / lock-free MPMC",
 "Circular queue, circular deque, bounded blocking queue",
 "LMAX Disruptor, GPU command rings, high-throughput network packet ingestion"),

("HNSW graph search",
 "approximate nearest neighbor (ANN), vector similarity, high dimensionality (d=128 to 1536)",
 "dataset N up to 10^8 vectors, query latency < 5ms",
 "Multi-layer proximity graph (skip-list concept); greedy routing on coarse upper layers, beam search on layer 0",
 "layered adjacency list, candidate priority queue, visited set",
 "Local minima traps with too small efSearch; cyclic graph infinite loops without visited filter",
 "O(log N) average query time",
 "Vector embeddings, multimodal search, semantic retrieval",
 "Vector databases (Milvus, Pinecone, Qdrant, FAISS), RAG pipelines"),
]

PATTERN_SEARCH_KEYS = {
    'Complexity calibration': 'Complexity',
    'Frequency/counting + hashing': 'Frequency',
    'Prefix/suffix reasoning': 'Prefix',
    'Two pointers (opposite ends)': 'opposite ends',
    'Two pointers (same direction / read-write)': 'read/write',
    'Sliding window (variable)': 'variable',
    'Sliding window + counting': 'frequency',
    'Binary search (index)': 'Binary search',
    'Binary search on answer': 'Binary search on answer',
    'Sort + linear scan (preprocessing)': 'Sort',
    'Interval / sweep line': 'Interval',
    'Monotonic stack': 'Monotonic stack',
    'Monotonic deque': 'Monotonic deque',
    'Heap / top-K / streaming extremum': 'Heap',
    'Greedy invariants': 'Greedy',
    'Design / structure composition': 'Design',
    'Bit manipulation': 'Bit',
    'Tree recursion (contract-first)': 'Tree recursion',
    'Tree DP (post-order)': 'Tree DP',
    'BST ordering': 'BST',
    'BFS levels / shortest hops': 'BFS',
    'Graph DFS / components': 'Graph',
    'Union Find (DSU)': 'Union Find',
    'Topological sorting': 'Topological',
    'Dijkstra / weighted shortest path': 'Dijkstra',
    'State-space BFS/Dijkstra': 'State-space',
    'Backtracking + pruning': 'Backtracking',
    'Trie / prefix tree': 'Trie',
    'DP (1D state design)': 'DP (1D)',
    'DP (knapsack family)': 'knapsack',
    'DP (two sequences)': 'sequences',
    'DP (interval)': 'interval',
    'DP (bitmask)': 'bitmask',
    'DP optimization (deque/heap in transition)': 'deque',
    'Fenwick Tree (BIT)': 'Fenwick',
    'Segment Tree (range query)': 'Segment Tree',
    'Tarjan\'s DFS (bridges & SCC)': 'Tarjan',
    'Hardware / Cache calibration': 'Hardware',
    'High-performance hashing': 'hashing',
    'Adaptive Cache (ARC)': 'ARC',
    'Lock-free ring buffer': 'Lock-free',
    'HNSW graph search': 'HNSW',
}

for i, row in enumerate(PATTERNS):
    r = i + 2
    for c, v in enumerate(row, 1):
        cell = put(ws_pl, r, c, v)
        if c == 10: cell.alignment = CTR
    # formula: count appearances in DayPlan pattern column
    pat_name = row[0]
    core_kw = PATTERN_SEARCH_KEYS.get(pat_name, pat_name.split("(")[0].strip())
    ws_pl.cell(row=r, column=11, value=f'=COUNTIF(DayPlan!$E$2:$E${DAYS+1},"*{core_kw}*")')
    ws_pl.cell(row=r, column=11).alignment = CTR
    ws_pl.cell(row=r, column=11).border = BORDER
    ws_pl.cell(row=r, column=12, value=f'=IF(MAXIFS(ProblemDB!$F$2:$F${PDB_ROWS},ProblemDB!$D$2:$D${PDB_ROWS},"*{core_kw}*")>0,MAXIFS(ProblemDB!$F$2:$F${PDB_ROWS},ProblemDB!$D$2:$D${PDB_ROWS},"*{core_kw}*"),"-")')
    ws_pl.cell(row=r, column=12).number_format = "dd-mmm"
    ws_pl.cell(row=r, column=12).alignment = CTR
    ws_pl.cell(row=r, column=12).border = BORDER
    ws_pl.row_dimensions[r].height = 44

dv(ws_pl, SCORE_VALS, f"J2:J{len(PATTERNS)+1}", "Mastery 1-5")
ws_pl.conditional_formatting.add(f"J2:J{len(PATTERNS)+1}",
    ColorScaleRule(start_type="num", start_value=1, start_color=RED_D,
                   mid_type="num",   mid_value=3,   mid_color=AMBER_D,
                   end_type="num",   end_value=5,   end_color=GREEN_D))
ws_pl.auto_filter.ref = f"A1:L{len(PATTERNS)+1}"
print(f"[OK] PatternLibrary: {len(PATTERNS)} patterns")

# --- SHEET: PatternCards ------------------------------------------------------
ws_pc = wb.create_sheet("PatternCards")
ws_pc.sheet_view.showGridLines = False

PC_H = [
    "Anchor Problem","Pattern",
    "Trigger [pre-filled]","Core Insight [YOU fill from memory]",
    "Data Structure + why [pre-filled]","Invariant [YOU fill from memory]",
    "Complexity + argument [pre-filled]","Failure Mode of average candidate",
    "Interviewer Variations","Recognition Cue (next time)",
    "Last reconstructed","Reconstruction score (1-5)",
]
PC_W = [34,24,40,42,28,40,26,44,40,34,12,12]
write_header(ws_pc, PC_H, PC_W, freeze="C2")

CARDS = [
("LC 560 Subarray Sum Equals K","Prefix + hash",
 "'count subarrays with sum = k' + negatives present  ->  window fails",
 "hash map prefix -> count; store what you've seen; look up (prefix - k)",
 "O(n) time O(n) space: one pass, O(1) map ops",
 "Sliding window fails with negatives (non-monotone). Use prefix+count map.",
 "F11: tries sliding window; fails because negatives break monotonicity",
 "Return the longest such subarray; 2D version; sum divisible by k",
 "Contiguous + sum + negatives = prefix hash, not window"),

("LC 76 Minimum Window Substring","Sliding window + counting",
 "'minimum window containing all characters of t'",
 "need/have counters + two pointers; expand right, shrink left when have==need",
 "O(n+m): amortized pointer movement",
 "When 'have' increments (only when freq goes from need-1 to need); shrink while valid",
 "F6: recomputes the whole counter check each step  ->  O(n^2)",
 "Multiple pattern strings; window over a stream; minimum window subsequence",
 "Shortest valid window = expand right first, shrink left aggressively"),

("LC 875 Koko Eating Bananas","Binary search on answer",
 "'minimum speed such that all piles eaten within h hours'",
 "feasible(speed) = all(ceil(p/speed) for p in piles) <= h; monotone decreasing as speed grows",
 "O(n log(max_pile)): predicate is O(n)",
 "feasible(x) is monotone: if x works, x+1 also works",
 "F3: tries greedy or average; doesn't see the monotone predicate",
 "Non-integer speeds; per-pile costs; maximize instead of minimize",
 "'minimum X such that condition holds' = BS on answer"),

("LC 84 Largest Rectangle in Histogram","Monotonic stack",
 "'largest rectangle area under bars'",
 "maintain increasing-height stack of indices; on each pop, compute the rectangle using right-left-1",
 "O(n) amortized: each index pushed and popped exactly once",
 "Stack contains indices of bars in strictly increasing height order at all times",
 "F6: nested loops O(n^2); mishandles equal heights or the end-of-array flush",
 "Maximal rectangle in binary matrix; 3D variant; sum of subarray minimums",
 "Need previous-smaller and next-smaller boundaries simultaneously = monotonic stack"),

("LC 295 Find Median from Data Stream","Two heaps (streaming)",
 "'median of a stream' + online insertion",
 "max-heap for lower half + min-heap for upper half; rebalance so sizes differ by at most 1",
 "O(log n) insert, O(1) median query",
 "max-heap.size  in  {min-heap.size, min-heap.size+1} at all times; max-heap.top <= min-heap.top",
 "F3: re-sorts on every query; O(n log n) per call",
 "Sliding-window median; arbitrary percentile; distributed streaming quantiles",
 "Online order statistic = two heaps or segment tree + BIT"),

("LC 146 LRU Cache","Design composition",
 "'O(1) get and put with LRU eviction'",
 "hash map for O(1) lookup + doubly linked list for O(1) move-to-front and O(1) eviction from tail",
 "O(1) per operation",
 "Most-recently-used node is always at head; least-recently-used is always at tail",
 "F4: uses array/list  ->  O(n) moves; or forgets to update the map on eviction",
 "TTL eviction; thread-safe LRU; LFU; write-through/write-back",
 "O(1) ordered access = hash map + doubly linked list"),

("LC 460 LFU Cache","Design composition",
 "'O(1) get and put with LFU eviction'",
 "freq -> OrderedDict bucket map + key -> (val,freq) map + minFreq pointer",
 "O(1) per operation",
 "minFreq can only increase by 0 or 1 on an access; it resets to 1 on every put of a new key",
 "F3: scans for min frequency O(n); loses the minFreq invariant on edge cases",
 "Aging/decay of counts; window LFU; hybrid ARC policy",
 "Frequency-ordered eviction = bucketed frequency lists with a minFreq pointer"),

("LC 124 Binary Tree Maximum Path Sum","Tree DP post-order",
 "'maximum path sum' where path can bend at any node",
 "at each node, return max(0, node.val + best_downward) for parent; update global answer with left+node+right",
 "O(n): one visit per node",
 "Return value = best downward gain from this node; global answer = best bent path through this node",
 "F3: returns the bent path upward; forgets to clamp negative downward gains to 0",
 "Path with at most k turns; count of maximum paths; k-ary tree variant",
 "Global answer updated at node != value returned to parent"),

("LC 297 Serialize/Deserialize Tree","Encoding design",
 "'serialize a tree to a string and deserialize it back'",
 "preorder traversal + null markers; use a queue/index cursor during deserialization",
 "O(n) both directions",
 "Every null must be explicitly encoded; the grammar determines unique decodability",
 "F1: improvises the format; cannot parse back an ambiguous encoding",
 "N-ary tree; BST-optimized encoding (no nulls needed); compact binary format",
 "Define the grammar BEFORE writing code  ->  guaranteed decodability"),

("LC 207 Course Schedule (topological sort)","Topological sort",
 "'prerequisites exist','valid ordering required','detect cycle in directed graph'",
 "Kahn: maintain in-degree array + queue; emit when in-degree reaches 0; cycle if emitted < n",
 "O(V+E)",
 "In-degree-0 nodes are always safe to emit; the queue holds exactly the current safe-to-emit set",
 "F6: cannot detect cycles; assumes unique ordering",
 "Lexicographically smallest order; parallel scheduling with k workers; critical path",
 "'ordering with dependencies' = topological sort (Kahn or DFS-colours)"),

("LC 743 Network Delay Time","Dijkstra",
 "'minimum time for signal to reach all nodes' + non-negative weights",
 "standard Dijkstra; answer = max of all shortest distances; -1 if any node unreachable",
 "O(E log V)",
 "Once a node is popped from the min-heap, its distance is final (non-negative weights guarantee this)",
 "F3: uses plain BFS on weighted edges; or forgets to skip stale heap entries",
 "Negative weights (use Bellman-Ford); k-hop limit (add hop dimension); multi-source",
 "Weighted min cost + non-negative weights = Dijkstra"),

("LC 787 Cheapest Flights Within K Stops","Layered DP / Bellman-Ford",
 "'cheapest path with at most k stops' = extra constraint on path length",
 "dp[t][v] = min cost to reach v using at most t hops; iterate t from 1 to k+1",
 "O(k | E): k+1 rounds of edge relaxation",
 "Using exactly t hops distinguishes dp layers; copy previous layer before updating",
 "F3: runs plain Dijkstra and ignores the stop constraint; or modifies dist in-place breaking the layer",
 "Exactly k stops; time windows; multiple path constraints",
 "Extra constraint on a path = add a state dimension (hops, resources, keys)"),

("LC 1293 Shortest Path Grid with Obstacles","State-space BFS",
 "'minimum steps' + 'budget of k removals'",
 "BFS over state = (row, col, remaining_removals); visited is a 3D array",
 "O(rows | cols | k)",
 "The state is (position + resource); visited must include ALL components of the state",
 "F3: keys visited on (r,c) only  ->  finds a path but not necessarily the minimum (wrong answer silently)",
 "Multiple resource budgets; weighted removals  ->  Dijkstra over states",
 "Budget/resource in problem = extra state dimension  ->  state-space search"),

("LC 51 N-Queens","Backtracking + pruning",
 "'place n non-attacking queens on n*n board'",
 "recurse row by row; track occupied cols, main diags, anti-diags with bitmasks for O(1) conflict check",
 "O(n!) with heavy pruning",
 "At any partial placement, each attacked set is maintained incrementally (add on enter, remove on exit)",
 "F6: no incremental conflict tracking; rescans the board each step",
 "Count only; n<=15 with bitmask DP; other piece types; hexagonal boards",
 "Constraint placement = backtracking with O(1) conflict checks via bitmasks"),

("LC 300 Longest Increasing Subsequence","DP + binary search",
 "'longest strictly increasing subsequence'",
 "tails[i] = smallest tail of all LIS of length i+1; binary search to find insertion point",
 "O(n log n); naive DP is O(n^2)",
 "tails is always sorted; tails[i] is updated in place; it does NOT store an actual subsequence",
 "F3: confuses tails with an actual subsequence; or uses wrong bound (lower vs upper)",
 "Count of LIS; 2D (envelopes); non-strict version; print one LIS",
 "Subsequence + order constraint = DP; optimize with patience sorting (tails + binary search)"),

("LC 312 Burst Balloons","Interval DP",
 "'optimal order of removals from a range', 'multiply with neighbors'",
 "dp[l][r] = max coins when all balloons in (l,r) are burst; try each k as the LAST to burst in range",
 "O(n^3)",
 "The LAST balloon to burst in a range sees its left and right boundaries as fixed; subproblems are independent",
 "F3: picks the FIRST burst  ->  subproblems overlap; the key is reversing to think about the last operation",
 "Merge stones; matrix chain; k-way merges; removing elements with range penalties",
 "Order-of-operations optimum = interval DP with 'last operation' framing"),

("LC 847 Shortest Path Visiting All Nodes","Bitmask BFS",
 "'shortest path visiting all n nodes', n<=12",
 "BFS over state = (node, visited_mask); seed with all (node, 1<<node) states at distance 0",
 "O(2^n | n^2)",
 "n<=12 is the only signal needed: 2^1^2=4096 states * 12 nodes = trivially enumerable",
 "F2: misses the n<=12 constraint; tries shortest path ignoring the 'visit all' constraint",
 "Weighted edges (Dijkstra over states); must return to start; k-of-n visits",
 "Tiny n + 'visit all' = bitmask state space"),

("LC 1425 Constrained Subsequence Sum","DP + monotonic deque",
 "'maximum subsequence sum where index gap <= k'",
 "dp[i] = max(nums[i], max(dp[j] for j in [i-k, i-1]) + nums[i]); optimize with a deque max",
 "O(n) after optimizing from O(nk)",
 "Deque maintains indices of maximum dp values in decreasing order; evict those outside [i-k, i-1]",
 "F5: writes O(nk) and times out; or optimizes before verifying correctness of the recurrence",
 "Two-sided constraints; weighted gaps; streaming variant with a sliding window",
 "Sliding-window maximum hidden inside a DP transition = monotonic deque"),

("LC 380 Insert Delete GetRandom O(1)","Design composition",
 "'O(1) insert, delete, and uniform random element'",
 "array for O(1) random access + hash map (val -> index) for O(1) lookup; delete by swap-with-last",
 "O(1) per operation amortized",
 "After swap-with-last, update the moved element's index in the map; then pop the last element",
 "F4: uses a set  ->  cannot do O(1) uniform random sample",
 "Duplicates allowed; weighted random; distributed sampling",
 "Uniform random + O(1) delete = array + index map (swap-with-last)"),

("LC 410 Split Array Largest Sum","BS on answer + DP (2-sol)",
 "'split array into m parts to minimize the largest part sum'",
 "BS: feasible(mid) = can we split with each part <= mid?  -  greedy O(n); DP: dp[k][i]=min largest for k parts in A[i:]",
 "O(n log(sum)); DP: O(mn^2)",
 "feasible(x) is monotone: if x works, x+1 also works; this is the key validity condition",
 "F3: jumps to DP and times out; or writes a non-monotone predicate",
 "Return the actual split; k as a variable; weights; minimize sum of maximums",
 "'Minimize the maximum' = binary search on answer + greedy feasibility check"),

("LC 307 Range Sum Query - Mutable", "Segment Tree / BIT",
 "'mutable array with dynamic range sum queries'",
 "binary tree over array intervals OR lowest-set-bit tree (i & -i); O(log n) update and query",
 "O(log n) update, O(log n) query",
 "Range sum in BIT: query(r) - query(l-1); Segment Tree: combine(left_child, right_child)",
 "F6: writes O(n) scan on query or O(n) rebuild on update; TLE on frequent updates",
 "Range minimum/maximum query; lazy propagation for range updates; 2D Fenwick",
 "Mutable array + frequent range queries = Segment Tree or BIT"),

("LC 1192 Critical Connections in a Network", "Tarjan's DFS",
 "'edges whose removal disconnects the graph (bridges)'",
 "DFS tracking discovery time tin[u] and lowest reachable ancestor low[u]; bridge if low[v] > tin[u]",
 "O(V + E) time, O(V) space",
 "low[u] = min(low[u], tin[v]) for back-edges; low[u] = min(low[u], low[v]) for tree-edges",
 "F3: removes each edge and runs BFS O(E * (V+E)) -> TLE; forgets to skip parent edge in low calculation",
 "Articulation points (cut vertices); strongly connected components (condensation DAG)",
 "Single point of failure / bridge edge = Tarjan tin/low DFS"),

("LC 332 Reconstruct Itinerary", "Eulerian Path",
 "'visit every directed edge exactly once in lexicographical order'",
 "Hierholzer's algorithm: post-order DFS with sorted adjacency lists; prepend to path on return",
 "O(E log E) due to sorting edges",
 "When current node has no outgoing edges, it must be the end of the Eulerian path; prepend to itinerary",
 "F6: greedy DFS gets stuck in dead ends without backtracking; does not reverse post-order traversal",
 "De Bruijn sequence; DNA fragment reconstruction; network packet trace",
 "Visit all edges exactly once = Hierholzer Eulerian traversal"),

("LC 28 Find First Occurrence in String", "KMP pattern matching",
 "'find needle in haystack in linear time without backtracking'",
 "precompute prefix function pi[i] (longest proper prefix also a suffix); transition state machine",
 "O(N + M) time, O(M) space",
 "pi[i] is the length of the longest proper prefix of s[0..i] that is also a suffix of s[0..i]",
 "F6: resets haystack pointer on mismatch -> O(N*M) worst case on repeating patterns",
 "Aho-Corasick multi-pattern search; shortest palindrome prefix; cyclic shift check",
 "Linear string matching without backtracking = KMP prefix function"),

("Adaptive Replacement Cache (ARC)", "Self-tuning cache",
 "'cache workload with mixed sequential scans and recurring hot loops'",
 "four lists (T1 recent, T2 frequent, B1 ghost recent, B2 ghost frequent); adapt target size p",
 "O(1) per lookup, insertion, and eviction",
 "Total cache entries in T1 + T2 <= c; total ghost + active entries in T1 + T2 + B1 + B2 <= 2c",
 "F4: uses standard LRU; single sequential scan flushes all frequent pages out of memory",
 "2Q cache; Clock-Pro page replacement; LRFU with exponential decay",
 "Scan-resistant self-tuning caching = ARC 4-list architecture"),

("Lock-Free SPSC Ring Buffer", "Concurrency primitive",
 "'ultra-low latency producer-consumer message queue without mutexes'",
 "head and tail indices with power-of-two mask; cache-line padding (64 bytes); acquire-release semantics",
 "O(1) wait-free operations",
 "Buffer is full when (tail - head) == capacity; empty when tail == head; indices monotonically increase",
 "F10: places head and tail in the same cache line -> massive false sharing penalty; uses slow modulo",
 "MPMC bounded queue; work-stealing deque; ring buffer stream compaction",
 "Wait-free single-producer single-consumer = padded lock-free ring buffer"),

("Chase-Lev Work-Stealing Deque", "Work runtime scheduling",
 "'thread pool scheduler with private fast-path and concurrent stealing'",
 "owner pushes and pops LIFO at bottom (no CAS needed); thief workers steal FIFO at top with atomic CAS",
 "O(1) owner amortized, O(1) concurrent steal",
 "Owner operations bottom-- and bottom++ only synchronize with steal_top when bottom - top <= 1",
 "F6: synchronizes owner operations with global mutex; destroys parallel scalability",
 "Go runtime scheduler; Tokio async runtime; Ray distributed execution engine",
 "Task pool with fast owner + concurrent steal = Chase-Lev Deque"),

("HNSW Vector Proximity Graph", "Vector search index",
 "'approximate nearest neighbor search on high-dimensional vectors in <5ms'",
 "hierarchical proximity graph; greedy search at top sparse layers; beam search on dense layer 0",
 "O(log N) query time, O(N * M) space",
 "At each layer, greedy step moves to neighbor closer to query; stops when no neighbor is strictly closer",
 "F3: uses KD-Tree for d=1536 -> degrades to O(N) exhaustive scan due to curse of dimensionality",
 "IVF-PQ indexing; random projection trees (Annoy); ScaNN anisotropic vector quantization",
 "High-dimensional vector search = HNSW proximity graph navigation"),

("LC 2050 Parallel Courses III", "Critical Path DAG",
 "'minimum time to complete all tasks with precedence constraints and task durations'",
 "topological sort computing longest path on DAG: dist[v] = max(dist[u] + time[v])",
 "O(V + E) time, O(V) space",
 "dist[v] represents earliest finish time of course v; global answer is max(dist[v]) across all v",
 "F3: tries Dijkstra with shortest path; critical path is LONGEST path in a DAG",
 "Memory-bounded operator scheduling; heterogeneous device placement; pipeline latency",
 "Precedence constraints + duration = Critical Path DAG scheduling"),

("Count-Min Sketch & Misra-Gries", "Streaming algorithms",
 "'estimate item frequencies and find top-K heavy hitters in sub-linear space'",
 "d x w 2D counter array with independent hash functions; Misra-Gries k-1 candidate pool",
 "O(1) per update, O(w * d) space",
 "Count-Min point estimate is min(C[i, h_i(x)]); Misra-Gries decrements all counts only when pool is full",
 "F4: stores all unique keys in hash map -> O(N) memory explosion on streaming big data",
 "HyperLogLog cardinality; Bloom filter set membership; Reservoir sampling",
 "Streaming top-K and frequency in bounded space = Count-Min Sketch + Misra-Gries"),
]

for i, card in enumerate(CARDS):
    r = i + 2
    (prob, pat, trigger, ds, comp, inv_note, fail, var, cue) = card
    vals_pc = [prob, pat, trigger, None, ds, None, comp, fail, var, cue, None, None]
    for c, v in enumerate(vals_pc, 1):
        cell = put(ws_pc, r, c, v)
        if c == 11: cell.number_format = "dd-mmm"
        if c in (11, 12): cell.alignment = CTR
    ws_pc.row_dimensions[r].height = 52

# Highlight the two YOU-FILL columns in amber
for col in ("D", "F"):
    ws_pc.conditional_formatting.add(f"{col}2:{col}{len(CARDS)+1}",
        FormulaRule(formula=[f'ISBLANK(${col}2)'],
                    fill=fill(AMBER)))

dv(ws_pc, SCORE_VALS, f"L2:L{len(CARDS)+1}", "Reconstruction score")
ws_pc.auto_filter.ref = f"A1:L{len(CARDS)+1}"
print(f"[OK] PatternCards: {len(CARDS)} cards")

# --- SHEET: ProblemDB ---------------------------------------------------------
ws_pdb = wb.create_sheet("ProblemDB")
ws_pdb.sheet_view.showGridLines = False

PDB_H = [
    "Problem","Platform","Difficulty","Pattern","Sub-pattern",
    "First Attempt","Solved Independently?","Time Taken (min)","Hints Used","Solution Viewed?",
    "TC","SC","Mistake Category","Key Insight (one line)","Recognition Cue",
    "Next Review","Review 2","Review 3","Mastered?","Notes",
    "Week","Priority Score","Days To Due","2nd Solution Found?",
]
PDB_W = [34,10,9,22,20,12,12,9,8,11,16,14,18,44,34,12,12,12,10,34,6,9,10,12]
write_header(ws_pdb, PDB_H, PDB_W, freeze="B2")

for r in range(2, PDB_ROWS + 1):
    for c in range(1, 25):
        cell = ws_pdb.cell(row=r, column=c)
        cell.border = BORDER
        cell.alignment = WRAP if c in (1,4,5,13,14,15,20) else CTR

    # Adaptive review dates (performance-based)
    # Next review: solution viewed  ->  +1 day; not independent  ->  +2 days; hints  ->  +3; else +7
    ws_pdb.cell(r, 16).value = (
        f'=IF($F{r}="","",IF($J{r}="Yes",$F{r}+1,'
        f'IF($G{r}="No",$F{r}+2,'
        f'IF(N($I{r})>2,$F{r}+3,'
        f'IF(N($I{r})>0,$F{r}+5,$F{r}+7)))))')
    ws_pdb.cell(r, 16).number_format = "dd-mmm"

    # Review 2: if prev was due soon, shorter interval = still shaky
    ws_pdb.cell(r, 17).value = (
        f'=IF($P{r}="","",IF($J{r}="Yes",$P{r}+3,'
        f'IF($G{r}="No",$P{r}+5,'
        f'IF(N($I{r})>0,$P{r}+7,$P{r}+14))))')
    ws_pdb.cell(r, 17).number_format = "dd-mmm"

    # Review 3
    ws_pdb.cell(r, 18).value = (
        f'=IF($Q{r}="","",IF($J{r}="Yes",$Q{r}+7,'
        f'IF($G{r}="No",$Q{r}+14,$Q{r}+30)))')
    ws_pdb.cell(r, 18).number_format = "dd-mmm"

    ws_pdb.cell(r, 6).number_format  = "dd-mmm"

    # Priority score (higher = review sooner)
    # = 4*(solution viewed) + 3*(not independent) + 2*(hints>0) + 1*(slow>45min) + 3*(overdue) - 6*(mastered)
    ws_pdb.cell(r, 22).value = (
        f'=IF($A{r}=""," ",'
        f'4*($J{r}="Yes")'
        f'+3*($G{r}="No")'
        f'+2*(N($I{r})>0)'
        f'+1*(AND(ISNUMBER($H{r}),$H{r}>45))'
        f'+3*(AND(ISNUMBER($P{r}),$P{r}<=TODAY()))'
        f'-6*($S{r}="Yes")'
        f'+({PDB_ROWS}-ROW())/100000)')

    # Days to due (negative = overdue)
    ws_pdb.cell(r, 23).value = (
        f'=IF(OR($A{r}="",NOT(ISNUMBER($P{r}))),"",INT($P{r}-TODAY()))')

    # Auto-calculate Week in Col 21 (U) from First Attempt date
    ws_pdb.cell(r, 21).value = f'=IF($F{r}="","",MIN({WEEKS},MAX(1,ROUNDUP(($F{r}-DayPlan!$C$2+1)/7,0))))'
    ws_pdb.cell(r, 21).alignment = CTR
    ws_pdb.cell(r, 21).border = BORDER

dv(ws_pdb, DIFF_VALS, f"C2:C{PDB_ROWS}", "Difficulty")
dv(ws_pdb, YN_VALS,   f"G2:G{PDB_ROWS}", "Independent?")
dv(ws_pdb, YN_VALS,   f"J2:J{PDB_ROWS}", "Solution viewed?")
dv(ws_pdb, YN_VALS,   f"S2:S{PDB_ROWS}", "Mastered?")
dv(ws_pdb, YN_VALS,   f"X2:X{PDB_ROWS}", "2nd solution found?")
dv(ws_pdb, FCATS,     f"M2:M{PDB_ROWS}", "Mistake category")

ws_pdb.conditional_formatting.add(f"G2:G{PDB_ROWS}",
    CellIsRule("equal", ['"No"'],  fill=fill(RED)))
ws_pdb.conditional_formatting.add(f"G2:G{PDB_ROWS}",
    CellIsRule("equal", ['"Yes"'], fill=fill(GREEN)))
ws_pdb.conditional_formatting.add(f"J2:J{PDB_ROWS}",
    CellIsRule("equal", ['"Yes"'], fill=fill(RED)))
ws_pdb.conditional_formatting.add(f"S2:S{PDB_ROWS}",
    CellIsRule("equal", ['"Yes"'], fill=fill(GREEN)))
ws_pdb.conditional_formatting.add(f"W2:W{PDB_ROWS}",
    CellIsRule("lessThanOrEqual", ["0"], fill=fill(AMBER)))
ws_pdb.conditional_formatting.add(f"V2:V{PDB_ROWS}",
    ColorScaleRule(start_type="num", start_value=0, start_color=GREEN_D,
                   mid_type="num",   mid_value=5,   mid_color=AMBER_D,
                   end_type="num",   end_value=10,  end_color=RED_D))

# Seed one example row (only user-editable columns)
seed_data = {
    1: "LC 1 Two Sum", 2: "LeetCode", 3: "E", 4: "Frequency/hashing",
    5: "complement lookup", 6: START, 7: "Yes", 8: 12, 9: 0, 10: "No",
    11: "O(n)", 12: "O(n)", 13: "",
    14: "Store the complement you need, not the values you have seen",
    15: "'pair sums to target' + unsorted -> hash complement",
    19: "No", 20: "Starter example entry", 24: "No"
}
for c, v in seed_data.items():
    ws_pdb.cell(2, c).value = v
ws_pdb.cell(2, 6).number_format = "dd-mmm"
ws_pdb.auto_filter.ref = f"A1:X{PDB_ROWS}"
print("[OK] ProblemDB sheet built")

# --- SHEET: FailureLog --------------------------------------------------------
ws_fl = wb.create_sheet("FailureLog")
ws_fl.sheet_view.showGridLines = False

FL_H = [
    "Date","Week","Problem","Failure Type","What I thought (my model)",
    "What was actually wrong","Correct mental model",
    "Preventive rule (one sentence, actionable)",
    "Related problems","Re-test Date","Retest Result",
    "Rule fired on retest?",
]
FL_W = [12,8,32,20,38,38,38,48,24,12,12,14]
write_header(ws_fl, FL_H, FL_W, freeze="D2")

for r in range(2, FL_ROWS + 1):
    for c in range(1, 13):
        cell = ws_fl.cell(row=r, column=c)
        cell.border = BORDER
        cell.alignment = WRAP if c in (3,5,6,7,8,9) else CTR
    ws_fl.cell(r, 1).number_format = "dd-mmm"
    # Auto-calculate Week in Col 2 (B)
    ws_fl.cell(r, 2).value = f'=IF($A{r}="","",MIN({WEEKS},MAX(1,ROUNDUP(($A{r}-DayPlan!$C$2+1)/7,0))))'
    ws_fl.cell(r, 2).alignment = CTR
    # Re-test date in Col 10 (J)
    ws_fl.cell(r, 10).value = f'=IF($A{r}="","",$A{r}+3)'
    ws_fl.cell(r, 10).number_format = "dd-mmm"
    ws_fl.cell(r, 10).border = BORDER
    ws_fl.cell(r, 10).alignment = CTR

dv(ws_fl, FCATS, f"D2:D{FL_ROWS}", "Failure type")
dv(ws_fl, ["Solved independently","Solved with hint","Failed again","Not yet retested"],
   f"K2:K{FL_ROWS}", "Retest result")
dv(ws_fl, YN_VALS, f"L2:L{FL_ROWS}", "Rule fired?")

ws_fl.conditional_formatting.add(f"K2:K{FL_ROWS}",
    CellIsRule("equal", ['"Failed again"'], fill=fill(RED)))
ws_fl.conditional_formatting.add(f"K2:K{FL_ROWS}",
    CellIsRule("equal", ['"Solved independently"'], fill=fill(GREEN)))
ws_fl.conditional_formatting.add(f"L2:L{FL_ROWS}",
    CellIsRule("equal", ['"No"'], fill=fill(AMBER)))
ws_fl.auto_filter.ref = f"A1:L{FL_ROWS}"
print("[OK] FailureLog sheet built")

# --- SHEET: ReviewQueue -------------------------------------------------------
ws_rq = wb.create_sheet("ReviewQueue")
ws_rq.sheet_view.showGridLines = False

RQ_H = ["Rank","Problem","Pattern","Diff","Priority","Due Date","Days Overdue",
        "Why Queued","Required Action","Priority Key"]
RQ_W = [6,34,24,6,9,12,11,40,56,12]
write_header(ws_rq, RQ_H, RQ_W, freeze="B2")

ws_rq["L1"] = ("PRIORITY FORMULA: 4*(solution viewed) + 3*(not independent) + "
               "2*(hints>0) + 1*(slow >45min) + 3*(overdue) - 6*(mastered). "
               "Autosorts by priority. Top 25 shown.")
ws_rq["L1"].font = fnt(italic=True, sz=9, color="475569")

P_SRC = "ProblemDB"
for i in range(25):
    r = i + 2
    rank_val = i + 1
    put(ws_rq, r, 1, rank_val, align=CTR)

    large_f = f'=IFERROR(LARGE({P_SRC}!$V$2:$V${PDB_ROWS},A{r}),"")'
    sortkey_cell = ws_rq.cell(r, 10)
    sortkey_cell.value = large_f
    sortkey_cell.border = BORDER
    sortkey_cell.alignment = CTR

    m = f'MATCH(${chr(64+10)}{r},{P_SRC}!$V$2:$V${PDB_ROWS},0)'

    def idx(col_letter):
        return f'IFERROR(INDEX({P_SRC}!${col_letter}$2:${col_letter}${PDB_ROWS},{m}),"")'

    put(ws_rq, r, 2, f'={idx("A")}')
    put(ws_rq, r, 3, f'={idx("D")}')
    put(ws_rq, r, 4, f'={idx("C")}', align=CTR)
    put(ws_rq, r, 5, f'=IFERROR(INT({idx("V")}),"")', align=CTR)
    cell_due = put(ws_rq, r, 6, f'={idx("P")}', align=CTR)
    cell_due.number_format = "dd-mmm"
    put(ws_rq, r, 7, f'=IF(OR($F{r}="",$B{r}=""),"",INT(TODAY()-$F{r}))', align=CTR)

    put(ws_rq, r, 8,
        f'=IF($B{r}="","",IF({idx("J")}="Yes","Needed the solution (highest priority)",'
        f'IF({idx("G")}="No","Not solved independently",'
        f'IF(N({idx("I")})>0,"Hint-assisted",'
        f'IF(AND(ISNUMBER({idx("H")}),{idx("H")}>45),"Solved slowly (>45 min)",'
        f'"Spaced repetition due")))))')

    put(ws_rq, r, 9,
        f'=IF($B{r}="","",IF($E{r}>=7,'
        f'"Blank editor + timed. Rebuild from scratch. Explain aloud.",'
        f'IF($E{r}>=4,'
        f'"Rederive on paper first, then code clean. No notes.",'
        f'"Retrieval: state trigger + invariant + TC in 60 seconds only.")))')

    ws_rq.row_dimensions[r].height = 28

ws_rq.column_dimensions["J"].hidden = True

ws_rq.conditional_formatting.add("E2:E26",
    ColorScaleRule(start_type="num", start_value=0, start_color=GREEN_D,
                   mid_type="num",   mid_value=5,   mid_color=AMBER_D,
                   end_type="num",   end_value=10,  end_color=RED_D))
ws_rq.conditional_formatting.add("G2:G26",
    CellIsRule("greaterThan", ["0"], fill=fill(RED)))
print("[OK] ReviewQueue sheet built")

# --- SHEET: WeeklyAssessment --------------------------------------------------
ws_wa = wb.create_sheet("WeeklyAssessment")
ws_wa.sheet_view.showGridLines = False

WA_H = [
    "Week","Theme","Attempted","Independent","Hint-assisted","Solution needed",
    "Avg time (min)","Pattern recog (1-5)","Complexity (1-5)",
    "Coding accuracy (1-5)","Debugging (1-5)","Explanation (1-5)","Retention (1-5)",
    "Week score (/5)","Dominant failure","Biggest weakness","Next week focus",
    "F2 count","F3 count","F5 count","F10 count","Auto-escalation triggered?",
]
WA_W = [6,36,10,11,12,13,9,10,10,10,10,10,10,10,18,36,44,8,8,8,8,22]
write_header(ws_wa, WA_H, WA_W, freeze="C2")

WEEK_DATA = [
    (1,"Constraints + Counting + Hashing + Prefix"),
    (2,"Two Pointers + Sliding Window (variable + counting + fixed)"),
    (3,"Binary Search (index + rotated + on-answer)"),
    (4,"Sort + Intervals/Sweep + Monotonic Stack/Deque + Diagnostic 1"),
    (5,"Heaps + Streaming Statistics + Greedy (proof-based)"),
    (6,"Design (LRU/LFU) + Linked List Pointers + Bit Manipulation"),
    (7,"Tree Recursion (contract) + Tree DP + BST + Serialization"),
    (8,"Tries + Cross-Pattern Fusion + Communication + Diagnostic 2"),
    (9,"Graph Modelling + BFS/DFS + Union Find + Topological Sort"),
    (10,"BFS Shortest Path + State-Space BFS + Dijkstra + Dijkstra Variants"),
    (11,"Backtracking (dedup + pruning + bitmask) + Memoisation Bridge"),
    (12,"DP 1D + LIS + Knapsack + Two-Sequence + Space Optimization + Diagnostic 3"),
    (13,"Interval DP + Tree/DAG DP + Bitmask DP + DP Optimization + Counting DP"),
    (14,"Mid-Program Consolidation + Advanced Flows + Diagnostic 4"),
    (15,"Range Queries: Fenwick Trees (BIT) & Segment Trees (Point & Lazy)"),
    (16,"Advanced Graph Topologies: Bridges, SCC, Eulerian & Max-Flow"),
    (17,"Hardware Reality: Cache Locality, Robin Hood & Compressed Tries"),
    (18,"String Automata: KMP, Z-Algorithm, Aho-Corasick & BPE Tokenizers"),
    (19,"Cache Architectures: Adaptive Replacement Cache (ARC), 2Q & Clock"),
    (20,"Concurrency Primitives: Lock-Free SPSC, MPMC & Work-Stealing Deques"),
    (21,"Vector Search & Indexing: KD-Trees, IVF & HNSW Proximity Graphs"),
    (22,"ML Compilers: Heterogeneous DAG Scheduling & Tensor Strides"),
    (23,"Streaming & Probabilistic: Sketches, HyperLogLog & Quantization"),
    (24,"Capstone Grand Diagnostics, Memory Allocators & Systems Mastery"),
]

for i, (wk, theme) in enumerate(WEEK_DATA):
    r = i + 2
    put(ws_wa, r, 1, wk, align=CTR, bold=True)
    put(ws_wa, r, 2, theme)
    put(ws_wa, r, 3, f'=COUNTIFS(ProblemDB!$U$2:$U${PDB_ROWS},$A{r})', align=CTR)
    put(ws_wa, r, 4, f'=COUNTIFS(ProblemDB!$U$2:$U${PDB_ROWS},$A{r},ProblemDB!$G$2:$G${PDB_ROWS},"Yes")', align=CTR)
    put(ws_wa, r, 5, f'=COUNTIFS(ProblemDB!$U$2:$U${PDB_ROWS},$A{r},ProblemDB!$I$2:$I${PDB_ROWS},">0")', align=CTR)
    put(ws_wa, r, 6, f'=COUNTIFS(ProblemDB!$U$2:$U${PDB_ROWS},$A{r},ProblemDB!$J$2:$J${PDB_ROWS},"Yes")', align=CTR)
    put(ws_wa, r, 7, f'=IFERROR(ROUND(AVERAGEIFS(ProblemDB!$H$2:$H${PDB_ROWS},ProblemDB!$U$2:$U${PDB_ROWS},$A{r}),0),"")', align=CTR)
    for c in range(8, 14):
        put(ws_wa, r, c, None, align=CTR)
    put(ws_wa, r, 14, f'=IFERROR(ROUND(AVERAGE($H{r}:$M{r}),1),"")', align=CTR)
    put(ws_wa, r, 15, None)
    put(ws_wa, r, 16, None)
    put(ws_wa, r, 17, None)
    # F-category counts from FailureLog (Col D=Failure Type, Col B=Week)
    for j, fcat in enumerate(["F2-Pattern","F3-Derive","F5-Complexity","F10-Pressure"], start=18):
        ws_wa.cell(r, j).value = (
            f'=COUNTIFS(FailureLog!$D$2:$D${FL_ROWS},"{fcat}",'
            f'FailureLog!$B$2:$B${FL_ROWS},$A{r})')
        ws_wa.cell(r, j).border = BORDER
        ws_wa.cell(r, j).alignment = CTR
    # Auto-escalation: any F-category >= 3
    ws_wa.cell(r, 22).value = f'=IF(OR($R{r}>=3,$S{r}>=3,$T{r}>=3,$U{r}>=3),"YES - see README","No")'
    ws_wa.cell(r, 22).border = BORDER
    ws_wa.cell(r, 22).alignment = CTR
    ws_wa.row_dimensions[r].height = 30

for col in "HIJKLM":
    dv(ws_wa, SCORE_VALS, f"{col}2:{col}15", "Score 1-5")
dv(ws_wa, FCATS, "O2:O15", "Dominant failure")

ws_wa.conditional_formatting.add("H2:N15",
    ColorScaleRule(start_type="num", start_value=1, start_color=RED_D,
                   mid_type="num",   mid_value=3,   mid_color=AMBER_D,
                   end_type="num",   end_value=5,   end_color=GREEN_D))
ws_wa.conditional_formatting.add("V2:V15",
    CellIsRule("equal", ['"YES  -  see README"'], fill=fill(RED)))
ws_wa.conditional_formatting.add("R2:U25",
    CellIsRule("greaterThanOrEqual", ["3"], fill=fill(RED)))
print("[OK] WeeklyAssessment sheet built")

# --- SHEET: MockInterviews ----------------------------------------------------
ws_mi = wb.create_sheet("MockInterviews")
ws_mi.sheet_view.showGridLines = False

MI_H = [
    "Planned Day","Date","Type","Problem","Difficulty","Time Limit (min)",
    "Solved?","Time Taken (min)","Hints Used","Time to Pattern (min)",
    "Explanation (1-5)","TC/SC accuracy (1-5)","Follow-up (1-5)",
    "Final Score (/10)","Main Weakness","Concrete Fix for Next Mock",
    "Compared to previous mock",
]
MI_W = [11,12,16,40,10,12,9,12,10,14,12,12,12,12,36,46,40]
write_header(ws_mi, MI_H, MI_W, freeze="D2")

MOCKS = [
    (28,"Diagnostic 1","LC 918 Max Sum Circular Subarray (unlabelled)","M",30),
    (28,"Diagnostic 1","LC 795 Subarrays with Bounded Max (unlabelled)","M",30),
    (28,"Diagnostic 1","LC 581 Shortest Unsorted Continuous Subarray (unlabelled)","M",30),
    (42,"Mock #1 (2 hints)","1 medium problem  -  narrate every decision aloud","M",45),
    (56,"Diagnostic 2","LC 315 Count of Smaller After Self (unlabelled)","H",34),
    (56,"Diagnostic 2","LC 1110 Delete Nodes and Return Forest (unlabelled)","M",33),
    (56,"Diagnostic 2","LC 1396 Design Underground System (unlabelled)","M",33),
    (70,"Mock #2 (1 hint)","1 medium-hard + 1 infra follow-up question","H",45),
    (84,"Diagnostic 3","LC 1383 Maximum Performance of a Team (unlabelled)","H",37),
    (84,"Diagnostic 3","LC 1326 Min Taps to Water Garden (unlabelled)","H",37),
    (84,"Diagnostic 3","LC 2092 Find All People With Secret (unlabelled)","M",36),
    (92,"Mock #3 (no hints)","1 medium + 1 hard follow-up  -  verbal throughout","H",50),
    (95,"Mock #4 (unfamiliar)","1 unfamiliar hard from blind pool  -  no hints","H",45),
    (98,"Mid Diagnostic","LC 1751 Max Events Attended II (unlabelled)","H",37),
    (98,"Mid Diagnostic","LC 2421 Number of Good Paths (unlabelled)","H",37),
    (98,"Mid Diagnostic","LC 1463 Cherry Pickup II (unlabelled)","M",36),
    (112,"Diagnostic 4","LC 315 / LC 1192 / LC 715 Range & Graph Diagnostic","H",105),
    (126,"Diagnostic 5","LC 214 / LC 1044 / LC 1032 String & Automata Diagnostic","H",110),
    (140,"Diagnostic 6","SPSC Buffer / Consistent Hash / 2Q Cache Diagnostic","H",110),
    (154,"Diagnostic 7","LC 2050 / Blelloch Scan / SpMM Matrix Diagnostic","H",110),
    (164,"Capstone Mock 1","Tier-1 Distributed Storage & Cache Algorithm (verbal)","H",45),
    (165,"Capstone Mock 2","Tier-1 ML Infra / Scheduling Algorithm (verbal)","H",45),
    (166,"Capstone Mock 3","Tier-1 High-Dimensional Vector Search (verbal)","H",45),
    (168,"Grand Diagnostic","Final 3 Unlabelled Multi-Domain Hard Problems","H",120),
]

for i, (day, typ, prob, diff, lim) in enumerate(MOCKS):
    r = i + 2
    put(ws_mi, r, 1, day, align=CTR)
    put(ws_mi, r, 2, START + timedelta(days=day-1), fmt="dd-mmm-yy", align=CTR)
    put(ws_mi, r, 3, typ, align=CTR)
    put(ws_mi, r, 4, prob)
    put(ws_mi, r, 5, diff, align=CTR)
    put(ws_mi, r, 6, lim, align=CTR)
    for c in range(7, 14):
        put(ws_mi, r, c, None, align=CTR)
    put(ws_mi, r, 14,
        f'=IFERROR(ROUND(AVERAGE($K{r}:$M{r})*2,1),"N/A")', align=CTR)
    put(ws_mi, r, 15, None)
    put(ws_mi, r, 16, None)
    # Compared to previous mock
    if r > 2:
        put(ws_mi, r, 17,
            f'=IF(OR(NOT(ISNUMBER($N{r})),NOT(ISNUMBER($N{r-1}))),"",'
            f'IF($N{r}>$N{r-1},"Improved (+"&ROUND($N{r}-$N{r-1},1)&" pts)",'
            f'IF($N{r}<$N{r-1},"Regressed (-"&ROUND($N{r-1}-$N{r},1)&" pts)","Unchanged")))',
            align=CTR)
    else:
        put(ws_mi, r, 17, "baseline", align=CTR)
dv(ws_mi, YN_VALS,   "G2:G30", "Solved?")
dv(ws_mi, DIFF_VALS, "E2:E30", "Difficulty")
for col in "KLM":
    dv(ws_mi, SCORE_VALS, f"{col}2:{col}30", "Score 1-5")

ws_mi.conditional_formatting.add("N2:N30",
    ColorScaleRule(start_type="num", start_value=2,  start_color=RED_D,
                   mid_type="num",   mid_value=6,    mid_color=AMBER_D,
                   end_type="num",   end_value=10,   end_color=GREEN_D))
ws_mi.conditional_formatting.add("J2:J30",
    CellIsRule("greaterThan", ["12"], fill=fill(RED)))
ws_mi.conditional_formatting.add("J2:J30",
    CellIsRule("lessThanOrEqual", ["5"], fill=fill(GREEN)))
print("[OK] MockInterviews sheet built")

# --- SHEET: ResourcePlan ------------------------------------------------------
ws_rp = wb.create_sheet("ResourcePlan")
ws_rp.sheet_view.showGridLines = False

RP_H = [
    "Day","Resource","Topic","Where","Duration (min)",
    "Why needed (what mental model gap)","What to EXTRACT",
    "What NOT to memorize","Problems immediately after",
    "What to recall next day","Watched?","Watch-by Date",
    "Primary YouTube Video",
    "📺 Striver",
    "📺 Aditya Verma",
    "📺 Love Babbar",
    "📺 Padho with Pratyush",
    "📺 NeetCode",
    "📺 Other / Specialized",
]
RP_W = [6,22,32,28,10,44,42,36,34,36,10,12,24,18,18,18,22,18,24]
write_header(ws_rp, RP_H, RP_W, freeze="C2")

RESOURCES = [
    (1,"NeetCode / CPH ch.2","Big-O + n -> TC constraint mapping","neetcode.io + CPH ch.2",25,
     "Without this you cannot eliminate approaches before coding  -  most expensive mistake in interviews",
     "The n -> feasible-TC table; how to read constraints; O(n^2) death at n=10^5",
     "Formal limit definitions; big-O arithmetic proofs",
     "LC 1, LC 121","Recite the n -> TC table from memory"),

    (3,"NeetCode","Prefix sums and prefix+hashmap","neetcode.io (Subarray Sum Equals K)",20,
     "Prefix+hash is non-obvious and reused for 12+ weeks; gaps here compound badly",
     "Why a COUNT map beats a seen-set; why prefix[0]=0 must be seeded; loop invariant",
     "The exact code; how to handle overflow",
     "LC 560, LC 238","Explain the prefix invariant in one sentence"),

    (8,"NeetCode","Two pointers: why the movement is valid","neetcode.io (Two Sum II / 3Sum)",20,
     "Most learners memorize the motion but cannot explain why no valid pair is skipped",
     "The discard argument for each pointer move; the duplicate-skip rule and why it is safe",
     "The loop skeleton as a template",
     "LC 167, LC 15","State the discard argument without notes"),

    (10,"NeetCode","Sliding window: expand/shrink + when it FAILS","neetcode.io (Longest Substring)",25,
     "Knowing when the window is INVALID (non-monotone conditions) prevents silent wrong answers",
     "The monotone feasibility condition; the loop invariant; one example where window fails",
     "The while-loop skeleton",
     "LC 3, LC 209","Name a problem where sliding window fails and why"),

    (15,"NeetCode + CPH ch.3","Binary search boundaries: invariant-first","neetcode.io + CPH ch.3",25,
     "Off-by-one bugs here corrupt every future binary search problem silently",
     "Half-open invariant; lower_bound vs upper_bound; how to derive the correct loop condition",
     "Any memorized lo/hi template",
     "LC 704, LC 34","Write lower_bound cold with no template"),

    (17,"NeetCode","Binary search on answer (parametric search)","neetcode.io (Koko / Ship)",25,
     "Single highest-leverage pattern in this program; appears disguised in infra interviews",
     "The 3 validity conditions; how to write feasible(); why the answer space is monotone",
     "Specific predicates from the video",
     "LC 875, LC 1011","State the 3 validity conditions"),

    (23,"CPH ch.30 / cp-algorithms","Sweep line and event counting","CPH ch.30",20,
     "Interval problems collapse once you model them as a sweep; two equivalent implementations",
     "Event encoding (+1/-1); tie-breaking between end and start events at the same time",
     "Library implementations",
     "LC 253, LC 1094","Sweep vs heap equivalence proof"),

    (24,"NeetCode","Monotonic stack from first principles","neetcode.io (Daily Temperatures)",25,
     "The amortized argument is the reusable, transferable part  -  not the specific loop",
     "Why total pops <= n; what the stack invariant is at any moment; where the answer is resolved",
     "Problem-specific loop code",
     "LC 739, LC 503","Explain amortization in 60 seconds to a sceptical listener"),

    (29,"NeetCode + CPH ch.4","Heaps: sift-up/down, heapify, cost comparison","neetcode.io + CPH ch.4",25,
     "You must be able to compare heap vs sort cost on the spot; heapify being O(n) is non-obvious",
     "Partial-order insight; heapify O(n) proof sketch; when O(n log k) < O(n log n)",
     "Manual heap implementation details",
     "LC 215, LC 973","Compare heap vs sort cost for specific k/n values"),

    (32,"CPH ch.6","Proving greedy: exchange and staying-ahead arguments","CPH ch.6",20,
     "Unproven greedy is the top hard-interview failure; you need two reusable proof schemas",
     "Exchange argument schema; staying-ahead argument schema; how to construct counterexamples",
     "Specific greedy solutions from the chapter",
     "LC 45, LC 134","Give an exchange argument proof for LC 45"),

    (37,"NeetCode","LRU cache design: structure composition","neetcode.io (LRU Cache)",20,
     "Canonical structure-composition problem and an AI-infra interview staple",
     "Why hashmap+DLL yields O(1) on all ops; the deletion and move-to-front invariant",
     "Boilerplate node class code",
     "LC 146, LC 142","Rebuild LRU from a blank file in under 20 minutes"),

    (39,"CPH ch.10","Bit manipulation that actually recurs","CPH ch.10",20,
     "Needed for bitmask DP in week 13; also for constraint-tracking in backtracking",
     "Mask set/clear/test/iterate-all-subsets; XOR cancellation; popcount",
     "Exotic hacks that do not appear in interviews",
     "LC 137, LC 371","Write subset iteration with bitmasks"),

    (43,"NeetCode","Recursion as contract + call stack","neetcode.io (tree basics)",25,
     "Contract-first recursion eliminates most tree bugs before they happen",
     "How to state a return contract precisely in English; how the call stack relates to a tree traversal",
     "Individual tree solutions from the video",
     "LC 104, LC 110","State two recursion contracts from today's problems"),

    (50,"NeetCode","Trie construction and use","neetcode.io (Implement Trie)",20,
     "New data structure with a non-obvious memory/TC trade-off",
     "Node layout; insert/search; memory trade-off vs hashset; when trie loses",
     "Array-vs-map micro-implementation details",
     "LC 208, LC 139","State the trie vs hashset trade-off clearly"),

    (57,"NeetCode + CPH ch.11-12","Graph representations + BFS/DFS discipline","neetcode.io + CPH ch.11",25,
     "Modelling errors cause more graph failures than algorithm errors; visited discipline is critical",
     "Adjacency list vs matrix trade-offs; mark on PUSH not POP; the input that breaks pop-marking",
     "Grid-specific boilerplate code",
     "LC 200, LC 133","State when to mark visited and why; construct the breaking input"),

    (59,"WilliamFiset (YouTube)","Union-Find with path compression + union by size","WilliamFiset DSU video",25,
     "DSU appears heavily in infra-style problems; must be writeable cold in 5 minutes",
     "Both optimizations and why each is needed; amortized complexity argument",
     "The complexity proof details",
     "LC 547, LC 684","Write DSU cold from memory in under 5 minutes"),

    (61,"NeetCode + CPH ch.16","Topological sort: Kahn + DFS colours","neetcode.io + CPH ch.16",20,
     "DAG scheduling is the most infra-relevant graph pattern; must know two implementations",
     "In-degree invariant; cycle detection in BOTH variants; what happens to isolated nodes",
     "One fixed implementation as a template",
     "LC 207, LC 210","Explain cycle detection in both implementations"),

    (65,"cp-algorithms.com","State-space search: state encoding and counting","cp-algorithms (BFS)",20,
     "Keying visited on partial state is a silent bug that produces wrong answers  -  very hard to debug",
     "How to define a full state tuple; how to count the state space and derive TC from it",
     "Puzzle-specific state encodings",
     "LC 1293, LC 433","Define a state tuple for a new problem before coding"),

    (66,"WilliamFiset + CPH ch.13","Dijkstra: correctness proof","WilliamFiset Dijkstra + CPH ch.13",25,
     "You must know WHY the algorithm works, not just the code; negative edges are a common trap",
     "Relaxation; popped-distance invariant; why negative weights break the invariant",
     "Fibonacci-heap or D-ary heap variants",
     "LC 743, LC 1514","Prove the popped-node invariant; give the negative-weight counterexample"),

    (71,"NeetCode","Backtracking: template + complexity counting","neetcode.io (Subsets)",25,
     "Backtracking complexity counting is almost never taught; you need it for every hard interview",
     "Choose/explore/unchoose; counting recursion-tree leaves for TC; pruning effect on the tree",
     "Per-problem backtracking templates",
     "LC 78, LC 39","Count the leaves of a specific recursion tree"),

    (76,"NeetCode","From recursion to memoisation: state identification","neetcode.io (DP intro)",20,
     "State identification is the bridge into all DP; without it you cannot design new DP",
     "How to detect overlapping subproblems; how to name and count distinct states",
     "Memoisation decorator syntax",
     "LC 140, LC 494","Name the state for 3 problems from memory"),

    (78,"NeetCode + CPH ch.7","DP state design (5-step method)","neetcode.io + CPH ch.7",30,
     "Templates fail on unfamiliar DP; state-first design does not  -  this is the critical difference",
     "State  ->  transition  ->  base case  ->  evaluation order  ->  answer location (in that order)",
     "Classic DP code from videos",
     "LC 70, LC 198, LC 91","Recite the 5 steps without notes"),

    (80,"CPH ch.7 / cp-algorithms","Knapsack variants and loop order","CPH ch.7",25,
     "Loop order is the single most misunderstood DP detail; most candidates guess and get wrong",
     "Why 0/1 knapsack goes descending; why unbounded goes ascending; construct the failing example",
     "Table layout diagrams",
     "LC 416, LC 322","Explain loop order by constructing the failing counterexample"),

    (85,"cp-algorithms.com","Interval DP","cp-algorithms (interval DP)",20,
     "The 'last operation' insight is non-obvious and cannot be guessed; must be understood once deeply",
     "Iterate by length; why picking the LAST operation makes subproblems independent",
     "Matrix-chain-specific formulas",
     "LC 312, LC 516","Explain why last operation, not first operation"),

    (87,"cp-algorithms.com","Bitmask DP: state design","cp-algorithms (bitmask DP)",20,
     "Problems with n<=20 are unsolvable without this; the constraint is the only signal you get",
     "(mask, position) state design; transition over bits; exact state count formula",
     "Problem-specific masks",
     "LC 847, LC 473","Compute the state count for a new problem"),

    (99, "Errichto / CP-Algorithms", "Fenwick Tree (BIT): point update and range sum", "youtube.com/errichto + cp-algorithms", 25,
     "Mastering the binary index structure and lowest-set-bit trick",
     "The (i & -i) isolation proof; how 1-based indexing maps partial sums; 2D extension",
     "Specific problem solutions",
     "LC 307, LC 315", "Code BIT add() and query() in 60 seconds"),

    (100, "Errichto / CP-Algorithms", "Segment Tree: point update and range query", "youtube.com/errichto + cp-algorithms", 25,
     "Associative range queries require understanding the binary tree representation",
     "Array representation (2i, 2i+1); divide-and-conquer range intersection; 4n size bound",
     "Recursive boilerplates without understanding bounds",
     "LC 307, LC 732", "Draw tree array layout for n=6"),

    (101, "William Fiset", "Lazy Propagation in Segment Trees", "youtube.com/williamfiset", 25,
     "Deferred updates are critical for range additions and interval modifications",
     "The push_down invariant; clearing lazy tags before recursive child visits",
     "Code verbatim",
     "LC 218, LC 699", "State the push_down invariant in one sentence"),

    (106, "William Fiset", "Tarjan's Bridge & Cut Vertex Algorithm", "youtube.com/williamfiset", 25,
     "Single point of failure discovery in graphs without brute-force re-checking",
     "tin[u] vs low[u]; tree edges vs back edges; bridge condition low[v] > tin[u]",
     "Adjacency list boilerplate",
     "LC 1192, LC 1568", "State bridge condition vs articulation condition"),

    (109, "William Fiset", "Network Flow: Dinic's Algorithm & Min-Cut", "youtube.com/williamfiset", 25,
     "Capacity-constrained routing and bipartite matching equivalence",
     "Residual graph; augmenting paths; level graph via BFS; blocking flow via DFS",
     "Complex flow variants",
     "LC 1349, LC 1970", "Explain max-flow min-cut theorem"),

    (120, "Abdul Bari / NeetCode", "KMP Algorithm: Prefix Function & State Machine", "youtube.com + cp-algorithms", 25,
     "Linear string matching without backtracking is non-obvious and heavily tested",
     "Prefix function pi derivation; state transition fallback j = pi[j-1]; O(N) amortized argument",
     "Specific table values",
     "LC 28, LC 214", "Explain the amortized O(N) proof of KMP"),

    (127, "USENIX Fast '03", "Adaptive Replacement Cache (ARC) Paper & Mechanics", "Megiddo & Modha USENIX paper", 25,
     "Industrial standard for scan-resistant buffer caching in distributed systems",
     "Four lists (T1, T2, B1, B2); learning parameter p adaptation rule; ghost cache utility",
     "Proof formalisms",
     "ARC Simulation, LC 146", "Explain ARC adaptation when hit in B1 vs B2"),

    (134, "Martin Thompson", "Lock-Free SPSC Queue & Mechanical Sympathy", "mechanical-sympathy.blogspot.com", 25,
     "Understanding false sharing, memory barriers, and cache lines in concurrent queues",
     "64-byte cache line padding; monotonic sequence counters; acquire-release semantics",
     "Hardware-specific assembly",
     "LC 622, LC 641", "Explain false sharing and cache line bouncing"),

    (143, "Malkov & Yashunin", "HNSW Algorithm: Proximity Graph Navigation", "IEEE TPAMI Paper / Pinecone", 25,
     "Foundation of vector databases and embedding search in modern AI infrastructure",
     "Multi-layer skip-list graph; greedy coarse routing; beam search on layer 0; efSearch trade-off",
     "Distance metric implementations",
     "HNSW Simulation, LC 743", "Explain layer assignment probability in HNSW"),

    (148, "Stanford / MIT", "DAG Scheduling & Critical Path Method in ML Compilers", "MIT 6.172 / CS217", 25,
     "Core algorithm for operator scheduling, pipeline parallelism, and activation memory",
     "Earliest Start Time (EST), Latest Start Time (LST), slack = LST - EST; critical path DAG DP",
     "Specific hardware timing values",
     "LC 2050, LC 207", "Derive critical path duration on DAG"),
]

for i, row in enumerate(RESOURCES):
    r = i + 2
    (day, res, topic, where, dur, why, extract, notmem, after, recall) = row
    put(ws_rp, r, 1, day, align=CTR, bold=True)
    put(ws_rp, r, 2, res)
    put(ws_rp, r, 3, topic)
    put(ws_rp, r, 4, where)
    put(ws_rp, r, 5, dur, align=CTR)
    put(ws_rp, r, 6, why)
    put(ws_rp, r, 7, extract)
    put(ws_rp, r, 8, notmem)
    put(ws_rp, r, 9, after)
    put(ws_rp, r, 10, recall)
    put(ws_rp, r, 11, None, align=CTR)
    # Watch-by date = start + day - 1
    # Watch-by date dynamically linked to DayPlan
    ws_rp.cell(r, 12).value = f'=IF($A{r}="","",INDEX(DayPlan!$C$2:$C${DAYS+1},MATCH($A{r},DayPlan!$A$2:$A${DAYS+1},0)))'
    ws_rp.cell(r, 12).number_format = "dd-mmm"
    ws_rp.cell(r, 12).border = BORDER
    ws_rp.cell(r, 12).alignment = CTR
    ws_rp.row_dimensions[r].height = 44

    tut = get_tutorial_resource(day, topic)

    # Col 13: Primary
    put(ws_rp, r, 13, f'=HYPERLINK("{tut["primary_url"]}", "▶ Watch ({tut["primary"]}) ↗")', align=CTR)
    ws_rp.cell(r, 13).font = fnt(color=GREEN_D, underline="single", bold=True)

    def find_ch_url(ch_name):
        for ch in tut["channels"]:
            if ch["name"].lower() == ch_name.lower():
                return f"https://www.youtube.com/results?search_query={urllib.parse.quote(ch['query'])}"
        return None

    # Col 14: Striver
    striver_url = find_ch_url("Striver")
    if striver_url:
        put(ws_rp, r, 14, f'=HYPERLINK("{striver_url}", "📺 Striver ↗")', align=CTR)
        ws_rp.cell(r, 14).font = fnt(color=BLUE, underline="single")
    else:
        put(ws_rp, r, 14, "—", align=CTR)
        ws_rp.cell(r, 14).font = fnt(color="94A3B8")

    # Col 15: Aditya Verma
    aditya_url = find_ch_url("Aditya Verma")
    if aditya_url:
        put(ws_rp, r, 15, f'=HYPERLINK("{aditya_url}", "📺 Aditya Verma ↗")', align=CTR)
        ws_rp.cell(r, 15).font = fnt(color=BLUE, underline="single")
    else:
        put(ws_rp, r, 15, "—", align=CTR)
        ws_rp.cell(r, 15).font = fnt(color="94A3B8")

    # Col 16: Love Babbar
    babbar_url = find_ch_url("Love Babbar")
    if babbar_url:
        put(ws_rp, r, 16, f'=HYPERLINK("{babbar_url}", "📺 Love Babbar ↗")', align=CTR)
        ws_rp.cell(r, 16).font = fnt(color=BLUE, underline="single")
    else:
        put(ws_rp, r, 16, "—", align=CTR)
        ws_rp.cell(r, 16).font = fnt(color="94A3B8")

    # Col 17: Padho with Pratyush
    pratyush_url = find_ch_url("Padho with Pratyush")
    if pratyush_url:
        put(ws_rp, r, 17, f'=HYPERLINK("{pratyush_url}", "📺 Padho with Pratyush ↗")', align=CTR)
        ws_rp.cell(r, 17).font = fnt(color=BLUE, underline="single")
    else:
        put(ws_rp, r, 17, "—", align=CTR)
        ws_rp.cell(r, 17).font = fnt(color="94A3B8")

    # Col 18: NeetCode
    neetcode_url = find_ch_url("NeetCode")
    if neetcode_url:
        put(ws_rp, r, 18, f'=HYPERLINK("{neetcode_url}", "📺 NeetCode ↗")', align=CTR)
        ws_rp.cell(r, 18).font = fnt(color=BLUE, underline="single")
    else:
        put(ws_rp, r, 18, "—", align=CTR)
        ws_rp.cell(r, 18).font = fnt(color="94A3B8")

    # Col 19: Additional / Specialized
    spec_channels = [ch for ch in tut["channels"] if ch["name"].lower() not in ("striver", "aditya verma", "love babbar", "padho with pratyush", "neetcode")]
    if spec_channels:
        sp = spec_channels[0]
        sp_name = sp["name"]
        sp_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(sp['query'])}"
        put(ws_rp, r, 19, f'=HYPERLINK("{sp_url}", "📺 {sp_name} ↗")', align=CTR)
        ws_rp.cell(r, 19).font = fnt(color=PURPLE, underline="single")
    else:
        put(ws_rp, r, 19, "—", align=CTR)
        ws_rp.cell(r, 19).font = fnt(color="94A3B8")

dv(ws_rp, YN_VALS, f"K2:K{len(RESOURCES)+1}", "Watched?")
ws_rp.conditional_formatting.add(f"K2:K{len(RESOURCES)+1}",
    CellIsRule("equal", ['"Yes"'], fill=fill(GREEN)))
ws_rp.conditional_formatting.add(f"K2:K{len(RESOURCES)+1}",
    CellIsRule("equal", ['"No"'],  fill=fill(AMBER)))

ws_rp.auto_filter.ref = f"A1:S{len(RESOURCES)+1}"

# Rule banner
ws_rp["U1"] = (f"RULE: {len(RESOURCES)} tutorials in {DAYS} days = the cap. "
               "Every tutorial not on this list that you watch is procrastination. "
               "Log it as a productivity trap in FailureLog if you break this rule.")
ws_rp["U1"].font = fnt(bold=True, sz=10, color=RED_D)
print(f"[OK] ResourcePlan: {len(RESOURCES)} tutorials")

# --- SHEET: YouTubeChannels (Master YouTube Creator & Playlists Directory) ------
ws_ch = wb.create_sheet("YouTubeChannels")
ws_ch.sheet_view.showGridLines = False

YTC_H = [
    "Creator / Channel",
    "Platform Handle",
    "Pedagogy & Language",
    "Domain Specialization",
    "Strategist Recommendation (Why Watch)",
    "Flagship Master Series & Playlists",
    "Master Playlist Link (1-Click)",
    "Channel Link (1-Click)",
    "Curriculum Alignment (Weeks)"
]
YTC_W = [26, 20, 26, 38, 52, 44, 28, 24, 24]
write_header(ws_ch, YTC_H, YTC_W, freeze="B2", bg=NAVY)

YOUTUBE_CHANNELS_DATA = [
    (
        "Striver (take U forward)",
        "@takeUforward",
        "Systematic & Template-Driven (Hinglish / English)",
        "A2Z DSA Course, SDE Sheet, Trees, Graphs, DP, Disjoint Set, Binary Search on Answers",
        "Primary interview baseline. Watch complete playlists for new topics (Trees, Graphs, DP) to master edge cases and standard optimal templates.",
        "A2Z DSA Course, SDE Sheet, Graph Series (54 vids), DP Series (56 vids), Binary Trees",
        "https://www.youtube.com/playlist?list=PLgUwDviBIf0oF6QL8m22w1hIDC1vJ_BHz",
        "https://www.youtube.com/@takeUforward",
        "Weeks 1 - 18 (Core to Advanced DSA)"
    ),
    (
        "Aditya Verma",
        "@TheAdityaVerma",
        "Intuitive Mental Models (Hindi)",
        "Dynamic Programming (Knapsack, LCS, MCM), Sliding Window, Monotonic Stack, Heaps / Top-K",
        "The undisputed master for DP recurrence intuition and sliding window. Watch whenever stuck on state transitions or identification.",
        "DP Playlist (50+ vids), Sliding Window (16 vids), Stack & Monotonic Stack, Heap Playlist",
        "https://www.youtube.com/playlist?list=PL_z_8CaSLPWekqh3KpdC9045s07upF834",
        "https://www.youtube.com/@TheAdityaVerma",
        "Weeks 2, 3, 4, 5, 11 - 14 (DP & Window)"
    ),
    (
        "Padho with Pratyush",
        "@padhowithpratyush",
        "Systems-Level & Low-Level Depth (Hinglish)",
        "Systems DSA: LRU/ARC Buffer Pools, Lock-Free Ring Buffers, HNSW Vector Indexing, DAG Compiler Scheduling, Interval DP",
        "Crucial for AI Infra & Systems tracks. Bridges competitive DSA with kernel/storage engineering, cache hierarchies, and vector search internals.",
        "Advanced DSA Series, Dynamic Programming & Recursion, Systems Concurrency & Cache Internals",
        "https://www.youtube.com/@padhowithpratyush",
        "https://www.youtube.com/@padhowithpratyush",
        "Weeks 6, 15 - 18, 19 - 24 (Systems & AI Infra)"
    ),
    (
        "Love Babbar (CodeHelp)",
        "@CodeHelp",
        "Visual & Energetic C++ (Hindi)",
        "Complete C++ DSA Course, Recursion & Backtracking, Linked Lists, Trees, Graph Traversals",
        "Exceptional C++ memory layout diagrams and clean implementations. Ideal for building rock-solid C++ pointer, tree, and recursion fundamentals.",
        "Complete C++ DSA Course (140+ videos), Recursion Series, Graph Theory Series",
        "https://www.youtube.com/playlist?list=PLDzeHZWIZsTryvtXdMr6rPh4IDexB5NIA",
        "https://www.youtube.com/@CodeHelp",
        "Weeks 1 - 12 (C++ Foundation & Classic DSA)"
    ),
    (
        "NeetCode",
        "@NeetCode",
        "Concise Visual Walkthroughs (English)",
        "NeetCode 150, Blind 75, LeetCode Problem Walkthroughs, System Design, Algorithm Visualizations",
        "The gold standard for rapid daily problem review (5-15 min). Watch after 20 min of struggling to verify optimal time/space complexity invariants.",
        "NeetCode 150 Walkthroughs, Blind 75, DP Playlist, Advanced Graphs",
        "https://www.youtube.com/playlist?list=PLot-Xpze53ldVwtstag2TL4HQhAnC8ATf",
        "https://www.youtube.com/@NeetCode",
        "Weeks 1 - 24 (Daily Verification & Diagnostics)"
    ),
    (
        "Abdul Bari",
        "@abdul_bari",
        "Academic Chalkboard Rigor (English)",
        "Analysis of Algorithms, Dynamic Programming proofs, Divide & Conquer, Greedy, Shortest Paths (Dijkstra, Bellman-Ford)",
        "Essential for mathematical rigor and recurrence relations. If an interviewer asks to prove optimality or asymptotic bounds, Bari gives the proof.",
        "Algorithms (Design & Analysis) Complete Course, Dynamic Programming Series, Graph Algorithms",
        "https://www.youtube.com/playlist?list=PLDN4rrl48XKpZkf03iYFl-O29szjTrs_O",
        "https://www.youtube.com/@abdul_bari",
        "Weeks 1, 5, 10 - 12 (Algorithm Proofs & DP)"
    ),
    (
        "WilliamFiset",
        "@WilliamFiset-videos",
        "Animated Visual Slide Decks (English)",
        "Graph Theory, Segment Trees, Fenwick Trees, Tarjan's SCC & Bridges, Dinic's Max Flow, Eulerian Paths",
        "The best visualizer for advanced graph and tree algorithms. Invaluable for internalizing residual graphs, flow networks, and range trees.",
        "Graph Theory Series (Complete), Data Structures Series, Network Flow / Dinic's Algorithm",
        "https://www.youtube.com/playlist?list=PLDV1Zeh2NRsDGO4--qE8yH72HFL1Km93P",
        "https://www.youtube.com/@WilliamFiset-videos",
        "Weeks 9, 10, 15 - 18 (Range Trees & Flow)"
    ),
    (
        "Errichto (Kamil Debowski)",
        "@Errichto",
        "Competitive Programming Master (English)",
        "Bitwise Operations, Bitmask DP, Segment Trees with Lazy Propagation, Two Pointers vs DP, Fast Modulo Math",
        "World-class competitive programming speed techniques. Watch during Week 7 (Bitwise) and Week 13 (Bitmask DP) for hardware-level bit tricks.",
        "Competitive Programming Tutorials, Dynamic Programming Series, Bitwise Operations Playlist",
        "https://www.youtube.com/playlist?list=PLl0KD3g-oDOHpWRyyGBUJ9jmul0lUODS5",
        "https://www.youtube.com/@Errichto",
        "Weeks 7, 13, 15 (Bitmask DP & Range Trees)"
    ),
    (
        "Martin Thompson / CppCon",
        "@CppCon",
        "Silicon & Hardware Sympathy (English)",
        "Lock-Free SPSC Ring Buffers, Cache Locality, False Sharing, Atomic Memory Fences, Low-Latency C++",
        "Mandatory for NVIDIA, Tenstorrent, Cerebras, and AI Infra interviews. Explains lock-free queues, cache alignment, and GPU work dispatching.",
        "CppCon Back to Basics: Concurrency, Mechanical Sympathy, Cache-Conscious Data Structures",
        "https://www.youtube.com/@CppCon",
        "https://www.youtube.com/@CppCon",
        "Weeks 19 - 24 (Silicon Concurrency & AI Infra)"
    ),
    (
        "CMU Database Group (Prof. Andy Pavlo)",
        "@CMUDatabaseGroup",
        "Systems Architecture & Storage (English)",
        "Buffer Pool Replacement (LRU, ARC, Clock), B+ Trees, Concurrent Hash Tables, Vectorized Query Execution",
        "Provides the production architecture behind paging and caching. Directly maps to LLM KV-cache paging (vLLM) and GPU memory hierarchies.",
        "CMU 15-445/645 Database Systems, Storage Engine Internals, Buffer Pool Policies",
        "https://www.youtube.com/@CMUDatabaseGroup",
        "https://www.youtube.com/@CMUDatabaseGroup",
        "Weeks 6, 19 - 24 (Paging & Buffer Systems)"
    )
]

for idx, item in enumerate(YOUTUBE_CHANNELS_DATA, start=2):
    c_name, c_handle, c_ped, c_spec, c_rec, c_flag, c_plist, c_churl, c_align = item
    bg = "F8FAFC" if idx % 2 == 0 else WHITE
    put(ws_ch, idx, 1, c_name, bold=True, bg=bg, sz=10)
    put(ws_ch, idx, 2, c_handle, color="64748B", bg=bg, sz=9)
    put(ws_ch, idx, 3, c_ped, bg=bg, sz=9)
    put(ws_ch, idx, 4, c_spec, bg=bg, sz=9)
    put(ws_ch, idx, 5, c_rec, bg=bg, sz=9)
    put(ws_ch, idx, 6, c_flag, bg=bg, sz=9)
    put(ws_ch, idx, 7, f'=HYPERLINK("{c_plist}", "▶ Master Playlist ↗")', align=CTR, bg=bg)
    ws_ch.cell(idx, 7).font = fnt(color=GREEN_D, underline="single", bold=True, sz=9)
    put(ws_ch, idx, 8, f'=HYPERLINK("{c_churl}", "📺 Visit Channel ↗")', align=CTR, bg=bg)
    ws_ch.cell(idx, 8).font = fnt(color=BLUE, underline="single", sz=9)
    put(ws_ch, idx, 9, c_align, align=CTR, bg=bg, color="475569", sz=9)
    ws_ch.row_dimensions[idx].height = 36

ws_ch.auto_filter.ref = f"A1:I{len(YOUTUBE_CHANNELS_DATA)+1}"
print(f"[OK] YouTubeChannels: {len(YOUTUBE_CHANNELS_DATA)} creator guides built")

# --- SHEET: ProgressionCurve --------------------------------------------------
ws_prog = wb.create_sheet("ProgressionCurve")
ws_prog.sheet_view.showGridLines = False
ws_prog.column_dimensions["A"].width = 6
ws_prog.column_dimensions["B"].width = 14
ws_prog.column_dimensions["C"].width = 32
ws_prog.column_dimensions["D"].width = 22
ws_prog.column_dimensions["E"].width = 18
ws_prog.column_dimensions["F"].width = 18
ws_prog.column_dimensions["G"].width = 20
ws_prog.column_dimensions["H"].width = 20
ws_prog.column_dimensions["I"].width = 20

write_header(ws_prog,
    ["Day","Date","Milestone","Target: Time-to-Pattern (med)","Actual","Target: Indep-Solve %","Actual %","Target: Hint-Dep %","Actual %"],
    [6,14,32,22,10,20,10,18,10],
    freeze="C2")

MILESTONES = [
    (7,   "End of Week 1  -  counting/hashing/prefix", 12, 50, 40),
    (14,  "End of Week 2  -  two pointers/window",      11, 55, 38),
    (21,  "End of Week 3  -  binary search",            10, 58, 35),
    (28,  "Month 1 Diagnostic",                         9, 60, 32),
    (35,  "End of Week 5  -  heaps/greedy",              9, 62, 30),
    (42,  "Mock #1 / End of Week 6",                    8, 65, 28),
    (49,  "End of Week 7  -  trees",                     8, 67, 26),
    (56,  "Month 2 Diagnostic",                          7, 70, 25),
    (63,  "End of Week 9  -  graphs/DSU",                7, 72, 23),
    (70,  "Mock #2 / End of Week 10",                   6, 75, 22),
    (77,  "End of Week 11  -  backtracking",             6, 77, 20),
    (84,  "Month 3 Diagnostic",                          5, 80, 18),
    (91,  "End of Week 13  -  advanced DP",              5, 82, 16),
    (98,  "Mid-Program Grand Diagnostic",                5, 84, 15),
    (105, "End of Week 15 -  range query trees",        5, 85, 14),
    (112, "Diagnostic 4: Advanced Graph Topologies",    4, 86, 13),
    (119, "End of Week 17 -  hardware-aware DS",        4, 87, 12),
    (126, "Diagnostic 5: Strings & Automata",           4, 88, 12),
    (133, "End of Week 19 -  advanced caching",         4, 89, 11),
    (140, "Diagnostic 6: Concurrency & Queues",         4, 90, 10),
    (147, "End of Week 21 -  vector search HNSW",       3, 91, 10),
    (154, "Diagnostic 7: ML Compilers & DAGs",          3, 92,  9),
    (161, "End of Week 23 -  streaming & sketches",     3, 93,  8),
    (168, "Final Specialist Certification",             3, 95,  8),
]

for i, (day, milestone, t_ttp, t_indep, t_hint) in enumerate(MILESTONES):
    r = i + 2
    put(ws_prog, r, 1, day, align=CTR, bold=True)
    put(ws_prog, r, 2, START + timedelta(days=day-1), fmt="dd-mmm-yy", align=CTR)
    put(ws_prog, r, 3, milestone, bold=(day in (28,56,84,98,112,126,140,154,168)))
    put(ws_prog, r, 4, f"< {t_ttp} min", align=CTR)
    put(ws_prog, r, 5, None, align=CTR)  # user fills
    put(ws_prog, r, 6, f"> {t_indep}%",  align=CTR)
    put(ws_prog, r, 7, None, align=CTR)  # user fills
    put(ws_prog, r, 8, f"< {t_hint}%",   align=CTR)
    put(ws_prog, r, 9, None, align=CTR)  # user fills
    ws_prog.row_dimensions[r].height = 24
    if day in (28, 56, 84, 98, 112, 126, 140, 154, 168):
        for c in range(1, 10):
            ws_prog.cell(r, c).fill = fill("FFF9C4")

ws_prog.conditional_formatting.add("E2:E25",
    ColorScaleRule(start_type="num", start_value=12, start_color=RED_D,
                   mid_type="num",   mid_value=7,    mid_color=AMBER_D,
                   end_type="num",   end_value=3,    end_color=GREEN_D))
ws_prog.conditional_formatting.add("G2:G25",
    ColorScaleRule(start_type="num", start_value=40, start_color=RED_D,
                   mid_type="num",   mid_value=65,   mid_color=AMBER_D,
                   end_type="num",   end_value=90,   end_color=GREEN_D))

note = ws_prog.cell(1, 11)
note.value = ("Fill columns E, G, I after each diagnostic/mock. "
              "Target cells are highlighted yellow for diagnostic days. "
              "If Actual > Target for time-to-pattern in two consecutive rows, "
              "recognition training must increase immediately (see auto-escalation in README).")
note.font = fnt(italic=True, sz=9, color="475569")
print("[OK] ProgressionCurve sheet built")

# --- SHEET: BlindProblemPool --------------------------------------------------
ws_bpp = wb.create_sheet("BlindProblemPool")
ws_bpp.sheet_view.showGridLines = False

BPP_H = ["Problem","LeetCode #","Difficulty","Pattern (hidden  -  fill after attempt)",
         "Recommended for Day","Used on Day","Solved?","Time Taken","Hints Used",
         "Time to Pattern","TC Correct?","Notes"]
BPP_W = [40,10,10,28,16,10,9,10,10,12,10,34]
write_header(ws_bpp, BPP_H, BPP_W, freeze="D2")

BLIND_POOL = [
    ("Maximum Sum Circular Subarray","918","M","Prefix + Kadane variant",28),
    ("Number of Subarrays with Bounded Maximum","795","M","Prefix/counting",28),
    ("Shortest Unsorted Continuous Subarray","581","M","Sort + two pointers",28),
    ("Count of Smaller Numbers After Self","315","H","Merge sort / BIT / BST",56),
    ("Delete Nodes and Return Forest","1110","M","Tree DFS (post-order)",56),
    ("Design Underground System","1396","M","Design / hashing",56),
    ("Maximum Performance of a Team","1383","H","Heap + sorting",84),
    ("Minimum Number of Taps to Open","1326","H","Greedy / interval DP",84),
    ("Find All People With Secret","2092","H","BFS / Union Find",84),
    ("Max Number of Events That Can Be Attended II","1751","H","DP + binary search",98),
    ("Number of Good Paths","2421","H","DSU + sorting",98),
    ("Cherry Pickup II","1463","H","3D DP",98),
    ("Maximum Profit in Job Scheduling","1235","H","DP + binary search","90-97"),
    ("Shortest Subarray with Sum at Least K","862","H","Monotonic deque","90-97"),
    ("Checking Existence of Edge Length Limited Paths","1697","H","Offline DSU","90-97"),
    ("Maximum AND Sum of Array","2172","H","Bitmask DP","90-97"),
    ("Trapping Rain Water II","407","H","BFS / min-heap","90-97"),
    ("Minimum Cost to Reach Destination in Time","1928","H","DP on graph","90-97"),
    ("Maximum Number of Non-Overlapping Palindrome Substrings","2472","H","Greedy + DP","90-97"),
    ("Count Ways to Build Rooms in an Ant Colony","2050","H","Tree DP + combinatorics","90-97"),
]

for i, row in enumerate(BLIND_POOL):
    r = i + 2
    prob, num, diff, hidden_pat, day_rec = row
    put(ws_bpp, r, 1, prob)
    put(ws_bpp, r, 2, num, align=CTR)
    put(ws_bpp, r, 3, diff, align=CTR)
    put(ws_bpp, r, 4, None, bg=AMBER)   # user fills after attempt  -  hidden now
    put(ws_bpp, r, 5, str(day_rec), align=CTR)
    for c in range(6, 13):
        put(ws_bpp, r, c, None, align=CTR)
    ws_bpp.row_dimensions[r].height = 22
    if diff == "H":
        ws_bpp.cell(r, 3).fill = fill(RED)
    elif diff == "M":
        ws_bpp.cell(r, 3).fill = fill(AMBER)

dv(ws_bpp, DIFF_VALS, f"C2:C{len(BLIND_POOL)+1}", "Difficulty")
dv(ws_bpp, YN_VALS,   f"G2:G{len(BLIND_POOL)+1}", "Solved?")
dv(ws_bpp, YN_VALS,   f"K2:K{len(BLIND_POOL)+1}", "TC correct?")

ws_bpp["M1"] = ("RULE: Do NOT look at column D until AFTER you have attempted the problem. "
                "Column D is intentionally blank to prevent anchoring. "
                "Fill it with your pattern guess BEFORE checking the answer.")
ws_bpp["M1"].font = fnt(bold=True, sz=10, color=RED_D)
print(f"[OK] BlindProblemPool: {len(BLIND_POOL)} problems")

# --- SHEET: Dashboard (built last, moved first) -------------------------------
ws_dash = wb.create_sheet("Dashboard")
wb.move_sheet("Dashboard", offset=-(len(wb.sheetnames) - 1))
ws_dash.sheet_view.showGridLines = False
for col, w in zip("ABCDEFG", [34, 48, 4, 28, 10, 4, 70]):
    ws_dash.column_dimensions[col].width = w

# Title
ws_dash.merge_cells("A1:G1")
for col in "ABCDEFG":
    ws_dash[f"{col}1"].fill = fill(NAVY)
t = ws_dash["A1"]
t.value = "DSA TRAINING DASHBOARD - NVIDIA & AI-INFRASTRUCTURE SYSTEMS"
t.font  = fnt(bold=True, sz=14, color=WHITE)
t.alignment = Alignment(horizontal="center", vertical="center")
ws_dash.row_dimensions[1].height = 38

ws_dash.merge_cells("A2:G2")
for col in "ABCDEFG":
    ws_dash[f"{col}2"].fill = fill(LIGHT)
s = ws_dash["A2"]
s.value = (f"Started: {START.strftime('%d %b %Y')}   |   "
           f"Ends: {(START+timedelta(days=DAYS-1)).strftime('%d %b %Y')}   |   "
           "Target: NVIDIA, Hyperscalers & AI-Infra Systems | Fill ProblemDB & DayPlan honestly")
s.font  = fnt(italic=True, sz=9, color="475569")
s.alignment = Alignment(horizontal="center", vertical="center")
ws_dash.row_dimensions[2].height = 24

DPL  = "DayPlan"
PDB  = "ProblemDB"
FLG  = "FailureLog"
MIS  = "MockInterviews"
PLB  = "PatternLibrary"
PC   = "PatternCards"

METRICS = [
    # (label, formula, number_format, section)
    ("TODAY'S WORKFLOW","","","header"),
    ("Current day",
     f'=MIN({DAYS},COUNTIF({DPL}!$W$2:$W${DAYS+1},"Yes")+1)',
     "0","today"),
    ("Current week",
     '=ROUNDUP($B4/7,0)',
     "0","today"),
    ("TODAY: objective",
     f'=IFERROR(INDEX({DPL}!$D$2:$D${DAYS+1},$B4),"")',
     None,"today"),
    ("TODAY: pattern",
     f'=IFERROR(INDEX({DPL}!$E$2:$E${DAYS+1},$B4),"")',
     None,"today"),
    ("TODAY: mode / help",
     f'=IFERROR(INDEX({DPL}!$J$2:$J${DAYS+1},$B4)&"  |  "&INDEX({DPL}!$K$2:$K${DAYS+1},$B4),"")',
     None,"today"),
    ("TODAY: problems",
     f'=IFERROR(INDEX({DPL}!$L$2:$L${DAYS+1},$B4)&"    |    "&INDEX({DPL}!$O$2:$O${DAYS+1},$B4),"")',
     None,"today"),
    ("TODAY: tutorial?",
     f'=IFERROR(IF(INDEX({DPL}!$G$2:$G${DAYS+1},$B4)="YES",INDEX({DPL}!$H$2:$H${DAYS+1},$B4)&" ("&INDEX({DPL}!$I$2:$I${DAYS+1},$B4)&" min)","NO tutorial  -  struggle first"),"")',
     None,"today"),
    ("Days completed",
     f'=COUNTIF({DPL}!$W$2:$W${DAYS+1},"Yes")',
     "0","today"),
    ("Program progress",
     f'=IFERROR($B11/{DAYS},0)',  # completed / 168 days
     "0%","today"),

    ("SOLVE QUALITY METRICS","","","header"),
    ("Problems attempted",
     f'=COUNTA({PDB}!$A$2:$A${PDB_ROWS})',
     "0","quality"),
    ("Solved independently",
     f'=COUNTIF({PDB}!$G$2:$G${PDB_ROWS},"Yes")',
     "0","quality"),
    ("Solved with hints",
     f'=COUNTIFS({PDB}!$I$2:$I${PDB_ROWS},">0",{PDB}!$J$2:$J${PDB_ROWS},"<>Yes")',
     "0","quality"),
    ("Needed the solution",
     f'=COUNTIF({PDB}!$J$2:$J${PDB_ROWS},"Yes")',
     "0","quality"),
    ("Independent-solve rate",
     f'=IFERROR($B15/$B14,0)',
     "0%","quality"),
    ("Hint-dependency rate",
     f'=IFERROR(($B16+$B17)/$B14,0)',
     "0%","quality"),
    ("Problems mastered",
     f'=COUNTIF({PDB}!$S$2:$S${PDB_ROWS},"Yes")',
     "0","quality"),
    ("Avg solve time (min)",
     f'=IFERROR(ROUND(AVERAGE({PDB}!$H$2:$H${PDB_ROWS}),0),0)',
     "0","quality"),
    ("2nd solutions found",
     f'=COUNTIF({PDB}!$X$2:$X${PDB_ROWS},"Yes")',
     "0","quality"),

    ("INTERVIEW READINESS","","","header"),
    ("Mock/diagnostic avg (/10)",
     f'=IFERROR(ROUND(AVERAGE({MIS}!$N$2:$N$30),1),0)',
     "0.0","interview"),
    ("Avg time-to-pattern (min)",
     f'=IFERROR(ROUND(AVERAGE({MIS}!$J$2:$J$30),1),0)',
     "0.0","interview"),
    ("Avg pattern mastery (/5)",
     f'=IFERROR(ROUND(AVERAGE({PLB}!$J$2:$J${len(PATTERNS)+1}),2),0)',
     "0.00","interview"),
    ("Reviews due today",
     f'=COUNTIFS({PDB}!$P$2:$P${PDB_ROWS},"<="&TODAY(),{PDB}!$S$2:$S${PDB_ROWS},"<>Yes")',
     "0","interview"),
    ("INTERVIEW READINESS SCORE",
     ('=IF($B14<5,0,ROUND('
      '30*MIN(1,MAX(0,IFERROR($B18/0.80,0)))+'   # independent-solve rate target 80%
      '25*MIN(1,MAX(0,IFERROR((1-$B19)/0.80,0)))+' # hint-dep target <20%
      '25*MIN(1,MAX(0,IFERROR($B24/10,0)))+'      # mock avg target 10
      '20*IF($B25=0,0,MIN(1,MAX(0,IFERROR((12-$B25)/8,0))))'  # time-to-pattern target 4 min (0 if no mocks yet)
      ',0))'),
     "0","interview"),

    ("PATTERN MASTERY & HEALTH","","","header"),
    ("Strongest pattern (self-rated)",
     f'=IFERROR(INDEX({PLB}!$A$2:$A${len(PATTERNS)+1},MATCH(MAX({PLB}!$J$2:$J${len(PATTERNS)+1}),{PLB}!$J$2:$J${len(PATTERNS)+1},0)),"Rate patterns first")',
     None,"patterns"),
    ("Weakest pattern (self-rated)",
     f'=IFERROR(INDEX({PLB}!$A$2:$A${len(PATTERNS)+1},MATCH(MINIFS({PLB}!$J$2:$J${len(PATTERNS)+1},{PLB}!$J$2:$J${len(PATTERNS)+1},">0"),{PLB}!$J$2:$J${len(PATTERNS)+1},0)),"Rate patterns first")',
     None,"patterns"),
    ("Most failure-prone category",
     '=IF(MAX($E$4:$E$15)=0,"No failures logged yet",INDEX($D$4:$D$15,MATCH(MAX($E$4:$E$15),$E$4:$E$15,0))&" ("&MAX($E$4:$E$15)&" failures)")',
     None,"patterns"),
    ("Current level",
     ('=IF($B14<10,"Unmeasured - solve 10+ logged problems first",'
      'IF($B28<35,"Beginner: knows topics but pattern-blind",'
      'IF($B28<55,"Intermediate: recognises common patterns",'
      'IF($B28<75,"Strong: derives most solutions independently",'
      '"Expert-level: can derive unfamiliar problems under pressure"))))'),
     None,"patterns"),

    ("SYSTEM OPERATING GUIDE","","","header"),
]

r = 3
section_fills = {
    "header":   NAVY,
    "today":    "EFF6FF",
    "quality":  "F0FDF4",
    "interview":"FFF9C4",
    "patterns": "FDF4FF",
}
for label, formula, fmt, section in METRICS:
    if section == "header":
        ws_dash.merge_cells(f"A{r}:B{r}")
        for col_l in ("A", "B"):
            ws_dash[f"{col_l}{r}"].fill = fill(BLUE)
            ws_dash[f"{col_l}{r}"].border = BORDER_H
        hc = ws_dash[f"A{r}"]
        hc.value     = f"  {label}"
        hc.font      = fnt(bold=True, sz=10, color=WHITE)
        hc.alignment = Alignment(vertical="center", horizontal="left")
        ws_dash.row_dimensions[r].height = 26
        r += 1
        continue

    bg = section_fills.get(section, WHITE)
    a = ws_dash.cell(row=r, column=1, value=label)
    a.font = fnt(bold=(label == "INTERVIEW READINESS SCORE"), sz=10,
                 color=WHITE if label == "INTERVIEW READINESS SCORE" else NAVY)
    a.fill = fill(NAVY if label == "INTERVIEW READINESS SCORE" else bg)
    a.border = BORDER
    a.alignment = WRAP

    b = ws_dash.cell(row=r, column=2, value=formula)
    b.border = BORDER
    b.alignment = Alignment(wrap_text=True, vertical="center", horizontal="left")
    b.fill = fill(NAVY if label == "INTERVIEW READINESS SCORE" else bg)
    if label == "INTERVIEW READINESS SCORE":
        b.font = fnt(bold=True, sz=18, color=WHITE)
    else:
        b.font = fnt(bold=False, sz=10, color=NAVY)
    if fmt: b.number_format = fmt
    ws_dash.row_dimensions[r].height = 24 if section != "today" else 30
    r += 1

# Interview readiness color scale
ws_dash.conditional_formatting.add(f"B{r-5}:B{r-5}",
    ColorScaleRule(start_type="num", start_value=20,  start_color=RED_D,
                   mid_type="num",   mid_value=60,    mid_color=AMBER_D,
                   end_type="num",   end_value=100,   end_color=GREEN_D))

# Failure category block (feeds "most failure-prone category")
ws_dash.row_dimensions[3].height = 26
hh = ws_dash.cell(row=3, column=4, value="Failure Category")
hh.font = fnt(bold=True, sz=10, color=WHITE)
hh.fill = fill(BLUE)
hh.border = BORDER_H
hh.alignment = Alignment(vertical="center", horizontal="left")

hh2 = ws_dash.cell(row=3, column=5, value="Count")
hh2.font = fnt(bold=True, sz=10, color=WHITE)
hh2.fill = fill(BLUE)
hh2.border = BORDER_H
hh2.alignment = CTR
for j, cat in enumerate(FCATS):
    rr = 4 + j
    c1 = ws_dash.cell(rr, 4, value=cat); c1.border=BORDER; c1.alignment=WRAP; c1.font=fnt(sz=9)
    c2 = ws_dash.cell(rr, 5,
        value=f'=COUNTIF({FLG}!$D$2:$D${FL_ROWS},D{rr})+COUNTIF({PDB}!$M$2:$M${PDB_ROWS},D{rr})')
    c2.border=BORDER; c2.alignment=CTR; c2.font=fnt(sz=9)
ws_dash.conditional_formatting.add("E4:E15",
    ColorScaleRule(start_type="min", start_color=GREEN_D,
                   end_type="max",   end_color=RED_D))

# Link to Master YouTube Directory in Dashboard
ws_dash.merge_cells("D17:E17")
c17 = ws_dash["D17"]
c17.value = "MASTER YOUTUBE DIRECTORY"
c17.font = fnt(bold=True, sz=10, color=WHITE)
c17.fill = fill(NAVY)
c17.alignment = Alignment(vertical="center", horizontal="left")
c17.border = BORDER_H
ws_dash.row_dimensions[17].height = 24

ws_dash.merge_cells("D18:E18")
c18 = ws_dash["D18"]
c18.value = '=HYPERLINK("#\'YouTubeChannels\'!A1", "📺 Open Master YouTube Directory (10 Creators) ↗")'
c18.font = fnt(bold=True, sz=9, color=GREEN_D, underline="single")
c18.fill = fill(LIGHT)
c18.alignment = CTR
c18.border = BORDER
ws_dash.row_dimensions[18].height = 24

ws_dash.merge_cells("D19:E19")
c19 = ws_dash["D19"]
c19.value = "Striver • Aditya Verma • Pratyush • Babbar • NeetCode"
c19.font = fnt(sz=8, color="64748B", italic=True)
c19.fill = fill(WHITE)
c19.alignment = CTR
c19.border = BORDER
ws_dash.row_dimensions[19].height = 20

# Quick-start guide column G
GUIDE_LINES = [
    ("QUICK-START DAILY PROTOCOL", True),
    ("1. Open DayPlan  ->  go to 'Current day' row. Do exactly that row.", False),
    ("2. Write target TC from constraints BEFORE touching the keyboard.", False),
    ("3. Obey the Stuck Protocol (see README): 0 -> 10 -> 20 -> 30 min checkpoints.", False),
    ("4. Log every problem in ProblemDB the same day. Review dates auto-compute.", False),
    ("5. Log every failure in FailureLog with a category + one preventive rule.", False),
    ("6. Sunday: fill WeeklyAssessment. Let the data steer the next week.", False),
    ("7. Diagnostics on Days 28/56/84/98. Unlabelled. Timed. No hints. Real measurements.", False),
    ("8. Master YouTube Directory: Check 'YouTubeChannels' sheet for flagship playlists.", False),
    ("", False),
    ("SIGNS THE PLAN IS WORKING", True),
    ("[OK] Time-to-pattern dropping at each diagnostic", False),
    ("[OK] Hint-dependency rate below 25% by week 8", False),
    ("[OK] Can reconstruct any pattern without notes 3 days later", False),
    ("[OK] Mock scores increasing", False),
    ("", False),
    ("SIGNS YOU NEED TO ADJUST", True),
    ("[NO] Same failure category 3+ weeks in a row", False),
    ("[NO] Hint-dependency above 40% for 2+ weeks", False),
    ("[NO] Time-to-pattern not dropping between diagnostics", False),
    ("[NO] Can solve only when problem is labelled with the pattern", False),
    ("[NO] Cannot reconstruct a solution 2 days after solving it", False),
]

gr = 3
for text, bold in GUIDE_LINES:
    c = ws_dash.cell(row=gr, column=7, value=text)
    c.border = BORDER
    if bold:
        c.fill = fill(LIGHT)
        c.font = fnt(bold=True, sz=10, color=NAVY)
        c.alignment = Alignment(vertical="center", horizontal="left")
        ws_dash.row_dimensions[gr].height = 26
    else:
        c.font = fnt(bold=False, sz=9, color="334155")
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="left")
        ws_dash.row_dimensions[gr].height = 22
    gr += 1

print("[OK] Dashboard sheet built")

# --- MOVE README AFTER DASHBOARD ----------------------------------------------
# Dashboard first, README second (already done by move_sheet above)
# Final sheet order:
# Dashboard | README | DayPlan | PatternLibrary | PatternCards |
# ProblemDB | FailureLog | ReviewQueue | WeeklyAssessment |
# MockInterviews | ResourcePlan | YouTubeChannels | ProgressionCurve | BlindProblemPool

# --- UNIVERSAL FONT NORMALIZATION (Strict Arial across all cells) -------------
print("[...] Normalizing all workbook cell fonts to Arial...")
for sheet in wb.worksheets:
    for row in sheet.iter_rows():
        for cell in row:
            if cell.font is None:
                cell.font = Font(name="Arial", size=10)
            elif cell.font.name != "Arial":
                f = cell.font
                cell.font = Font(
                    name="Arial",
                    size=f.size or 10,
                    bold=f.bold,
                    italic=f.italic,
                    color=f.color,
                    underline=f.underline,
                )

# --- SAVE ---------------------------------------------------------------------
wb.save(OUT)
print(f"\n{'='*60}")
print(f"[SUCCESS] {OUT} saved successfully")
import shutil, os
if os.path.exists("../package.json"):
    shutil.copyfile(OUT, "../DSA_AI_Infra_Training.xlsx")
    print(f"[SYNC] Copied {OUT} -> ../DSA_AI_Infra_Training.xlsx")
elif os.path.exists("dsa"):
    shutil.copyfile(OUT, "dsa/DSA_AI_Infra_Training.xlsx")
    print(f"[SYNC] Copied {OUT} -> dsa/DSA_AI_Infra_Training.xlsx")
print(f"{'='*60}")
print(f"Sheets : {', '.join(ws.title for ws in wb.worksheets)}")
print(f"Days   : {DAYS}")
print(f"Patterns: {len(PATTERNS)}")
print(f"Pattern cards: {len(CARDS)}")
print(f"Tutorials: {len(RESOURCES)}")
print(f"Blind pool: {len(BLIND_POOL)} problems")
print(f"Mocks/Diagnostics: {len(MOCKS)} sessions")
