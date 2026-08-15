from __future__ import annotations

import hashlib
import json
from pathlib import Path

from audit_phase6d_corpus_migration import _load_corpus_index, _load_ledger, _load_manifest

from romeo_crt_engine.research.registry_v1 import load_source_registry_v1

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research/romeo/phase6d"
INVENTORY = BASE / "RECOVERY_007_ACQUISITION_INVENTORY.json"
RECORDS = BASE / "RECOVERY_007_EVIDENCE_RECORDS.json"
PAYLOADS = BASE / "payloads"
ACQUISITIONS = BASE / "acquisitions"

RAW = {
    "ROMEO-2025-S1": ("a54782c7f52b6ec9a09507a711fb6ef689ecd98f6e4147444fbf630c2f363bf2", 398017),
    "ROMEO-2025-S9": ("2bfb5365e44e720bd0408f0072392b821a036d0711b7663bae6751a9d3876d3c", 264058),
    "ROMEO-2025-S6": ("84cd28204ecbceead265bee09ee9c29f6fd5b52ff38aa67e19d987f03b62c825", 366643),
    "ROMEO-2026-CRTOLOGY-01": ("81fbfc871567ea9580d439f736cda8304f7d39898139e8b909d6557d13d11d56", 313992),
    "ROMEO-2024-TS": ("0e85576aba75bcc038dcceb5a7db3c6d12cf1efe43c3ffd75d0f16715b60478b", 268799),
    "ROMEO-2025-S5": ("6058fa91b1e7f5060e5e38b7bc96f4f9fa85870d4ec4c254937ef20ea99aadff", 225129),
}
VIDEO_IDS = {
    "ROMEO-2025-S1": "T7udbrWlARI",
    "ROMEO-2025-S9": "2sxdsgcIeYA",
    "ROMEO-2025-S6": "3IWgc52Dqsg",
    "ROMEO-2026-CRTOLOGY-01": "4DZWbCzEvhM",
    "ROMEO-2024-TS": "U-gNCwbGtTI",
    "ROMEO-2025-S5": "p8UYOgVn1-g",
}
EXPECTED_REGISTRY_SOURCE_IDS = frozenset((
    "ROMEO-2024-TS", "ROMEO-2024-CRT", "ROMEO-2025-S1", "ROMEO-2025-LIVE",
    "ROMEO-2025-S2", "ROMEO-2025-S3", "ROMEO-2025-S4", "ROMEO-2025-S5",
    "ROMEO-2025-S6", "ROMEO-2025-S7", "ROMEO-2025-S8", "ROMEO-2025-S9",
    "ROMEO-2025-S10", "ROMEO-2026-LIVE-02", "ROMEO-2026-CRTOLOGY-INTRO",
    "ROMEO-2026-CRTOLOGY-01", "ROMEO-2026-TG-TIME-TS-6361", "ROMEO-TG-MODEL1-6180",
    "ROMEO-TG-TS-6219", "ROMEO-TG-TS-D1-6221", "ROMEO-TG-KEYLEVEL-6273",
    "ROMEO-TG-KEYLEVEL-6274", "ROMEO-TG-KEYTIME-6289", "ROMEO-TG-KEYTIME-6290",
    "ROMEO-TG-BIAS-6357", "ROMEO-TG-SMT-PAIRS-6363", "ROMEO-TG-SMT-SUB-6520",
    "ROMEO-TG-EP9-SCOPE-6536", "ROMEO-TG-CRTOLOGY01-6905", "ROMEO-TG-SS-CONTEXT-6912",
    "ROMEO-TG-SS-NOFORCE-6914", "ROMEO-TG-TREND-6915",
))
REQUIRED = {
    "record_id", "source_id", "source_type", "first_party_provenance", "source_url", "title",
    "publication_date", "timestamp_or_location", "locator", "exact_romeo_statement_or_visual_evidence",
    "supported_predicate", "field", "coverage", "what_this_evidence_proves", "what_it_does_not_prove",
    "remaining_ambiguities", "confidence", "raw_timed_text_sha256", "artifact_sha256",
}


def main() -> None:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    if inventory.get("schema_version") != "P6D_RECOVERY_007_ACQUISITION_INVENTORY_V1":
        raise ValueError("unsupported Recovery 007 inventory schema")
    if inventory.get("classification") != "B_STRONG_NEW_EVIDENCE_BUT_PREDICATE_INCOMPLETE":
        raise ValueError("Recovery 007 classification changed")
    sources = inventory.get("sources")
    if not isinstance(sources, list) or {item.get("source_id") for item in sources} != set(RAW):
        raise ValueError("Recovery 007 must admit exactly the six known sources")
    inventory_by_source = {item["source_id"]: item for item in sources}
    registry_rows = load_source_registry_v1(ROOT / "research/romeo/SOURCE_REGISTRY.csv")
    registry_ids = [row.source_id for row in registry_rows]
    if len(registry_rows) != 32 or len(set(registry_ids)) != 32:
        raise ValueError("Recovery 007 registry must contain exactly 32 unique rows")
    if frozenset(registry_ids) != EXPECTED_REGISTRY_SOURCE_IDS:
        raise ValueError("Recovery 007 registry source-ID set differs from the HEAD baseline")
    registry = {row.source_id: row for row in registry_rows}
    for source_id, (digest, length) in RAW.items():
        item = inventory_by_source[source_id]
        if (item.get("raw_timed_text_sha256"), item.get("raw_timed_text_byte_length")) != (digest, length):
            raise ValueError(f"raw timed-text binding mismatch: {source_id}")
        filename = item.get("raw_timed_text_filename")
        if filename != f"{VIDEO_IDS[source_id]}.en.json3" or "/" in filename or "\\" in filename:
            raise ValueError(f"raw timed-text filename mismatch: {source_id}")
        local_raw = ROOT / ".local_acquisition" / filename
        if local_raw.exists():
            payload = local_raw.read_bytes()
            if (hashlib.sha256(payload).hexdigest(), len(payload)) != (digest, length):
                raise ValueError(f"local raw timed-text digest mismatch: {source_id}")
        if not isinstance(item.get("admitted_excerpt_artifacts"), list) or not item["admitted_excerpt_artifacts"]:
            raise ValueError(f"missing admitted artifacts: {source_id}")
        if registry[source_id].status != "ARTIFACT_CAPTURED_PARTIAL":
            raise ValueError(f"Recovery 007 registry status mismatch: {source_id}")

    raw_records = json.loads(RECORDS.read_text(encoding="utf-8"))
    records = raw_records.get("records")
    if not isinstance(records, list) or len(records) != 14:
        raise ValueError("Recovery 007 must contain exactly 14 evidence records")
    if len({record.get("record_id") for record in records}) != 14:
        raise ValueError("Recovery 007 record IDs must be unique")
    artifact_records: dict[str, dict[str, object]] = {}
    for record in records:
        if not REQUIRED.issubset(record):
            raise ValueError("Recovery 007 record required field missing")
        if record["source_id"] not in RAW or record["coverage"] != "PARTIAL":
            raise ValueError("Recovery 007 evidence must be admitted partial evidence")
        source = registry[record["source_id"]]
        if (
            record["source_url"],
            record["title"],
            record["publication_date"],
        ) != (source.url, source.title, source.published_date):
            raise ValueError("Recovery 007 record source metadata mismatch")
        if record["confidence"] not in {"DIRECT", "STRONG_PARTIAL", "CONTEXTUAL", "INSUFFICIENT"}:
            raise ValueError("unsupported Recovery 007 confidence")
        if record["confidence"] != "DIRECT" or record["raw_timed_text_sha256"] != RAW[record["source_id"]][0]:
            raise ValueError("Recovery 007 direct provenance binding mismatch")
        sha = record["artifact_sha256"]
        if not isinstance(sha, str) or sha in artifact_records:
            raise ValueError("Recovery 007 artifact binding must be unique")
        payload = (PAYLOADS / f"{sha}.txt").read_bytes()
        if hashlib.sha256(payload).hexdigest() != sha or not payload.endswith(b"\n"):
            raise ValueError("Recovery 007 payload digest mismatch")
        if payload.decode("utf-8").rstrip("\n") != record["exact_romeo_statement_or_visual_evidence"]:
            raise ValueError("Recovery 007 payload must be the exact minimal quoted evidence")
        if not record["locator"].startswith("https://www.youtube.com/watch?v=") or "#auto-en-json3-" not in record["locator"]:
            raise ValueError("Recovery 007 locator is not replayable json3 provenance")
        artifact_records[sha] = record
    if len(artifact_records) != 14:
        raise ValueError("Recovery 007 must bind fourteen payloads")

    corpus, _ = _load_corpus_index()
    corpus_by_source = {entry.source_id: entry for entry in corpus.entries}
    ledger = _load_ledger()
    ledger_artifacts = {e.artifact_sha256 for row in ledger.rows for e in row.evidence}
    for source_id, item in inventory_by_source.items():
        manifest, digest = _load_manifest(ACQUISITIONS / f"{source_id}.json")
        expected = {entry["artifact_sha256"] for entry in item["admitted_excerpt_artifacts"]}
        actual = {artifact.payload_sha256 for artifact in manifest.artifacts}
        if manifest.source.url != item["source_url"] or not expected.issubset(actual):
            raise ValueError(f"Recovery 007 manifest binding mismatch: {source_id}")
        corpus_artifacts = set(corpus_by_source[source_id].artifact_sha256s)
        if corpus_by_source[source_id].manifest_sha256 != digest or not expected.issubset(corpus_artifacts):
            raise ValueError(f"Recovery 007 corpus binding mismatch: {source_id}")
        for sha in expected:
            artifact = next((entry for entry in manifest.artifacts if entry.payload_sha256 == sha), None)
            record = artifact_records.get(sha)
            if artifact is None or record is None or artifact.locator != record["locator"] or artifact.byte_length != len((PAYLOADS / f"{sha}.txt").read_bytes()):
                raise ValueError(f"Recovery 007 artifact locator binding mismatch: {source_id}")
    if not set(artifact_records).issubset(ledger_artifacts):
        raise ValueError("Recovery 007 evidence was not integrated into predicate ledger")
    auth = inventory.get("authorizations", {})
    if any(auth.get(key) is not False for key in auth) or inventory.get("closing_field_evidence") != 0 or inventory.get("closed_predicates") != 0 or inventory.get("candidate_ready_rows") != 0 or inventory.get("issue_16_recommendation") != "KEEP_BLOCKED" or inventory.get("issue_37") != "MUST_NOT_START":
        raise ValueError("Recovery 007 safety disposition changed")
    print(json.dumps({"registry_rows": 32, "registry_unique_source_ids": 32, "raw_timed_text_sources": 6, "evidence_records": 14, "payloads": 14, "closing_field_evidence": 0, "closed_predicates": 0, "candidate_ready_rows": 0, **auth}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
