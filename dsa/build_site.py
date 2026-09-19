#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_site.py
Generates a complete, multi-page, static website with 100% data parity.
No Python server needed - open any HTML page directly in the browser!
Pages generated:
  - index.html       : Cockpit / Today's Mission & Live Stopwatch
  - plan.html        : Complete 168-Day Curriculum Explorer
  - patterns.html    : 42 Algorithmic & Systems Patterns Library
  - flashcards.html  : 30 Interactive 3D Flashcard Deck
  - nvidia.html      : NVIDIA Systems, CUDA & AI-Infra Playbook
  - failures.html    : Failure Log & Dynamic SRS Review Queue
  - mocks.html       : 24 Mock Interviews & Diagnostic Sessions
  - resources.html   : 35 Curated Tutorials & Concept Guides
  - rules.html       : System Rules, Stuck Protocol & Failure Codes
"""

import json
import html

def escape(s):
    if s is None:
        return ""
    return html.escape(str(s))

def get_nav_html(active_page):
    nav_items = [
        ("index.html", "🎛️ Dashboard"),
        ("plan.html", "🗓️ 168-Day Plan"),
        ("patterns.html", "🧠 Pattern Library"),
        ("flashcards.html", "🃏 3D Flashcards"),
        ("nvidia.html", "🟢 NVIDIA Track"),
        ("failures.html", "💥 Failure Log"),
        ("mocks.html", "🎯 Mocks & Diags"),
        ("resources.html", "📺 Resources"),
        ("rules.html", "📜 System Rules"),
        ("assess.html", "🧭 Day 0 Assessment")
    ]
    links = []
    for href, label in nav_items:
        cls = "nav-tab active" if href == active_page else "nav-tab"
        extra_style = ' style="color:var(--nv-green);border-color:rgba(118,185,0,0.35);"' if href == "assess.html" and href != active_page else ''
        links.append(f'<a href="{href}" class="{cls}"{extra_style}>{label}</a>')
    links.append('<a href="../index.html" class="nav-tab" style="color: #c084fc; border: 1px solid rgba(192,132,252,0.35); background: rgba(168,85,247,0.08); margin-left: auto; font-weight: 700;">🤖 AI Infra Roadmap ↗</a>')
    return "\n      ".join(links)

def page_shell(title, active_page, content_html):
    nav_html = get_nav_html(active_page)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(title)} - NVIDIA & AI-Infra Systems Track</title>
  <meta name="description" content="168-Day Silicon-Aware DSA & AI-Infrastructure Systems Specialist Training System">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="app-container">
    <!-- Top Persistent Header -->
    <header class="app-header">
      <div class="header-top">
        <div class="brand-section">
          <a href="index.html" style="text-decoration: none; display: flex; align-items: center; gap: 0.75rem;">
            <span class="brand-badge">NVIDIA TRACK</span>
            <span class="brand-title">DSA & AI-INFRASTRUCTURE SPECIALIST COCKPIT</span>
          </a>
          <a href="../index.html" class="brand-badge" style="background: rgba(168,85,247,0.2); color: #c084fc; border: 1px solid rgba(168,85,247,0.4); text-decoration: none;" title="Go back to the AI Infrastructure Engineering Roadmap">🤖 AI ROADMAP ↗</a>
        </div>
        <div class="header-quick-stats">
          <div class="stat-chip" title="Current Day in 168-Day Program">
            <span class="chip-label">TODAY:</span>
            <span class="chip-value highlight-green" id="header-current-day">Day 1</span>
          </div>
          <div class="stat-chip" title="Progress across 168 days">
            <span class="chip-label">PROGRESS:</span>
            <span class="chip-value" id="header-progress-pct">0%</span>
          </div>
          <div class="stat-chip" title="Interview Readiness Score based on real performance">
            <span class="chip-label">READINESS:</span>
            <span class="chip-value highlight-green" id="header-readiness-score">0 / 100</span>
          </div>
          <div class="stat-chip" title="Consecutive days practiced">
            <span class="chip-label">🔥 STREAK:</span>
            <span class="chip-value" id="header-streak">0 Days</span>
          </div>
          <a href="../DSA_AI_Infra_Training.xlsx" class="btn btn-outline" style="background: rgba(118,185,0,0.12); border-color: rgba(118,185,0,0.4); color: var(--nv-green); text-decoration: none; display: inline-flex; align-items: center; gap: 4px;" download title="Download Complete 14-Sheet Master Excel Workbook">📥 Excel Sheet</a>
          <button class="btn btn-outline" id="btn-open-sync" title="Export/Import and Backup data">💾 Sync / Backup</button>
        </div>
      </div>
      <!-- Multi-Page Nav Tabs -->
      <nav class="nav-tabs">
        {nav_html}
      </nav>
    </header>

    <!-- Page Body -->
    <main class="main-content">
      {content_html}
    </main>
  </div>

  <!-- MODAL: Complete Day -->
  <div class="modal-overlay" id="modal-complete-day">
    <div class="modal-content">
      <div class="modal-header">
        <h3 style="font-size: 1.15rem; font-weight: 700; color: #fff;" id="modal-day-title">Mark Day Complete</h3>
        <button class="modal-close" id="btn-close-modal">&times;</button>
      </div>
      <form id="form-complete-day">
        <input type="hidden" id="modal-day-num" value="1">
        <div class="form-group">
          <label class="form-label">Total Time Spent (Minutes)</label>
          <input type="number" class="form-control" id="modal-time-spent" min="10" max="300" value="60" required>
        </div>
        <div class="form-group">
          <label class="form-label">Solved Both Independently?</label>
          <select class="form-control" id="modal-solved-indep">
            <option value="Yes">Yes (No solution viewed, minimal/no hints)</option>
            <option value="No">No (Struggled or consulted hints)</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Hints Taken</label>
          <select class="form-control" id="modal-hints-count">
            <option value="0">0 Hints</option>
            <option value="1">1 Hint</option>
            <option value="2">2 Hints</option>
            <option value="3">3+ Hints</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Solution / Editorial Viewed?</label>
          <select class="form-control" id="modal-sol-viewed">
            <option value="No">No (Clean solve)</option>
            <option value="Yes">Yes (Looked up approach/code)</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Key Invariant / Mental Model Takeaway</label>
          <textarea class="form-control" id="modal-key-insight" rows="2" placeholder="e.g. Invariant: prefix[r] - prefix[l-1] is the sum of range [l, r]"></textarea>
        </div>
        <div style="display: flex; justify-content: flex-end; gap: 0.5rem;">
          <button type="button" class="btn btn-outline" id="btn-cancel-modal">Cancel</button>
          <button type="submit" class="btn btn-primary">Save & Advance ✨</button>
        </div>
      </form>
    </div>
  </div>

  <!-- MODAL: Data Sync & Backup -->
  <div class="modal-overlay" id="modal-sync">
    <div class="modal-content">
      <div class="modal-header">
        <h3 style="font-size: 1.15rem; font-weight: 700; color: #fff;">💾 Data Backup & Portability</h3>
        <button class="modal-close" id="btn-close-sync-modal">&times;</button>
      </div>
      <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 1.25rem;">
        Your logs, completed days, and metrics are automatically saved in your browser's <code style="color: var(--nv-green);">localStorage</code> across all pages without needing a server.
      </p>
      <div style="display: flex; flex-direction: column; gap: 0.75rem; margin-bottom: 1.5rem;">
        <button class="btn btn-primary" id="btn-export-json">⬇️ Export Progress to JSON</button>
        <button class="btn btn-outline" id="btn-export-csv">⬇️ Export Completed Days to CSV</button>
      </div>
      <div class="form-group">
        <label class="form-label">Restore Progress from JSON</label>
        <input type="file" id="input-import-file" accept=".json" class="form-control">
      </div>
      <hr style="border: 0; border-top: 1px solid var(--border-subtle); margin: 1.25rem 0;">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 0.75rem; color: var(--red-accent);">Danger Zone:</span>
        <button class="btn btn-outline" id="btn-reset-data" style="border-color: var(--red-accent); color: var(--red-accent);">Clear All Saved Progress</button>
      </div>
    </div>
  </div>

  <script src="data.js"></script>
  <script src="site.js"></script>
</body>
</html>
"""

def generate_index_html(data):
    d1 = data["days"][0]
    content = f"""
      <!-- Hero Mission Banner -->
      <div class="mission-hero">
        <div class="mission-header">
          <div>
            <div class="mission-day-badge">
              <span>🟢 TODAY'S MISSION</span> &bull; <span id="hero-day-date">Day 1 of 168 ({escape(d1['dateDisplay'])})</span>
            </div>
            <h1 class="mission-title" id="hero-topic">{escape(d1['pattern'])}</h1>
            <div class="mission-topic" id="hero-objective">{escape(d1['objective'])}</div>
          </div>
          <div style="display: flex; gap: 0.5rem; align-items: center;">
            <button class="btn btn-outline" id="btn-prev-mission" title="Inspect previous day">◀</button>
            <button class="btn btn-outline" id="btn-next-mission" title="Inspect next day">▶</button>
            <button class="btn btn-primary" id="btn-complete-today">✓ Mark Day Complete</button>
          </div>
        </div>

        <div class="mission-grid">
          <!-- Left Box: Assigned Problems & NVIDIA Hardware Hint -->
          <div>
            <div class="problem-box" id="hero-p1-box">
              <div class="problem-info">
                <span class="diff-tag diff-{d1['d1']}" id="hero-p1-diff">{d1['d1']}</span>
                <div>
                  <div class="problem-title" id="hero-p1-title">{escape(d1['p1'])}</div>
                  <div class="problem-meta" id="hero-p1-meta">Target: {d1['t1']} min | Mode: {escape(d1['mode'])}</div>
                </div>
              </div>
              <div style="display: flex; gap: 0.5rem;">
                <a href="{d1['p1Url']}" target="_blank" class="btn btn-outline" id="hero-p1-link">Solve on LC ↗</a>
              </div>
            </div>

            <div class="problem-box" id="hero-p2-box">
              <div class="problem-info">
                <span class="diff-tag diff-{d1['d2']}" id="hero-p2-diff">{d1['d2']}</span>
                <div>
                  <div class="problem-title" id="hero-p2-title">{escape(d1['p2'])}</div>
                  <div class="problem-meta" id="hero-p2-meta">Target: {d1['t2']} min | Difficulty: {d1['d2']}</div>
                </div>
              </div>
              <div style="display: flex; gap: 0.5rem;">
                <a href="{d1['p2Url']}" target="_blank" class="btn btn-outline" id="hero-p2-link">Solve on LC ↗</a>
              </div>
            </div>

            <!-- Today's Tutorial Video Callout (if scheduled) -->
            <div class="problem-box" id="hero-tut-box" style="border-left: 3px solid #f59e0b; background: rgba(245, 158, 11, 0.04); margin-bottom: 0.75rem; {'' if d1.get('tutYn') == 'YES' else 'display: none;'}">
              <div class="problem-info">
                <span class="diff-tag" style="background: rgba(245, 158, 11, 0.2); color: #fbbf24;" id="hero-tut-badge">📺 TUTORIAL ({d1.get('tutMin', 25)}m)</span>
                <div>
                  <div class="problem-title" id="hero-tut-title">{escape(d1.get('tutTopic', ''))}</div>
                  <div class="problem-meta" id="hero-tut-meta">Recommended: {escape(d1.get('tutResource', {}).get('primaryChannel', 'Striver') if d1.get('tutResource') else 'Striver')} &bull; Striver, Aditya Verma, Love Babbar, Padho with Pratyush, NeetCode</div>
                </div>
              </div>
              <div style="display: flex; flex-direction: column; gap: 0.35rem; align-items: flex-end;" id="hero-tut-actions">
                <a href="{d1.get('tutResource', {}).get('primaryUrl', 'resources.html') if d1.get('tutResource') else 'resources.html'}" target="_blank" class="btn btn-primary" id="hero-tut-link" style="padding: 0.35rem 0.75rem; font-size: 0.78rem; text-decoration: none; font-weight: 700;">
                  ▶ Watch on YouTube ↗
                </a>
                <a href="resources.html" style="font-size: 0.72rem; color: var(--cyan-accent); text-decoration: none;">All 35 Tutorials &rarr;</a>
              </div>
            </div>

            <!-- AI Infra / Hardware Callout -->
            <div style="background: rgba(118, 185, 0, 0.08); border: 1px solid rgba(118, 185, 0, 0.3); border-radius: var(--radius-md); padding: 0.75rem 1rem; font-size: 0.85rem;">
              <span style="color: var(--nv-green); font-weight: 700;">🟢 NVIDIA & AI-INFRA CONNECTION:</span>
              <span id="hero-infra-note" style="color: var(--text-primary); margin-left: 0.25rem;">{escape(d1['infra'])}</span>
            </div>
          </div>

          <!-- Right Box: Live Stuck Protocol Timer -->
          <div class="timer-card">
            <div>
              <div style="font-size: 0.8rem; font-weight: 700; color: var(--text-secondary); letter-spacing: 0.05em; text-transform: uppercase;">
                ⏱️ STUCK PROTOCOL STOPWATCH
              </div>
              <div class="timer-display" id="timer-display">45:00</div>
              <div class="timer-status-badge status-silence" id="timer-status-badge">Phase 1: Complete Silence (0–10m)</div>
              <div id="timer-instruction" style="font-size: 0.78rem; color: var(--text-muted); margin-bottom: 0.75rem;">
                Derive target TC, annotate constraints, sketch 2 custom test inputs. Zero hints permitted.
              </div>
            </div>
            <div class="timer-controls">
              <button class="btn btn-primary" id="timer-btn-start">▶ Start</button>
              <button class="btn btn-outline" id="timer-btn-pause">⏸ Pause</button>
              <button class="btn btn-outline" id="timer-btn-reset">🔄 Reset</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Metric Cards Grid -->
      <div class="grid-4" style="margin-bottom: 1.5rem;">
        <div class="card">
          <div class="card-subtitle">INTERVIEW READINESS (B28)</div>
          <div style="font-size: 2rem; font-weight: 800; font-family: var(--font-mono); color: var(--nv-green);" id="kpi-readiness">0 / 100</div>
          <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.25rem;">30% Indep + 25% Hint + 25% Mock + 20% TTP</div>
        </div>
        <div class="card">
          <div class="card-subtitle">INDEPENDENT SOLVE RATE</div>
          <div style="font-size: 2rem; font-weight: 800; font-family: var(--font-mono);" id="kpi-indep">0%</div>
          <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.25rem;">Target: &gt;80% (Certified Specialist: &gt;95%)</div>
        </div>
        <div class="card">
          <div class="card-subtitle">HINT DEPENDENCY RATE</div>
          <div style="font-size: 2rem; font-weight: 800; font-family: var(--font-mono);" id="kpi-hints">0%</div>
          <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.25rem;">Target: &lt;20% (Certified Specialist: &lt;8%)</div>
        </div>
        <div class="card">
          <div class="card-subtitle">AVG TIME-TO-PATTERN</div>
          <div style="font-size: 2rem; font-weight: 800; font-family: var(--font-mono);" id="kpi-ttp">-- min</div>
          <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.25rem;">Target: &lt;5 min (Certified Specialist: &lt;3 min)</div>
        </div>
      </div>

      <!-- Assessment Banner (JS-toggled) -->
      <div id="assessment-banner" style="display:none;background:rgba(118,185,0,0.07);border:1px solid rgba(118,185,0,0.25);border-radius:10px;padding:0.75rem 1.25rem;margin-bottom:1rem;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap;">
        <div style="display:flex;align-items:center;gap:10px;"><span style="font-size:1.1rem;">🧭</span><div><div style="font-size:0.8rem;font-weight:800;color:var(--nv-green);letter-spacing:0.06em;">DAY 0 ASSESSMENT COMPLETE</div><div style="font-size:0.82rem;color:var(--text-secondary);" id="banner-assess-text">Recommended start: Week 1 &middot; Score: 0/45</div></div></div>
        <a href="assess.html" style="font-size:0.78rem;font-weight:700;color:var(--nv-green);background:rgba(118,185,0,0.12);border:1px solid rgba(118,185,0,0.3);padding:4px 12px;border-radius:6px;text-decoration:none;">Retake ↗</a>
      </div>
      <div id="no-assessment-banner" style="background:rgba(245,158,11,0.07);border:1px dashed rgba(245,158,11,0.3);border-radius:10px;padding:0.65rem 1.25rem;margin-bottom:1rem;display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap;">
        <span style="font-size:0.82rem;color:var(--amber-accent);">🧭 <strong>Haven't taken the Day 0 Assessment yet?</strong> Find your optimal starting week and skip what you already know.</span>
        <a href="assess.html" style="font-size:0.78rem;font-weight:800;color:#000;background:linear-gradient(135deg,#f59e0b,#d97706);padding:5px 14px;border-radius:6px;text-decoration:none;white-space:nowrap;">Take Assessment &rarr;</a>
      </div>
      <!-- ══════════════════════════════════════════════════════════ -->
      <!-- ADAPTIVE WEEKLY ENGINE                                    -->
      <!-- ══════════════════════════════════════════════════════════ -->
      <div class="card" style="margin-bottom:1.5rem;border-color:rgba(56,189,248,0.3);">
        <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.75rem;margin-bottom:1.25rem;">
          <div>
            <div class="card-subtitle" style="color:var(--cyan-accent);">⚙️ ADAPTIVE WEEKLY ENGINE</div>
            <div class="card-title" style="font-size:1rem;font-weight:800;">Weekly Check-In → Next Week Recommendation</div>
          </div>
          <button id="awe-toggle-history" style="font-size:0.75rem;font-weight:700;background:transparent;border:1px solid var(--border-subtle);color:var(--text-muted);padding:4px 12px;border-radius:6px;cursor:pointer;" title="View past check-ins">📋 History</button>
        </div>

        <!-- Status display -->
        <div id="awe-status-display" style="display:none;border-radius:10px;padding:1rem 1.25rem;margin-bottom:1.25rem;border-left-width:3px;border-left-style:solid;">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:0.4rem;">
            <span id="awe-status-icon" style="font-size:1.5rem;">⚡</span>
            <div>
              <div id="awe-status-badge" style="font-size:0.7rem;font-weight:900;letter-spacing:0.1em;">STATUS</div>
              <div id="awe-status-title" style="font-size:1rem;font-weight:800;">—</div>
            </div>
          </div>
          <div id="awe-status-action" style="font-size:0.85rem;line-height:1.6;"></div>
        </div>

        <!-- Check-in form -->
        <form id="awe-form" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:0.85rem;align-items:end;">
          <div>
            <div style="font-size:0.72rem;font-weight:700;color:var(--text-muted);margin-bottom:0.35rem;text-transform:uppercase;letter-spacing:0.06em;">Week Completed</div>
            <select id="awe-week" class="form-control">
              <option value="">— Select Week —</option>
              <!-- filled by JS -->
            </select>
          </div>
          <div>
            <div style="font-size:0.72rem;font-weight:700;color:var(--text-muted);margin-bottom:0.35rem;text-transform:uppercase;letter-spacing:0.06em;">Problems Solved Independently</div>
            <select id="awe-indep" class="form-control">
              <option value="0">0 problems</option>
              <option value="1">1–3 problems</option>
              <option value="2">4–7 problems</option>
              <option value="3">8–10 problems</option>
              <option value="4">11–14 problems</option>
            </select>
          </div>
          <div>
            <div style="font-size:0.72rem;font-weight:700;color:var(--text-muted);margin-bottom:0.35rem;text-transform:uppercase;letter-spacing:0.06em;">Mocks Completed This Week</div>
            <select id="awe-mocks" class="form-control">
              <option value="0">0 mocks</option>
              <option value="1">1 mock</option>
              <option value="2">2+ mocks</option>
            </select>
          </div>
          <div>
            <div style="font-size:0.72rem;font-weight:700;color:var(--text-muted);margin-bottom:0.35rem;text-transform:uppercase;letter-spacing:0.06em;">Primary Failure Code</div>
            <select id="awe-fcode" class="form-control">
              <option value="none">No recurring failure</option>
              <option value="pattern">F1/F2 — Pattern identification</option>
              <option value="derive">F3 — Can't derive recurrence</option>
              <option value="ds">F4 — Wrong data structure</option>
              <option value="complexity">F5 — Wrong complexity / TLE</option>
              <option value="impl">F6/F7/F8 — Implementation bugs</option>
              <option value="recall">F9 — Forgot previously learned</option>
              <option value="pressure">F10 — Timer panic / freeze</option>
            </select>
          </div>
          <div style="display:flex;align-items:flex-end;">
            <button type="submit" class="btn btn-primary" style="width:100%;justify-content:center;">⚡ Compute</button>
          </div>
        </form>

        <!-- History panel (hidden by default) -->
        <div id="awe-history-panel" style="display:none;margin-top:1.25rem;border-top:1px solid var(--border-subtle);padding-top:1rem;">
          <div style="font-size:0.75rem;font-weight:800;color:var(--text-muted);letter-spacing:0.06em;margin-bottom:0.75rem;">PAST CHECK-INS (last 6 weeks)</div>
          <div id="awe-history-list" style="display:flex;flex-direction:column;gap:0.5rem;"></div>
        </div>
      </div>

      <!-- Two Columns: Diagnostics & Quick Failure Action -->
      <div class="grid-2">
        <div class="card">
          <div class="card-title">🎯 Next Upcoming Milestone Diagnostic</div>
          <div id="dashboard-next-diag" style="margin-top: 0.75rem;">Loading upcoming diagnostic...</div>
        </div>
        <div class="card">
          <div class="card-title">💥 Quick Failure Hotspot Alert</div>
          <div id="dashboard-failure-hotspot" style="margin-top: 0.75rem; font-size: 0.9rem; color: var(--text-secondary);">
            No recurring failure hotspots detected yet. Keep logging all stuck points in the Failure Log.
          </div>
        </div>
      </div>
    """
    return page_shell("Dashboard", "index.html", content)

def generate_plan_html(data):
    rows_html = []
    for d in data["days"]:
        nv_tag = '<span class="brand-badge" style="font-size: 0.65rem;">🟢 NVIDIA</span>' if d['isNvidia'] else '—'
        if d['tutYn'] == 'YES':
            tut_res = d.get('tutResource')
            if tut_res:
                primary_ch = tut_res.get('primaryChannel', 'Striver')
                cls = tut_res['channels'][0]['cls'] if tut_res.get('channels') else 'striver'
                tut_tag = f"""
                  <div style="min-width: 170px;">
                    <div style="font-size: 0.78rem; font-weight: 600; color: #fff; margin-bottom: 0.25rem;">{escape(d['tutTopic'])}</div>
                    <div style="display: flex; gap: 0.35rem; align-items: center; flex-wrap: wrap;">
                      <a href="{tut_res['primaryUrl']}" target="_blank" class="btn btn-primary" style="padding: 0.15rem 0.45rem; font-size: 0.68rem; text-decoration: none; font-weight: 700;">
                        ▶ Watch ({escape(primary_ch)}) ↗
                      </a>
                      <a href="resources.html" class="yt-channel-pill {cls}" style="font-size: 0.65rem; padding: 0.1rem 0.35rem;">
                        All Creators &rarr;
                      </a>
                    </div>
                  </div>
                """
            else:
                tut_tag = f"📺 {escape(d['tutTopic'])}"
        else:
            tut_tag = '<span style="color: var(--text-muted);">—</span>'
        rows_html.append(f"""
          <tr data-day="{d['day']}" data-phase="{d['phase']}" data-week="{d['week']}" data-nvidia="{str(d['isNvidia']).lower()}">
            <td style="font-weight: 700; color: #fff;">{d['day']}</td>
            <td style="white-space: nowrap; font-size: 0.8rem; color: var(--text-secondary);">{escape(d['dateDisplay'])}</td>
            <td>
              <div style="font-weight: 600; color: #fff;">{escape(d['pattern'])}</div>
              <div style="font-size: 0.75rem; color: var(--text-muted);">{escape(d['objective'])}</div>
            </td>
            <td><span style="font-size: 0.8rem; color: var(--cyan-accent);">{escape(d['skill'])}</span></td>
            <td>
              <a href="{d['p1Url']}" target="_blank" style="color: var(--text-primary); text-decoration: none; font-weight: 500;">
                {escape(d['p1'])}
              </a>
              <span class="diff-tag diff-{d['d1']}" style="font-size: 0.65rem; margin-left: 0.25rem;">{d['d1']}</span>
            </td>
            <td>
              <a href="{d['p2Url']}" target="_blank" style="color: var(--text-primary); text-decoration: none; font-weight: 500;">
                {escape(d['p2'])}
              </a>
              <span class="diff-tag diff-{d['d2']}" style="font-size: 0.65rem; margin-left: 0.25rem;">{d['d2']}</span>
            </td>
            <td><span style="font-size: 0.75rem;">{tut_tag}</span></td>
            <td><span style="font-size: 0.75rem; color: var(--text-muted);">{escape(d['mode'])}</span></td>
            <td>{nv_tag}</td>
            <td>
              <span class="day-status-pill" data-day-status="{d['day']}" style="font-size: 0.8rem; font-weight: 600; color: var(--text-muted);">
                Pending
              </span>
            </td>
            <td>
              <button class="btn btn-outline btn-complete-row" style="padding: 0.2rem 0.6rem; font-size: 0.75rem;" data-day="{d['day']}">
                Complete
              </button>
            </td>
          </tr>
        """)

    content = f"""
      <div class="search-filter-bar">
        <input type="text" class="search-input" id="plan-search" placeholder="Search by topic, problem name, pattern, or keyword...">
        <select class="filter-select" id="plan-filter-phase">
          <option value="ALL">All Phases (1–4)</option>
          <option value="1">Phase 1: Linear & Hardware (Days 1–42)</option>
          <option value="2">Phase 2: Hierarchical & Topologies (Days 43–84)</option>
          <option value="3">Phase 3: Optimization & Flows (Days 85–126)</option>
          <option value="4">Phase 4: Systems & AI-Infra (Days 127–168)</option>
        </select>
        <select class="filter-select" id="plan-filter-week">
          <option value="ALL">All 24 Weeks</option>
          {''.join([f'<option value="{w}">Week {w}</option>' for w in range(1, 25)])}
        </select>
        <select class="filter-select" id="plan-filter-nvidia">
          <option value="ALL">All Topics</option>
          <option value="NVIDIA">🟢 NVIDIA Systems Only</option>
        </select>
        <select class="filter-select" id="plan-filter-status">
          <option value="ALL">All Statuses</option>
          <option value="PENDING">Incomplete Only</option>
          <option value="DONE">Completed Only</option>
        </select>
      </div>

      <div class="table-container">
        <table class="data-table" id="table-dayplan">
          <thead>
            <tr>
              <th style="width: 50px;">Day</th>
              <th>Date</th>
              <th>Topic & Objective</th>
              <th>Pattern</th>
              <th>Problem 1</th>
              <th>Problem 2</th>
              <th>Tutorial</th>
              <th>Mode</th>
              <th>NVIDIA Focus</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody id="tbody-dayplan">
            {''.join(rows_html)}
          </tbody>
        </table>
      </div>
    """
    return page_shell("168-Day Curriculum Plan", "plan.html", content)

def generate_patterns_html(data):
    cards_html = []
    for p in data["patterns"]:
        cards_html.append(f"""
          <div class="card pattern-card-item" data-pattern-name="{escape(p['name'].lower())}" data-pattern-desc="{escape((p['recognitionCues'] + ' ' + p['coreIdea'] + ' ' + p['aiInfraRelevance']).lower())}">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
              <h4 style="font-size: 1.05rem; font-weight: 700; color: #fff;">#{p['id']} {escape(p['name'])}</h4>
              <span class="brand-badge" style="font-size: 0.65rem;">{escape(p['complexity'].split(';')[0])}</span>
            </div>
            <div style="font-size: 0.82rem; color: var(--cyan-accent); margin-bottom: 0.5rem;">
              <strong>Trigger:</strong> {escape(p['recognitionCues'])}
            </div>
            <div style="font-size: 0.82rem; color: var(--text-secondary); margin-bottom: 0.75rem;">
              <strong>Core Idea:</strong> {escape(p['coreIdea'])}
            </div>
            <div style="background: rgba(0, 0, 0, 0.4); padding: 0.6rem; border-radius: var(--radius-sm); font-size: 0.78rem; font-family: var(--font-mono); color: var(--text-primary); margin-bottom: 0.75rem;">
              <strong>Structures:</strong> {escape(p['dataStructures'])}
            </div>
            <div style="border-top: 1px solid var(--border-subtle); padding-top: 0.6rem; font-size: 0.8rem; color: var(--text-nv);">
              <strong>🟢 AI-Infra / Hardware:</strong> {escape(p['aiInfraRelevance'])}
            </div>
          </div>
        """)

    content = f"""
      <div class="search-filter-bar">
        <input type="text" class="search-input" id="pattern-search" placeholder="Search all 42 patterns by cue, constraint, name, or hardware relevance...">
        <span style="font-size: 0.85rem; color: var(--text-secondary); margin-left: auto;">Total 42 Patterns</span>
      </div>
      <div class="grid-2" id="patterns-grid">
        {''.join(cards_html)}
      </div>
    """
    return page_shell("Pattern Library", "patterns.html", content)

def generate_flashcards_html(data):
    cards_html = []
    for c in data["cards"]:
        cards_html.append(f"""
          <div class="flashcard-wrapper" data-card-text="{escape((c['problem'] + ' ' + c['pattern'] + ' ' + c['triggerCue']).lower())}">
            <div class="flashcard-inner">
              <!-- Front Face -->
              <div class="flashcard-front">
                <div>
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <span class="diff-tag diff-H" style="font-size: 0.7rem;">CARD #{c['id']}</span>
                    <span style="font-size: 0.75rem; color: var(--cyan-accent); font-weight: 600;">{escape(c['pattern'])}</span>
                  </div>
                  <h3 style="font-size: 1.15rem; font-weight: 700; color: #fff; margin-bottom: 0.75rem;">
                    {escape(c['problem'])}
                  </h3>
                  <div style="font-size: 0.88rem; color: var(--text-secondary); line-height: 1.5; margin-bottom: 1rem;">
                    <strong style="color: var(--amber-accent);">Trigger Cue:</strong><br>
                    {escape(c['triggerCue'])}
                  </div>
                  <div style="background: rgba(0, 0, 0, 0.4); border-left: 2px solid var(--cyan-accent); padding: 0.5rem 0.75rem; border-radius: var(--radius-sm); font-size: 0.8rem; color: var(--text-muted);">
                    {escape(c['variants'])}
                  </div>
                </div>
                <div class="card-flip-prompt">
                  <span>👆 Click to flip & reveal Invariant, Code & NVIDIA note</span>
                </div>
              </div>

              <!-- Back Face -->
              <div class="flashcard-back">
                <div>
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span class="brand-badge" style="font-size: 0.65rem;">REVEALED INVARIANT</span>
                    <span style="font-size: 0.75rem; color: var(--text-nv); font-family: var(--font-mono);">{escape(c['complexity'])}</span>
                  </div>
                  <div style="font-size: 0.85rem; color: #fff; font-weight: 600; margin-bottom: 0.5rem;">
                    {escape(c['invariant'])}
                  </div>
                  <div style="background: rgba(0, 0, 0, 0.6); padding: 0.6rem; border-radius: var(--radius-sm); font-size: 0.78rem; font-family: var(--font-mono); color: var(--text-nv); margin-bottom: 0.6rem;">
                    {escape(c['coreIdea'])}
                  </div>
                  <div style="font-size: 0.78rem; color: #f87171; margin-bottom: 0.5rem;">
                    <strong>⚠️ Failure Trap:</strong> {escape(c['failureTrap'])}
                  </div>
                  <div style="border-top: 1px solid var(--border-subtle); padding-top: 0.5rem; font-size: 0.8rem; color: var(--text-nv);">
                    <strong>🟢 One-Line Anchor:</strong> {escape(c['anchorCue'])}
                  </div>
                </div>
                <div class="card-flip-prompt">
                  <span>👆 Click to flip back</span>
                </div>
              </div>
            </div>
          </div>
        """)

    content = f"""
      <div class="search-filter-bar">
        <input type="text" class="search-input" id="flashcard-search" placeholder="Search flashcards by problem or trigger keyword...">
        <button class="btn btn-outline" id="btn-flip-all">🔄 Flip All Cards</button>
        <span style="font-size: 0.85rem; color: var(--text-secondary); margin-left: auto;">Total 30 Cards</span>
      </div>
      <div class="flashcards-grid" id="flashcards-container">
        {''.join(cards_html)}
      </div>
    """
    return page_shell("3D Flashcards Deck", "flashcards.html", content)

def generate_nvidia_html(data):
    pillars_html = []
    for p in data["nvidiaPlaybook"]["pillars"]:
        prims_html = ""
        if "primitives" in p:
            prims_html = '<div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0.75rem 0;">' + "".join([
                f'<div style="background: rgba(0,0,0,0.5); border: 1px solid var(--border-subtle); border-radius: 4px; padding: 0.25rem 0.5rem; font-size: 0.75rem;"><code style="color: var(--nv-green);">{escape(pr["code"])}</code> &bull; <span style="color: var(--text-secondary);">{escape(pr["desc"])}</span></div>'
                for pr in p["primitives"]
            ]) + '</div>'

        trap_html = f'<div style="font-size: 0.8rem; color: #f87171; margin-top: 0.35rem;"><strong>The Trap:</strong> {escape(p["trap"])}</div>' if "trap" in p else ""
        days_str = ", ".join(map(str, p["days"]))

        pillars_html.append(f"""
          <div class="nvidia-pillar-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
              <h4 style="font-size: 1.1rem; font-weight: 700; color: #fff;">
                Pillar {p['id']}: {escape(p['title'])}
              </h4>
              <span class="brand-badge" style="font-size: 0.7rem;">{escape(p['badge'])}</span>
            </div>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 0.5rem;">{escape(p['summary'])}</p>
            {trap_html}
            {prims_html}
            <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 0.75rem; border-top: 1px solid var(--border-subtle); padding-top: 0.5rem;">
              <span style="font-size: 0.8rem; color: var(--text-muted);">Practiced in Curriculum: Days {days_str}</span>
              <a href="plan.html" class="btn btn-outline" style="padding: 0.25rem 0.6rem; font-size: 0.75rem;">
                View Days in Plan ↗
              </a>
            </div>
          </div>
        """)

    framework_html = []
    for step in data["nvidiaPlaybook"]["responseFramework"]:
        framework_html.append(f"""
          <div style="background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 1rem; margin-bottom: 0.75rem;">
            <div style="font-weight: 700; color: var(--cyan-accent); margin-bottom: 0.25rem;">{escape(step['step'])}</div>
            <div style="font-size: 0.88rem; color: var(--text-secondary); font-style: italic;">"{escape(step['quote'])}"</div>
          </div>
        """)

    content = f"""
      <div class="nvidia-banner">
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
          <span class="brand-badge" style="font-size: 0.85rem;">GREEN TEAM EXCELLENCE</span>
          <h2 style="font-size: 1.4rem; font-weight: 800; color: #fff;">The NVIDIA Systems, CUDA & AI-Infrastructure Playbook</h2>
        </div>
        <p style="color: var(--text-secondary); font-size: 0.95rem; max-width: 900px; margin-bottom: 1rem;">
          At NVIDIA, Big-O alone in a vacuum is rejected. Interviews in CUDA, TensorRT, Triton, NCCL, and GPU System Software test whether your algorithmic intuition respects physical silicon: cache lines, memory coalescing, warp divergence, and lock-free queues.
        </p>
        <div style="background: rgba(0, 0, 0, 0.4); border-left: 3px solid var(--nv-green); padding: 0.85rem 1.25rem; border-radius: var(--radius-sm); font-size: 0.88rem;">
          <strong style="color: var(--nv-green);">🎙️ The Killer Interview Dialogue:</strong>
          <p style="color: #e2e8f0; font-style: italic; margin-top: 0.25rem;">
            "{escape(data['nvidiaPlaybook']['killerDialogue'])}"
          </p>
        </div>
      </div>

      <h3 style="font-size: 1.15rem; font-weight: 700; margin-bottom: 1rem; color: #fff;">The 7 Pillars of Silicon Empathy</h3>
      <div id="nvidia-pillars-container">
        {''.join(pillars_html)}
      </div>

      <h3 style="font-size: 1.15rem; font-weight: 700; margin: 1.5rem 0 1rem 0; color: #fff;">The 3-Tier NVIDIA Interview Response Structure</h3>
      <div>
        {''.join(framework_html)}
      </div>
    """
    return page_shell("NVIDIA Systems Playbook", "nvidia.html", content)

def generate_failures_html(data):
    content = f"""
      <div class="grid-2" style="margin-bottom: 1.5rem;">
        <div class="card">
          <div class="card-title">💥 Log a Failure / Stuck Point</div>
          <div class="card-subtitle">Every struggle is automated learning data. Pick an F-code to schedule targeted recovery.</div>
          <form id="form-log-failure">
            <div class="form-group">
              <label class="form-label">Problem / Day</label>
              <input type="text" class="form-control" id="fl-input-problem" placeholder="e.g. Day 10 - LC 3 Longest Substring" required>
            </div>
            <div class="form-group">
              <label class="form-label">Failure Category (F1–F12)</label>
              <select class="form-control" id="fl-input-code" required>
                {''.join([f'<option value="{fc["code"]}">{fc["code"]}: {escape(fc["label"])} ({escape(fc["desc"])})</option>' for fc in data['fcats']])}
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">What Happened & One Actionable Preventive Rule</label>
              <textarea class="form-control" id="fl-input-rule" rows="2" placeholder="e.g. Thought it was sliding window but negatives broke monotonicity. Rule: Check for negatives before window!" required></textarea>
            </div>
            <button type="submit" class="btn btn-primary">Submit Failure Log</button>
          </form>
        </div>

        <div class="card">
          <div class="card-title">🔄 Dynamic Spaced Repetition Queue (SRS)</div>
          <div class="card-subtitle">Prioritized review: Solution viewed (+1d), Hints (+3d), Independent (+7d).</div>
          <div id="review-queue-container" style="max-height: 260px; overflow-y: auto;">
            <p style="color: var(--text-muted); font-size: 0.85rem;">No items currently due for spaced repetition review. Clean record!</p>
          </div>
        </div>
      </div>

      <h3 style="font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">Historical Failure Ledger</h3>
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Problem</th>
              <th>Category</th>
              <th>Preventive Rule</th>
              <th>Next Due</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody id="tbody-failure-history">
            <!-- Populated via site.js from localStorage -->
          </tbody>
        </table>
      </div>
    """
    return page_shell("Failure Log & Review Queue", "failures.html", content)

def generate_mocks_html(data):
    rows_html = []
    for m in data["mocks"]:
        rows_html.append(f"""
          <tr>
            <td style="font-weight: 700; color: var(--cyan-accent);">#{m['id']}</td>
            <td style="font-weight: 600;">Day {m['day']}</td>
            <td style="font-size: 0.8rem; color: var(--text-secondary);">{escape(m['dateDisplay'])}</td>
            <td><span class="brand-badge" style="font-size: 0.7rem;">{escape(m['sessionType'])}</span></td>
            <td style="font-weight: 500; color: #fff;">{escape(m['problemDesc'])}</td>
            <td><span class="diff-tag diff-{m['difficulty']}">{m['difficulty']}</span></td>
            <td style="font-family: var(--font-mono); font-size: 0.85rem;">{m['timeLimit']} min</td>
            <td><a href="{m['lcUrl']}" target="_blank" class="btn btn-outline" style="padding: 0.2rem 0.5rem; font-size: 0.75rem;">Solve ↗</a></td>
            <td><span style="font-size: 0.75rem; color: var(--text-muted);">Scheduled</span></td>
          </tr>
        """)

    content = f"""
      <div class="card" style="margin-bottom: 1.25rem;">
        <div class="card-title">🎯 24-Session Diagnostic & Mock Roadmap</div>
        <div class="card-subtitle">Graduated escalation: Milestone Diagnostics, Unlabelled problem tests, and Capstone Systems verbal mocks.</div>
      </div>
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>Session</th>
              <th>Day</th>
              <th>Target Date</th>
              <th>Type</th>
              <th>Assigned Problem Set</th>
              <th>Diff</th>
              <th>Time Limit</th>
              <th>Link</th>
              <th>Result</th>
            </tr>
          </thead>
          <tbody id="tbody-mocks">
            {''.join(rows_html)}
          </tbody>
        </table>
      </div>
    """
    return page_shell("Mock Interviews & Diagnostics", "mocks.html", content)

def generate_resources_html(data):
    rows_html = []
    for r in data["resources"]:
        channel_pills = []
        for ch in r.get("channels", []):
            channel_pills.append(
                f'<a href="{ch["url"]}" target="_blank" class="yt-channel-pill {ch["cls"]}" title="Search {escape(r["topic"])} on {escape(ch["name"])}">📺 {escape(ch["name"])} ↗</a>'
            )
        pills_html = "".join(channel_pills)

        search_terms = (
            str(r["day"]) + " " +
            r["topic"] + " " +
            r["source"] + " " +
            r["whyItMatters"] + " " +
            r["whatToExtract"] + " " +
            r.get("primaryChannel", "") + " " +
            " ".join([c["name"] for c in r.get("channels", [])])
        ).lower()

        rows_html.append(f"""
          <tr class="resource-row-item" data-text="{escape(search_terms)}">
            <td style="font-weight: 700; color: var(--nv-green); white-space: nowrap;">Day {r['day']}</td>
            <td>
              <div style="font-weight: 700; color: #fff; font-size: 0.95rem; margin-bottom: 0.25rem;">{escape(r['topic'])}</div>
              <div style="font-size: 0.75rem; color: var(--cyan-accent);">{escape(r['source'])}</div>
            </td>
            <td style="font-family: var(--font-mono); font-size: 0.8rem; white-space: nowrap;">{r['duration']} min</td>
            <td style="font-size: 0.82rem; color: var(--text-secondary); max-width: 240px; line-height: 1.4;">{escape(r['whyItMatters'])}</td>
            <td style="font-size: 0.82rem; color: var(--text-muted); max-width: 260px; line-height: 1.4;">{escape(r['whatToExtract'])}</td>
            <td style="min-width: 250px;">
              <div style="margin-bottom: 0.45rem;">
                <a href="{r['primaryUrl']}" target="_blank" class="btn btn-primary" style="padding: 0.35rem 0.75rem; font-size: 0.78rem; display: inline-flex; align-items: center; gap: 0.4rem; text-decoration: none; font-weight: 700;">
                  ▶ Watch ({escape(r['primaryChannel'])}) ↗
                </a>
              </div>
              <div class="channel-links-group">
                {pills_html}
              </div>
            </td>
          </tr>
        """)

    content = f"""
      <!-- MASTER YOUTUBE CREATORS DIRECTORY SHOWCASE -->
      <div class="card" style="margin-bottom: 1.5rem; background: linear-gradient(135deg, rgba(18, 28, 42, 0.95), rgba(9, 16, 24, 0.95)); border: 1px solid rgba(118, 185, 0, 0.35);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; flex-wrap: wrap; gap: 0.75rem;">
          <div>
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
              <span class="brand-badge" style="font-size: 0.7rem;">MASTER DIRECTORY</span>
              <span style="font-size: 0.75rem; color: var(--text-nv); font-family: var(--font-mono);">10 Curated Creators • Direct Master Playlists</span>
            </div>
            <h2 style="font-size: 1.35rem; font-weight: 800; color: #fff; margin: 0;">Silicon-Aware Algorithmic &amp; Systems Creators</h2>
          </div>
          <a href="../DSA_AI_Infra_Training.xlsx" download="DSA_AI_Infra_Training.xlsx" class="btn btn-primary" style="text-decoration: none; display: inline-flex; align-items: center; gap: 6px; font-weight: 700; font-size: 0.85rem;">
            <span>📥 Download Master Excel Sheet (.xlsx)</span>
          </a>
        </div>
        <p style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.6; margin-bottom: 1.25rem;">
          Every tutorial in this curriculum is mapped to top global educators in algorithmic patterns, C++ concurrency, and AI infrastructure systems. Use the 1-click links below to jump straight to their flagship master series:
        </p>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem;">
          <!-- Striver -->
          <div style="background: rgba(7, 10, 14, 0.7); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 1rem; border-top: 3px solid #f59e0b;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
              <strong style="color: #fff; font-size: 0.95rem;">Striver (take U forward)</strong>
              <span style="font-size: 0.7rem; color: #fbbf24; background: rgba(245,158,11,0.15); padding: 0.1rem 0.4rem; border-radius: 4px;">Baseline</span>
            </div>
            <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.4; margin-bottom: 0.75rem;">
              A2Z DSA Course, SDE Sheet, Graph Series (54 vids), DP Series (56 vids), Binary Trees. Standard interview baseline.
            </p>
            <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
              <a href="https://www.youtube.com/playlist?list=PLgUwDviBIf0oF6QL8m22w1hIDC1vJ_BHz" target="_blank" class="btn btn-outline" style="font-size: 0.72rem; padding: 0.2rem 0.5rem; color: #fbbf24; border-color: rgba(245,158,11,0.4);">▶ A2Z Course ↗</a>
              <a href="https://www.youtube.com/@takeUforward" target="_blank" class="btn btn-outline" style="font-size: 0.72rem; padding: 0.2rem 0.5rem;">📺 Channel ↗</a>
            </div>
          </div>

          <!-- Aditya Verma -->
          <div style="background: rgba(7, 10, 14, 0.7); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 1rem; border-top: 3px solid #76b900;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
              <strong style="color: #fff; font-size: 0.95rem;">Aditya Verma</strong>
              <span style="font-size: 0.7rem; color: var(--nv-green); background: rgba(118,185,0,0.15); padding: 0.1rem 0.4rem; border-radius: 4px;">DP Master</span>
            </div>
            <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.4; margin-bottom: 0.75rem;">
              DP Recurrence (Knapsack, LCS, MCM), Sliding Window (16 vids), Stack &amp; Monotonic Stack, Heaps.
            </p>
            <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
              <a href="https://www.youtube.com/playlist?list=PL_z_8CaSLPWekqh3KpdC9045s07upF834" target="_blank" class="btn btn-outline" style="font-size: 0.72rem; padding: 0.2rem 0.5rem; color: var(--nv-green); border-color: rgba(118,185,0,0.4);">▶ DP Series ↗</a>
              <a href="https://www.youtube.com/@TheAdityaVerma" target="_blank" class="btn btn-outline" style="font-size: 0.72rem; padding: 0.2rem 0.5rem;">📺 Channel ↗</a>
            </div>
          </div>

          <!-- Padho with Pratyush -->
          <div style="background: rgba(7, 10, 14, 0.7); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 1rem; border-top: 3px solid #a855f7;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
              <strong style="color: #fff; font-size: 0.95rem;">Padho with Pratyush</strong>
              <span style="font-size: 0.7rem; color: #c084fc; background: rgba(168,85,247,0.15); padding: 0.1rem 0.4rem; border-radius: 4px;">Systems DSA</span>
            </div>
            <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.4; margin-bottom: 0.75rem;">
              LRU/ARC Buffer Pools, Lock-Free Ring Buffers, HNSW Vector Indexing, DAG Compiler Scheduling, Interval DP.
            </p>
            <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
              <a href="https://www.youtube.com/@padhowithpratyush" target="_blank" class="btn btn-outline" style="font-size: 0.72rem; padding: 0.2rem 0.5rem; color: #c084fc; border-color: rgba(168,85,247,0.4);">▶ Systems Playlists ↗</a>
              <a href="https://www.youtube.com/@padhowithpratyush" target="_blank" class="btn btn-outline" style="font-size: 0.72rem; padding: 0.2rem 0.5rem;">📺 Channel ↗</a>
            </div>
          </div>

          <!-- Love Babbar -->
          <div style="background: rgba(7, 10, 14, 0.7); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 1rem; border-top: 3px solid #38bdf8;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
              <strong style="color: #fff; font-size: 0.95rem;">Love Babbar (CodeHelp)</strong>
              <span style="font-size: 0.7rem; color: #38bdf8; background: rgba(56,189,248,0.15); padding: 0.1rem 0.4rem; border-radius: 4px;">C++ DSA</span>
            </div>
            <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.4; margin-bottom: 0.75rem;">
              Complete C++ DSA Course (140+ videos), Pointer diagrams, Recursion &amp; Backtracking, Trees, Graphs.
            </p>
            <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
              <a href="https://www.youtube.com/playlist?list=PLDzeHZWIZsTryvtXdMr6rPh4IDexB5NIA" target="_blank" class="btn btn-outline" style="font-size: 0.72rem; padding: 0.2rem 0.5rem; color: #38bdf8; border-color: rgba(56,189,248,0.4);">▶ C++ Course ↗</a>
              <a href="https://www.youtube.com/@CodeHelp" target="_blank" class="btn btn-outline" style="font-size: 0.72rem; padding: 0.2rem 0.5rem;">📺 Channel ↗</a>
            </div>
          </div>

          <!-- NeetCode -->
          <div style="background: rgba(7, 10, 14, 0.7); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 1rem; border-top: 3px solid #10b981;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
              <strong style="color: #fff; font-size: 0.95rem;">NeetCode</strong>
              <span style="font-size: 0.7rem; color: #34d399; background: rgba(16,185,129,0.15); padding: 0.1rem 0.4rem; border-radius: 4px;">Rapid Review</span>
            </div>
            <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.4; margin-bottom: 0.75rem;">
              NeetCode 150 &amp; Blind 75 walkthroughs. 5-10 min animated diagrams with optimal invariant checks.
            </p>
            <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
              <a href="https://www.youtube.com/playlist?list=PLot-Xpze53ldVwtstag2TL4HQhAnC8ATf" target="_blank" class="btn btn-outline" style="font-size: 0.72rem; padding: 0.2rem 0.5rem; color: #34d399; border-color: rgba(16,185,129,0.4);">▶ NeetCode 150 ↗</a>
              <a href="https://www.youtube.com/@NeetCode" target="_blank" class="btn btn-outline" style="font-size: 0.72rem; padding: 0.2rem 0.5rem;">📺 Channel ↗</a>
            </div>
          </div>

          <!-- Abdul Bari -->
          <div style="background: rgba(7, 10, 14, 0.7); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 1rem; border-top: 3px solid #6366f1;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
              <strong style="color: #fff; font-size: 0.95rem;">Abdul Bari</strong>
              <span style="font-size: 0.7rem; color: #818cf8; background: rgba(99,102,241,0.15); padding: 0.1rem 0.4rem; border-radius: 4px;">Proofs &amp; Theory</span>
            </div>
            <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.4; margin-bottom: 0.75rem;">
              Algorithm analysis, recurrence proofs, divide &amp; conquer, dynamic programming proofs, shortest paths.
            </p>
            <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
              <a href="https://www.youtube.com/playlist?list=PLDN4rrl48XKpZkf03iYFl-O29szjTrs_O" target="_blank" class="btn btn-outline" style="font-size: 0.72rem; padding: 0.2rem 0.5rem; color: #818cf8; border-color: rgba(99,102,241,0.4);">▶ Algorithms ↗</a>
              <a href="https://www.youtube.com/@abdul_bari" target="_blank" class="btn btn-outline" style="font-size: 0.72rem; padding: 0.2rem 0.5rem;">📺 Channel ↗</a>
            </div>
          </div>

          <!-- WilliamFiset -->
          <div style="background: rgba(7, 10, 14, 0.7); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 1rem; border-top: 3px solid #ec4899;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
              <strong style="color: #fff; font-size: 0.95rem;">WilliamFiset</strong>
              <span style="font-size: 0.7rem; color: #f472b6; background: rgba(236,72,153,0.15); padding: 0.1rem 0.4rem; border-radius: 4px;">Advanced Graphs</span>
            </div>
            <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.4; margin-bottom: 0.75rem;">
              Graph Theory animations, Fenwick &amp; Segment trees, Tarjan's SCC &amp; bridges, Dinic's network flow.
            </p>
            <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
              <a href="https://www.youtube.com/playlist?list=PLDV1Zeh2NRsDGO4--qE8yH72HFL1Km93P" target="_blank" class="btn btn-outline" style="font-size: 0.72rem; padding: 0.2rem 0.5rem; color: #f472b6; border-color: rgba(236,72,153,0.4);">▶ Graph Theory ↗</a>
              <a href="https://www.youtube.com/@WilliamFiset-videos" target="_blank" class="btn btn-outline" style="font-size: 0.72rem; padding: 0.2rem 0.5rem;">📺 Channel ↗</a>
            </div>
          </div>

          <!-- Errichto -->
          <div style="background: rgba(7, 10, 14, 0.7); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 1rem; border-top: 3px solid #ea580c;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
              <strong style="color: #fff; font-size: 0.95rem;">Errichto</strong>
              <span style="font-size: 0.7rem; color: #fb923c; background: rgba(234,88,12,0.15); padding: 0.1rem 0.4rem; border-radius: 4px;">CP &amp; Bit Tricks</span>
            </div>
            <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.4; margin-bottom: 0.75rem;">
              Competitive programming master. Bitwise tricks, bitmask DP, fast modulo math, lazy propagation.
            </p>
            <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
              <a href="https://www.youtube.com/playlist?list=PLl0KD3g-oDOHpWRyyGBUJ9jmul0lUODS5" target="_blank" class="btn btn-outline" style="font-size: 0.72rem; padding: 0.2rem 0.5rem; color: #fb923c; border-color: rgba(234,88,12,0.4);">▶ DP &amp; Bitwise ↗</a>
              <a href="https://www.youtube.com/@Errichto" target="_blank" class="btn btn-outline" style="font-size: 0.72rem; padding: 0.2rem 0.5rem;">📺 Channel ↗</a>
            </div>
          </div>

          <!-- Martin Thompson / CppCon -->
          <div style="background: rgba(7, 10, 14, 0.7); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 1rem; border-top: 3px solid #0d9488;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
              <strong style="color: #fff; font-size: 0.95rem;">CppCon &amp; Martin Thompson</strong>
              <span style="font-size: 0.7rem; color: #2dd4bf; background: rgba(13,148,136,0.15); padding: 0.1rem 0.4rem; border-radius: 4px;">Lock-Free</span>
            </div>
            <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.4; margin-bottom: 0.75rem;">
              Mechanical sympathy, hardware cache lines, lock-free SPSC ring buffers, cache false sharing.
            </p>
            <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
              <a href="https://www.youtube.com/@CppCon" target="_blank" class="btn btn-outline" style="font-size: 0.72rem; padding: 0.2rem 0.5rem; color: #2dd4bf; border-color: rgba(13,148,136,0.4);">▶ Concurrency ↗</a>
              <a href="https://www.youtube.com/@CppCon" target="_blank" class="btn btn-outline" style="font-size: 0.72rem; padding: 0.2rem 0.5rem;">📺 Channel ↗</a>
            </div>
          </div>

          <!-- CMU DB -->
          <div style="background: rgba(7, 10, 14, 0.7); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 1rem; border-top: 3px solid #4f46e5;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
              <strong style="color: #fff; font-size: 0.95rem;">CMU Database Group</strong>
              <span style="font-size: 0.7rem; color: #818cf8; background: rgba(79,70,229,0.15); padding: 0.1rem 0.4rem; border-radius: 4px;">Paging &amp; Buffers</span>
            </div>
            <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.4; margin-bottom: 0.75rem;">
              Prof. Andy Pavlo. Buffer pool management (LRU-K, ARC), in-memory indexing, KV-cache paging architecture.
            </p>
            <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
              <a href="https://www.youtube.com/@CMUDatabaseGroup" target="_blank" class="btn btn-outline" style="font-size: 0.72rem; padding: 0.2rem 0.5rem; color: #818cf8; border-color: rgba(79,70,229,0.4);">▶ CMU 15-445 ↗</a>
              <a href="https://www.youtube.com/@CMUDatabaseGroup" target="_blank" class="btn btn-outline" style="font-size: 0.72rem; padding: 0.2rem 0.5rem;">📺 Channel ↗</a>
            </div>
          </div>
        </div>
      </div>

      <div class="search-filter-bar">
        <input type="text" class="search-input" id="resource-search" placeholder="Search 35 tutorials by topic, concept, or creator...">
        <div style="display: flex; gap: 0.4rem; align-items: center; flex-wrap: wrap;">
          <span style="font-size: 0.8rem; color: var(--text-muted);">Creator Filter:</span>
          <button class="btn btn-outline btn-resource-filter" data-filter="" style="padding: 0.2rem 0.5rem; font-size: 0.75rem;">All</button>
          <button class="btn btn-outline btn-resource-filter" data-filter="striver" style="padding: 0.2rem 0.5rem; font-size: 0.75rem; border-color: rgba(245,158,11,0.5); color: #fbbf24;">Striver</button>
          <button class="btn btn-outline btn-resource-filter" data-filter="aditya" style="padding: 0.2rem 0.5rem; font-size: 0.75rem; border-color: rgba(118,185,0,0.5); color: var(--nv-green);">Aditya Verma</button>
          <button class="btn btn-outline btn-resource-filter" data-filter="babbar" style="padding: 0.2rem 0.5rem; font-size: 0.75rem; border-color: rgba(56,189,248,0.5); color: #38bdf8;">Love Babbar</button>
          <button class="btn btn-outline btn-resource-filter" data-filter="pratyush" style="padding: 0.2rem 0.5rem; font-size: 0.75rem; border-color: rgba(168,85,247,0.5); color: #c084fc;">Padho with Pratyush</button>
          <button class="btn btn-outline btn-resource-filter" data-filter="neetcode" style="padding: 0.2rem 0.5rem; font-size: 0.75rem; border-color: rgba(16,185,129,0.5); color: #34d399;">NeetCode</button>
        </div>
        <span style="font-size: 0.85rem; color: var(--text-secondary); margin-left: auto;">Total 35 Tutorials</span>
      </div>
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th style="width: 70px;">Day</th>
              <th style="width: 220px;">Topic & Curriculum Focus</th>
              <th style="width: 80px;">Duration</th>
              <th>Why It Matters</th>
              <th>What to Extract</th>
              <th style="width: 260px;">Watch on YouTube (Direct Creator Links)</th>
            </tr>
          </thead>
          <tbody id="tbody-resources">
            {''.join(rows_html)}
          </tbody>
        </table>
      </div>
    """
    return page_shell("Curated Resource Center", "resources.html", content)

def generate_rules_html(data):
    sections_html = []
    for sec in data["readme"]:
        sections_html.append(f"""
          <div class="card" style="margin-bottom: 1.25rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; border-bottom: 1px solid var(--border-subtle); padding-bottom: 0.5rem;">
              <h3 style="font-size: 1.1rem; font-weight: 700; color: #fff;">{escape(sec['title'])}</h3>
            </div>
            <div style="font-size: 0.88rem; color: var(--text-secondary); line-height: 1.6; white-space: pre-line;">
              {escape(sec['body'])}
            </div>
          </div>
        """)

    content = f"""
      <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.4rem; font-weight: 800; color: #fff; margin-bottom: 0.25rem;">Program Operating Rules & System Protocols</h2>
        <p style="color: var(--text-secondary); font-size: 0.9rem;">
          Non-negotiable training guidelines, the Stuck Protocol, Failure categorization, and NVIDIA systems hiring standards.
        </p>
      </div>
      <div id="rules-container">
        {''.join(sections_html)}
      </div>
    """
    return page_shell("System Rules & Protocols", "rules.html", content)

def build_all():
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    pages = {
        "index.html": generate_index_html(data),
        "plan.html": generate_plan_html(data),
        "patterns.html": generate_patterns_html(data),
        "flashcards.html": generate_flashcards_html(data),
        "nvidia.html": generate_nvidia_html(data),
        "failures.html": generate_failures_html(data),
        "mocks.html": generate_mocks_html(data),
        "resources.html": generate_resources_html(data),
        "rules.html": generate_rules_html(data),
    }

    for filename, html_content in pages.items():
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"[OK] Generated {filename} ({len(html_content)} bytes)")

    print("[SUCCESS] All 9 static HTML pages generated with pre-rendered data and zero server dependency.")

if __name__ == "__main__":
    build_all()
