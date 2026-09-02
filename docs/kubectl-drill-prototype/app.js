// kubectl-drill prototype — UI wiring (PROTOTYPE, not integrated into the real app)
//
// Depends on matcher.js being loaded first (window.KubectlDrillMatcher).
// Zero network calls, zero external dependencies — open index.html directly
// from disk (file://) to verify the offline claim.

(function () {
  'use strict';

  const HINT_AFTER_ATTEMPTS = 2;   // show the authored hint starting on the 2nd wrong attempt
  const REVEAL_AFTER_ATTEMPTS = 3; // reveal reference_command starting on the 3rd wrong attempt

  const STRINGS = {
    en: {
      taskLabel: (i, n) => `Task ${i} / ${n}`,
      simulatedBadge: 'Simulated — no real cluster',
      promptIntro: 'Task:',
      nudge: 'Not quite — check the command and try again.',
      hintPrefix: 'Hint:',
      revealPrefix: 'Reference solution:',
      revealFollow: 'Take a look, then try typing it yourself before moving on.',
      nextTask: 'Next task →',
      restartTask: 'Try this task again',
      allDone: 'All sample tasks complete.',
      inputPlaceholder: 'type a kubectl command and press Enter',
      langBtn: 'DE',
    },
    de: {
      taskLabel: (i, n) => `Aufgabe ${i} / ${n}`,
      simulatedBadge: 'Simuliert — kein echter Cluster',
      promptIntro: 'Aufgabe:',
      nudge: 'Noch nicht richtig — prüfe den Befehl und versuche es erneut.',
      hintPrefix: 'Hinweis:',
      revealPrefix: 'Musterlösung:',
      revealFollow: 'Schau sie dir an und tippe sie danach selbst ein, bevor du weitermachst.',
      nextTask: 'Nächste Aufgabe →',
      restartTask: 'Aufgabe erneut versuchen',
      allDone: 'Alle Beispielaufgaben abgeschlossen.',
      inputPlaceholder: 'kubectl-Befehl eingeben und Enter drücken',
      langBtn: 'EN',
    },
  };

  const state = {
    lang: 'en',
    drills: [],
    index: 0,
    attempts: 0,
    solved: false,
    revealed: false,
  };

  const el = {};

  function $(id) { return document.getElementById(id); }

  function currentDrill() { return state.drills[state.index]; }

  function t() { return STRINGS[state.lang]; }

  function appendLine(text, cls) {
    const line = document.createElement('div');
    line.className = 'term-line' + (cls ? ' ' + cls : '');
    line.textContent = text;
    el.log.appendChild(line);
    el.log.scrollTop = el.log.scrollHeight;
  }

  function renderTaskHeader() {
    const n = state.drills.length;
    const drill = currentDrill();
    el.taskLabel.textContent = t().taskLabel(state.index + 1, n);
    el.taskPrompt.textContent = drill.prompt[state.lang] || drill.prompt.en;
  }

  function resetTaskState() {
    state.attempts = 0;
    state.solved = false;
    state.revealed = false;
    el.log.innerHTML = '';
    renderTaskHeader();
    appendLine(`# ${t().promptIntro} ${currentDrill().prompt[state.lang] || currentDrill().prompt.en}`, 'term-tasknote');
    el.input.value = '';
    el.input.disabled = false;
    el.input.focus();
    el.nextBtn.hidden = true;
  }

  function loadDrill(idx) {
    state.index = idx;
    resetTaskState();
  }

  function goNext() {
    if (state.index + 1 < state.drills.length) {
      loadDrill(state.index + 1);
    } else {
      appendLine(t().allDone, 'term-alldone');
      el.input.disabled = true;
      el.nextBtn.hidden = true;
    }
  }

  function handleSubmit() {
    const raw = el.input.value;
    if (!raw.trim() || state.solved) return;

    appendLine(`$ ${raw}`, 'term-echo');
    el.input.value = '';

    const drill = currentDrill();
    const result = window.KubectlDrillMatcher.checkCommand(raw, drill.accepted_grammar);

    if (result.success) {
      state.solved = true;
      appendLine(drill.success_message[state.lang] || drill.success_message.en, 'term-success');
      el.input.disabled = true;
      el.nextBtn.hidden = false;
      el.nextBtn.focus();
      return;
    }

    state.attempts += 1;

    if (state.attempts >= REVEAL_AFTER_ATTEMPTS) {
      state.revealed = true;
      appendLine(t().revealPrefix + ' ' + drill.reference_command, 'term-reveal');
      appendLine(t().revealFollow, 'term-reveal-note');
    } else if (state.attempts >= HINT_AFTER_ATTEMPTS) {
      appendLine(t().hintPrefix + ' ' + (drill.hint[state.lang] || drill.hint.en), 'term-hint');
    } else {
      appendLine(t().nudge, 'term-nudge');
    }
  }

  function toggleLang() {
    state.lang = state.lang === 'en' ? 'de' : 'en';
    el.langBtn.textContent = t().langBtn;
    el.input.placeholder = t().inputPlaceholder;
    el.simBadge.textContent = t().simulatedBadge;
    el.nextBtn.textContent = t().nextTask;
    renderTaskHeader();
  }

  function init(drills) {
    el.taskLabel = $('task-label');
    el.taskPrompt = $('task-prompt');
    el.log = $('term-log');
    el.input = $('term-input');
    el.nextBtn = $('next-btn');
    el.langBtn = $('lang-btn');
    el.simBadge = $('sim-badge');

    state.drills = drills;

    el.simBadge.textContent = t().simulatedBadge;
    el.input.placeholder = t().inputPlaceholder;
    el.nextBtn.textContent = t().nextTask;
    el.langBtn.textContent = t().langBtn;

    el.input.addEventListener('keydown', (ev) => {
      if (ev.key === 'Enter') {
        ev.preventDefault();
        handleSubmit();
      }
    });
    el.nextBtn.addEventListener('click', goNext);
    el.langBtn.addEventListener('click', toggleLang);

    // Keep focus on the input whenever the terminal window is clicked,
    // mimicking a real terminal — but don't steal focus from the Next
    // button or language toggle.
    $('term-window').addEventListener('click', (ev) => {
      if (ev.target === el.input || ev.target === el.nextBtn || ev.target === el.langBtn) return;
      if (!el.input.disabled) el.input.focus();
    });

    loadDrill(0);
  }

  // drills.sample.json is loaded via fetch() when served over http(s); when
  // opened as a bare file:// URL, fetch() of local JSON is blocked by browser
  // CORS policy in some browsers (notably Chrome) even for same-directory
  // files. So the sample data is ALSO inlined as a fallback constant below —
  // this keeps the "open the HTML file directly, zero network requests"
  // offline claim true across browsers without depending on fetch-from-disk
  // behavior that varies by browser. The real integration will fetch this
  // from app/data/... like every other content file in this app already does.
  fetch('drills.sample.json')
    .then(r => r.json())
    .then(data => init(data.drills))
    .catch(() => init(window.KUBECTL_DRILLS_FALLBACK.drills));
})();
