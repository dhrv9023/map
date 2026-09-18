# 🤖 AI Infrastructure Engineering Roadmap & 168-Day Silicon DSA Cockpit (2026)

> Complete end-to-end learning path, interactive timetable, career transition guide, and specialized **168-Day Silicon-Aware DSA & NVIDIA Cockpit** designed to take you from foundational programming to an AI / AI Infrastructure Systems Engineer.

---

## ⚡ Two Unified Systems in One Repository

This repository integrates two production-ready web applications:

1. **AI Infrastructure Roadmap & Study OS** (`/index.html`)
   - **27 Comprehensive Modules**: Foundations, Classical ML, Deep Learning, GenAI, LLMs, AI Infrastructure (vLLM, CUDA, Triton, TensorRT-LLM, NCCL), System Design, and Real-world Projects.
   - **Modern Interactive UI**: Liquid morph floating navigation pill, Spotlight search (<kbd>⌘K</kbd> / <kbd>Ctrl+K</kbd>), dynamic reading progress indicator, dark/light theme, and browser-saved weekly learning log.
   - **Instant DSA Linkage**: Direct redirection to the DSA Cockpit from top navbar, section 6 hero card, spotlight search, and floating action button.

2. **168-Day Silicon-Aware DSA & NVIDIA Cockpit** (`/dsa/index.html`)
   - **9 Dedicated Interactive Pages**: Dashboard, 168-Day Daily Plan (24 weeks), 22 Algorithmic Patterns, Flashcards (with SRS flip & filter), NVIDIA Silicon-Aware DSA, Failure Modes & Fixes, 12 Mock Interviews, Curated Video Resources (Striver, NeetCode, Aditya Verma, Padho with Pratyush, Love Babbar), and Golden Rules.
   - **100% Zero-Server & Offline**: Built with vanilla HTML/CSS/JS and embedded datasets (`data.js`). Works out-of-the-box locally and on any static host.
   - **Bidirectional Return**: Every DSA page features an **"🤖 AI Infra Roadmap ↗"** button in both the header and navbar to jump straight back to the main roadmap.

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

## ⏱️ Timeline

- **Phase 1 (Months 1-6):** Foundations
  - Python, Math, Linux, Backend
  - DSA (parallel)
  
- **Phase 2 (Months 6-12):** ML & DL
  - Classical ML, Deep Learning
  - Hugging Face, Experiment Tracking
  - DSA (parallel)
  
- **Phase 3 (Months 12-17):** GenAI & LLMs
  - RAG Systems, Fine-tuning
  - Agents, Evaluation
  - DSA (parallel)
  
- **Phase 4 (Months 17-24):** AI Infrastructure
  - GPU Optimization, vLLM
  - Distributed Training
  - Production Deployment

## 💡 Key Features

✅ **No Paid Resources** - Everything is free
✅ **Realistic Timeline** - 20-24 months, 3-5 hours/day
✅ **DSA Parallel** - 1 hour weekday, 2 hours Saturday
✅ **Real Projects** - Build portfolio-worthy projects
✅ **Interview Prep** - Interview questions & system design
✅ **Cheat Sheets** - 4 comprehensive reference guides
✅ **Day Plans** - Detailed daily schedules
✅ **Brutal Honesty** - Real market insights

## 🎯 What You'll Learn

### Phase 1: Foundations
- Python (production-level)
- Mathematics (Linear Algebra, Probability, Calculus)
- Linux & Systems
- Backend Development (FastAPI, Databases)
- DSA (Arrays, Strings, Sorting)

### Phase 2: ML & Deep Learning
- Classical ML (Scikit-learn, XGBoost)
- Deep Learning (PyTorch, Transformers)
- Hugging Face Ecosystem
- Experiment Tracking (MLflow, W&B)
- DSA (Trees, Graphs, DP)

### Phase 3: GenAI & LLMs
- Production RAG Systems
- Fine-tuning & Adaptation
- Agents & Evaluation
- LLM Optimization
- DSA (Advanced patterns)

### Phase 4: AI Infrastructure
- GPU Optimization & CUDA
- vLLM & Model Serving
- Distributed Training
- Kubernetes & Deployment
- System Design at Scale

## 📊 Salary Expectations

- **Entry Level (6 months):** ₹20-30L / $80-120K
- **Mid Level (12 months):** ₹35-60L / $150-250K
- **Senior (18+ months):** ₹60-120L / $250-500K

*Note: Salaries vary by location, company, and negotiation skills*

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
2. **Do DSA daily** - 1 hour weekday, 2 hours Saturday
3. **Build projects** - Real projects > tutorials
4. **Join communities** - Find peers learning the same path
5. **Track progress** - Use weekly self-audit questions
6. **Stay consistent** - 3-5 hours daily is key
7. **Review regularly** - Use cheat sheets for quick reference
8. **Build in public** - Share progress on GitHub/Twitter

## 🚨 Common Mistakes to Avoid

❌ Skipping Phase 1 foundations
❌ Not doing DSA consistently
❌ Only watching tutorials (no coding)
❌ Trying to learn everything at once
❌ Not building real projects
❌ Ignoring system design
❌ Not reading error messages carefully
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

**Last Updated:** May 27, 2026

---

**Ready to become an AI Infrastructure Engineer? Start with Phase 1! 🚀**
