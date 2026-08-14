from __future__ import annotations

import argparse
import json
from pathlib import Path

from romeo_crt_engine.research.source_acquisition_v1 import (
    AcquisitionStatus,
    CaptureKind,
    SourceAcquisitionManifestV1,
    SourceArtifactV1,
    SourceIdentityV1,
    SourceKind,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a credential-free Phase-6D manifest for a captured first-party artifact."
    )
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--source-kind", choices=[item.value for item in SourceKind], required=True)
    parser.add_argument("--provenance", required=True)
    parser.add_argument("--capture-file", type=Path, required=True)
    parser.add_argument("--capture-kind", choices=[item.value for item in CaptureKind], required=True)
    parser.add_argument("--content-type", required=True)
    parser.add_argument("--locator", required=True)
    parser.add_argument("--notes", required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = args.capture_file.read_bytes()
    source = SourceIdentityV1(
        source_id=args.source_id,
        url=args.url,
        source_kind=SourceKind(args.source_kind),
        provenance_statement=args.provenance,
    )
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
