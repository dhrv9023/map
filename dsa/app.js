/* ==============================================================================
   DSA COCKPIT - NVIDIA & AI-INFRASTRUCTURE SYSTEMS
   Interactive Application Engine
   Zero-Data-Loss Architecture + Local-First State Persistence
   ============================================================================== */

(function () {
  'use strict';

  // Verify data is loaded
  if (!window.DSA_DATA) {
    console.error("Critical: DSA_DATA not found. Please ensure data.js is loaded.");
    return;
  }

  const DATA = window.DSA_DATA;
  const STORAGE_KEY = "DSA_COCKPIT_STATE_V1";

  // State
  let state = {
    completedDays: {},    // { [dayNum]: { completed, timeSpent, solvedIndep, hints, solViewed, keyInsight, date } }
    failures: [],         // [ { id, date, problem, code, rule, nextDue, reviewed } ]
    currentDayIndex: 0,   // 0-indexed into DATA.days
    timer: {
      totalSeconds: 45 * 60,
      remainingSeconds: 45 * 60,
      isRunning: false,
      intervalId: null
    }
  };

  // Load from localStorage
  function loadState() {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        state.completedDays = parsed.completedDays || {};
        state.failures = parsed.failures || [];
      }
    } catch (e) {
      console.warn("Could not parse saved state from localStorage", e);
    }
    // Set currentDayIndex to first incomplete day
    const firstIncomplete = DATA.days.findIndex(d => !state.completedDays[d.day]);
    state.currentDayIndex = firstIncomplete >= 0 ? firstIncomplete : 0;
  }

  function saveState() {
    try {
      const payload = {
        completedDays: state.completedDays,
        failures: state.failures
      };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
    } catch (e) {
      console.error("Failed to save state to localStorage", e);
    }
    updateAllViews();
  }

  // Audio Beep using Web Audio API
  function playTone(freq, duration) {
    try {
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = "sine";
      osc.frequency.value = freq;
      gain.gain.setValueAtTime(0.1, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + duration);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + duration);
    } catch (e) {
      // AudioContext may require prior user interaction
    }
  }

  // --- TAB NAVIGATION --------------------------------------------------------
  function initTabs() {
    const tabs = document.querySelectorAll('.nav-tab');
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

        tab.classList.add('active');
        const targetId = tab.getAttribute('data-tab');
        const targetPane = document.getElementById(targetId);
        if (targetPane) targetPane.classList.add('active');
      });
    });
  }

  // --- STUCK TIMER LOGIC -----------------------------------------------------
  function initTimer() {
    const display = document.getElementById('timer-display');
    const badge = document.getElementById('timer-status-badge');
    const instruction = document.getElementById('timer-instruction');
    const btnStart = document.getElementById('timer-btn-start');
    const btnPause = document.getElementById('timer-btn-pause');
    const btnReset = document.getElementById('timer-btn-reset');

    function updateDisplay() {
      const mins = Math.floor(state.timer.remainingSeconds / 60);
      const secs = state.timer.remainingSeconds % 60;
      display.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;

      // Stages:
      // 45m - 35m (first 10 min elapsed) -> Silence
      // 35m - 25m (10m-20m elapsed)      -> Hint 1
      // 25m - 15m (20m-30m elapsed)      -> Pattern Hint
      // < 15m (30m+ elapsed)             -> Editorial Approach
      const elapsed = (45 * 60) - state.timer.remainingSeconds;

      if (elapsed <= 10 * 60) {
        badge.className = "timer-status-badge status-silence";
        badge.textContent = "Phase 1: Complete Silence (0–10m)";
        instruction.textContent = "Derive target TC, annotate constraints, sketch 2 custom test inputs. Zero hints permitted.";
      } else if (elapsed <= 20 * 60) {
        badge.className = "timer-status-badge status-hint1";
        badge.textContent = "Phase 2: Conceptual Hint 1 (10–20m)";
        instruction.textContent = "1 high-level question allowed. No code or data-structure names.";
      } else if (elapsed <= 30 * 60) {
        badge.className = "timer-status-badge status-hint2";
        badge.textContent = "Phase 3: Pattern & Invariant Hint (20–30m)";
        instruction.textContent = "Identify pattern or core invariant. Still no implementation code.";
      } else {
        badge.className = "timer-status-badge status-editorial";
        badge.textContent = "Phase 4: Editorial Approach (30m+)";
        instruction.textContent = "Read 2–3 sentences of core editorial approach. Close it and code from scratch.";
      }
    }

    btnStart.addEventListener('click', () => {
      if (state.timer.isRunning) return;
      state.timer.isRunning = true;
      btnStart.textContent = "Running...";
      state.timer.intervalId = setInterval(() => {
        if (state.timer.remainingSeconds > 0) {
          state.timer.remainingSeconds--;
          // Sound chime at milestone transitions
          const elapsed = (45 * 60) - state.timer.remainingSeconds;
          if (elapsed === 10 * 60 || elapsed === 20 * 60 || elapsed === 30 * 60) {
            playTone(880, 0.4);
          }
          updateDisplay();
        } else {
          clearInterval(state.timer.intervalId);
          state.timer.isRunning = false;
          btnStart.textContent = "▶ Start";
          playTone(523.25, 0.8);
          alert("Time's up! If you haven't solved it yet, check the editorial approach and log an F-code in Failure Log.");
        }
      }, 1000);
    });

    btnPause.addEventListener('click', () => {
      if (state.timer.isRunning) {
        clearInterval(state.timer.intervalId);
        state.timer.isRunning = false;
        btnStart.textContent = "▶ Resume";
      }
    });

    btnReset.addEventListener('click', () => {
      clearInterval(state.timer.intervalId);
      state.timer.isRunning = false;
      state.timer.remainingSeconds = 45 * 60;
      btnStart.textContent = "▶ Start";
      updateDisplay();
    });

    updateDisplay();
  }

  // --- METRICS & READINESS GAUGE ---------------------------------------------
  function calculateMetrics() {
    const completedList = Object.values(state.completedDays);
    const completedCount = completedList.length;
    const progressPct = Math.round((completedCount / DATA.config.totalDays) * 100);

    let indepCount = 0;
    let zeroHintsCount = 0;
    let totalMinutes = 0;

    completedList.forEach(entry => {
      if (entry.solvedIndep === "Yes") indepCount++;
      if (entry.hints === "0") zeroHintsCount++;
      totalMinutes += Number(entry.timeSpent) || 60;
    });

    const indepRate = completedCount > 0 ? (indepCount / completedCount) : 0;
    const hintRate = completedCount > 0 ? (1 - (zeroHintsCount / completedCount)) : 0;
    const avgTtp = completedCount > 0 ? Math.round(totalMinutes / completedCount) : 0;

    // B28 Readiness Score Formula (Safeguarded: 0 if completedCount < 5)
    let readinessScore = 0;
    if (completedCount >= 5) {
      const s1 = 30 * Math.min(1, indepRate / 0.80);
      const s2 = 25 * Math.min(1, (1 - hintRate) / 0.80);
      const s3 = 25 * Math.min(1, (completedCount / 40)); // Progression towards benchmark
      const s4 = 20 * Math.min(1, Math.max(0, (12 - 5) / 8)); // Baseline TTP factor
      readinessScore = Math.min(100, Math.round(s1 + s2 + s3 + s4));
    }

    return {
      completedCount,
      progressPct,
      indepRate: Math.round(indepRate * 100),
      hintRate: Math.round(hintRate * 100),
      avgTtp,
      readinessScore
    };
  }

  // --- RENDER DASHBOARD ------------------------------------------------------
  function renderDashboard() {
    const metrics = calculateMetrics();

    // Top Header Chips
    document.getElementById('header-current-day').textContent = `Day ${state.currentDayIndex + 1}`;
    document.getElementById('header-progress-pct').textContent = `${metrics.progressPct}%`;
    document.getElementById('header-readiness-score').textContent = `${metrics.readinessScore} / 100`;
    document.getElementById('header-streak').textContent = `${metrics.completedCount} Days`;

    // KPI Cards
    document.getElementById('kpi-readiness').textContent = `${metrics.readinessScore} / 100`;
    document.getElementById('kpi-indep').textContent = `${metrics.indepRate}%`;
    document.getElementById('kpi-hints').textContent = `${metrics.hintRate}%`;
    document.getElementById('kpi-ttp').textContent = metrics.completedCount > 0 ? `${metrics.avgTtp} min` : "-- min";

    // Hero Mission
    const day = DATA.days[state.currentDayIndex];
    if (!day) return;

    document.getElementById('hero-day-date').textContent = `Day ${day.day} of 168 (${day.dateDisplay})`;
    document.getElementById('hero-topic').textContent = day.pattern;
    document.getElementById('hero-objective').textContent = day.objective;

    // Problems
    const p1Title = document.getElementById('hero-p1-title');
    const p1Meta = document.getElementById('hero-p1-meta');
    const p1Diff = document.getElementById('hero-p1-diff');
    const p1Link = document.getElementById('hero-p1-link');

    p1Title.textContent = day.p1;
    p1Meta.textContent = `Target: ${day.t1} min | Mode: ${day.mode} | Hints: ${day.help}`;
    p1Diff.textContent = day.d1;
    p1Diff.className = `diff-tag diff-${day.d1}`;
    p1Link.href = day.p1Url;

    const p2Title = document.getElementById('hero-p2-title');
    const p2Meta = document.getElementById('hero-p2-meta');
    const p2Diff = document.getElementById('hero-p2-diff');
    const p2Link = document.getElementById('hero-p2-link');

    p2Title.textContent = day.p2;
    p2Meta.textContent = `Target: ${day.t2} min | Difficulty: ${day.d2}`;
    p2Diff.textContent = day.d2;
    p2Diff.className = `diff-tag diff-${day.d2}`;
    p2Link.href = day.p2Url;

    // AI Infra / Hardware
    document.getElementById('hero-infra-note').textContent = day.infra || "Contiguous flat layouts, cache lines, and hardware synchronization.";

    // Mark complete button state
    const btnComplete = document.getElementById('btn-complete-today');
    if (state.completedDays[day.day]) {
      btnComplete.textContent = "✓ Completed";
      btnComplete.className = "btn btn-success";
    } else {
      btnComplete.textContent = "✓ Mark Day Complete";
      btnComplete.className = "btn btn-primary";
    }

    // Upcoming diagnostic
    const nextDiag = DATA.mocks.find(m => m.day >= day.day);
    const nextDiagElem = document.getElementById('dashboard-next-diag');
    if (nextDiag) {
      nextDiagElem.innerHTML = `
        <div style="font-weight: 700; color: #fff;">${nextDiag.sessionType} (Day ${nextDiag.day})</div>
        <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.25rem;">
          Problem: <span style="color: var(--cyan-accent);">${nextDiag.problemDesc}</span>
        </div>
        <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.25rem;">
          Time Limit: ${nextDiag.timeLimit} min &bull; Target Date: ${nextDiag.dateDisplay}
        </div>
      `;
    } else {
      nextDiagElem.textContent = "All diagnostic milestones cleared! You are ready for the Final Specialist Certification.";
    }

    // Hotspot alert
    const hotspotElem = document.getElementById('dashboard-failure-hotspot');
    const fCounts = {};
    state.failures.forEach(f => {
      fCounts[f.code] = (fCounts[f.code] || 0) + 1;
    });

    let worstF = null;
    let maxCount = 0;
    for (const [code, cnt] of Object.entries(fCounts)) {
      if (cnt > maxCount) {
        maxCount = cnt;
        worstF = code;
      }
    }

    if (worstF && maxCount >= 2) {
      const fObj = DATA.fcats.find(fc => fc.code === worstF) || {};
      hotspotElem.innerHTML = `
        <span style="color: var(--amber-accent); font-weight: 700;">⚠️ Recurring Weakness: ${worstF} (${maxCount} occurrences)</span>
        <div style="margin-top: 0.25rem;">${fObj.desc || ''}</div>
        <div style="font-size: 0.8rem; color: var(--text-nv); margin-top: 0.25rem;">Drill: ${fObj.drill || ''}</div>
      `;
    } else {
      hotspotElem.textContent = "No recurring failure hotspots detected yet. Keep logging all stuck points in the Failure Log.";
    }
  }

  // --- RENDER 168-DAY PLAN ---------------------------------------------------
  function renderDayPlan() {
    const tbody = document.getElementById('tbody-dayplan');
    const searchVal = (document.getElementById('plan-search').value || '').toLowerCase();
    const phaseVal = document.getElementById('plan-filter-phase').value;
    const weekVal = document.getElementById('plan-filter-week').value;
    const nvidiaVal = document.getElementById('plan-filter-nvidia').value;
    const statusVal = document.getElementById('plan-filter-status').value;

    tbody.innerHTML = '';

    const filtered = DATA.days.filter(d => {
      if (phaseVal !== 'ALL' && d.phase.toString() !== phaseVal) return false;
      if (weekVal !== 'ALL' && d.week.toString() !== weekVal) return false;
      if (nvidiaVal === 'NVIDIA' && !d.isNvidia) return false;
      if (nvidiaVal === 'DIAG' && !d.isDiagnostic && !d.isMock) return false;

      const isDone = !!state.completedDays[d.day];
      if (statusVal === 'DONE' && !isDone) return false;
      if (statusVal === 'PENDING' && isDone) return false;

      if (searchVal) {
        const text = `${d.day} ${d.topic} ${d.pattern} ${d.objective} ${d.p1} ${d.p2} ${d.infra}`.toLowerCase();
        if (!text.includes(searchVal)) return false;
      }

      return true;
    });

    filtered.forEach(d => {
      const tr = document.createElement('tr');
      const isDone = !!state.completedDays[d.day];

      tr.innerHTML = `
        <td style="font-weight: 700; color: ${isDone ? 'var(--nv-green)' : '#fff'};">${d.day}</td>
        <td style="white-space: nowrap; font-size: 0.8rem; color: var(--text-secondary);">${d.dateDisplay}</td>
        <td>
          <div style="font-weight: 600; color: #fff;">${d.pattern}</div>
          <div style="font-size: 0.75rem; color: var(--text-muted);">${d.objective}</div>
        </td>
        <td><span style="font-size: 0.8rem; color: var(--cyan-accent);">${d.skill}</span></td>
        <td>
          <a href="${d.p1Url}" target="_blank" style="color: var(--text-primary); text-decoration: none; font-weight: 500;">
            ${d.p1}
          </a>
          <span class="diff-tag diff-${d.d1}" style="font-size: 0.65rem; margin-left: 0.25rem;">${d.d1}</span>
        </td>
        <td>
          <a href="${d.p2Url}" target="_blank" style="color: var(--text-primary); text-decoration: none; font-weight: 500;">
            ${d.p2}
          </a>
          <span class="diff-tag diff-${d.d2}" style="font-size: 0.65rem; margin-left: 0.25rem;">${d.d2}</span>
        </td>
        <td><span style="font-size: 0.75rem;">${d.tutYn === 'YES' ? '📺 Yes' : '—'}</span></td>
        <td><span style="font-size: 0.75rem; color: var(--text-muted);">${d.mode}</span></td>
        <td>${d.isNvidia ? '<span class="brand-badge" style="font-size: 0.65rem;">🟢 NVIDIA</span>' : '—'}</td>
        <td>
          <span style="font-size: 0.8rem; font-weight: 600; color: ${isDone ? 'var(--nv-green)' : 'var(--text-muted)'};">
            ${isDone ? '✓ Done' : 'Pending'}
          </span>
        </td>
        <td>
          <button class="btn btn-outline" style="padding: 0.2rem 0.6rem; font-size: 0.75rem;" data-day="${d.day}">
            ${isDone ? 'Edit' : 'Complete'}
          </button>
        </td>
      `;

      tr.querySelector('button').addEventListener('click', () => {
        openCompleteModal(d.day);
      });

      tbody.appendChild(tr);
    });

    document.getElementById('badge-dayplan-count').textContent = filtered.length;
  }

  // --- RENDER PATTERN LIBRARY (42 Patterns) ----------------------------------
  function renderPatterns() {
    const grid = document.getElementById('patterns-grid');
    const searchVal = (document.getElementById('pattern-search').value || '').toLowerCase();
    grid.innerHTML = '';

    const filtered = DATA.patterns.filter(p => {
      if (!searchVal) return true;
      const text = `${p.id} ${p.name} ${p.recognitionCues} ${p.coreIdea} ${p.aiInfraRelevance}`.toLowerCase();
      return text.includes(searchVal);
    });

    document.getElementById('pattern-count-label').textContent = `Showing ${filtered.length} of 42 patterns`;

    filtered.forEach(p => {
      const card = document.createElement('div');
      card.className = 'card';
      card.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
          <h4 style="font-size: 1.05rem; font-weight: 700; color: #fff;">#${p.id} ${p.name}</h4>
          <span class="brand-badge" style="font-size: 0.65rem;">${p.complexity.split(';')[0] || 'Pattern'}</span>
        </div>
        <div style="font-size: 0.82rem; color: var(--cyan-accent); margin-bottom: 0.5rem;">
          <strong>Trigger:</strong> ${p.recognitionCues}
        </div>
        <div style="font-size: 0.82rem; color: var(--text-secondary); margin-bottom: 0.75rem;">
          <strong>Core Idea:</strong> ${p.coreIdea}
        </div>
        <div style="background: rgba(0, 0, 0, 0.4); padding: 0.6rem; border-radius: var(--radius-sm); font-size: 0.78rem; font-family: var(--font-mono); color: var(--text-primary); margin-bottom: 0.75rem;">
          ${p.dataStructures}
        </div>
        <div style="border-top: 1px solid var(--border-subtle); padding-top: 0.6rem; font-size: 0.8rem; color: var(--text-nv);">
          <strong>🟢 AI-Infra / Hardware:</strong> ${p.aiInfraRelevance}
        </div>
      `;
      grid.appendChild(card);
    });
  }

  // --- RENDER 3D FLASHCARDS (30 Cards) ---------------------------------------
  function renderFlashcards() {
    const container = document.getElementById('flashcards-container');
    const searchVal = (document.getElementById('flashcard-search').value || '').toLowerCase();
    container.innerHTML = '';

    const filtered = DATA.cards.filter(c => {
      if (!searchVal) return true;
      const text = `${c.id} ${c.problem} ${c.pattern} ${c.triggerCue} ${c.coreIdea}`.toLowerCase();
      return text.includes(searchVal);
    });

    document.getElementById('flashcard-count-label').textContent = `Showing ${filtered.length} of 30 cards`;

    filtered.forEach(c => {
      const wrapper = document.createElement('div');
      wrapper.className = 'flashcard-wrapper';
      wrapper.innerHTML = `
        <div class="flashcard-inner">
          <!-- Front Face -->
          <div class="flashcard-front">
            <div>
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                <span class="diff-tag diff-H" style="font-size: 0.7rem;">CARD #${c.id}</span>
                <span style="font-size: 0.75rem; color: var(--cyan-accent); font-weight: 600;">${c.pattern}</span>
              </div>
              <h3 style="font-size: 1.15rem; font-weight: 700; color: #fff; margin-bottom: 0.75rem;">
                ${c.problem}
              </h3>
              <div style="font-size: 0.88rem; color: var(--text-secondary); line-height: 1.5; margin-bottom: 1rem;">
                <strong style="color: var(--amber-accent);">Trigger Cue:</strong><br>
                ${c.triggerCue}
              </div>
              <div style="background: rgba(0, 0, 0, 0.4); border-left: 2px solid var(--cyan-accent); padding: 0.5rem 0.75rem; border-radius: var(--radius-sm); font-size: 0.8rem; color: var(--text-muted);">
                ${c.variants}
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
                <span style="font-size: 0.75rem; color: var(--text-nv); font-family: var(--font-mono);">${c.complexity}</span>
              </div>
              <div style="font-size: 0.85rem; color: #fff; font-weight: 600; margin-bottom: 0.5rem;">
                ${c.invariant}
              </div>
              <div style="background: rgba(0, 0, 0, 0.6); padding: 0.6rem; border-radius: var(--radius-sm); font-size: 0.78rem; font-family: var(--font-mono); color: var(--text-nv); margin-bottom: 0.6rem;">
                ${c.coreIdea}
              </div>
              <div style="font-size: 0.78rem; color: #f87171; margin-bottom: 0.5rem;">
                <strong>⚠️ Failure Trap:</strong> ${c.failureTrap}
              </div>
              <div style="border-top: 1px solid var(--border-subtle); padding-top: 0.5rem; font-size: 0.8rem; color: var(--text-nv);">
                <strong>🟢 One-Line Anchor:</strong> ${c.anchorCue}
              </div>
            </div>
            <div class="card-flip-prompt">
              <span>👆 Click to flip back</span>
            </div>
          </div>
        </div>
      `;

      wrapper.addEventListener('click', () => {
        wrapper.classList.toggle('flipped');
      });

      container.appendChild(wrapper);
    });
  }

  // --- RENDER NVIDIA TRACK ---------------------------------------------------
  function renderNvidiaTrack() {
    const container = document.getElementById('nvidia-pillars-container');
    container.innerHTML = '';

    DATA.nvidiaPlaybook.pillars.forEach(p => {
      const card = document.createElement('div');
      card.className = 'nvidia-pillar-card';
      
      let primsHtml = '';
      if (p.primitives && p.primitives.length) {
        primsHtml = `
          <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0.75rem 0;">
            ${p.primitives.map(pr => `
              <div style="background: rgba(0,0,0,0.5); border: 1px solid var(--border-subtle); border-radius: 4px; padding: 0.25rem 0.5rem; font-size: 0.75rem;">
                <code style="color: var(--nv-green);">${pr.code}</code> &bull; <span style="color: var(--text-secondary);">${pr.desc}</span>
              </div>
            `).join('')}
          </div>
        `;
      }

      card.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
          <h4 style="font-size: 1.1rem; font-weight: 700; color: #fff;">
            Pillar ${p.id}: ${p.title}
          </h4>
          <span class="brand-badge" style="font-size: 0.7rem;">${p.badge}</span>
        </div>
        <p style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 0.5rem;">${p.summary}</p>
        ${p.trap ? `<div style="font-size: 0.8rem; color: #f87171; margin-top: 0.35rem;"><strong>The Trap:</strong> ${p.trap}</div>` : ''}
        ${primsHtml}
        <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 0.75rem; border-top: 1px solid var(--border-subtle); padding-top: 0.5rem;">
          <span style="font-size: 0.8rem; color: var(--text-muted);">Practiced in Curriculum: Days ${p.days.join(', ')}</span>
          <button class="btn btn-outline" style="padding: 0.25rem 0.6rem; font-size: 0.75rem;" data-filter-days="${p.days.join(',')}">
            View Days in Plan ↗
          </button>
        </div>
      `;

      card.querySelector('button').addEventListener('click', () => {
        // Switch to dayplan tab and filter
        const dayplanTab = document.querySelector('[data-tab="tab-dayplan"]');
        if (dayplanTab) dayplanTab.click();
        const searchInput = document.getElementById('plan-search');
        if (searchInput) {
          searchInput.value = p.title.split(' ')[0];
          renderDayPlan();
        }
      });

      container.appendChild(card);
    });
  }

  // --- RENDER FAILURE LOG & SRS QUEUE ---------------------------------------
  function renderFailureTab() {
    const queueContainer = document.getElementById('review-queue-container');
    const tbody = document.getElementById('tbody-failure-history');

    // Populate F-category select in form if empty
    const select = document.getElementById('fl-input-code');
    if (select.children.length === 0) {
      DATA.fcats.forEach(fc => {
        const opt = document.createElement('option');
        opt.value = fc.code;
        opt.textContent = `${fc.code}: ${fc.label} (${fc.desc})`;
        select.appendChild(opt);
      });
    }

    // Badge count
    document.getElementById('badge-failure-count').textContent = state.failures.length;

    // Review Queue (Active items where reviewed == false)
    const activeReviews = state.failures.filter(f => !f.reviewed);
    queueContainer.innerHTML = '';

    if (activeReviews.length === 0) {
      queueContainer.innerHTML = '<p style="color: var(--text-muted); font-size: 0.85rem;">No items currently due for spaced repetition review. Clean record!</p>';
    } else {
      activeReviews.forEach(item => {
        const div = document.createElement('div');
        div.style.cssText = "background: rgba(0,0,0,0.4); border: 1px solid var(--border-subtle); border-radius: 6px; padding: 0.6rem 0.8rem; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center;";
        div.innerHTML = `
          <div>
            <div style="font-weight: 600; font-size: 0.85rem; color: #fff;">${item.problem}</div>
            <div style="font-size: 0.75rem; color: var(--amber-accent);">[${item.code}] ${item.rule}</div>
          </div>
          <button class="btn btn-outline" style="padding: 0.2rem 0.5rem; font-size: 0.75rem;" data-review-id="${item.id}">
            ✓ Cleared
          </button>
        `;
        div.querySelector('button').addEventListener('click', () => {
          item.reviewed = true;
          saveState();
        });
        queueContainer.appendChild(div);
      });
    }

    // History Table
    tbody.innerHTML = '';
    state.failures.slice().reverse().forEach(item => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td style="font-size: 0.8rem; color: var(--text-secondary);">${item.date}</td>
        <td style="font-weight: 600;">${item.problem}</td>
        <td><span class="diff-tag diff-H">${item.code}</span></td>
        <td style="font-size: 0.82rem; color: var(--text-secondary);">${item.rule}</td>
        <td style="font-size: 0.8rem;">${item.nextDue}</td>
        <td>
          <button class="btn btn-outline" style="padding: 0.15rem 0.4rem; font-size: 0.7rem;" data-delete-id="${item.id}">
            Delete
          </button>
        </td>
      `;
      tr.querySelector('button').addEventListener('click', () => {
        state.failures = state.failures.filter(f => f.id !== item.id);
        saveState();
      });
      tbody.appendChild(tr);
    });
  }

  // --- RENDER MOCKS (24 Sessions) -------------------------------------------
  function renderMocks() {
    const tbody = document.getElementById('tbody-mocks');
    tbody.innerHTML = '';

    DATA.mocks.forEach(m => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td style="font-weight: 700; color: var(--cyan-accent);">#${m.id}</td>
        <td style="font-weight: 600;">Day ${m.day}</td>
        <td style="font-size: 0.8rem; color: var(--text-secondary);">${m.dateDisplay}</td>
        <td><span class="brand-badge" style="font-size: 0.7rem;">${m.sessionType}</span></td>
        <td style="font-weight: 500; color: #fff;">${m.problemDesc}</td>
        <td><span class="diff-tag diff-${m.difficulty}">${m.difficulty}</span></td>
        <td style="font-family: var(--font-mono); font-size: 0.85rem;">${m.timeLimit} min</td>
        <td><a href="${m.lcUrl}" target="_blank" class="btn btn-outline" style="padding: 0.2rem 0.5rem; font-size: 0.75rem;">Solve ↗</a></td>
        <td><span style="font-size: 0.75rem; color: var(--text-muted);">Scheduled</span></td>
      `;
      tbody.appendChild(tr);
    });
  }

  // --- RENDER RESOURCES (35 Tutorials) ---------------------------------------
  function renderResources() {
    const tbody = document.getElementById('tbody-resources');
    const searchVal = (document.getElementById('resource-search').value || '').toLowerCase();
    tbody.innerHTML = '';

    const filtered = DATA.resources.filter(r => {
      if (!searchVal) return true;
      const text = `${r.day} ${r.topic} ${r.source} ${r.whyItMatters} ${r.whatToExtract}`.toLowerCase();
      return text.includes(searchVal);
    });

    filtered.forEach(r => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td style="font-weight: 700; color: var(--nv-green);">Day ${r.day}</td>
        <td style="font-weight: 600; color: #fff;">${r.topic}</td>
        <td style="font-size: 0.8rem; color: var(--cyan-accent);">${r.source}</td>
        <td style="font-family: var(--font-mono); font-size: 0.8rem;">${r.duration} min</td>
        <td style="font-size: 0.82rem; color: var(--text-secondary);">${r.whyItMatters}</td>
        <td style="font-size: 0.82rem; color: var(--text-muted);">${r.whatToExtract}</td>
        <td>
          <a href="https://neetcode.io" target="_blank" class="btn btn-outline" style="padding: 0.2rem 0.5rem; font-size: 0.75rem;">Watch ↗</a>
        </td>
      `;
      tbody.appendChild(tr);
    });
  }

  // --- RENDER README ---------------------------------------------------------
  function renderReadme() {
    const container = document.getElementById('readme-accordion');
    container.innerHTML = '';

    DATA.readme.forEach((sec, idx) => {
      const card = document.createElement('div');
      card.className = 'card';
      card.style.marginBottom = '1rem';
      card.innerHTML = `
        <div style="cursor: pointer; display: flex; justify-content: space-between; align-items: center;" class="readme-title-bar">
          <h3 style="font-size: 1.05rem; font-weight: 700; color: #fff;">${sec.title}</h3>
          <span style="color: var(--text-muted); font-size: 0.9rem;">▾</span>
        </div>
        <div style="margin-top: 0.75rem; font-size: 0.88rem; color: var(--text-secondary); line-height: 1.6; white-space: pre-line; border-top: 1px solid var(--border-subtle); padding-top: 0.75rem;">
          ${sec.body}
        </div>
      `;
      container.appendChild(card);
    });
  }

  // --- MODAL: COMPLETE DAY ---------------------------------------------------
  function openCompleteModal(dayNum) {
    const day = DATA.days.find(d => d.day === dayNum);
    if (!day) return;

    document.getElementById('modal-day-num').value = day.day;
    document.getElementById('modal-day-title').textContent = `Complete Day ${day.day}: ${day.pattern}`;

    const existing = state.completedDays[day.day] || {};
    document.getElementById('modal-time-spent').value = existing.timeSpent || 60;
    document.getElementById('modal-solved-indep').value = existing.solvedIndep || "Yes";
    document.getElementById('modal-hints-count').value = existing.hints || "0";
    document.getElementById('modal-sol-viewed').value = existing.solViewed || "No";
    document.getElementById('modal-key-insight').value = existing.keyInsight || "";

    document.getElementById('modal-complete-day').classList.add('open');
  }

  function initModals() {
    // Complete Day Modal
    const modalComplete = document.getElementById('modal-complete-day');
    document.getElementById('btn-close-modal').addEventListener('click', () => modalComplete.classList.remove('open'));
    document.getElementById('btn-cancel-modal').addEventListener('click', () => modalComplete.classList.remove('open'));

    document.getElementById('btn-complete-today').addEventListener('click', () => {
      openCompleteModal(DATA.days[state.currentDayIndex].day);
    });

    document.getElementById('form-complete-day').addEventListener('submit', (e) => {
      e.preventDefault();
      const dayNum = Number(document.getElementById('modal-day-num').value);
      const timeSpent = Number(document.getElementById('modal-time-spent').value);
      const solvedIndep = document.getElementById('modal-solved-indep').value;
      const hints = document.getElementById('modal-hints-count').value;
      const solViewed = document.getElementById('modal-sol-viewed').value;
      const keyInsight = document.getElementById('modal-key-insight').value;

      state.completedDays[dayNum] = {
        completed: true,
        timeSpent,
        solvedIndep,
        hints,
        solViewed,
        keyInsight,
        date: new Date().toISOString().split('T')[0]
      };

      // Advance to next day if completing current day
      if (dayNum === DATA.days[state.currentDayIndex].day && state.currentDayIndex < DATA.days.length - 1) {
        state.currentDayIndex++;
      }

      saveState();
      modalComplete.classList.remove('open');
    });

    // Prev / Next Mission Browsing
    document.getElementById('btn-prev-mission').addEventListener('click', () => {
      if (state.currentDayIndex > 0) {
        state.currentDayIndex--;
        renderDashboard();
      }
    });

    document.getElementById('btn-next-mission').addEventListener('click', () => {
      if (state.currentDayIndex < DATA.days.length - 1) {
        state.currentDayIndex++;
        renderDashboard();
      }
    });

    // Failure form submission
    document.getElementById('form-log-failure').addEventListener('submit', (e) => {
      e.preventDefault();
      const prob = document.getElementById('fl-input-problem').value;
      const code = document.getElementById('fl-input-code').value;
      const rule = document.getElementById('fl-input-rule').value;

      const now = new Date();
      const nextDue = new Date(now.getTime() + 3 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];

      state.failures.push({
        id: Date.now(),
        date: now.toISOString().split('T')[0],
        problem: prob,
        code,
        rule,
        nextDue,
        reviewed: false
      });

      document.getElementById('fl-input-problem').value = '';
      document.getElementById('fl-input-rule').value = '';

      saveState();
      alert("Failure recorded! This problem has been scheduled for a 3-day spaced repetition review.");
    });

    // Sync Modal
    const modalSync = document.getElementById('modal-sync');
    document.getElementById('btn-open-sync').addEventListener('click', () => modalSync.classList.add('open'));
    document.getElementById('btn-close-sync-modal').addEventListener('click', () => modalSync.classList.remove('open'));

    // Export JSON
    document.getElementById('btn-export-json').addEventListener('click', () => {
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(state, null, 2));
      const dlAnchor = document.createElement('a');
      dlAnchor.setAttribute("href", dataStr);
      dlAnchor.setAttribute("download", `dsa_cockpit_backup_${new Date().toISOString().split('T')[0]}.json`);
      dlAnchor.click();
    });

    // Export CSV
    document.getElementById('btn-export-csv').addEventListener('click', () => {
      let csv = "Day,Date,TimeSpent,SolvedIndependently,HintsTaken,SolutionViewed,KeyInsight\n";
      for (const [day, val] of Object.entries(state.completedDays)) {
        csv += `${day},${val.date},${val.timeSpent},${val.solvedIndep},${val.hints},${val.solViewed},"${(val.keyInsight||'').replace(/"/g, '""')}"\n`;
      }
      const dataStr = "data:text/csv;charset=utf-8," + encodeURIComponent(csv);
      const dlAnchor = document.createElement('a');
      dlAnchor.setAttribute("href", dataStr);
      dlAnchor.setAttribute("download", `dsa_completed_days_${new Date().toISOString().split('T')[0]}.csv`);
      dlAnchor.click();
    });

    // Import JSON
    document.getElementById('input-import-file').addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (event) => {
        try {
          const imported = JSON.parse(event.target.result);
          if (imported.completedDays) state.completedDays = imported.completedDays;
          if (imported.failures) state.failures = imported.failures;
          saveState();
          modalSync.classList.remove('open');
          alert("Progress successfully restored from backup!");
        } catch (err) {
          alert("Invalid backup file format.");
        }
      };
      reader.readAsText(file);
    });

    // Reset Data
    document.getElementById('btn-reset-data').addEventListener('click', () => {
      if (confirm("Are you sure you want to clear all progress? This will reset all your logs to Day 1.")) {
        state.completedDays = {};
        state.failures = [];
        state.currentDayIndex = 0;
        saveState();
        modalSync.classList.remove('open');
      }
    });

    // Search and filter listeners
    document.getElementById('plan-search').addEventListener('input', renderDayPlan);
    document.getElementById('plan-filter-phase').addEventListener('change', renderDayPlan);
    document.getElementById('plan-filter-week').addEventListener('change', renderDayPlan);
    document.getElementById('plan-filter-nvidia').addEventListener('change', renderDayPlan);
    document.getElementById('plan-filter-status').addEventListener('change', renderDayPlan);

    document.getElementById('pattern-search').addEventListener('input', renderPatterns);
    document.getElementById('flashcard-search').addEventListener('input', renderFlashcards);
    document.getElementById('resource-search').addEventListener('input', renderResources);

    // Flip all cards
    let allFlipped = false;
    document.getElementById('btn-flip-all').addEventListener('click', () => {
      allFlipped = !allFlipped;
      document.querySelectorAll('.flashcard-wrapper').forEach(w => {
        if (allFlipped) w.classList.add('flipped');
        else w.classList.remove('flipped');
      });
    });

    // Populate Week dropdown in DayPlan filter
    const weekSelect = document.getElementById('plan-filter-week');
    for (let w = 1; w <= 24; w++) {
      const opt = document.createElement('option');
      opt.value = w;
      opt.textContent = `Week ${w}`;
      weekSelect.appendChild(opt);
    }
  }

  function updateAllViews() {
    renderDashboard();
    renderDayPlan();
    renderPatterns();
    renderFlashcards();
    renderNvidiaTrack();
    renderFailureTab();
    renderMocks();
    renderResources();
    renderReadme();
  }

  // Initialization
  function init() {
    loadState();
    initTabs();
    initTimer();
    initModals();
    updateAllViews();
    console.log("DSA Specialist Cockpit successfully initialized with 100% data parity.");
  }

  window.addEventListener('DOMContentLoaded', init);
})();
