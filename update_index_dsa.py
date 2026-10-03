import json, re, urllib.parse

def lc_url(title):
    clean = re.sub(r"^LC\s*\d+\s*", "", title).strip()
    clean = clean.split("(")[0].strip()
    return f"https://leetcode.com/problem-list/all/?search={urllib.parse.quote(clean)}"

SHEET_DATA = [
    {
        "phaseId": "phase-1",
        "phaseTitle": "Phase 1: Foundations & Arrays (Steps 1–3)",
        "phaseDesc": "C++ syntax, loop invariants, concrete Big-O, basic math, hashing, sorting, and array problem solving from Easy to Hard.",
        "badge": "Phase 1",
        "badgeCls": "pg",
        "steps": [
            {
                "stepNum": "Step 1",
                "stepTitle": "Learn the Basics",
                "stepDesc": "C++ environment setup, syntax, conditionals, loops, functions, memory references (&), basic math, and STL vectors.",
                "subtopics": [
                    {
                        "subId": "1.1",
                        "title": "Things to Know in C++ (Language Basics)",
                        "desc": "Compiler setup, <code>#include &lt;iostream&gt;</code>, data types, cin/cout, if/else, for and while loops, functions, and pass-by-reference (&).",
                        "yt": "https://www.youtube.com/results?search_query=striver+c%2B%2B+basics+for+beginners",
                        "ytLabel": "Striver C++ Basics",
                        "probs": [
                            ("LC 2235 Add Two Integers", "E"),
                            ("LC 2469 Convert the Temperature", "E"),
                            ("LC 9 Palindrome Number", "E")
                        ]
                    },
                    {
                        "subId": "1.2",
                        "title": "Logic Building & Number Operations",
                        "desc": "Loop stepping on paper, extracting digits via % 10 and / 10, digit counting, number reversal, and palindrome checks.",
                        "yt": "https://www.youtube.com/results?search_query=striver+basic+maths+dsa",
                        "ytLabel": "Striver Basic Math",
                        "probs": [
                            ("LC 7 Reverse Integer", "M"),
                            ("LC 1480 Running Sum of 1d Array", "E"),
                            ("Count Digits & Armstrong Number", "E")
                        ]
                    },
                    {
                        "subId": "1.3",
                        "title": "Concrete Time & Space Complexity (Big-O)",
                        "desc": "Loop counts: 1 loop = O(N), 2 nested loops = O(N^2), binary halving = O(log N). The 10^8 ops/sec rule: why N=10^5 causes TLE on O(N^2).",
                        "yt": "https://www.youtube.com/results?search_query=abdul+bari+algorithm+analysis+time+complexity",
                        "ytLabel": "Abdul Bari Big-O",
                        "probs": [
                            ("LC 1929 Concatenation of Array", "E"),
                            ("LC 2011 Final Value of Variable", "E")
                        ]
                    },
                    {
                        "subId": "1.4",
                        "title": "C++ STL & Dynamic Arrays (std::vector)",
                        "desc": "<code>std::vector&lt;int&gt;</code>, push_back(), size(), indexing, range-based for loops, pairs, and why passing by reference (&) prevents RAM copies.",
                        "yt": "https://www.youtube.com/results?search_query=love+babbar+c%2B%2B+stl+vector",
                        "ytLabel": "Love Babbar C++ STL",
                        "probs": [
                            ("LC 27 Remove Element", "E"),
                            ("LC 26 Remove Duplicates from Sorted Array", "E")
                        ]
                    },
                    {
                        "subId": "1.5",
                        "title": "Basic Hashing & Frequency Counting",
                        "desc": "Direct-index frequency array int count[26] vs std::unordered_map. O(1) average lookup vs O(N) linear scan.",
                        "yt": "https://www.youtube.com/results?search_query=striver+hashing+dsa",
                        "ytLabel": "Striver Hashing",
                        "probs": [
                            ("LC 242 Valid Anagram", "E"),
                            ("LC 217 Contains Duplicate", "E")
                        ]
                    }
                ]
            },
            {
                "stepNum": "Step 2",
                "stepTitle": "Learn Important Sorting Techniques",
                "stepDesc": "Elementary O(N^2) sorts to understand invariants, followed by O(N log N) divide-and-conquer sorts.",
                "subtopics": [
                    {
                        "subId": "2.1",
                        "title": "Elementary Sorting (Selection, Bubble, Insertion)",
                        "desc": "Selection sort (find min and swap), Bubble sort (adjacent comparisons), Insertion sort (place element in sorted sub-array).",
                        "yt": "https://www.youtube.com/results?search_query=striver+selection+bubble+insertion+sort",
                        "ytLabel": "Striver Elementary Sorts",
                        "probs": [
                            ("Selection Sort Implementation", "E"),
                            ("Bubble Sort Implementation", "E"),
                            ("Insertion Sort Implementation", "E")
                        ]
                    },
                    {
                        "subId": "2.2",
                        "title": "Divide & Conquer Sorting (Merge Sort & Quick Sort)",
                        "desc": "Merge Sort (recursive divide & merge, O(N log N) guaranteed), Quick Sort (partition around pivot, in-place sorting).",
                        "yt": "https://www.youtube.com/results?search_query=striver+merge+sort+quick+sort",
                        "ytLabel": "Striver Merge & Quick Sort",
                        "probs": [
                            ("LC 912 Sort an Array (Merge Sort)", "M"),
                            ("Quick Sort Implementation", "M")
                        ]
                    }
                ]
            },
            {
                "stepNum": "Step 3",
                "stepTitle": "Solve Problems on Arrays [Easy → Medium → Hard]",
                "stepDesc": "The cornerstone of DSA interviews: linear scans, two-pointer invariants, prefix sums, and matrix rotations.",
                "subtopics": [
                    {
                        "subId": "3.1",
                        "title": "Easy Array Problems",
                        "desc": "Largest element, check if sorted, rotate by K positions, move zeroes, linear search, union of sorted arrays, missing number.",
                        "yt": "https://www.youtube.com/results?search_query=striver+arrays+easy+problems",
                        "ytLabel": "Striver Easy Arrays",
                        "probs": [
                            ("LC 1752 Check if Array Is Sorted and Rotated", "E"),
                            ("LC 283 Move Zeroes", "E"),
                            ("LC 268 Missing Number", "E"),
                            ("LC 485 Max Consecutive Ones", "E"),
                            ("LC 136 Single Number", "E")
                        ]
                    },
                    {
                        "subId": "3.2",
                        "title": "Medium Array Problems (FAANG Core)",
                        "desc": "Two Sum, Sort Colors (Dutch Flag), Majority Element (>N/2), Kadane's algorithm, Stock Buy & Sell, Next Permutation, Longest Consecutive Sequence.",
                        "yt": "https://www.youtube.com/results?search_query=striver+arrays+medium+problems",
                        "ytLabel": "Striver Medium Arrays",
                        "probs": [
                            ("LC 1 Two Sum", "E"),
                            ("LC 75 Sort Colors (Dutch Flag)", "M"),
                            ("LC 169 Majority Element", "E"),
                            ("LC 53 Maximum Subarray (Kadane)", "M"),
                            ("LC 121 Best Time to Buy and Sell Stock", "E"),
                            ("LC 31 Next Permutation", "M"),
                            ("LC 128 Longest Consecutive Sequence", "M"),
                            ("LC 73 Set Matrix Zeroes", "M"),
                            ("LC 48 Rotate Image", "M")
                        ]
                    },
                    {
                        "subId": "3.3",
                        "title": "Hard Array Problems",
                        "desc": "Pascal's Triangle, Majority Element (>N/3), 3Sum, 4Sum, Subarray Sum Equals K, Merge Intervals, Count Inversions, Maximum Product Subarray.",
                        "yt": "https://www.youtube.com/results?search_query=striver+arrays+hard+problems",
                        "ytLabel": "Striver Hard Arrays",
                        "probs": [
                            ("LC 118 Pascal's Triangle", "E"),
                            ("LC 15 3Sum", "M"),
                            ("LC 18 4Sum", "M"),
                            ("LC 560 Subarray Sum Equals K", "M"),
                            ("LC 56 Merge Intervals", "M"),
                            ("LC 88 Merge Sorted Array", "E"),
                            ("LC 152 Maximum Product Subarray", "M")
                        ]
                    }
                ]
            }
        ]
    },
    {
        "phaseId": "phase-2",
        "phaseTitle": "Phase 2: Linear Data Structures & Search (Steps 4–8)",
        "phaseDesc": "Binary Search on arrays and answer spaces, string manipulation, linked lists, recursion foundations, and hardware bitwise arithmetic.",
        "badge": "Phase 2",
        "badgeCls": "pt",
        "steps": [
            {
                "stepNum": "Step 4",
                "stepTitle": "Binary Search [1D, 2D Arrays & Answer Space]",
                "stepDesc": "Invariant-first boundary search, rotated arrays, and the parametric search-on-answer pattern.",
                "subtopics": [
                    {
                        "subId": "4.1",
                        "title": "BS on 1D Arrays",
                        "desc": "Half-open boundaries, Lower & Upper Bound, Search Insert Position, First & Last Occurrence, Rotated Sorted Array, Peak Element.",
                        "yt": "https://www.youtube.com/results?search_query=striver+binary+search+1d+array",
                        "ytLabel": "Striver BS 1D",
                        "probs": [
                            ("LC 704 Binary Search", "E"),
                            ("LC 35 Search Insert Position", "E"),
                            ("LC 34 Find First and Last Position", "M"),
                            ("LC 33 Search in Rotated Sorted Array", "M"),
                            ("LC 153 Find Minimum in Rotated Sorted Array", "M"),
                            ("LC 162 Find Peak Element", "M")
                        ]
                    },
                    {
                        "subId": "4.2",
                        "title": "BS on Answers (Parametric Search — High Value)",
                        "desc": "Monotonic feasibility predicate feasible(x): Koko Eating Bananas, Capacity to Ship Packages, Aggressive Cows, Book Allocation.",
                        "yt": "https://www.youtube.com/results?search_query=striver+binary+search+on+answers",
                        "ytLabel": "Striver BS on Answers",
                        "probs": [
                            ("LC 875 Koko Eating Bananas", "M"),
                            ("LC 1011 Capacity to Ship Packages Within D Days", "M"),
                            ("LC 1482 Minimum Days to Make m Bouquets", "M"),
                            ("LC 410 Split Array Largest Sum", "H"),
                            ("LC 4 Median of Two Sorted Arrays", "H")
                        ]
                    },
                    {
                        "subId": "4.3",
                        "title": "BS on 2D Arrays",
                        "desc": "Search in 2D Matrix with row-wise and column-wise monotonicity, peak element in 2D grid.",
                        "yt": "https://www.youtube.com/results?search_query=striver+binary+search+2d+matrix",
                        "ytLabel": "Striver BS 2D",
                        "probs": [
                            ("LC 74 Search a 2D Matrix", "M"),
                            ("LC 240 Search a 2D Matrix II", "M")
                        ]
                    }
                ]
            },
            {
                "stepNum": "Step 5",
                "stepTitle": "Strings [Basic & Intermediate]",
                "stepDesc": "Character frequency arrays, two-pointer string symmetry, sliding substrings, and palindrome verification.",
                "subtopics": [
                    {
                        "subId": "5.1",
                        "title": "Basic & Easy Strings",
                        "desc": "Reverse words in string, longest common prefix, valid palindrome, isomorphic strings, string rotation checks.",
                        "yt": "https://www.youtube.com/results?search_query=striver+strings+basic+problems",
                        "ytLabel": "Striver Basic Strings",
                        "probs": [
                            ("LC 151 Reverse Words in a String", "M"),
                            ("LC 14 Longest Common Prefix", "E"),
                            ("LC 125 Valid Palindrome", "E"),
                            ("LC 205 Isomorphic Strings", "E")
                        ]
                    },
                    {
                        "subId": "5.2",
                        "title": "Intermediate String Problems",
                        "desc": "Sort characters by frequency, Roman to Integer, String to Integer (atoi), Longest Palindromic Substring.",
                        "yt": "https://www.youtube.com/results?search_query=striver+strings+medium+problems",
                        "ytLabel": "Striver Medium Strings",
                        "probs": [
                            ("LC 451 Sort Characters By Frequency", "M"),
                            ("LC 13 Roman to Integer", "E"),
                            ("LC 8 String to Integer (atoi)", "M"),
                            ("LC 5 Longest Palindromic Substring", "M")
                        ]
                    }
                ]
            },
            {
                "stepNum": "Step 6",
                "stepTitle": "Linked Lists [Single, Double, Fast/Slow]",
                "stepDesc": "Node pointer manipulation, Tortoise & Hare cycle detection, reversing sub-lists, and k-group transformations.",
                "subtopics": [
                    {
                        "subId": "6.1",
                        "title": "1D & Doubly Linked List Fundamentals",
                        "desc": "Node definitions, memory heap allocation, forward and backward traversal, insertion and deletion operations.",
                        "yt": "https://www.youtube.com/results?search_query=striver+linked+list+introduction",
                        "ytLabel": "Striver LL Intro",
                        "probs": [
                            ("LC 206 Reverse Linked List", "E"),
                            ("LC 876 Middle of the Linked List", "E")
                        ]
                    },
                    {
                        "subId": "6.2",
                        "title": "Medium Linked List (Pointers & Fast/Slow)",
                        "desc": "Cycle detection (Floyd's algorithm), find cycle start node, palindrome check, odd-even reordering, remove Nth node from end, add two numbers.",
                        "yt": "https://www.youtube.com/results?search_query=striver+linked+list+medium+problems",
                        "ytLabel": "Striver Medium LL",
                        "probs": [
                            ("LC 141 Linked List Cycle", "E"),
                            ("LC 142 Linked List Cycle II", "M"),
                            ("LC 234 Palindrome Linked List", "E"),
                            ("LC 19 Remove Nth Node From End of List", "M"),
                            ("LC 2 Add Two Numbers", "M"),
                            ("LC 160 Intersection of Two Linked Lists", "E"),
                            ("LC 148 Sort List", "M")
                        ]
                    },
                    {
                        "subId": "6.3",
                        "title": "Hard Linked List",
                        "desc": "Reverse nodes in k-Group, flatten multi-level linked list, clone list with random pointers.",
                        "yt": "https://www.youtube.com/results?search_query=striver+linked+list+hard+problems",
                        "ytLabel": "Striver Hard LL",
                        "probs": [
                            ("LC 25 Reverse Nodes in k-Group", "H"),
                            ("LC 138 Copy List with Random Pointer", "M")
                        ]
                    }
                ]
            },
            {
                "stepNum": "Step 7",
                "stepTitle": "Recursion & Backtracking",
                "stepDesc": "Subsequence generation, combination trees, recursion state identification, and search space pruning.",
                "subtopics": [
                    {
                        "subId": "7.1",
                        "title": "Recursion Foundations & Subsequences",
                        "desc": "Call stack frames, base cases, power function, subset generation, subsequence take/not-take pattern.",
                        "yt": "https://www.youtube.com/results?search_query=striver+recursion+playlist",
                        "ytLabel": "Striver Recursion",
                        "probs": [
                            ("LC 78 Subsets", "M"),
                            ("LC 90 Subsets II", "M"),
                            ("LC 39 Combination Sum", "M"),
                            ("LC 40 Combination Sum II", "M"),
                            ("LC 46 Permutations", "M")
                        ]
                    },
                    {
                        "subId": "7.2",
                        "title": "Hard Backtracking (State Space Search)",
                        "desc": "Grid search with backtracking, N-Queens problem, Sudoku solver, Rat in a Maze.",
                        "yt": "https://www.youtube.com/results?search_query=striver+backtracking+n+queens+sudoku",
                        "ytLabel": "Striver Backtracking",
                        "probs": [
                            ("LC 79 Word Search", "M"),
                            ("LC 51 N-Queens", "H"),
                            ("LC 37 Sudoku Solver", "H")
                        ]
                    }
                ]
            },
            {
                "stepNum": "Step 8",
                "stepTitle": "Bit Manipulation [Hardware & Logic]",
                "stepDesc": "Bitwise operations, bitmasking, bit counting (__builtin_popcount), and parity tricks essential for GPU systems.",
                "subtopics": [
                    {
                        "subId": "8.1",
                        "title": "Bitwise Fundamentals & Bitmasking",
                        "desc": "Check/set/clear/toggle ith bit, remove lowest set bit (n & (n-1)), check power of 2, count set bits, XOR properties.",
                        "yt": "https://www.youtube.com/results?search_query=striver+bit+manipulation+playlist",
                        "ytLabel": "Striver Bit Manipulation",
                        "probs": [
                            ("LC 136 Single Number", "E"),
                            ("LC 137 Single Number II", "M"),
                            ("LC 260 Single Number III", "M"),
                            ("LC 2220 Minimum Bit Flips to Convert Number", "E")
                        ]
                    }
                ]
            }
        ]
    },
    {
        "phaseId": "phase-3",
        "phaseTitle": "Phase 3: Advanced Linear Structures & Heaps (Steps 9–12)",
        "phaseDesc": "Monotonic stacks and queues, sliding window invariants, min/max heaps, and greedy decision proofs.",
        "badge": "Phase 3",
        "badgeCls": "pa",
        "steps": [
            {
                "stepNum": "Step 9",
                "stepTitle": "Stacks & Queues [Monotonic & Design]",
                "stepDesc": "LIFO/FIFO data structures, Min Stack design, and boundary-finding monotonic stacks.",
                "subtopics": [
                    {
                        "subId": "9.1",
                        "title": "Implementation & Core Designs",
                        "desc": "Implement stack using array/queues, implement queue using stacks, Min Stack design in O(1).",
                        "yt": "https://www.youtube.com/results?search_query=striver+stack+and+queue+implementation",
                        "ytLabel": "Striver Stack Intro",
                        "probs": [
                            ("LC 20 Valid Parentheses", "E"),
                            ("LC 155 Min Stack", "M"),
                            ("LC 232 Implement Queue using Stacks", "E")
                        ]
                    },
                    {
                        "subId": "9.2",
                        "title": "Monotonic Stack / Queue (FAANG Tier 1)",
                        "desc": "Next Greater Element I/II, Next Smaller Element, Trapping Rain Water, Sum of Subarray Minimums, Largest Rectangle in Histogram, Sliding Window Maximum.",
                        "yt": "https://www.youtube.com/results?search_query=aditya+verma+stack+playlist",
                        "ytLabel": "Aditya Verma Stack",
                        "probs": [
                            ("LC 496 Next Greater Element I", "E"),
                            ("LC 503 Next Greater Element II", "M"),
                            ("LC 42 Trapping Rain Water", "H"),
                            ("LC 739 Daily Temperatures", "M"),
                            ("LC 907 Sum of Subarray Minimums", "M"),
                            ("LC 84 Largest Rectangle in Histogram", "H"),
                            ("LC 239 Sliding Window Maximum", "H")
                        ]
                    }
                ]
            },
            {
                "stepNum": "Step 10",
                "stepTitle": "Sliding Window & Two Pointers",
                "stepDesc": "Fixed and variable size windows, shrink invariants, atMost(K) subtraction trick, and counting constraints.",
                "subtopics": [
                    {
                        "subId": "10.1",
                        "title": "Medium Sliding Window",
                        "desc": "Longest substring without repeating characters, Max consecutive ones III, Fruit into baskets, Longest repeating character replacement.",
                        "yt": "https://www.youtube.com/results?search_query=aditya+verma+sliding+window+playlist",
                        "ytLabel": "Aditya Verma Window",
                        "probs": [
                            ("LC 3 Longest Substring Without Repeating Characters", "M"),
                            ("LC 1004 Max Consecutive Ones III", "M"),
                            ("LC 904 Fruit Into Baskets", "M"),
                            ("LC 424 Longest Repeating Character Replacement", "M"),
                            ("LC 930 Binary Subarrays With Sum", "M")
                        ]
                    },
                    {
                        "subId": "10.2",
                        "title": "Hard Sliding Window",
                        "desc": "Subarrays with K Different Integers (atMost(K) - atMost(K-1)), Minimum Window Substring with have/need counter state.",
                        "yt": "https://www.youtube.com/results?search_query=neetcode+minimum+window+substring",
                        "ytLabel": "NeetCode Min Window",
                        "probs": [
                            ("LC 992 Subarrays with K Different Integers", "H"),
                            ("LC 76 Minimum Window Substring", "H")
                        ]
                    }
                ]
            },
            {
                "stepNum": "Step 11",
                "stepTitle": "Heaps & Priority Queues",
                "stepDesc": "Binary heaps, O(N) heapify, priority queues, streaming data quantiles, and K-way sorted merges.",
                "subtopics": [
                    {
                        "subId": "11.1",
                        "title": "Heap Concepts & Top-K Problems",
                        "desc": "Min-heap vs Max-heap, std::priority_queue, Kth largest element in array, Top K frequent elements, Task Scheduler.",
                        "yt": "https://www.youtube.com/results?search_query=aditya+verma+heap+playlist",
                        "ytLabel": "Aditya Verma Heaps",
                        "probs": [
                            ("LC 215 Kth Largest Element in an Array", "M"),
                            ("LC 347 Top K Frequent Elements", "M"),
                            ("LC 621 Task Scheduler", "M")
                        ]
                    },
                    {
                        "subId": "11.2",
                        "title": "Hard Heap & Streaming Applications",
                        "desc": "Merge K Sorted Lists, Find Median from Data Stream (dual balancing heaps: max-heap + min-heap).",
                        "yt": "https://www.youtube.com/results?search_query=striver+heaps+hard+problems",
                        "ytLabel": "Striver Hard Heaps",
                        "probs": [
                            ("LC 23 Merge k Sorted Lists", "H"),
                            ("LC 295 Find Median from Data Stream", "H")
                        ]
                    }
                ]
            },
            {
                "stepNum": "Step 12",
                "stepTitle": "Greedy Algorithms",
                "stepDesc": "Local optimal choice proofs, exchange arguments, interval scheduling, and monotonic greedy traversals.",
                "subtopics": [
                    {
                        "subId": "12.1",
                        "title": "Greedy Invariants & Intervals",
                        "desc": "Assign cookies, fractional knapsack, non-overlapping intervals, minimum platforms, Jump Game I/II, Candy distribution.",
                        "yt": "https://www.youtube.com/results?search_query=striver+greedy+algorithms+playlist",
                        "ytLabel": "Striver Greedy",
                        "probs": [
                            ("LC 455 Assign Cookies", "E"),
                            ("LC 435 Non-overlapping Intervals", "M"),
                            ("LC 55 Jump Game", "M"),
                            ("LC 45 Jump Game II", "M"),
                            ("LC 135 Candy", "H")
                        ]
                    }
                ]
            }
        ]
    },
    {
        "phaseId": "phase-4",
        "phaseTitle": "Phase 4: Hierarchies, Graphs & Dynamic Programming (Steps 13–17)",
        "phaseDesc": "Binary trees, BST invariants, graph traversals, topological sorting, shortest path relaxation, and multi-dimensional dynamic programming.",
        "badge": "Phase 4",
        "badgeCls": "pp",
        "steps": [
            {
                "stepNum": "Step 13",
                "stepTitle": "Binary Trees [Traversals, Medium & Hard]",
                "stepDesc": "Recursive contracts, tree diameter, lowest common ancestor, path sums, and tree serialization.",
                "subtopics": [
                    {
                        "subId": "13.1",
                        "title": "Tree Traversals (DFS & BFS)",
                        "desc": "Preorder, Inorder, Postorder (recursive and iterative), Level-order traversal using queue.",
                        "yt": "https://www.youtube.com/results?search_query=striver+tree+traversals",
                        "ytLabel": "Striver Tree Traversals",
                        "probs": [
                            ("LC 102 Binary Tree Level Order Traversal", "M"),
                            ("LC 144 Binary Tree Preorder Traversal", "E"),
                            ("LC 94 Binary Tree Inorder Traversal", "E")
                        ]
                    },
                    {
                        "subId": "13.2",
                        "title": "Medium Tree Problems",
                        "desc": "Max depth, balanced binary tree, diameter, max path sum, same tree, zigzag level order, vertical order traversal, views of tree.",
                        "yt": "https://www.youtube.com/results?search_query=striver+binary+trees+medium+problems",
                        "ytLabel": "Striver Medium Trees",
                        "probs": [
                            ("LC 104 Maximum Depth of Binary Tree", "E"),
                            ("LC 110 Balanced Binary Tree", "E"),
                            ("LC 543 Diameter of Binary Tree", "E"),
                            ("LC 124 Binary Tree Maximum Path Sum", "H"),
                            ("LC 100 Same Tree", "E"),
                            ("LC 103 Binary Tree Zigzag Level Order Traversal", "M"),
                            ("LC 987 Vertical Order Traversal of a Binary Tree", "H"),
                            ("LC 101 Symmetric Tree", "E")
                        ]
                    },
                    {
                        "subId": "13.3",
                        "title": "Hard Tree Problems",
                        "desc": "Lowest Common Ancestor (LCA), maximum tree width, nodes at distance K, construct tree from Preorder + Inorder, serialize and deserialize.",
                        "yt": "https://www.youtube.com/results?search_query=striver+binary+trees+hard+problems",
                        "ytLabel": "Striver Hard Trees",
                        "probs": [
                            ("LC 236 Lowest Common Ancestor of a Binary Tree", "M"),
                            ("LC 662 Maximum Width of Binary Tree", "M"),
                            ("LC 863 All Nodes Distance K in Binary Tree", "M"),
                            ("LC 105 Construct Binary Tree from Preorder and Inorder", "M"),
                            ("LC 297 Serialize and Deserialize Binary Tree", "H")
                        ]
                    }
                ]
            },
            {
                "stepNum": "Step 14",
                "stepTitle": "Binary Search Trees [BST]",
                "stepDesc": "BST order invariant: Left < Root < Right. Search, insertion, validation, and successor navigation in O(h) time.",
                "subtopics": [
                    {
                        "subId": "14.1",
                        "title": "BST Operations & Invariants",
                        "desc": "Search in BST, insert into BST, delete node in BST, Kth smallest element, validate BST, LCA in BST, Inorder Successor, Two Sum in BST.",
                        "yt": "https://www.youtube.com/results?search_query=striver+binary+search+tree+playlist",
                        "ytLabel": "Striver BST Playlist",
                        "probs": [
                            ("LC 700 Search in a Binary Search Tree", "E"),
                            ("LC 701 Insert into a Binary Search Tree", "M"),
                            ("LC 450 Delete Node in a BST", "M"),
                            ("LC 230 Kth Smallest Element in a BST", "M"),
                            ("LC 98 Validate Binary Search Tree", "M"),
                            ("LC 235 Lowest Common Ancestor of a BST", "M"),
                            ("LC 653 Two Sum IV - Input is a BST", "E")
                        ]
                    }
                ]
            },
            {
                "stepNum": "Step 15",
                "stepTitle": "Graphs [BFS/DFS, Topo, Shortest Path, DSU]",
                "stepDesc": "Graph representations, topological sort on DAGs, Dijkstra shortest path, and Disjoint Set Union by rank/size.",
                "subtopics": [
                    {
                        "subId": "15.1",
                        "title": "Graph Traversal (BFS & DFS)",
                        "desc": "Adjacency list representation, connected components, Number of Provinces, Rotting Oranges, Flood Fill, Cycle detection in undirected/directed graphs.",
                        "yt": "https://www.youtube.com/results?search_query=striver+graph+bfs+dfs+playlist",
                        "ytLabel": "Striver Graph BFS/DFS",
                        "probs": [
                            ("LC 547 Number of Provinces", "M"),
                            ("LC 994 Rotting Oranges", "M"),
                            ("LC 733 Flood Fill", "E"),
                            ("LC 200 Number of Islands", "M"),
                            ("LC 542 01 Matrix", "M"),
                            ("LC 130 Surrounded Regions", "M"),
                            ("LC 127 Word Ladder", "H"),
                            ("LC 785 Is Graph Bipartite?", "M")
                        ]
                    },
                    {
                        "subId": "15.2",
                        "title": "Topological Sort (DAG Dependency Scheduling)",
                        "desc": "DFS Topo Sort, Kahn's algorithm (BFS with in-degrees), cycle detection in directed graphs, Course Schedule I/II, Alien Dictionary.",
                        "yt": "https://www.youtube.com/results?search_query=striver+topological+sort+kahns+algorithm",
                        "ytLabel": "Striver Topo Sort",
                        "probs": [
                            ("LC 207 Course Schedule", "M"),
                            ("LC 210 Course Schedule II", "M"),
                            ("Alien Dictionary", "H")
                        ]
                    },
                    {
                        "subId": "15.3",
                        "title": "Shortest Path Algorithms",
                        "desc": "Dijkstra's algorithm with priority queue, shortest path in binary matrix, path with minimum effort, network delay time, Bellman-Ford, Floyd-Warshall.",
                        "yt": "https://www.youtube.com/results?search_query=striver+dijkstra+algorithm+graph",
                        "ytLabel": "Striver Shortest Path",
                        "probs": [
                            ("LC 1091 Shortest Path in Binary Matrix", "M"),
                            ("LC 1631 Path With Minimum Effort", "M"),
                            ("LC 743 Network Delay Time", "M")
                        ]
                    },
                    {
                        "subId": "15.4",
                        "title": "Disjoint Set Union (DSU) & Spanning Trees",
                        "desc": "Disjoint Set by rank/size with path compression, Kruskal's MST, Accounts Merge, Number of Operations to Make Network Connected.",
                        "yt": "https://www.youtube.com/results?search_query=striver+disjoint+set+union+by+rank",
                        "ytLabel": "Striver DSU",
                        "probs": [
                            ("LC 1319 Number of Operations to Make Network Connected", "M"),
                            ("LC 721 Accounts Merge", "M"),
                            ("LC 684 Redundant Connection", "M"),
                            ("LC 778 Swim in Rising Water", "H")
                        ]
                    }
                ]
            },
            {
                "stepNum": "Step 16",
                "stepTitle": "Dynamic Programming [1D, 2D, Knapsack, Strings, Stocks, LIS]",
                "stepDesc": "Overlapping subproblems: memoization to bottom-up tabulation, space optimization, grid paths, 0/1 knapsack, string edits, and LIS.",
                "subtopics": [
                    {
                        "subId": "16.1",
                        "title": "1D DP & Grid Paths",
                        "desc": "Climbing Stairs, Frog Jump, House Robber I/II, Unique Paths I/II, Minimum Path Sum, Triangle.",
                        "yt": "https://www.youtube.com/results?search_query=striver+dp+playlist+1d+grid",
                        "ytLabel": "Striver 1D & Grid DP",
                        "probs": [
                            ("LC 70 Climbing Stairs", "E"),
                            ("LC 198 House Robber", "M"),
                            ("LC 213 House Robber II", "M"),
                            ("LC 62 Unique Paths", "M"),
                            ("LC 63 Unique Paths II", "M"),
                            ("LC 64 Minimum Path Sum", "M")
                        ]
                    },
                    {
                        "subId": "16.2",
                        "title": "DP on Subsequences & Knapsack",
                        "desc": "Subset Sum equals K, Partition Equal Subset Sum, 0/1 Knapsack, Coin Change I/II, Target Sum.",
                        "yt": "https://www.youtube.com/results?search_query=striver+dp+on+subsequences+knapsack",
                        "ytLabel": "Striver DP Subsequences",
                        "probs": [
                            ("LC 416 Partition Equal Subset Sum", "M"),
                            ("LC 322 Coin Change", "M"),
                            ("LC 518 Coin Change II", "M"),
                            ("LC 494 Target Sum", "M")
                        ]
                    },
                    {
                        "subId": "16.3",
                        "title": "DP on Strings & Stocks",
                        "desc": "Longest Common Subsequence (LCS), Longest Palindromic Subsequence, Edit Distance, Best Time to Buy and Sell Stock with Cooldown/Fee.",
                        "yt": "https://www.youtube.com/results?search_query=striver+dp+on+strings+stocks",
                        "ytLabel": "Striver DP Strings & Stocks",
                        "probs": [
                            ("LC 1143 Longest Common Subsequence", "M"),
                            ("LC 516 Longest Palindromic Subsequence", "M"),
                            ("LC 72 Edit Distance", "M"),
                            ("LC 44 Wildcard Matching", "H"),
                            ("LC 309 Best Time to Buy and Sell Stock with Cooldown", "M")
                        ]
                    },
                    {
                        "subId": "16.4",
                        "title": "Longest Increasing Subsequence (LIS) & Partition DP",
                        "desc": "LIS in O(N^2) and O(N log N) using binary search, Largest Divisible Subset, Matrix Chain Multiplication (MCM), Burst Balloons.",
                        "yt": "https://www.youtube.com/results?search_query=striver+lis+matrix+chain+multiplication",
                        "ytLabel": "Striver LIS & MCM",
                        "probs": [
                            ("LC 300 Longest Increasing Subsequence", "M"),
                            ("LC 368 Largest Divisible Subset", "M"),
                            ("LC 1048 Longest String Chain", "M"),
                            ("LC 312 Burst Balloons", "H")
                        ]
                    }
                ]
            },
            {
                "stepNum": "Step 17",
                "stepTitle": "Tries [Prefix Trees & Bitwise Xor]",
                "stepDesc": "Prefix trees for fast dictionary lookups and bitwise tries for maximum XOR range queries.",
                "subtopics": [
                    {
                        "subId": "17.1",
                        "title": "Trie Implementation & Bit Trie",
                        "desc": "Implement Trie (Prefix Tree), count distinct substrings, Maximum XOR of two numbers using binary trie.",
                        "yt": "https://www.youtube.com/results?search_query=striver+trie+data+structure",
                        "ytLabel": "Striver Trie Playlist",
                        "probs": [
                            ("LC 208 Implement Trie (Prefix Tree)", "M"),
                            ("LC 421 Maximum XOR of Two Numbers in an Array", "M")
                        ]
                    }
                ]
            }
        ]
    },
    {
        "phaseId": "phase-5",
        "phaseTitle": "Phase 5: Silicon Hardware & AI-Infrastructure Systems (Step 18 - NVIDIA Specialist Track)",
        "phaseDesc": "Where classical software algorithms meet physical GPU silicon, memory coalescing, lock-free concurrency, and transformer inference engines.",
        "badge": "Phase 5 (NVIDIA)",
        "badgeCls": "pr",
        "steps": [
            {
                "stepNum": "Step 18",
                "stepTitle": "Silicon-Aware Systems Algorithms (The AI-Infra Capstone)",
                "stepDesc": "The specific systems algorithms tested by NVIDIA, Meta AI Infra, Anthropic, and OpenAI systems teams.",
                "subtopics": [
                    {
                        "subId": "18.1",
                        "title": "GPU Warp Primitives & Bitwise Masks",
                        "desc": "Branch divergence elimination, __ballot_sync(), __shfl_down_sync() for register-level warp reductions without shared memory, __builtin_popcount().",
                        "yt": "https://github.com/cuda-mode",
                        "ytLabel": "CUDA Mode Community",
                        "probs": [
                            ("Warp Reduction & Scan Kernel", "H"),
                            ("Branchless Predicated Masking", "M")
                        ]
                    },
                    {
                        "subId": "18.2",
                        "title": "Memory Layouts (SoA vs AoS) & Cache Coalescing",
                        "desc": "Structure of Arrays (SoA: x[N], y[N]) for SIMD/GPU coalesced memory loads vs Array of Structures (AoS: Point pts[N]) cache misses; 64-byte cache lines; false sharing avoidance with alignas(64).",
                        "yt": "https://www.youtube.com/playlist?list=PLoROMvodv4rPOWA-omMM6STXaWW4FvJT8",
                        "ytLabel": "Stanford CS149 Parallel Computing",
                        "probs": [
                            ("Coalesced Memory Transposition", "H"),
                            ("Cache-Friendly Strided Traversal", "M")
                        ]
                    },
                    {
                        "subId": "18.3",
                        "title": "Lock-Free Ring Buffers & Producer-Consumer Queues",
                        "desc": "Single-Producer Single-Consumer (SPSC) circular queues with acquire/release memory semantics; power-of-two mask indexing (idx & (CAP - 1)); NCCL IPC queues.",
                        "yt": "https://github.com/cuda-mode",
                        "ytLabel": "Lock-Free SPSC in C++17",
                        "probs": [
                            ("SPSC Lock-Free Ring Buffer", "H"),
                            ("CUDA Command Ring Buffer", "H")
                        ]
                    },
                    {
                        "subId": "18.4",
                        "title": "PagedAttention & KV-Cache Block Tables (vLLM)",
                        "desc": "Virtual memory paging applied to transformer KV caches to eliminate internal/external HBM fragmentation; copy-on-write fork tables for speculative decoding.",
                        "yt": "https://docs.vllm.ai/",
                        "ytLabel": "vLLM PagedAttention Architecture",
                        "probs": [
                            ("PagedAttention Block Manager Simulation", "H"),
                            ("KV-Cache Memory Compactor", "M")
                        ]
                    },
                    {
                        "subId": "18.5",
                        "title": "Parallel Prefix Scan (Blelloch Algorithm)",
                        "desc": "Work-efficient parallel scan (up-sweep / down-sweep tree reductions) in O(log N) parallel steps across GPU threads; foundation of parallel prefix sum in CUDA.",
                        "yt": "https://www.youtube.com/playlist?list=PLoROMvodv4rPOWA-omMM6STXaWW4FvJT8",
                        "ytLabel": "Blelloch Parallel Scan (CS149)",
                        "probs": [
                            ("Blelloch Work-Efficient Scan", "H"),
                            ("Segmented Parallel Scan", "H")
                        ]
                    },
                    {
                        "subId": "18.6",
                        "title": "High-Dimensional Vector Search (HNSW & IVF)",
                        "desc": "Hierarchical Navigable Small World (HNSW) graph search, Inverted File Indexing (IVF), and vector quantization used in Faiss and cuVS for billion-scale embeddings.",
                        "yt": "https://github.com/facebookresearch/faiss",
                        "ytLabel": "Faiss & cuVS Architecture",
                        "probs": [
                            ("HNSW Graph Search Algorithm", "H"),
                            ("IVF-PQ Approximate Nearest Neighbors", "H")
                        ]
                    }
                ]
            }
        ]
    }
]

def build_dsa_html():
    out = []
    out.append('<!-- DSA MASTER SHEET (STRIVER A2Z + SILICON TRACK) -->')
    out.append('<div id="page-dsa" class="page">')
    out.append('  <div class="hero">')
    out.append('    <div class="tag">DSA Sheet — Striver A2Z + Silicon Systems Track</div>')
    out.append('    <h1>Master DSA Phase & Topic-Wise</h1>')
    out.append('    <p>Zero artificial calendar pressure. Go step-by-step from C++ basics and arrays to advanced dynamic programming and GPU-aware silicon algorithms.</p>')
    out.append('  </div>')

    out.append('  <div class="dla">')
    out.append('    <h2>Interactive Silicon-Aware DSA Cockpit</h2>')
    out.append('    <p>Practice platform with live stopwatch, 42 patterns library, 30 SRS flashcards, dynamic revision vault, and 24 mock interview sessions.</p>')
    out.append('    <div class="dbs">')
    out.append('      <a href="./dsa/index.html" class="db dbp">🚀 Launch DSA Cockpit →</a>')
    out.append('      <a href="./dsa/patterns.html" class="db dbg">🧠 42 Patterns Library</a>')
    out.append('      <a href="./dsa/revision.html" class="db dbg">🔄 Revision Vault</a>')
    out.append('      <a href="./DSA_AI_Infra_Training.xlsx" download class="db dbg">📥 Master Excel Sheet</a>')
    out.append('    </div>')
    out.append('  </div>')

    out.append('  <div class="alert ai">')
    out.append('    <strong>💡 Why Topic-Wise Progression Works Best:</strong><br>')
    out.append('    Day-wise schedules cause artificial guilt when life happens or when a difficult concept (like Recursion or DP) takes 3 days instead of 1.<br>')
    out.append('    Here, topics are structured in the renowned <strong>Striver A2Z order</strong>: you master one step, write the brute force on paper first, optimize, and check off the subtopics at your own pace. You finish with <strong>Step 18</strong>, our dedicated <em>Silicon & AI-Infra Systems Track</em> for NVIDIA/systems roles.')
    out.append('  </div>')

    # Quick phase selector buttons
    out.append('  <div style="display:flex;gap:8px;flex-wrap:wrap;margin:1.5rem 0 2rem;position:sticky;top:52px;z-index:900;background:var(--bg);padding:0.75rem 0;border-bottom:1px solid var(--border);">')
    out.append('    <button class="ubtn" onclick="filterPhase(\'all\')" id="fbtn-all" style="background:var(--accent);color:#fff;border-color:var(--accent);">All 18 Steps</button>')
    out.append('    <button class="ubtn" onclick="filterPhase(\'phase-1\')" id="fbtn-phase-1">Phase 1: Basics & Arrays</button>')
    out.append('    <button class="ubtn" onclick="filterPhase(\'phase-2\')" id="fbtn-phase-2">Phase 2: Linear & Search</button>')
    out.append('    <button class="ubtn" onclick="filterPhase(\'phase-3\')" id="fbtn-phase-3">Phase 3: Stacks & Heaps</button>')
    out.append('    <button class="ubtn" onclick="filterPhase(\'phase-4\')" id="fbtn-phase-4">Phase 4: Trees, Graphs & DP</button>')
    out.append('    <button class="ubtn" onclick="filterPhase(\'phase-5\')" id="fbtn-phase-5" style="border-color:var(--coral);color:var(--coral)">Phase 5: Silicon & AI-Infra (NVIDIA)</button>')
    out.append('  </div>')

    # Render Phases & Steps
    for phase in SHEET_DATA:
        p_id = phase["phaseId"]
        out.append(f'  <div class="dsa-phase-section" id="{p_id}" style="margin-bottom:3rem;">')
        out.append(f'    <div style="display:flex;align-items:center;gap:10px;margin-bottom:0.5rem;">')
        out.append(f'      <span class="pill {phase["badgeCls"]}">{phase["badge"]}</span>')
        out.append(f'      <h2 style="margin:0;border:none;padding:0;font-size:20px;">{phase["phaseTitle"]}</h2>')
        out.append(f'    </div>')
        out.append(f'    <p style="color:var(--text2);font-size:13.5px;margin-bottom:1.5rem;">{phase["phaseDesc"]}</p>')

        for step in phase["steps"]:
            out.append('    <div class="block" style="margin-bottom:1.5rem;padding:1.5rem;border-radius:12px;background:var(--bg2);">')
            out.append('      <div style="display:flex;align-items:center;gap:10px;margin-bottom:0.5rem;flex-wrap:wrap;">')
            out.append(f'        <span class="chip" style="color:var(--accent2);background:var(--bg3);font-weight:800;border-color:var(--border2);">{step["stepNum"]}</span>')
            out.append(f'        <span style="font-size:16px;font-weight:800;color:var(--text);">{step["stepTitle"]}</span>')
            out.append('      </div>')
            out.append(f'      <div style="font-size:13px;color:var(--text2);margin-bottom:1.25rem;">{step["stepDesc"]}</div>')

            # Subtopics
            out.append('      <div style="display:flex;flex-direction:column;gap:1rem;">')
            for sub in step["subtopics"]:
                out.append('        <div style="background:var(--bg3);border:1px solid var(--border);border-radius:8px;padding:1rem;">')
                out.append('          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:10px;flex-wrap:wrap;margin-bottom:0.4rem;">')
                out.append(f'            <div style="font-size:14px;font-weight:700;color:var(--text);"><span style="color:var(--accent2);margin-right:6px;">{sub["subId"]}</span>{sub["title"]}</div>')
                if sub.get("yt"):
                    out.append(f'            <a href="{sub["yt"]}" target="_blank" style="font-size:11.5px;font-weight:700;color:var(--amber);background:#f59e0b14;border:1px solid #f59e0b30;padding:2px 8px;border-radius:5px;text-decoration:none;display:inline-flex;align-items:center;gap:4px;">▶ {sub["ytLabel"]} ↗</a>')
                out.append('          </div>')
                out.append(f'          <div style="font-size:12.5px;color:var(--text2);margin-bottom:0.75rem;line-height:1.5;">{sub["desc"]}</div>')

                # Problems
                out.append('          <div style="display:flex;flex-wrap:wrap;gap:6px;">')
                for p_title, diff in sub["probs"]:
                    diff_cls = "pg" if diff == "E" else ("pa" if diff == "M" else "pr")
                    p_url = lc_url(p_title)
                    out.append(f'            <a href="{p_url}" target="_blank" style="font-size:11.5px;font-family:var(--sans);font-weight:600;background:var(--bg2);border:1px solid var(--border);color:var(--text);padding:3px 8px;border-radius:6px;text-decoration:none;display:inline-flex;align-items:center;gap:6px;transition:border-color .15s;">')
                    out.append(f'              <span>{p_title}</span><span class="pill {diff_cls}" style="font-size:9.5px;padding:1px 5px;">{diff}</span>')
                    out.append('            </a>')
                out.append('          </div>')
                out.append('        </div>')
            out.append('      </div>')
            out.append('    </div>')

        out.append('  </div>')

    # The Beginner's 4-Step Stuck Protocol
    out.append('  <h2>The Beginner\'s 4-Step "Stuck Protocol"</h2>')
    out.append('  <ul class="steps">')
    out.append('    <li><strong>Step 1: Pen & Paper First (5 min):</strong> Never touch the keyboard immediately. Write down a tiny sample array (e.g. <code>[2, 7, 11, 15]</code>, target 9). Walk through how your human eyes solve it.</li>')
    out.append('    <li><strong>Step 2: Shameless Brute Force (10 min):</strong> Write the naive solution first! A working nested loop with O(N²) is infinitely better than staring at an empty editor. Getting test cases to pass builds immediate confidence.</li>')
    out.append('    <li><strong>Step 3: Spot the Bottleneck:</strong> Ask: <em>"Which part of my brute force is slow?"</em> Example: <em>"I am searching for (target - x) across the array in O(N). Can I do it in O(1)?"</em> → Hash map discovered!</li>')
    out.append('    <li><strong>Step 4: Refactor to C++ Optimal (15 min):</strong> Replace the slow search with the optimal data structure, check edge cases (empty array, single element, negative numbers), and submit.</li>')
    out.append('  </ul>')

    # Curated Video Mentors
    out.append('  <h2>Curated Video Mentors (Watch When Stuck)</h2>')
    out.append('  <div class="g3">')
    out.append('    <div class="cc" style="border-top:2.5px solid #f59e0b">')
    out.append('      <div class="cn">Striver (take U forward)</div>')
    out.append('      <div class="cs">@takeUforward · Hinglish</div>')
    out.append('      <div class="cd">The undisputed #1 resource for beginner-to-advanced structured DSA. Start with his C++ Basics & A2Z sheet.</div>')
    out.append('      <div class="cl"><a href="https://www.youtube.com/playlist?list=PLgUwDviBIf0oF6QL8m22w1hIDC1vJ_BHz" target="_blank" style="color:#f59e0b;border-color:#f59e0b30;background:#f59e0b12">▶ A2Z DSA Course</a></div>')
    out.append('    </div>')
    out.append('    <div class="cc" style="border-top:2.5px solid #38bdf8">')
    out.append('      <div class="cn">Love Babbar (CodeHelp)</div>')
    out.append('      <div class="cs">@CodeHelp · Hindi</div>')
    out.append('      <div class="cd">Best beginner C++ syntax, memory diagrams, pointer intuition, and STL vector breakdowns.</div>')
    out.append('      <div class="cl"><a href="https://www.youtube.com/playlist?list=PLDzeHZWIZsTryvtXdMr6rPh4IDexB5NIA" target="_blank" style="color:#0284c7;border-color:#38bdf830;background:#38bdf812">▶ C++ Basics Course</a></div>')
    out.append('    </div>')
    out.append('    <div class="cc" style="border-top:2.5px solid #059669">')
    out.append('      <div class="cn">NeetCode</div>')
    out.append('      <div class="cs">@NeetCode · English</div>')
    out.append('      <div class="cd">Crisp 5–10 min animated problem walkthroughs. Watch after struggling for 20 min on a problem.</div>')
    out.append('      <div class="cl"><a href="https://www.youtube.com/playlist?list=PLot-Xpze53ldVwtstag2TL4HQhAnC8ATf" target="_blank" style="color:#059669;border-color:#05996930;background:#05996912">▶ NeetCode 150</a></div>')
    out.append('    </div>')
    out.append('    <div class="cc" style="border-top:2.5px solid #10b981">')
    out.append('      <div class="cn">Aditya Verma</div>')
    out.append('      <div class="cs">@TheAdityaVerma · Hindi</div>')
    out.append('      <div class="cd">Master of mental models for Sliding Window, Dynamic Programming, and Monotonic Stacks.</div>')
    out.append('      <div class="cl"><a href="https://www.youtube.com/playlist?list=PL_z_8CaSLPWekqh3KpdC9045s07upF834" target="_blank" style="color:#10b981;border-color:#10b98130;background:#10b98112">▶ DP Master Series</a></div>')
    out.append('    </div>')
    out.append('    <div class="cc" style="border-top:2.5px solid #6366f1">')
    out.append('      <div class="cn">Abdul Bari</div>')
    out.append('      <div class="cs">@abdul_bari · English</div>')
    out.append('      <div class="cd">Theoretical and mathematical clarity on Big-O analysis, recurrence relations, and graph algorithms.</div>')
    out.append('      <div class="cl"><a href="https://www.youtube.com/playlist?list=PLDN4rrl48XKpZkf03iYFl-O29szjTrs_O" target="_blank" style="color:#6366f1;border-color:#6366f130;background:#6366f112">▶ Algorithms Course</a></div>')
    out.append('    </div>')
    out.append('    <div class="cc" style="border-top:2.5px solid #ec4899">')
    out.append('      <div class="cn">WilliamFiset</div>')
    out.append('      <div class="cs">@WilliamFiset · English</div>')
    out.append('      <div class="cd">Spectacular animations for Graph Theory, Tarjan\'s SCC, Fenwick Trees, and Segment Trees.</div>')
    out.append('      <div class="cl"><a href="https://www.youtube.com/playlist?list=PLDV1Zeh2NRsDGO4--qE8yH72HFL1Km93P" target="_blank" style="color:#ec4899;border-color:#ec489930;background:#ec489912">▶ Graph Theory Series</a></div>')
    out.append('    </div>')
    out.append('  </div>')

    # NVIDIA Silicon Mapping Table
    out.append('  <h2>NVIDIA & Systems Top 30 Topics — Silicon Mapping <span class="hs">hardware relevance</span></h2>')
    out.append('  <div class="tw"><table>')
    out.append('    <thead><tr><th>#</th><th>Topic</th><th>Priority</th><th>Step</th><th>Physical Silicon Mapping</th></tr></thead>')
    out.append('    <tbody>')
    out.append('      <tr><td>T12</td><td>Topological Sort (Kahn\'s)</td><td><span class="pill pr">🔥 Critical</span></td><td>Step 15</td><td>PyTorch Inductor FX Graph scheduling & compiler passes</td></tr>')
    out.append('      <tr><td>T21</td><td>Blelloch Parallel Scan</td><td><span class="pill pr">🔥 Critical</span></td><td>Step 18</td><td>CUDA shared-memory parallel reduction & prefix scan</td></tr>')
    out.append('      <tr><td>T22</td><td>Warp Primitives (__ballot, __shfl)</td><td><span class="pill pr">🔥 Critical</span></td><td>Step 18</td><td>Register-level warp operations without shared memory overhead</td></tr>')
    out.append('      <tr><td>T24</td><td>PagedAttention / KV Cache</td><td><span class="pill pr">🔥 Critical</span></td><td>Step 18</td><td>vLLM HBM virtual memory paging & block table allocation</td></tr>')
    out.append('      <tr><td>T7</td><td>LRU + LFU Cache Design</td><td><span class="pill pa">⚡ High</span></td><td>Step 9</td><td>GPU L2 cache eviction policies & token cache eviction</td></tr>')
    out.append('      <tr><td>T23</td><td>SPSC Ring Buffer (lock-free)</td><td><span class="pill pa">⚡ High</span></td><td>Step 18</td><td>CUDA command ring buffer, NCCL host-device IPC queues</td></tr>')
    out.append('      <tr><td>T13</td><td>Disjoint Set Union (DSU)</td><td><span class="pill pt">▲ Medium</span></td><td>Step 15</td><td>NVLink / InfiniBand network topology partitioning</td></tr>')
    out.append('      <tr><td>T25</td><td>HNSW Graph (ANN search)</td><td><span class="pill pt">▲ Medium</span></td><td>Step 18</td><td>Faiss / cuVS billion-scale high-dimensional vector retrieval</td></tr>')
    out.append('      <tr><td>T27</td><td>Buddy / Slab Allocator</td><td><span class="pill pt">▲ Medium</span></td><td>Step 18</td><td>CUDA memory pool management (cudaMallocAsync)</td></tr>')
    out.append('    </tbody>')
    out.append('  </table></div>')

    out.append('</div>')
    return "\n".join(out)

if __name__ == "__main__":
    new_dsa_html = build_dsa_html()
    with open("/home/dhruv/Desktop/dsa_new/index.html", "r") as f:
        content = f.read()

    pattern = r'<!-- DSA.*?<!-- SYSTEM DESIGN -->'
    replacement = f'{new_dsa_html}\n\n<!-- SYSTEM DESIGN -->'
    updated, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
    if count == 1:
        # Also append filterPhase function in script
        js_filter = """
function filterPhase(phaseId){
  document.querySelectorAll('.dsa-phase-section').forEach(s=>{
    if(phaseId==='all'||s.id===phaseId){s.style.display='block';}
    else{s.style.display='none';}
  });
  const btns = ['all','phase-1','phase-2','phase-3','phase-4','phase-5'];
  btns.forEach(b=>{
    const el = document.getElementById('fbtn-'+b);
    if(!el)return;
    if(b===phaseId){
      el.style.background='var(--accent)';
      el.style.color='#fff';
      el.style.borderColor='var(--accent)';
    }else{
      el.style.background='var(--bg3)';
      el.style.color='var(--text2)';
      el.style.borderColor='var(--border)';
    }
  });
}
"""
        if "function filterPhase" not in updated:
            updated = updated.replace("function sP(id){", js_filter + "\nfunction sP(id){")

        with open("/home/dhruv/Desktop/dsa_new/index.html", "w") as f:
            f.write(updated)
        print("Successfully updated index.html with Striver-style topic-wise sheet!")
    else:
        print(f"Error: pattern match count = {count}")
