from __future__ import annotations

import argparse
import json
from pathlib import Path

from romeo_crt_engine.research.registry_v1 import (
    get_registered_source_v1,
    load_source_registry_v1,
    source_identity_from_registry_v1,
)
from romeo_crt_engine.research.source_acquisition_v1 import (
    AcquisitionStatus,
    CaptureKind,
    SourceAcquisitionManifestV1,
    SourceArtifactV1,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "research/romeo/SOURCE_REGISTRY.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a registry-bound Phase-6D manifest for a first-party artifact."
    )
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--capture-file", type=Path, required=True)
    parser.add_argument("--capture-kind", choices=[item.value for item in CaptureKind], required=True)
    parser.add_argument("--content-type", required=True)
    parser.add_argument("--locator", required=True)
    parser.add_argument("--notes", required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    registry = load_source_registry_v1(args.registry)
    registered = get_registered_source_v1(registry, args.source_id)
    source = source_identity_from_registry_v1(registered)
    payload = args.capture_file.read_bytes()
    artifact = SourceArtifactV1.from_bytes(
        source_id=source.source_id,
        capture_kind=CaptureKind(args.capture_kind),
        payload=payload,
        content_type=args.content_type,
        locator=args.locator,
    )
    manifest = SourceAcquisitionManifestV1(
        source=source,
        status=AcquisitionStatus.CAPTURED,
        artifacts=(artifact,),
        notes=args.notes,
    )
    record = manifest.canonical_record()
    record["manifest_sha256"] = manifest.digest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(manifest.digest())


if __name__ == "__main__":
    main()
