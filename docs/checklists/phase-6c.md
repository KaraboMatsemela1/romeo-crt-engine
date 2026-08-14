# Phase 6C — CRTology Evidence & Candidate Selection Checklist

**Status:** **IN PROGRESS — PRIMARY-SOURCE EVIDENCE GATE**  
**Doctrine stream:** `CRTOLOGY_2026_RESEARCH`  
**Primary source:** `ROMEO-2026-CRTOLOGY-01` — `CRTology episode 1: SS`  
**New alpha candidate:** **NOT SELECTED**  
**Phase 7:** **BLOCKED**

## A. Preserve completed research history

- [x] Preserve Phase-6 v0.1 `INSUFFICIENT_EVIDENCE` unchanged.
- [x] Preserve Phase-6B `INSUFFICIENT_MULTI_MARKET_SAMPLE` unchanged.
- [x] Preserve the 4/4 trusted OANDA dataset result.
- [x] Preserve the 7 pooled TradePlans / required 30 activity result.
- [x] Keep v0.1 OOS unopened.
- [x] Keep v0.1 CONFIRM unopened.
- [x] Prohibit threshold reduction to repair Phase 6B.
- [x] Prohibit parameter tuning against opened activity evidence.
- [x] Prohibit post-count instrument cherry-picking.
- [x] Keep P&L, paper, shadow and live unauthorized.

## B. 2026 doctrine version boundary

- [x] Keep `CRT_SECRETS_2025` historical rules versioned and immutable.
- [x] Quarantine new material under `CRTOLOGY_2026_RESEARCH` until reconciled.
- [x] Require every 2026 delta to be classified as clarification/refinement/new branch/superseding/non-alpha/unresolved.
- [x] Prohibit silently rewriting v0.1/v0.2 rules with 2026 material.

## C. CRTology Episode 1 source gate

- [x] Confirm source/video ID `4DZWbCzEvhM`.
- [x] Confirm first-party publication provenance.
- [x] Confirm title `CRTology episode 1: SS`.
- [x] Record that the source was previously only `DISCOVERED` in the registry.
- [ ] Capture direct transcript/captions or equivalent first-party technical frames.
- [ ] Establish Romeo's explicit meaning of `SS`.
- [ ] Identify whether `SS` is alpha, context, timing/session, entry, management, or non-alpha material.
- [ ] Extract deterministic required inputs.
- [ ] Freeze information-availability timestamp.
- [ ] Freeze direction/timeframe semantics.
- [ ] Freeze confirmation/invalidation/expiry if applicable.
- [ ] Capture positive examples.
- [ ] Capture negative/counterexamples.
- [ ] Map the rule against `CRT_SECRETS_2025`.
- [ ] Close Gate 6C-1 as `TECHNICAL_SOURCE_CAPTURE_SUFFICIENT` or `TECHNICAL_SOURCE_CAPTURE_INSUFFICIENT`.

## D. Candidate selection — locked until Gate 6C-1/2/3

- [ ] Complete semantic extraction for any source-supported `SS` rule.
- [ ] Reconcile contradictions/refinements against the frozen 2025 doctrine.
- [ ] Determine whether there is a legitimate executable delta.
- [ ] If no executable delta exists, record that result without forcing a candidate.
- [ ] If an executable delta exists, select exactly one narrow research hypothesis.
- [ ] Freeze inherited rules versus changed rules.
- [ ] Freeze excluded rules.
- [ ] Freeze exact market universe before detector counts.
- [ ] Freeze timeframe/calendar/data requirements.
- [ ] Freeze activity threshold and access protocol before outcomes.

## E. Implementation — not yet authorized

- [ ] Create a new strategy version only after candidate precommitment.
- [ ] Create positive/negative fixtures before historical detector outcomes.
- [ ] Implement without mutating v0.1/v0.2 historical code paths.
- [ ] Prove deterministic fixture parity.
- [ ] Preregister detector-only activity protocol.
- [ ] Keep backtester/P&L closed until a separate future gate permits access.

## Current handoff

```text
Phase 6C                         IN PROGRESS — PRIMARY-SOURCE EVIDENCE GATE
Branch                           agent/phase-6c-crtology-evidence
Doctrine stream                  CRTOLOGY_2026_RESEARCH
Primary source                   ROMEO-2026-CRTOLOGY-01
Source identity                  CONFIRMED
Technical meaning of SS          UNRESOLVED
New alpha candidate              NOT SELECTED
Alpha implementation             NOT AUTHORIZED
Detector activity                NOT AUTHORIZED
Backtest / P&L                   NOT AUTHORIZED
v0.1 OOS / CONFIRM               UNOPENED
Phase 7                          BLOCKED
Live trading                     NOT AUTHORIZED
```
