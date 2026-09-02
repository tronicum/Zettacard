// kubectl-drill matching engine (PROTOTYPE)
//
// Pure functions, no DOM access, no globals besides the KubectlDrillMatcher
// namespace below — written so this file (or its contents) can be copy-pasted
// almost verbatim into app/app.js during the later integration step. No
// dependencies, no network calls, works from a file:// URL.
//
// Grammar shape (matches data/cka_kubectl_drills.json, see docs note there):
//   accepted_grammar: {
//     base_command:        [string, ...]   // ordered verb/noun path, e.g. ["kubectl","get","pods"]
//     required_tokens:     [string, ...]   // each MUST be present somewhere (order-independent)
//     alternative_groups:  [[string,...], ...] // for each group, AT LEAST ONE member must be present
//     optional_tokens:     [string, ...]   // documentation only — never affects scoring, listed so
//                                          // content authors can note "these are also fine" without
//                                          // the matcher treating them as required
//   }
//
// A "unit" (used in required_tokens / alternative_groups entries) is itself a
// string that may contain multiple words, e.g. "-n kube-system" or "--follow".
// It is satisfied when its own tokens appear CONTIGUOUSLY, IN ORDER, anywhere
// in the learner's (expanded) token stream — see unitPresent().
//
// base_command tokens, by contrast, only need to appear IN ORDER but NOT
// necessarily contiguously, because real kubectl lets global flags land
// between them (`kubectl -n kube-system get pods` is as valid as
// `kubectl get pods -n kube-system`).

(function (root) {
  'use strict';

  // ---- tokenizer -----------------------------------------------------

  // Splits on whitespace but keeps single- or double-quoted spans intact,
  // e.g.  kubectl label pod x "foo=bar baz"  ->  [...,'foo=bar baz']
  function tokenizeCommand(raw) {
    const tokens = [];
    const re = /"([^"]*)"|'([^']*)'|(\S+)/g;
    let m;
    while ((m = re.exec(raw)) !== null) {
      tokens.push(m[1] !== undefined ? m[1] : (m[2] !== undefined ? m[2] : m[3]));
    }
    return tokens;
  }

  // kubectl accepts both `--flag=value` and `--flag value`. Expand the
  // `=` form into two tokens so both spellings compare equal downstream.
  // Also folds the common `k` shell alias for `kubectl` into the real word,
  // but ONLY as the very first token (so a resource literally named "k"
  // elsewhere in the command is untouched).
  function expandTokens(tokens) {
    const out = [];
    tokens.forEach((t, i) => {
      if (i === 0 && t.toLowerCase() === 'k') {
        out.push('kubectl');
        return;
      }
      const m = /^(--?[A-Za-z][\w-]*)=(.+)$/.exec(t);
      if (m) {
        out.push(m[1], m[2]);
      } else {
        out.push(t);
      }
    });
    return out;
  }

  function unitTokens(unitString) {
    return expandTokens(tokenizeCommand(unitString));
  }

  // Does `needle` (array of tokens) appear as a contiguous, case-insensitive
  // run inside `haystack` (array of tokens)?
  function containsContiguous(haystack, needle) {
    if (needle.length === 0) return true;
    outer:
    for (let i = 0; i + needle.length <= haystack.length; i++) {
      for (let j = 0; j < needle.length; j++) {
        if (haystack[i + j].toLowerCase() !== needle[j].toLowerCase()) continue outer;
      }
      return true;
    }
    return false;
  }

  function unitPresent(expandedHaystack, unitString) {
    return containsContiguous(expandedHaystack, unitTokens(unitString));
  }

  // base_command: each token must be found, in order, scanning forward —
  // tokens may have other tokens (flags, values) between them.
  function baseCommandPresent(expandedHaystack, baseTokens) {
    let searchFrom = 0;
    for (const bt of baseTokens) {
      let found = -1;
      for (let i = searchFrom; i < expandedHaystack.length; i++) {
        if (expandedHaystack[i].toLowerCase() === bt.toLowerCase()) { found = i; break; }
      }
      if (found === -1) return false;
      searchFrom = found + 1;
    }
    return true;
  }

  // ---- grammar check ---------------------------------------------------

  // Returns a result object; never throws on malformed grammar (missing
  // arrays default to empty).
  function checkCommand(rawInput, grammar) {
    grammar = grammar || {};
    const baseCommand = grammar.base_command || [];
    const requiredTokens = grammar.required_tokens || [];
    const altGroups = grammar.alternative_groups || [];

    const tokens = tokenizeCommand((rawInput || '').trim());
    const expanded = expandTokens(tokens);

    const baseOk = baseCommandPresent(expanded, baseCommand);

    const requiredMissing = requiredTokens.filter(u => !unitPresent(expanded, u));

    const altGroupMissing = [];
    altGroups.forEach((group, idx) => {
      const satisfied = group.some(u => unitPresent(expanded, u));
      if (!satisfied) altGroupMissing.push({ index: idx, options: group });
    });

    const success = baseOk && requiredMissing.length === 0 && altGroupMissing.length === 0;

    // Rough 0..1 "how close" score, used only to pick a friendlier nudge —
    // never shown to the learner as a number, never used to decide success.
    const totalUnits = 1 /* base_command counts as one unit */ + requiredTokens.length + altGroups.length;
    const satisfiedUnits =
      (baseOk ? 1 : 0) +
      (requiredTokens.length - requiredMissing.length) +
      (altGroups.length - altGroupMissing.length);
    const score = totalUnits === 0 ? 1 : satisfiedUnits / totalUnits;

    return {
      raw: rawInput,
      tokens,
      expanded,
      baseOk,
      requiredMissing,
      altGroupMissing,
      success,
      score,
    };
  }

  root.KubectlDrillMatcher = {
    tokenizeCommand,
    expandTokens,
    unitPresent,
    baseCommandPresent,
    checkCommand,
  };
})(typeof window !== 'undefined' ? window : globalThis);
