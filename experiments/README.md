# Experiment Convention

Every experiment must be reproducible and must not overwrite prior results.

Create one directory per experiment ID, for example:

```text
experiments/
  EXP-2026-0001/
    manifest.json
    README.md
    artifacts/
```

The manifest must record at minimum:

- experiment ID and hypothesis;
- exploratory or confirmatory classification;
- frozen strategy version and freeze-parameter version;
- git commit SHA;
- dataset ID/version/manifest digest;
- instruments and exact time range;
- provider/venue metadata where relevant;
- cost, spread, slippage and fill assumptions;
- all strategy-adjacent experiment parameters;
- random seed when applicable;
- generated metrics/artifact references;
- conclusion, limitations and negative findings.

Rules:

1. Do not overwrite a completed experiment. Create a new experiment ID.
2. Do not modify a frozen strategy in place because an experiment performs poorly.
3. Final out-of-sample windows must not be repeatedly reused for parameter selection.
4. Large generated artifacts stay out of Git and are referenced through integrity metadata.
5. Failed and inconclusive experiments are first-class records.
6. Paper, shadow and live observations must be clearly separated from historical simulation.

Generated files under `artifacts/` are intentionally ignored by Git; manifests and conclusions should remain version controlled.
