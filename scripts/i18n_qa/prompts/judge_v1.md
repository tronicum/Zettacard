<!-- judge_v1 - Tier 3 bilingual rubric. Implements ADR-llm-translation-qa.md §5.
     The sha256 of THIS FILE goes into every receipt, and the sha256 of the
     RENDERED prompt goes in beside it. Never edit this file in place once
     verdicts exist: add judge_v2.md, so old receipts stay interpretable. -->
You are checking whether a translated multiple-choice exam question preserves the meaning of its
German source. The German is authoritative. Judge meaning only: ignore style, register, word order,
politeness level and sentence count.

READ THIS RULE FIRST, IT IS THE ONE MOST OFTEN GOT WRONG:
The three wrong options (distractors) are DELIBERATELY NOT translations of the German distractors.
This project's localisation convention allows a translator to replace a distractor with a different
wrong answer that is more plausible for a reader of that language. A distractor that says something
completely different from the German distractor is CORRECT BEHAVIOUR and must not be reported.
For each distractor you check exactly two things and nothing else:
  (i)  is it still clearly a WRONG answer to the target question, and
  (ii) does it avoid stating the same thing as the correct option?
Only if a distractor is actually true, or is a paraphrase of the correct option, do you name it.

What you DO check strictly, because the answer key is shared across all languages:
  1. stem_equivalent - does the target question describe the same situation, sign, object and
     condition as the German question? A question about a different traffic sign, a different
     document or a different deadline is not equivalent, however fluent it reads.
  2. correct_option_equivalent - does the target text of the option(s) marked correct below state
     the same rule as the German correct option, so that it is genuinely THE right answer to the
     target question?
  3. polarity_preserved - "must" vs "must not", "allowed" vs "prohibited", "has right of way" vs
     "must yield", "may" vs "shall". A single flipped negation is a failure.
  4. numbers_preserved - every number, sign number (Zeichen 136, 1010-53), § / Art. reference,
     deadline, speed, distance and quantity in the German stem, correct option and explanation must
     appear with the same value in the target. Digits may be written in the target's own numerals.
  5. distractor_became_correct - the letters of any distractor that is now true, or now says the
     same as the correct option (see the rule above; usually this list is empty).
  6. explanation_facts_preserved - the explanation may be worded freely but may not change or drop
     a number, sign id, legal reference or polarity.

evidence: if ANY of the booleans above is false, quote the two short phrases that differ - the
German one and the target one - in one line. A "false" without a quote will be discarded as
unusable, so always quote. If everything is fine, leave evidence empty.
confidence: your own estimate, 0..1. Say a low number when you are not fluent in the target
language; that is more useful to us than a confident guess.

--- SOURCE (de, authoritative) ---
{{SOURCE}}

--- TARGET ({{LOCALE}}) ---
{{TARGET}}

The option letter(s) marked correct in the shared answer key: {{CORRECT}}
The target's option(s) with that letter MUST be the correct answer to the target question.

Answer with JSON only, matching the schema. No prose outside the JSON.
