# Phase 1 Research Log

## 2026-08-12 — Pass 1: corpus discovery

Phase 1 has started. This pass establishes a provenance-first inventory of Romeo / @Romeotpt public material before any strategy rules are promoted into the formal CRT specification.

### Research rules for this phase

1. Prefer Romeo's own YouTube/Telegram/X material as primary evidence.
2. Third-party summaries may be used for discovery and provisional notes only.
3. A trading rule cannot become `VERIFIED` from a third-party summary alone.
4. Preserve video IDs, titles, dates, durations, timestamps and contradictions.
5. Separate claims made by the source from facts independently established by this project.
6. Do not use profitability claims as evidence that a rule is valid.
7. Do not code candidate strategy logic until its required semantics are sufficiently resolved.

### Initial corpus discovery

Current discovery identified the original 2024 foundation videos, the 2025 `CRT Secrets` public mentorship series through episode 10, a live tape-reading session, and a newer 2026 `CRTology` series beginning with `CRTology episode 1: SS`.

The source registry is the machine-readable inventory. Items marked `DISCOVERED` still require a transcript/direct-video evidence pass before rule promotion.

### First high-value research targets

1. `What is CRT? Why do all other trading strategies suck?`
2. `CRT secrets ep.1: One CRT model for life`
3. `CRT secrets 3: The journey`
4. `CRT secrets 4: Candle anatomy`
5. `CRT secrets ep.5: Key level`
6. `CRT secrets ep.6: SMT`
7. `CRT secrets ep.7: Candle 3`
8. `CRT secrets ep.8: When does CRT fail?`
9. `CRT secrets ep.9: Connecting the dots`
10. `CRTology episode 1: SS`

These are prioritized because together they appear to define the object model (candle/range), setup sequence, timeframe relationship, context/key-level selection, confirmation, failure modes, and trade framing.

### Provisional concepts observed during discovery

These are hypotheses awaiting direct-source verification:

- Every candle is treated as a range.
- A candle/range can resolve through breakout or a Turtle Soup-type purge/rejection; inside bars require separate handling.
- CRT is described as fractal across timeframes.
- Candle 1 / Candle 2 / Candle 3 are associated with accumulation / manipulation / distribution.
- Romeo repeatedly emphasizes selecting the candle/range first, then using context rather than trading patterns blindly.
- Higher-timeframe context is paired with lower-timeframe execution/confirmation.
- The 50% level of a CRT range is repeatedly referenced as an important target/reaction level.
- Model #1, Turtle Soup, Kiss of Death, true market-structure shift, key levels and SMT are recurring components of the public system.
- Time is repeatedly described as more important than price; exact time rules remain unresolved.

None of the above is production logic yet.

### Known evidence-quality limitations

- The public YouTube channel HTML is difficult to enumerate directly through the current research interface.
- Video Highlight exposes YouTube metadata and AI-generated summaries for many videos; these summaries are useful for discovery but explicitly warn that they may be inaccurate.
- Romeo's public Telegram provides direct YouTube links/IDs for several videos and therefore serves as stronger provenance for existence/title association.
- Some exact publication dates/durations still need direct metadata confirmation.

### Next pass

Perform timestamped evidence extraction for the foundation videos and CRT Secrets episodes, beginning with `What is CRT?`, then create candidate rule records with confidence and contradictions. Do not freeze `CRT-v0.1` until this evidence pass is complete.

---

## 2026-08-12 — Pass 2: Turtle Soup foundation

Analyzed `ROMEO-2024-TS — What is turtle soup?` using indexed timestamped transcript/summary material.

### Result

The safest source-supported abstraction is:

```text
reference prior extreme
      ↓
price excursions beyond it
      ↓
continuation fails
      ↓
price reverses away
```

Bearish and bullish variants are mirror images around an old high / old low.

### Important boundary

This video does **not** yet provide enough deterministic detail to implement a production entry. Exact reference-extreme eligibility, timing, confirmation, entry, stop and target rules remain unresolved.

### Repository changes

- Added `research/romeo/videos/ROMEO-2024-TS.md`
- Updated `GLOSSARY.md`
- Expanded `OPEN_QUESTIONS.md`
- Marked `ROMEO-2024-TS` as `EVIDENCE_PASS_1` in the source registry
- Created provisional candidates `TS-P001` through `TS-P007`

### Architectural consequence

Treat Turtle Soup as a **structural primitive** that later CRT context and execution models constrain, not as the entire strategy by itself.

### Next source

`ROMEO-2025-S2 — CRT secrets episode 2: The kiss of death` is the next evidence target because it explicitly presents Kiss of Death as a Turtle Soup model and should clarify how a structural sweep is converted into an actionable CRT setup.

---

## 2026-08-12 — Pass 3: Kiss of Death

Analyzed `ROMEO-2025-S2 — CRT secrets episode 2: The kiss of death`.

### Result

Kiss of Death is source-backed as a specialized Turtle Soup within an already-active CRT journey. The demonstrated bearish path links Candle 1 range selection, movement through the range, a late Turtle Soup, optional FVG/old-high confluence, lower-timeframe Model #1 execution, 50% as an intermediate objective, and the opposite CRT extreme as a later objective.

### Critical validation finding

Romeo describes KOD as the **final Turtle Soup before the target is hit**. That wording is not directly safe to code because identifying the final event retrospectively would leak future information into historical signals.

Therefore `last_turtle_soup_before_target` is explicitly prohibited as a backtest classifier. Later sources must provide real-time qualifying conditions that allow a KOD candidate to be recognized before the target is reached.

### Repository changes

- Added `research/romeo/videos/ROMEO-2025-S2.md`
- Updated `GLOSSARY.md` with KOD, Candle 1/2/3, CRT 50%, opposite CRT extreme and FVG-confluence terms
- Expanded `OPEN_QUESTIONS.md` with KOD-specific and look-ahead-bias questions
- Marked `ROMEO-2025-S2` as `EVIDENCE_PASS_1` in `SOURCE_REGISTRY.csv`
- Created provisional candidates `KOD-P001` through `KOD-P010`

### Architectural consequence

The emerging decomposition is:

```text
parent CRT context
      ↓
Turtle Soup / KOD candidate
      ↓
confluence
      ↓
LTF entry model
      ↓
independent risk
      ↓
target management
```

KOD detection and Model #1 entry detection must remain separate modules.

### Next source

`ROMEO-2025-S3 — CRT secrets 3: The journey` should be analyzed next because it is the most likely source to clarify Candle 1→2→3 sequencing, target progression, and the ex-ante state needed to distinguish a late KOD from an arbitrary Turtle Soup.
