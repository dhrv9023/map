# 🤖 AI Infrastructure Engineering Roadmap & 168-Day Silicon DSA Cockpit (2026)

> Complete end-to-end learning path, interactive timetable, career transition guide, and specialized **168-Day Silicon-Aware DSA & NVIDIA Cockpit** designed to take you from foundational programming to an AI / AI Infrastructure Systems Engineer.

---

## ⚡ Three Unified Systems in One Repository

This repository integrates three production-ready web applications:

1. **AI Infrastructure Roadmap & Unified Study OS** (`/index.html`)
   - **✦ Dedicated AI Engineer Track (2026)**: Directly embedded career roadmap with 100% free resources, market salary data ($95k–$140k / ₹18L–₹40L), 8 daily responsibilities, weekly schedule (18–20 hrs/wk), and tactical career transition guidance for Catalog QA engineers.
   - **📐 Complete AI System Design Manual & Lab**: Directly integrated 13-Phase Curriculum (Phases A–M), Live Interactive Capacity & Sizing Calculator (VRAM, KV-cache, decode throughput, H100 counts), 7 Progressive Projects, Whiteboard Interview Vault (Levels 1–3), and Actionable First 14 Days Plan.
   - **4 Core Technical Phases**: Foundations, Classical ML & Deep Learning, GenAI & LLMs (with automated evals & Stage 1 Exit Gate), and AI Infrastructure (Triton, CUDA, vLLM/SGLang, FSDP/ZeRO, K8s).
   - **Hardware-Aware Silicon DSA**: C++ track with Step 18 physical silicon mapping (Warp shuffles, lock-free ring buffers, PagedAttention block manager).
   - **Modern Interactive UI**: Liquid morph floating navigation pill, Spotlight search (<kbd>⌘K</kbd> / <kbd>Ctrl+K</kbd>), dynamic reading progress indicator, dark mode, and browser-saved weekly learning log.
   - **Dual Cockpit Linkage**: Instant 1-click access to both the DSA Specialist Cockpit and the standalone System Design Cockpit suite.

2. **168-Day Silicon-Aware DSA & NVIDIA Cockpit** (`/dsa/index.html`)
   - **9 Dedicated Interactive Pages**: Dashboard, 168-Day Daily Plan (24 weeks), 22 Algorithmic Patterns, Flashcards (with SRS flip & filter), NVIDIA Silicon-Aware DSA, Failure Modes & Fixes, 12 Mock Interviews, Curated Video Resources, and Golden Rules.
   - **100% Zero-Server & Offline**: Built with vanilla HTML/CSS/JS and embedded datasets (`data.js`).

3. **AI Infrastructure System Design Cockpit** (`/system-design/index.html`)
   - **7 Dedicated Interactive Pages**: Executive Dashboard, 13-Phase Curriculum (Phases A–M), Verified Topic-to-Resource Matrix, 7 Progressive Implementation Projects, Whiteboard Interview Vault (Levels 1–3), Live Capacity & Sizing Calculator, and 6-Mo / 12-Mo Schedules + Actionable First 14 Days.
   - **Hardware-Aware & Zero Budget**: Tailored for laptop hardware (16GB RAM + RTX 2050 4GB VRAM) with 100% free verified canonical links.

---

## 🛡️ The Execution-Proof Engineering Framework (8 Inviolable Rules)

To eliminate analysis paralysis, tutorial hell, and cognitive overload, the entire roadmap operates under eight strict engineering principles:

1. **Strict Priority System (P0–P3):**
   - **P0 (Essential):** Immediate prerequisite for next project or interview milestone. *Non-negotiable.*
   - **P1 (Important):** Production hardening & observability, scheduled after P0 passes tests.
   - **P2 (Advanced):** Specialized systems/GPU infra, blocked until Stages 1–3 are clear.
   - **P3 (Optional):** Research tooling or hardware specifics, studied only on explicit demand.
   - **The Invariant:** *A P2 or P3 topic is STRICTLY FORBIDDEN from delaying P0 work.*

2. **The 5-Step Build-First Learning Loop:**
   - (1) Learn minimum theory (max 45 min reading) $\to$ (2) Implement small working example $\to$ (3) Self-debug (20-min AI blackout) $\to$ (4) Write 1-page TIL note $\to$ (5) Stop the moment criteria pass and advance immediately.

3. **Measurable Exit Gates:**
   - Advancement is gated by automated evidence, not videos watched: runnable code, passing `pytest`/`mypy`, single-command deployment, whiteboard architecture explanation, and verified latency/memory benchmarks.

4. **The Rule of Three (Zero Resource Bloat):**
   - For every single subject: **1 Primary Resource** (free preferred), **1 Reference Resource** for gap-filling, and **1 Practical Task** with an automated test and stopping condition.

5. **Zero-Debt Recovery Rules & Weekly Retrospective:**
   - Weekly 5-question review every Sunday at 5:00 PM.
   - **No-Debt Policy:** Missed study hours are **never rolled over** into the following week. When behind, shed scope (drop P3, defer P1); protect P0 and the Monday/Wednesday ergonomic health limit.

6. **Real Job Market Alignment:**
   - Concrete breakdown across 4 distinct roles: (1) AI / LLM Application Engineer (Stage 1 exit); (2) ML Platform / MLOps Engineer; (3) Machine Learning Engineer; (4) AI Infrastructure Engineer (Stage 2 exit). Assessed strictly on portfolio evidence, never calendar promises.

7. **Project-First Portfolio Bar (6 Core Artifacts):**
   - Every phase produces an MVP with unit tests, README, architecture diagrams, and empirical benchmarks (e.g. p95 latency, tokens/sec, VRAM profiling).

8. **Single Next Action Directive:**
   - Always provides a single, unambiguous next task with exact docs, a tight timebox, and automated acceptance criteria.

---

## 🌐 1-Click GitHub Pages Deployment

This repository is pre-configured for instant zero-configuration deployment to **GitHub Pages**:

1. Push this repository to GitHub on branch `main` (or `master`).
2. Open your repository on GitHub and navigate to:
   **Settings** ➔ **Pages** (in the left sidebar).
3. Under **Build and deployment** ➔ **Source**, select **Deploy from a branch**.
4. Set **Branch** to `main` and **Folder** to `/(root)`. Click **Save**.
5. Your live site will automatically deploy at:
   ```
   https://<your-username>.github.io/<your-repository-name>/
   ```
   - **AI Infra Roadmap**: `https://<your-username>.github.io/<your-repository-name>/`
   - **DSA Specialist Cockpit**: `https://<your-username>.github.io/<your-repository-name>/dsa/`

> [!NOTE]
> A `.nojekyll` file is already included at the root to prevent GitHub Pages from ignoring asset directories or underscore files. All internal links use relative paths, ensuring complete portability across local `file://` usage, custom domains, and GitHub repository sub-paths.

---

## 📁 Repository Directory Structure

```text
.
├── index.html                   # AI Infrastructure Roadmap & Study OS (GitHub Pages landing page)
├── assets/                      # Bundled CSS/JS for AI Roadmap React components
├── .nojekyll                    # Disables Jekyll processing on GitHub Pages
├── AI_Engineering_Timetable_v2.pdf # High-resolution printable timetable
│
├── dsa/                         # 168-Day Silicon-Aware DSA & NVIDIA Specialist Cockpit
│   ├── index.html               # DSA Cockpit Dashboard & KPI metrics
│   ├── plan.html                # 168-Day Day-by-Day Study Plan with filters & checkboxes
│   ├── patterns.html            # 22 Core Algorithmic Patterns with Big-O & hardware notes
│   ├── flashcards.html          # Interactive spaced-repetition flashcards
│   ├── nvidia.html              # NVIDIA Interview Specifics, System Topics & AI Infra DSA
│   ├── failures.html            # Top 15 Failure Modes & Architectural Fixes
│   ├── mocks.html               # 12 Step-by-Step Mock Interviews with rubrics
│   ├── resources.html           # Curated YouTube Channels & Topic-Wise Direct Links
│   ├── rules.html               # Golden Rules of Silicon DSA & Hardware-Aware Coding
│   ├── style.css                # Polished dark-mode responsive stylesheet
│   ├── site.js                  # Client-side filtering, search, local progress storage
│   ├── data.js                  # Complete 168-day dataset, flashcards, patterns, mocks
│   ├── data.json                # Raw JSON export for API / scripting use
│   ├── build_site.py            # Static site generator script
│   ├── export_data.py           # Data extraction script from Excel workbook
│   ├── DSA_AI_Infra_Training.xlsx # Complete 168-Day Excel Training Sheet
│   ├── HOW_TO_USE.md            # Comprehensive English Student Guide
│   └── HOW_TO_USE_HINGLISH.md   # Casual Hinglish Student Guide for easy reading
│
├── src/                         # Source React 19 & TypeScript components
│   ├── App.tsx                  # Main React container with DSA redirection handler
│   └── main.tsx                 # Entrypoint for floating widgets
├── components/                  # shadcn UI components (Liquid Morph Menu, Spotlight, etc.)
├── template.html                # Vite build template with unbundled script references
├── package.json                 # Node dependencies & GitHub Pages build scripts
├── vite.config.ts               # Vite configuration with relative base ('./')
└── README.md                    # Project documentation
```

- **Liquid Morph Floating Menu (`@/components/ui/liquid-morph-floating-menu.tsx`)**: Directly embedded on the main site! Framer Motion powered floating command pill with fluid dark circle morphing, spring physics, and split-flap kinetic typography roll.
- **Unified Single-Site Architecture**: React, TypeScript, and Tailwind are bundled directly into `index.html` — no separate pages or disconnected demos.
- **Top Navigation Bar (Non-sticky on scroll)**: Clean top navigation with reading progress line that scrolls away smoothly when reading down the page.
- **Spotlight Quick Jump Modal (<kbd>⌘K</kbd> / <kbd>Ctrl+K</kbd>)**: Real-time filterable search modal across all 27 roadmap sections.
- **Fluid Widescreen Layout**: Expands smoothly to take full advantage of ultra-wide and large monitors (`max-width: 1680px+`).
- **Standard shadcn UI Directory**: Configured via `components.json`, `@/*` path aliases, Tailwind CSS v4, and `cn()` utility (`lib/utils.ts`).

### Local Development & Scripts

```bash
# Install dependencies
npm install

# Start Vite dev server (serves the roadmap with React floating menu)
npm run dev

# Type check & production build (compiles all React & TS into dist/)
npm run build

# Preview production build
npm run preview
```

---

## 📚 Core Features

1. **`index.html`** - Unified Roadmap & Study OS
   - **24 Interactive Sections** covering Foundations, ML, GenAI, LLMs, AI Infra, System Design, and Projects.
   - **🚀 Career Switch Track**: Transition plan from quality/backend engineering to AI roles, remote job strategy for India, USD payment guides, and interview prep.
   - **📅 My Schedule**: Custom weekly timetable (Mon–Thu evenings, Friday power sessions, weekend deep dives, and Sunday revision).
   - **📓 Weekly Learning Log**: Browser-saved interactive journal to track learnings, DSA, projects, and goals each week with **1-click JSON Backup & Restore**.
   - **🌙 Dark Mode**: Global dark/light theme switch with persistent state.
   - **📄 3 Integrated Cheat Sheets**: Python, Git, and C++ (with all algorithmic patterns, templates, and flashcards consolidated into the dedicated [168-Day DSA Cockpit](./dsa/index.html)).
   - **✨ Liquid Morph Floating Navigation & Spotlight (<kbd>⌘K</kbd>)**: Fast keyboard and touch navigation across all curriculum modules.

**Learning Sections:**
1. Reality - Market insights & salary
2. Phase 1 - Foundations (Python, Math, Linux, Backend)
3. Phase 2 - ML & Deep Learning
4. Phase 3 - GenAI & LLMs
5. Phase 4 - AI Infrastructure
6. DSA - Direct launchpad to 168-Day Silicon-Aware DSA & NVIDIA Cockpit
7. System Design - Scalable systems
8. Projects - Real-world projects
9. Interviews - Interview prep
10. Brutal Advice - Hard truths

**Day Plans:**
11. Phase 1 Day Plan - Detailed daily schedule
12. Phase 2 Day Plan
13. Phase 3 Day Plan
14. Phase 4 Day Plan

**Specialized Topics:**
15. OS & C++ - Operating systems & C++
16. Sustainability - Long-term learning
17. Strategy - Career strategy
18. Papers - Research papers

**Cheat Sheets & Tools:**
19. Python Cheat Sheet - Complete Python reference
20. Git Cheat Sheet - All git commands
21. C++ Cheat Sheet - STL & modern C++
22. Career Switch Track - Career switch guide
23. My Schedule - Structured study schedule
24. Weekly Learning Log - Interactive browser journal

## ⏱️ Timeline & 2-Stage Career Transition

> [!TIP]
> **Don't wait 24 months to get hired!** Follow the **2-Stage Stepping-Stone Strategy**:

```text
[Now] Catalog QA Engineer
   │
   ▼ Stage 1: Fast-Track Exit (Months 6–9 · Phase 3 Completion)
[AI Evaluation & LLM Application Engineer]
 • Automated Evals (Ragas, DeepEval, Promptfoo, G-Eval)
 • RAG & Agent Systems (FastAPI, Qdrant/Pinecone, LangGraph)
 • Catalog & Fine-Tuning Data Curation (TRL/QLoRA)
 • Target: ₹18L–₹35L / $100K–$140K · 0–2 yrs exp
   │
   ▼ Stage 2: Systems Transition (Months 12–20 · Full Phase 4 Completion)
[Core AI Infrastructure & Systems Engineer]
 • OpenAI Triton & CUDA Kernels (FlashAttention, Fused RoPE)
 • High-Throughput Serving (vLLM, SGLang, TensorRT-LLM, FP8 KV-Cache)
 • Distributed Training (FSDP, DeepSpeed ZeRO 1-3, Megatron 3D Parallelism, NCCL)
 • Target: ₹30L–₹60L / $160K–$250K · 1–3 yrs exp (senior FAANG higher with proven track record)
```

- **Phase 1 (Months 1–6):** Foundations (Python 3.11+, Math, Linux OS, Docker, Backend FastAPI, C++ DSA)
- **Phase 2 (Months 6–12):** ML & DL (Scikit-Learn, PyTorch, Transformers, Hugging Face, Experiment Tracking)
- **Phase 3 (Months 12–17):** GenAI, LLMs & Automated Evals ➔ **🎯 STAGE 1 EXIT GATE**
- **Phase 4 (Months 17–24):** AI Infrastructure, Triton, CUDA & Systems ➔ **🚀 STAGE 2 EXIT GATE**

## 💡 Key Features

✅ **2-Stage Stepping Stone** - Get hired at Phase 3 in AI Evals / App Engineering, then pivot to AI Infra  
✅ **OpenAI Triton & CUDA** - Modern 2026 kernel development in Python + bare-metal C++  
✅ **Budget Hardware Lab (<$20/mo)** - Practice on Modal, RunPod spot instances, and CPU DDP without buying $8k GPUs  
✅ **2026 Serving Stacks** - vLLM, SGLang (RadixAttention), Chunked Prefill, FP8 Quantization  
✅ **Silicon-Aware Systems DSA** - Striver A2Z + Step 18 Hardware Track (Warp shuffles, lock-free ring buffers, PagedAttention block simulation)  
✅ **No Paid Courses** - 100% free gold-standard resources (Stanford CS149, CUDA Mode, Triton docs, fast.ai, DeepLearning.AI)  

## 🎯 What You'll Learn

### Phase 1: Foundations
- Production-level Python 3.11+ (asyncio, memory profiling, type safety)
- Mathematics for ML (Linear Algebra, Multivariable Calculus, Probability)
- Linux Operating System & Systems Programming (concurrency, memory hierarchy)
- Backend & Microservices (FastAPI, Docker, PostgreSQL)
- DSA Core (Arrays, Strings, Two Pointers, Sliding Window in C++)

### Phase 2: ML & Deep Learning
- Classical ML (Scikit-learn, XGBoost, Cross-validation)
- Deep Learning (PyTorch from scratch, Backpropagation, Attention mechanisms)
- Hugging Face Ecosystem (Transformers, Datasets, Tokenizers)
- Experiment Tracking & MLOps (MLflow, Weights & Biases, Optuna)
- DSA Intermediate (Trees, Graphs, Recursion, Dynamic Programming)

### Phase 3: GenAI, LLMs & Automated Evals (Stage 1 Exit)
- Production RAG Systems (Hybrid search, BM25 + Dense, Vector DBs, Context compression)
- Fine-tuning & Adaptation (QLoRA, PEFT, TRL, DPO, Data curation)
- Autonomous AI Agents (ReAct pattern, LangGraph, tool calling, persistent state)
- **Automated LLM Evaluation** (DeepEval, Ragas, Promptfoo, CI/CD regression gates)
- **Career Milestone:** Job-Ready as AI Engineer / AI Evaluation Engineer (₹18L–₹35L)

### Phase 4: AI Infrastructure & Systems (Stage 2 Exit)
- **OpenAI Triton & GPU Architecture** (Streaming Multiprocessors, Warps, SRAM vs HBM, `@triton.jit`, block pointers)
- **CUDA C++ & Nsight Profiling** (Tiled shared memory matmul, arithmetic intensity, Roofline model)
- **Production Inference** (vLLM PagedAttention, SGLang RadixAttention, Speculative Decoding, FP8/INT4 quantization)
- **Distributed Training & Networking** (PyTorch DDP/FSDP, DeepSpeed ZeRO 1-3, Megatron 3D Parallelism, NCCL ring all-reduce)
- **GPU Cluster Orchestration** (KubeRay, NVIDIA GPU Operator, DCGM Prometheus metrics, Grafana dashboards)
- **Capstone Project:** FlashAttention forward pass in both Triton & CUDA with Nsight Roofline benchmark report

## 📊 Realistic Salary Expectations (2026 Market)

- **Stage 1 — AI Eval / Application Engineer (Phase 3 exit, 0–2 yrs exp):** ₹18L–₹35L / $100K–$140K
- **Stage 2 — AI Infrastructure Systems Engineer (Phase 4, 1–3 yrs exp):** ₹30L–₹60L / $160K–$250K
- **Senior / Staff AI Infrastructure Engineer (5+ yrs systems track record):** ₹60L–₹100L+ / $250K–$450K+ *(top-tier FAANG/frontier lab compensation requires proven large-scale production delivery)*

## 🔗 Resources Included

- YouTube channels (NeetCode, Abdul Bari, Striver, etc.)
- Free courses (freeCodeCamp, fast.ai, DeepLearning.AI)
- Books (Chip Huyen's "Designing Machine Learning Systems" & "AI Engineering", Martin Kleppmann's "DDIA", "Fluent Python", etc.)
- Platforms (Leetcode, Kaggle, Hugging Face)
- Documentation (PyTorch, TensorFlow, etc.)

## 📋 How to Use the Cheat Sheets

1. **Python Cheat Sheet** - Reference for Python syntax & libraries
2. **Git Cheat Sheet** - All git commands for version control
3. **DSA Cheat Sheet** - Algorithm templates & patterns
4. **C++ Cheat Sheet** - STL reference for competitive programming

**Search with Ctrl+F** to find any command instantly.

## 🎓 Success Tips

1. **Start with Phase 1** - Don't skip foundations
2. **Do DSA daily** - 1 core problem daily from Striver A2Z (Steps 1–17)
3. **Build projects** - Real projects with automated tests > watching tutorials
4. **Join communities** - Find peers learning the same path (CUDA Mode, PyTorch forums)
5. **Track progress** - Use weekly self-audit questions
6. **Stay consistent with realistic workload** - ~24–26 hrs/week total: Mon/Wed light review (30–45m) to protect health/back; Tue/Thu 2.5–3h; Fri 6–7h; Sat 6–7h; Sun 4–5h
7. **Review regularly** - Use spaced-repetition flashcards
8. **Build in public** - Push clean code and benchmarks to GitHub

## 🚨 Common Mistakes to Avoid

❌ Skipping Phase 1 foundations
❌ Attempting 35+ hours/week on top of a full-time job (leads to immediate burnout)
❌ Attempting CUDA kernel programming before learning model serving and OS memory fundamentals
❌ Only watching tutorials (no code written or benchmarked)
❌ Trying to learn everything simultaneously (follow sequential modules)
❌ Fine-tuning 7B models locally on a 4GB GPU (use free Google Colab T4 or 1.5B/3B models)
❌ Ignoring system design and production observability
❌ Giving up too early

## 📞 Questions?

Each section includes:
- Detailed explanations
- Resource links
- Project ideas
- Interview questions
- Common mistakes
- Real-world context

## 🔄 Updates

This roadmap is updated regularly to reflect:
- Latest AI/ML trends
- New tools & frameworks
- Market demand changes
- Salary insights
- Interview patterns

**Last Updated:** October 2026 (Audited & Calibrated Edition)

---

**Ready to become an AI Infrastructure Engineer? Start with Phase 1! 🚀**
