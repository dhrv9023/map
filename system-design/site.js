// System Design Cockpit - Interactive Engine (2026)
(function() {
  'use strict';

  // --- LOCAL STORAGE PROGRESS TRACKER ---
  const STORAGE_KEY = 'ai_infra_sd_progress_v1';

  function getSavedState() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY)) || { checked: {}, readiness: 0, streak: 1 };
    } catch (e) {
      return { checked: {}, readiness: 0, streak: 1 };
    }
  }

  function saveState(state) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (e) {}
  }

  function updateHeaderStats() {
    const state = getSavedState();
    const checkedCount = Object.keys(state.checked).filter(k => state.checked[k]).length;
    const totalItems = document.querySelectorAll('.topic-check').length || 100;
    const pct = Math.min(100, Math.round((checkedCount / totalItems) * 100));

    const progressEl = document.getElementById('stat-progress');
    if (progressEl) progressEl.textContent = pct + '%';

    const readinessEl = document.getElementById('stat-readiness');
    if (readinessEl) readinessEl.textContent = (pct * 0.95).toFixed(0) + ' / 100';
  }

  window.toggleTopicCheck = function(topicId) {
    const state = getSavedState();
    state.checked[topicId] = !state.checked[topicId];
    saveState(state);
    updateHeaderStats();
  };

  // --- INTERACTIVE CAPACITY CALCULATOR ---
  window.calculateCapacity = function() {
    const modelParamB = parseFloat(document.getElementById('calc-params')?.value || 7);
    const precisionBytes = parseFloat(document.getElementById('calc-precision')?.value || 2);
    const seqLen = parseInt(document.getElementById('calc-seqlen')?.value || 2048, 10);
    const batchSize = parseInt(document.getElementById('calc-batch')?.value || 16, 10);
    const numLayers = parseInt(document.getElementById('calc-layers')?.value || 32, 10);
    const numKvHeads = parseInt(document.getElementById('calc-heads')?.value || 8, 10); // GQA
    const headDim = parseInt(document.getElementById('calc-dim')?.value || 128, 10);
    const gpuBandwidthGBs = parseFloat(document.getElementById('calc-bandwidth')?.value || 3350); // H100 default 3350 GB/s

    // 1. Raw Parameter Memory (GB)
    const paramMemGB = (modelParamB * 1e9 * precisionBytes) / (1024 ** 3);

    // 2. KV Cache Memory per token: 2 (K & V) * numLayers * numKvHeads * headDim * precisionBytes
    const kvBytesPerToken = 2 * numLayers * numKvHeads * headDim * precisionBytes;
    const kvMemPerSeqMB = (kvBytesPerToken * seqLen) / (1024 ** 2);
    const totalKvMemGB = (kvBytesPerToken * seqLen * batchSize) / (1024 ** 3);

    // 3. Activation & Runtime Overhead (~20%)
    const overheadGB = (paramMemGB + totalKvMemGB) * 0.20;
    const totalVramGB = paramMemGB + totalKvMemGB + overheadGB;

    // 4. Memory-Bandwidth Limited Single Stream Decode Speed (tokens/sec)
    // Decode is memory-bound: must read all weights per token generated
    const singleStreamTokensPerSec = (gpuBandwidthGBs / paramMemGB);

    // Update DOM
    const elParam = document.getElementById('res-param-mem');
    if (elParam) elParam.textContent = paramMemGB.toFixed(1) + ' GB';

    const elKvSeq = document.getElementById('res-kv-seq');
    if (elKvSeq) elKvSeq.textContent = kvMemPerSeqMB.toFixed(1) + ' MB';

    const elKvTotal = document.getElementById('res-kv-total');
    if (elKvTotal) elKvTotal.textContent = totalKvMemGB.toFixed(1) + ' GB';

    const elVram = document.getElementById('res-total-vram');
    if (elVram) elVram.textContent = totalVramGB.toFixed(1) + ' GB';

    const elSpeed = document.getElementById('res-decode-speed');
    if (elSpeed) elSpeed.textContent = Math.round(singleStreamTokensPerSec) + ' tok/s (single-stream ceiling)';

    const elH100 = document.getElementById('res-h100-count');
    if (elH100) {
      const gpusNeeded = Math.ceil(totalVramGB / 80); // 80GB SXM5 H100
      elH100.textContent = gpusNeeded + 'x 80GB GPUs (' + (gpusNeeded <= 1 ? '1 GPU' : 'Tensor Parallelism TP=' + (gpusNeeded <= 2 ? '2' : gpusNeeded <= 4 ? '4' : '8')) + ')';
    }
  };

  document.addEventListener('DOMContentLoaded', function() {
    updateHeaderStats();
    if (document.getElementById('calc-params')) {
      calculateCapacity();
      const inputs = document.querySelectorAll('.calc-trigger');
      inputs.forEach(input => {
        input.addEventListener('input', calculateCapacity);
        input.addEventListener('change', calculateCapacity);
      });
    }
  });

})();
