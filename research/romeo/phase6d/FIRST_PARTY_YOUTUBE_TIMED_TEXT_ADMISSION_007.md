# Phase 6D — First-Party YouTube Timed-Text Admission 007

**Date:** 2026-08-15
**Tracking:** Issue #16
**Classification:** **B — STRONG_NEW_EVIDENCE_BUT_PREDICATE_INCOMPLETE**

## Provenance and replay

Six direct official YouTube-generated English `json3` timed-text payloads were retrieved with `yt-dlp` from channel `Romeotpt` (`UCYCbFixbl2KcyLuH6cOfL2g`). Captions are ASR-derived first-party audio evidence: direct for the retrieved field text, but not independently audio/frame-verified.

```bash
yt-dlp --skip-download --write-info-json --write-auto-subs --sub-langs en --sub-format json3 --no-playlist -o "$DIR/$VIDEO_ID.%(ext)s" "https://www.youtube.com/watch?v=$VIDEO_ID"
```

| Source | Raw json3 SHA-256 | Bytes |
|---|---|---:|
| ROMEO-2025-S1 | a54782c7f52b6ec9a09507a711fb6ef689ecd98f6e4147444fbf630c2f363bf2 | 398017 |
| ROMEO-2025-S9 | 2bfb5365e44e720bd0408f0072392b821a036d0711b7663bae6751a9d3876d3c | 264058 |
| ROMEO-2025-S6 | 84cd28204ecbceead265bee09ee9c29f6fd5b52ff38aa67e19d987f03b62c825 | 366643 |
| ROMEO-2026-CRTOLOGY-01 | 81fbfc871567ea9580d439f736cda8304f7d39898139e8b909d6557d13d11d56 | 313992 |
| ROMEO-2024-TS | 0e85576aba75bcc038dcceb5a7db3c6d12cf1efe43c3ffd75d0f16715b60478b | 268799 |
| ROMEO-2025-S5 | 6058fa91b1e7f5060e5e38b7bc96f4f9fa85870d4ec4c254937ef20ea99aadff | 225129 |
## Evidence summary

Exactly 14 minimal, content-addressed caption excerpts are admitted in `RECOVERY_007_EVIDENCE_RECORDS.json`. They add direct partial support for Model #1, true MSS, SMT, SS, Turtle Soup, and key-level fields. No excerpt is `CLOSING`.

| Predicate | Status | Blocking fields |
|---|---|---|
| MODEL_1_GEOMETRY | STRONG_PARTIAL | old-extreme selector; numeric thick threshold; stop/buffer; ownership; invalidation/expiry |
| TRUE_MSS_ALGORITHM | STRONG_PARTIAL | swing construction; bearish form; timeframe; displacement; invalidation/expiry |
| SMT_EXECUTABLE_SEMANTICS | STRONG_PARTIAL | corresponding extremes; synchronization; polarity/traded leg; lifecycle |
| SS_MEANING_AND_CAUSAL_RULE | DIRECT_NON_ALPHA_CONTEXT | no trade-eligibility or causal alpha rule |
| TURTLE_SOUP_CONFIRMATION | STRONG_PARTIAL | qualifying extreme; close/wick confirmation; timeframe; invalidation/expiry |
| KEY_LEVEL_SELECTOR | STRONG_PARTIAL | selector/ranking; ownership; confirmation; invalidation/expiry |
| TIME_SELECTOR | OPEN_PARTIAL | timezone/DST; market/session scope; filter semantics; confirmation; expiry |

## Ambiguity and contradiction assessment

**Contradictions:** NONE ESTABLISHED. Close-trigger versus retrace language and Model #1 versus true-MSS language can describe alternative executions; they are not reconciled into a rule. Caption-sensitive wording remains subject to targeted audio/frame verification.

## Fixed disposition and safe next step

```text
PROPOSED_DETERMINISTIC_PREDICATE = NONE
CLOSING_FIELD_EVIDENCE           = 0
CLOSED_PREDICATES                = 0
CANDIDATE_READY_ROWS             = 0
INDEPENDENT_CLOSURE_AUDIT        = NOT_REQUESTED
ISSUE_16                         = KEEP_BLOCKED
ISSUE_37                         = MUST_NOT_START
CANDIDATE/DETECTOR/OUTCOME       = false
```

The safe next step is a bounded first-party audio/frame verification of predicate-critical caption wording, followed only by field-complete evidence review. No detector, count, backtest, P&L, OOS, CONFIRM, paper, or live path is authorized.
