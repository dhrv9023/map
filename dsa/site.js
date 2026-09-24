/* ==============================================================================
   DSA COCKPIT - NVIDIA & AI-INFRASTRUCTURE SYSTEMS
   Shared Static Multi-Page Client Engine (site.js)
   Works 100% Offline via file:// without any Python server
   ============================================================================== */

(function () {
  'use strict';

  const DATA = window.DSA_DATA || {};
  const STORAGE_KEY = "DSA_COCKPIT_STATE_V1";

  // Shared State
  let state = {
    completedDays: {},    // { [dayNum]: { completed, timeSpent, solvedIndep, hints, solViewed, keyInsight, date } }
    failures: [],         // [ { id, date, problem, code, rule, nextDue, reviewed } ]
    dayNotes: {},         // { [dayNum]: "personal notes..." }
    faangMastery: {},     // { [checkKey]: boolean }
    currentDayIndex: 0,
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
        state.dayNotes = parsed.dayNotes || {};
        state.faangMastery = parsed.faangMastery || {};
      }
    } catch (e) {
      console.warn("Could not load from localStorage:", e);
    }
    // Check if a specific day was requested from another page (e.g. Revision Vault)
    const pendingDay = localStorage.getItem('DSA_PENDING_DAY');
    if (pendingDay && DATA.days && DATA.days.length) {
      const pIdx = DATA.days.findIndex(d => d.day === Number(pendingDay));
      if (pIdx >= 0) {
        state.currentDayIndex = pIdx;
        localStorage.removeItem('DSA_PENDING_DAY');
        return;
      }
    }
    // Default to first uncompleted day
    if (DATA.days && DATA.days.length) {
      const firstIncomplete = DATA.days.findIndex(d => !state.completedDays[d.day]);
      state.currentDayIndex = firstIncomplete >= 0 ? firstIncomplete : 0;
    }
  }

  function saveState() {
    try {
      const payload = {
        completedDays: state.completedDays,
        failures: state.failures,
        dayNotes: state.dayNotes,
        faangMastery: state.faangMastery
      };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
    } catch (e) {
      console.error("Failed to save to localStorage:", e);
    }
    updateAllViews();
  }

  // Audio Beep via Web Audio API
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
      // Audio might require user interaction first
    }
  }

  // Calculate Metrics
  function calculateMetrics() {
    const completedList = Object.values(state.completedDays);
    const completedCount = completedList.length;
    const totalDays = (DATA.config && DATA.config.totalDays) || 168;
    const progressPct = Math.round((completedCount / totalDays) * 100);

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

    // Readiness Score Formula (Safeguarded: 0 if completed < 5)
    let readinessScore = 0;
    if (completedCount >= 5) {
      const s1 = 30 * Math.min(1, indepRate / 0.80);
      const s2 = 25 * Math.min(1, (1 - hintRate) / 0.80);
      const s3 = 25 * Math.min(1, (completedCount / 40));
      const s4 = 20 * Math.min(1, Math.max(0, (12 - 5) / 8));
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

  // Update Header on all pages
  function updateHeader() {
    const metrics = calculateMetrics();
    const currDayElem = document.getElementById('header-current-day');
    const progElem = document.getElementById('header-progress-pct');
    const readElem = document.getElementById('header-readiness-score');
    const streakElem = document.getElementById('header-streak');

    if (currDayElem) currDayElem.textContent = `Day ${state.currentDayIndex + 1}`;
    if (progElem) progElem.textContent = `${metrics.progressPct}%`;
    if (readElem) readElem.textContent = `${metrics.readinessScore} / 100`;
    if (streakElem) streakElem.textContent = `${metrics.completedCount} Days`;
  }

  // Timer Initialization (for index.html)
  function initTimer() {
    const display = document.getElementById('timer-display');
    const badge = document.getElementById('timer-status-badge');
    const instruction = document.getElementById('timer-instruction');
    const btnStart = document.getElementById('timer-btn-start');
    const btnPause = document.getElementById('timer-btn-pause');
    const btnReset = document.getElementById('timer-btn-reset');

    if (!display || !btnStart) return;

    function updateDisplay() {
      const mins = Math.floor(state.timer.remainingSeconds / 60);
      const secs = state.timer.remainingSeconds % 60;
      display.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;

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
          alert("Time's up! Consult the editorial approach and log an F-code in Failure Log.");
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

  // Dashboard Page Updating
  function updateDashboardView() {
    const heroTopic = document.getElementById('hero-topic');
    if (!heroTopic || !DATA.days) return;

    const metrics = calculateMetrics();
    const day = DATA.days[state.currentDayIndex];
    if (!day) return;

    // KPI Numbers
    const kpiReadiness = document.getElementById('kpi-readiness');
    const kpiIndep = document.getElementById('kpi-indep');
    const kpiHints = document.getElementById('kpi-hints');
    const kpiTtp = document.getElementById('kpi-ttp');

    if (kpiReadiness) kpiReadiness.textContent = `${metrics.readinessScore} / 100`;
    if (kpiIndep) kpiIndep.textContent = `${metrics.indepRate}%`;
    if (kpiHints) kpiHints.textContent = `${metrics.hintRate}%`;
    if (kpiTtp) kpiTtp.textContent = metrics.completedCount > 0 ? `${metrics.avgTtp} min` : "-- min";

    // Hero Mission Details
    document.getElementById('hero-day-date').textContent = `Day ${day.day} of 168 (${day.dateDisplay})`;
    heroTopic.textContent = day.pattern;
    document.getElementById('hero-objective').textContent = day.objective;

    // P1
    const p1Title = document.getElementById('hero-p1-title');
    const p1Meta = document.getElementById('hero-p1-meta');
    const p1Diff = document.getElementById('hero-p1-diff');
    const p1Link = document.getElementById('hero-p1-link');
    if (p1Title) {
      p1Title.textContent = day.p1;
      p1Meta.textContent = `Target: ${day.t1} min | Mode: ${day.mode}`;
      p1Diff.textContent = day.d1;
      p1Diff.className = `diff-tag diff-${day.d1}`;
      p1Link.href = day.p1Url;
    }

    // P2
    const p2Title = document.getElementById('hero-p2-title');
    const p2Meta = document.getElementById('hero-p2-meta');
    const p2Diff = document.getElementById('hero-p2-diff');
    const p2Link = document.getElementById('hero-p2-link');
    if (p2Title) {
      p2Title.textContent = day.p2;
      p2Meta.textContent = `Target: ${day.t2} min | Difficulty: ${day.d2}`;
      p2Diff.textContent = day.d2;
      p2Diff.className = `diff-tag diff-${day.d2}`;
      p2Link.href = day.p2Url;
    }

    // Infra
    const infraElem = document.getElementById('hero-infra-note');
    if (infraElem) infraElem.textContent = day.infra || "Contiguous flat layouts, cache lines, and hardware synchronization.";

    // Tutorial Callout Box
    const tutBox = document.getElementById('hero-tut-box');
    if (tutBox) {
      if (day.tutYn === 'YES') {
        tutBox.style.display = '';
        const tutTitle = document.getElementById('hero-tut-title');
        const tutBadge = document.getElementById('hero-tut-badge');
        const tutMeta = document.getElementById('hero-tut-meta');
        const tutLink = document.getElementById('hero-tut-link');
        if (tutTitle) tutTitle.textContent = day.tutTopic;
        if (tutBadge) tutBadge.textContent = `📺 TUTORIAL (${day.tutMin || 25}m)`;
        if (tutMeta) {
          const pChan = (day.tutResource && day.tutResource.primaryChannel) || "Striver";
          tutMeta.textContent = `Recommended: ${pChan} • Striver, Aditya Verma, Love Babbar, Padho with Pratyush, NeetCode`;
        }
        if (tutLink && day.tutResource) {
          tutLink.href = day.tutResource.primaryUrl;
          tutLink.textContent = `▶ Watch (${day.tutResource.primaryChannel}) ↗`;
        }
      } else {
        tutBox.style.display = 'none';
      }
    }

    // Button state
    const btnComplete = document.getElementById('btn-complete-today');
    const heroRevLink = document.getElementById('hero-revision-link');
    if (btnComplete) {
      if (state.completedDays[day.day]) {
        btnComplete.textContent = "✓ Completed";
        btnComplete.className = "btn btn-success";
        if (heroRevLink) {
          heroRevLink.style.display = 'inline-flex';
          heroRevLink.href = `revision.html#rev-card-${day.day}`;
          heroRevLink.textContent = `📖 Day ${day.day} Vault Unlocked ↗`;
        }
      } else {
        btnComplete.textContent = "✓ Mark Day Complete";
        btnComplete.className = "btn btn-primary";
        if (heroRevLink) {
          heroRevLink.style.display = 'none';
        }
      }
    }

    // Upcoming Diagnostic
    const nextDiagElem = document.getElementById('dashboard-next-diag');
    if (nextDiagElem && DATA.mocks) {
      const nextDiag = DATA.mocks.find(m => m.day >= day.day);
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
    }

    // Failure Hotspot
    const hotspotElem = document.getElementById('dashboard-failure-hotspot');
    if (hotspotElem) {
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

      if (worstF && maxCount >= 2 && DATA.fcats) {
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
  }

  // DayPlan Page Updating
  function updatePlanView() {
    const table = document.getElementById('table-dayplan');
    if (!table) return;

    // Update status pills and buttons
    const pills = document.querySelectorAll('.day-status-pill');
    pills.forEach(pill => {
      const dayNum = Number(pill.getAttribute('data-day-status'));
      const isDone = !!state.completedDays[dayNum];
      if (isDone) {
        pill.textContent = "✓ Done";
        pill.style.color = "var(--nv-green)";
      } else {
        pill.textContent = "Pending";
        pill.style.color = "var(--text-muted)";
      }
    });

    const btns = document.querySelectorAll('.btn-complete-row');
    btns.forEach(btn => {
      const dayNum = Number(btn.getAttribute('data-day'));
      const isDone = !!state.completedDays[dayNum];
      btn.textContent = isDone ? "Edit" : "Complete";
    });

    const vaultBtns = document.querySelectorAll('.btn-vault-row');
    vaultBtns.forEach(vb => {
      const dayNum = Number(vb.getAttribute('data-day'));
      const isDone = !!state.completedDays[dayNum];
      vb.style.display = isDone ? 'inline-flex' : 'none';
    });

    // Filtering logic
    const searchInput = document.getElementById('plan-search');
    const phaseSelect = document.getElementById('plan-filter-phase');
    const weekSelect = document.getElementById('plan-filter-week');
    const nvidiaSelect = document.getElementById('plan-filter-nvidia');
    const statusSelect = document.getElementById('plan-filter-status');

    function applyFilters() {
      const query = (searchInput.value || '').toLowerCase();
      const phase = phaseSelect.value;
      const week = weekSelect.value;
      const nvidia = nvidiaSelect.value;
      const status = statusSelect.value;

      const rows = document.querySelectorAll('#tbody-dayplan tr');
      rows.forEach(row => {
        const dNum = Number(row.getAttribute('data-day'));
        const dPhase = row.getAttribute('data-phase');
        const dWeek = row.getAttribute('data-week');
        const isNv = row.getAttribute('data-nvidia') === 'true';
        const isDone = !!state.completedDays[dNum];
        const text = row.textContent.toLowerCase();

        let visible = true;
        if (phase !== 'ALL' && dPhase !== phase) visible = false;
        if (week !== 'ALL' && dWeek !== week) visible = false;
        if (nvidia === 'NVIDIA' && !isNv) visible = false;
        if (status === 'DONE' && !isDone) visible = false;
        if (status === 'PENDING' && isDone) visible = false;
        if (query && !text.includes(query)) visible = false;

        row.style.display = visible ? '' : 'none';
      });
    }

    if (searchInput) searchInput.oninput = applyFilters;
    if (phaseSelect) phaseSelect.onchange = applyFilters;
    if (weekSelect) weekSelect.onchange = applyFilters;
    if (nvidiaSelect) nvidiaSelect.onchange = applyFilters;
    if (statusSelect) statusSelect.onchange = applyFilters;
  }

  // Flashcards Interactions
  function initFlashcards() {
    const container = document.getElementById('flashcards-container');
    if (!container) return;

    // Flip single card
    document.querySelectorAll('.flashcard-wrapper').forEach(wrapper => {
      wrapper.addEventListener('click', () => {
        wrapper.classList.toggle('flipped');
      });
    });

    // Flip All
    const btnFlipAll = document.getElementById('btn-flip-all');
    let allFlipped = false;
    if (btnFlipAll) {
      btnFlipAll.addEventListener('click', () => {
        allFlipped = !allFlipped;
        document.querySelectorAll('.flashcard-wrapper').forEach(w => {
          if (allFlipped) w.classList.add('flipped');
          else w.classList.remove('flipped');
        });
      });
    }

    // Search flashcards
    const searchInput = document.getElementById('flashcard-search');
    if (searchInput) {
      searchInput.addEventListener('input', () => {
        const query = searchInput.value.toLowerCase();
        document.querySelectorAll('.flashcard-wrapper').forEach(card => {
          const text = card.getAttribute('data-card-text') || '';
          card.style.display = text.includes(query) ? '' : 'none';
        });
      });
    }
  }

  // Pattern Search
  function initPatternSearch() {
    const searchInput = document.getElementById('pattern-search');
    if (!searchInput) return;

    searchInput.addEventListener('input', () => {
      const query = searchInput.value.toLowerCase();
      document.querySelectorAll('.pattern-card-item').forEach(card => {
        const name = card.getAttribute('data-pattern-name') || '';
        const desc = card.getAttribute('data-pattern-desc') || '';
        const match = name.includes(query) || desc.includes(query);
        card.style.display = match ? '' : 'none';
      });
    });
  }

  // Resource Search & Creator Filter
  function initResourceSearch() {
    const searchInput = document.getElementById('resource-search');
    const filterBtns = document.querySelectorAll('.btn-resource-filter');
    let activeCreator = '';

    function applyFilter() {
      const query = searchInput ? searchInput.value.toLowerCase().trim() : '';
      document.querySelectorAll('.resource-row-item').forEach(row => {
        const text = row.getAttribute('data-text') || '';
        const matchesQuery = !query || text.includes(query);
        const matchesCreator = !activeCreator || text.includes(activeCreator);
        row.style.display = (matchesQuery && matchesCreator) ? '' : 'none';
      });
    }

    if (searchInput) {
      searchInput.addEventListener('input', applyFilter);
    }

    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => {
          b.style.opacity = '0.65';
          b.style.fontWeight = 'normal';
        });
        btn.style.opacity = '1';
        btn.style.fontWeight = '700';
        activeCreator = (btn.getAttribute('data-filter') || '').toLowerCase();
        applyFilter();
      });
    });
  }

  // Failures Page Logic
  function updateFailuresView() {
    const queueContainer = document.getElementById('review-queue-container');
    const tbody = document.getElementById('tbody-failure-history');
    if (!queueContainer || !tbody) return;

    // Active review queue
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
          <button class="btn btn-outline" style="padding: 0.2rem 0.5rem; font-size: 0.75rem;">
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

    // Historical ledger
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
          <button class="btn btn-outline" style="padding: 0.15rem 0.4rem; font-size: 0.7rem;">
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

  // Modals (Sync + Complete Day)
  function openCompleteModal(dayNum) {
    const day = (DATA.days || []).find(d => d.day === dayNum);
    if (!day) return;

    const modal = document.getElementById('modal-complete-day');
    document.getElementById('modal-day-num').value = day.day;
    document.getElementById('modal-day-title').textContent = `Complete Day ${day.day}: ${day.pattern}`;

    const existing = state.completedDays[day.day] || {};
    document.getElementById('modal-time-spent').value = existing.timeSpent || 60;
    document.getElementById('modal-solved-indep').value = existing.solvedIndep || "Yes";
    document.getElementById('modal-hints-count').value = existing.hints || "0";
    document.getElementById('modal-sol-viewed').value = existing.solViewed || "No";
    document.getElementById('modal-key-insight').value = existing.keyInsight || "";

    modal.classList.add('open');
  }

  function initModals() {
    // Complete Day Modal
    const modalComplete = document.getElementById('modal-complete-day');
    const btnCloseModal = document.getElementById('btn-close-modal');
    const btnCancelModal = document.getElementById('btn-cancel-modal');

    if (btnCloseModal) btnCloseModal.onclick = () => modalComplete.classList.remove('open');
    if (btnCancelModal) btnCancelModal.onclick = () => modalComplete.classList.remove('open');

    const formComplete = document.getElementById('form-complete-day');
    if (formComplete) {
      formComplete.onsubmit = (e) => {
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

        if (DATA.days && dayNum === DATA.days[state.currentDayIndex].day && state.currentDayIndex < DATA.days.length - 1) {
          state.currentDayIndex++;
        }

        saveState();
        modalComplete.classList.remove('open');
      };
    }

    // Connect Complete Buttons
    const btnCompleteToday = document.getElementById('btn-complete-today');
    if (btnCompleteToday && DATA.days) {
      btnCompleteToday.onclick = () => openCompleteModal(DATA.days[state.currentDayIndex].day);
    }

    const prevBtn = document.getElementById('btn-prev-mission');
    const nextBtn = document.getElementById('btn-next-mission');
    if (prevBtn) {
      prevBtn.onclick = () => {
        if (state.currentDayIndex > 0) {
          state.currentDayIndex--;
          updateDashboardView();
        }
      };
    }
    if (nextBtn) {
      nextBtn.onclick = () => {
        if (DATA.days && state.currentDayIndex < DATA.days.length - 1) {
          state.currentDayIndex++;
          updateDashboardView();
        }
      };
    }

    // Connect plan.html row buttons
    document.querySelectorAll('.btn-complete-row').forEach(btn => {
      btn.onclick = () => {
        const dayNum = Number(btn.getAttribute('data-day'));
        openCompleteModal(dayNum);
      };
    });

    // Failure Form
    const formFailure = document.getElementById('form-log-failure');
    if (formFailure) {
      formFailure.onsubmit = (e) => {
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
        alert("Failure recorded! This problem is scheduled for a 3-day spaced repetition review.");
      };
    }

    // Sync Modal
    const modalSync = document.getElementById('modal-sync');
    const btnOpenSync = document.getElementById('btn-open-sync');
    const btnCloseSync = document.getElementById('btn-close-sync-modal');

    if (btnOpenSync && modalSync) btnOpenSync.onclick = () => modalSync.classList.add('open');
    if (btnCloseSync && modalSync) btnCloseSync.onclick = () => modalSync.classList.remove('open');

    // Export JSON
    const btnExportJson = document.getElementById('btn-export-json');
    if (btnExportJson) {
      btnExportJson.onclick = () => {
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(state, null, 2));
        const a = document.createElement('a');
        a.href = dataStr;
        a.download = `dsa_cockpit_backup_${new Date().toISOString().split('T')[0]}.json`;
        a.click();
      };
    }

    // Export CSV
    const btnExportCsv = document.getElementById('btn-export-csv');
    if (btnExportCsv) {
      btnExportCsv.onclick = () => {
        let csv = "Day,Date,TimeSpent,SolvedIndependently,HintsTaken,SolutionViewed,KeyInsight\n";
        for (const [day, val] of Object.entries(state.completedDays)) {
          csv += `${day},${val.date},${val.timeSpent},${val.solvedIndep},${val.hints},${val.solViewed},"${(val.keyInsight||'').replace(/"/g, '""')}"\n`;
        }
        const a = document.createElement('a');
        a.href = "data:text/csv;charset=utf-8," + encodeURIComponent(csv);
        a.download = `dsa_completed_days_${new Date().toISOString().split('T')[0]}.csv`;
        a.click();
      };
    }

    // Import JSON
    const inputImport = document.getElementById('input-import-file');
    if (inputImport) {
      inputImport.onchange = (e) => {
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
      };
    }

    // Reset Data
    const btnReset = document.getElementById('btn-reset-data');
    if (btnReset) {
      btnReset.onclick = () => {
        if (confirm("Are you sure you want to clear all progress? This will reset all your logs to Day 1.")) {
          state.completedDays = {};
          state.failures = [];
          state.currentDayIndex = 0;
          saveState();
          modalSync.classList.remove('open');
        }
      };
    }
  }

  // Revision Vault Handlers
  function initRevisionVault() {
    const revContainer = document.getElementById('revision-vault-container');
    if (!revContainer) return;

    // Filter Buttons
    const filterBtns = document.querySelectorAll('.rev-filter-btn');
    const searchInput = document.getElementById('rev-search-input');
    let currentFilter = 'all';

    function applyFilters() {
      const q = (searchInput ? searchInput.value : '').toLowerCase().trim();
      const cards = document.querySelectorAll('.revision-card');

      cards.forEach(card => {
        const isLocked = card.classList.contains('locked');
        const text = (card.getAttribute('data-search') || '') + ' ' + (card.textContent || '').toLowerCase();

        let matchesFilter = true;
        if (currentFilter === 'unlocked' && isLocked) matchesFilter = false;
        if (currentFilter === 'locked' && !isLocked) matchesFilter = false;

        let matchesSearch = true;
        if (q && !text.includes(q)) matchesSearch = false;

        card.style.display = (matchesFilter && matchesSearch) ? 'block' : 'none';
      });
    }

    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentFilter = btn.getAttribute('data-filter') || 'all';
        applyFilters();
      });
    });

    if (searchInput) {
      searchInput.addEventListener('input', applyFilters);
    }

    // Bind Notes Textareas with auto-save
    document.querySelectorAll('.rev-notes-textarea').forEach(textarea => {
      const dNum = textarea.getAttribute('data-day');
      if (state.dayNotes && state.dayNotes[dNum]) {
        textarea.value = state.dayNotes[dNum];
      }
      textarea.addEventListener('input', () => {
        state.dayNotes[dNum] = textarea.value;
        const ind = document.getElementById(`rev-save-status-${dNum}`);
        if (ind) {
          ind.textContent = "Saving...";
          ind.style.color = "var(--amber-accent)";
        }
        try {
          const payload = {
            completedDays: state.completedDays,
            failures: state.failures,
            dayNotes: state.dayNotes,
            faangMastery: state.faangMastery
          };
          localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
          if (ind) {
            setTimeout(() => {
              ind.textContent = "✓ Saved";
              ind.style.color = "var(--nv-green)";
            }, 300);
          }
        } catch (e) {
          console.error(e);
        }
      });
    });

    updateRevisionVaultView();

    // Auto-scroll and highlight target card if navigated with hash #rev-card-X or #day-X
    if (window.location.hash) {
      setTimeout(() => {
        const rawHash = window.location.hash.substring(1);
        const dayMatch = rawHash.match(/\d+/);
        const dayNum = dayMatch ? dayMatch[0] : null;
        const target = document.getElementById(rawHash) || (dayNum ? document.getElementById(`rev-card-${dayNum}`) : null);
        if (target) {
          target.style.display = 'block';
          target.scrollIntoView({ behavior: 'smooth', block: 'center' });
          target.classList.add('rev-card-target-highlight');
          setTimeout(() => target.classList.remove('rev-card-target-highlight'), 3000);
        }
      }, 200);
    }
  }

  function updateRevisionVaultView() {
    const revContainer = document.getElementById('revision-vault-container');
    if (!revContainer || !DATA.days) return;

    const completedList = Object.keys(state.completedDays);
    const completedCount = completedList.length;
    const totalDays = DATA.days.length;
    const pct = Math.round((completedCount / totalDays) * 100);

    const countEl = document.getElementById('rev-unlocked-count');
    const pctEl = document.getElementById('rev-unlocked-pct');
    if (countEl) countEl.textContent = completedCount;
    if (pctEl) pctEl.textContent = `${pct}%`;

    const progBar = document.getElementById('rev-prog-fill');
    if (progBar) progBar.style.width = `${pct}%`;

    DATA.days.forEach(d => {
      const card = document.getElementById(`rev-card-${d.day}`);
      if (!card) return;

      const completion = state.completedDays[d.day];
      if (completion) {
        card.classList.remove('locked');
        card.classList.add('unlocked');

        const dateEl = document.getElementById(`rev-comp-date-${d.day}`);
        if (dateEl && completion.date) dateEl.textContent = `• Completed ${completion.date}`;

        const timeEl = document.getElementById(`rev-time-${d.day}`);
        if (timeEl) timeEl.textContent = `${completion.timeSpent || 60}m`;

        const indepEl = document.getElementById(`rev-indep-${d.day}`);
        if (indepEl) {
          indepEl.textContent = completion.solvedIndep || "Yes";
          indepEl.style.color = completion.solvedIndep === "Yes" ? "var(--nv-green)" : "var(--amber-accent)";
        }

        const hintsEl = document.getElementById(`rev-hints-${d.day}`);
        if (hintsEl) hintsEl.textContent = `${completion.hints || "0"} hints`;

        const solEl = document.getElementById(`rev-sol-${d.day}`);
        if (solEl) {
          solEl.textContent = completion.solViewed || "No";
          solEl.style.color = completion.solViewed === "No" ? "var(--nv-green)" : "var(--red-accent)";
        }

        const insightBox = document.getElementById(`rev-insight-box-${d.day}`);
        const insightText = document.getElementById(`rev-insight-text-${d.day}`);
        if (insightBox && insightText) {
          if (completion.keyInsight && completion.keyInsight.trim()) {
            insightBox.style.display = 'block';
            insightText.textContent = `"${completion.keyInsight.trim()}"`;
          } else {
            insightBox.style.display = 'none';
          }
        }
      } else {
        card.classList.remove('unlocked');
        card.classList.add('locked');
      }
    });
  }

  // FAANG Patterns Checklist Handler
  function initFaangChecklist() {
    const checklistBox = document.getElementById('faang-checklist-container');
    if (!checklistBox) return;

    const checkboxes = checklistBox.querySelectorAll('input[type="checkbox"]');
    const totalChecks = checkboxes.length;

    function updateProgress() {
      let checkedCount = 0;
      checkboxes.forEach(cb => {
        const key = cb.getAttribute('data-check-key');
        if (cb.checked) checkedCount++;
        if (key) state.faangMastery[key] = cb.checked;
      });

      const fillEl = document.getElementById('faang-prog-fill');
      const textEl = document.getElementById('faang-prog-text');
      const pct = Math.round((checkedCount / totalChecks) * 100);
      if (fillEl) fillEl.style.width = `${pct}%`;
      if (textEl) textEl.textContent = `${checkedCount} / ${totalChecks} Milestones Complete (${pct}%)`;

      document.querySelectorAll('.faang-pat-item').forEach(item => {
        const cbs = item.querySelectorAll('input[type="checkbox"]');
        const allChecked = Array.from(cbs).every(c => c.checked);
        if (allChecked) item.classList.add('fully-mastered');
        else item.classList.remove('fully-mastered');
      });
    }

    checkboxes.forEach(cb => {
      const key = cb.getAttribute('data-check-key');
      if (key && state.faangMastery && state.faangMastery[key]) {
        cb.checked = true;
      }
      cb.addEventListener('change', () => {
        updateProgress();
        saveState();
      });
    });

    updateProgress();
  }

  function updateAllViews() {
    updateHeader();
    updateDashboardView();
    updatePlanView();
    updateFailuresView();
    updateRevisionVaultView();
  }

  function init() {
    loadState();
    initTimer();
    initFlashcards();
    initPatternSearch();
    initResourceSearch();
    initModals();
    initRevisionVault();
    initFaangChecklist();
    updateAllViews();
  }

  window.addEventListener('DOMContentLoaded', init);
})();

/* ============================================================ */
/* ADAPTIVE WEEKLY ENGINE + ASSESSMENT BANNER (Dashboard only)  */
/* ============================================================ */
(function () {
  'use strict';
  var AWE_KEY = 'DSA_WEEKLY_ENGINE_V1';
  var ASSESS_KEY = 'DSA_ASSESSMENT_V1';

  function computeStatus(indep, mocks, fcode, prevFcode) {
    var criticalFail = (fcode === 'pattern' || fcode === 'derive');
    var repeatedCritical = criticalFail && (prevFcode === 'pattern' || prevFcode === 'derive');
    if (indep === 0 || repeatedCritical) {
      return { key: 'STUCK', icon: '🚨', badge: 'STUCK PROTOCOL ACTIVATED',
        title: 'Stop advancing — invoke the Stuck Protocol', color: '#ef4444', bg: 'rgba(239,68,68,0.07)',
        action: '<strong>Do NOT proceed to next week\'s content.</strong> For the next 7 days:<br>1. Re-solve every problem from this week you couldn\'t do independently — blank editor, no hints.<br>2. Drill your F-code\'s specific exercise for 20 min/day.<br>3. Only proceed when you can solve any 3 problems from this week within target time.<br><span style="color:var(--amber-accent);font-size:0.82rem;">Remember: Stuck Protocol, not restart.</span>' };
    }
    if (indep >= 3 && mocks >= 1 && !criticalFail) {
      return { key: 'ACCELERATE', icon: '🚀', badge: 'ACCELERATE',
        title: 'You\'re ahead — push harder next week', color: '#76b900', bg: 'rgba(118,185,0,0.07)',
        action: '<strong>Next week: Replace one Medium with one Hard problem per day.</strong><br>Skip scheduled buffer/review days — you earned them back.<br>If mocks ≥ 2 this week: add one extra timed mock coming week.<br><span style="color:var(--text-muted);font-size:0.82rem;">If solve rate drops next week, drop back to On Track automatically.</span>' };
    }
    if (indep >= 2) {
      return { key: 'ON_TRACK', icon: '✅', badge: 'ON TRACK',
        title: 'Solid week — continue as planned', color: '#38bdf8', bg: 'rgba(56,189,248,0.07)',
        action: '<strong>Follow next week\'s plan exactly as written.</strong><br>' +
          (mocks === 0 ? '⚠️ <strong>No mock this week</strong> — schedule one for the coming week.<br>' : '✓ Mock completed — good.<br>') +
          (fcode !== 'none' ? 'Drill for <strong>' + fcode.toUpperCase() + '</strong>: 15 min targeted exercise/day.<br>' : 'No recurring failure — continue varied practice.<br>') +
          '<span style="color:var(--text-muted);font-size:0.82rem;">Consistency beats acceleration. Stay the course.</span>' };
    }
    return { key: 'SLOW_DOWN', icon: '⚠️', badge: 'SLOW DOWN',
      title: 'Below target — consolidate before advancing', color: '#f59e0b', bg: 'rgba(245,158,11,0.07)',
      action: '<strong>Next week: Repeat the hardest pattern from this week before any new content.</strong><br>Add 1 extra review day: re-solve 3 most difficult problems timed.<br>' +
        (fcode !== 'none' ? 'Dominant failure <strong>(' + fcode + ')</strong>: run its drill every single day.<br>' : '') +
        '<span style="color:var(--amber-accent);font-size:0.82rem;">2nd consecutive Slow Down → activate Stuck Protocol next check-in.</span>' };
  }

  function showStatus(status) {
    var disp = document.getElementById('awe-status-display');
    if (!disp) return;
    disp.style.display = 'block';
    disp.style.background = status.bg;
    disp.style.borderLeftColor = status.color;
    document.getElementById('awe-status-icon').textContent = status.icon;
    document.getElementById('awe-status-badge').textContent = status.badge;
    document.getElementById('awe-status-badge').style.color = status.color;
    document.getElementById('awe-status-title').textContent = status.title;
    document.getElementById('awe-status-action').innerHTML = status.action;
  }

  function renderHistory(history) {
    var list = document.getElementById('awe-history-list');
    if (!list) return;
    if (!history || history.length === 0) {
      list.innerHTML = '<span style="font-size:0.82rem;color:var(--text-muted);">No check-ins yet. Complete your first week and log it above.</span>';
      return;
    }
    var colors = { ACCELERATE: '#76b900', ON_TRACK: '#38bdf8', SLOW_DOWN: '#f59e0b', STUCK: '#ef4444' };
    list.innerHTML = history.slice().reverse().map(function (h) {
      var col = colors[h.status.key] || '#94a3b8';
      var dt = new Date(h.date).toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });
      return '<div style="display:flex;align-items:center;gap:10px;background:var(--bg-secondary);border:1px solid var(--border-subtle);border-radius:8px;padding:0.55rem 0.9rem;">' +
        '<span style="font-size:1rem;">' + h.status.icon + '</span><div style="flex:1;">' +
        '<span style="font-size:0.8rem;font-weight:800;color:' + col + ';">' + h.status.badge + '</span>' +
        '<span style="font-size:0.78rem;color:var(--text-muted);margin-left:8px;">Week ' + h.week + '</span></div>' +
        '<span style="font-size:0.72rem;color:var(--text-muted);font-family:var(--font-mono);">' + dt + '</span></div>';
    }).join('');
  }

  function initAdaptiveEngine() {
    var form = document.getElementById('awe-form');
    if (!form) return;
    var history = [];
    try { history = JSON.parse(localStorage.getItem(AWE_KEY)) || []; } catch (e) {}

    var weekSel = document.getElementById('awe-week');
    for (var w = 1; w <= 24; w++) {
      var opt = document.createElement('option');
      opt.value = w; opt.textContent = 'Week ' + w;
      weekSel.appendChild(opt);
    }
    if (history.length > 0) {
      var lw = history[history.length - 1].week;
      if (lw < 24) weekSel.value = lw + 1;
    } else { weekSel.value = 1; }

    if (history.length > 0) showStatus(history[history.length - 1].status);

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var week  = parseInt(weekSel.value, 10);
      var indep = parseInt(document.getElementById('awe-indep').value, 10);
      var mocks = parseInt(document.getElementById('awe-mocks').value, 10);
      var fcode = document.getElementById('awe-fcode').value;
      var prevFcode = history.length > 0 ? history[history.length - 1].fcode : 'none';
      if (!week) { weekSel.focus(); return; }
      var status = computeStatus(indep, mocks, fcode, prevFcode);
      var entry = { week: week, indep: indep, mocks: mocks, fcode: fcode, status: status, date: new Date().toISOString() };
      var idx = -1;
      for (var i = 0; i < history.length; i++) { if (history[i].week === week) { idx = i; break; } }
      if (idx >= 0) history[idx] = entry; else history.push(entry);
      if (history.length > 6) history = history.slice(-6);
      try { localStorage.setItem(AWE_KEY, JSON.stringify(history)); } catch (e) {}
      showStatus(status);
      renderHistory(history);
    });

    document.getElementById('awe-toggle-history').addEventListener('click', function () {
      var panel = document.getElementById('awe-history-panel');
      var vis = panel.style.display !== 'none';
      panel.style.display = vis ? 'none' : 'block';
      this.textContent = vis ? '📋 History' : '📋 Hide';
      if (!vis) renderHistory(history);
    });
  }

  function initAssessmentBanner() {
    var ab  = document.getElementById('assessment-banner');
    var nab = document.getElementById('no-assessment-banner');
    if (!ab || !nab) return;
    try {
      var result = JSON.parse(localStorage.getItem(ASSESS_KEY));
      if (result && result.startWeek) {
        ab.style.display = 'flex'; nab.style.display = 'none';
        var el = document.getElementById('banner-assess-text');
        if (el) el.textContent = 'Recommended start: Week ' + result.startWeek +
          ' · Score: ' + result.totalScore + '/45 · ' + result.daysSaved + ' days saved';
      } else { ab.style.display = 'none'; nab.style.display = 'flex'; }
    } catch (e) { ab.style.display = 'none'; nab.style.display = 'flex'; }
  }

  document.addEventListener('DOMContentLoaded', function () {
    initAdaptiveEngine();
    initAssessmentBanner();
  });
})();
