from __future__ import annotations

from hashlib import sha256
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlparse

from romeo_crt_engine.storage.contracts import ArtifactRef


class LocalArtifactStore:
    """Filesystem implementation of the Phase-0 immutable ArtifactStore contract."""

    def __init__(self, root: Path) -> None:
        self._root = root.resolve()
        self._root.mkdir(parents=True, exist_ok=True)

    def _path_for_key(self, key: str) -> Path:
        relative = PurePosixPath(key)
        if not key or relative.is_absolute() or ".." in relative.parts:
            raise ValueError("artifact key must be a non-empty relative path without '..'")
        path = (self._root / Path(*relative.parts)).resolve()
        if self._root not in path.parents and path != self._root:
            raise ValueError("artifact key escapes store root")
        return path

    def put_bytes(self, key: str, payload: bytes, media_type: str) -> ArtifactRef:
        if not media_type:
            raise ValueError("media_type must not be empty")
        digest = sha256(payload).hexdigest()
        path = self._path_for_key(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            existing = path.read_bytes()
            if existing != payload:
                raise ValueError(f"immutable artifact already exists with different bytes: {key}")
        else:
            path.write_bytes(payload)
        return ArtifactRef(
            uri=path.as_uri(),
            sha256=digest,
            size_bytes=len(payload),
            media_type=media_type,
        )

    def read_bytes(self, ref: ArtifactRef) -> bytes:
        parsed = urlparse(ref.uri)
        if parsed.scheme != "file":
            raise ValueError("LocalArtifactStore can only read file:// artifact references")
        path = Path(unquote(parsed.path)).resolve()
        if self._root not in path.parents and path != self._root:
            raise ValueError("artifact reference is outside store root")
        payload = path.read_bytes()
        if sha256(payload).hexdigest() != ref.sha256 or len(payload) != ref.size_bytes:
            raise ValueError("artifact integrity verification failed")
        return payload
