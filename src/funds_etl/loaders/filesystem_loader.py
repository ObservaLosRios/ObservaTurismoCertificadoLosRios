"""Loader that writes datasets to the local filesystem."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Dict, List

import pandas as pd

from funds_etl.contracts import Loader
from funds_etl.entities import DatasetArtifact


class FileSystemLoader(Loader):
    """Writes processed datasets and manifests to disk."""

    def __init__(
        self,
        *,
        output_dir: Path,
        unified_filename: str,
        manifest_filename: str,
    ) -> None:
        self._output_dir = output_dir
        self._unified_filename = unified_filename
        self._manifest_filename = manifest_filename
        self._artifacts: List[DatasetArtifact] = []
        self._output_dir.mkdir(parents=True, exist_ok=True)

    def persist_dataset(self, dataset_name: str, frame: pd.DataFrame) -> Path:
        output_path = self._output_dir / f"{dataset_name}.csv"
        frame.to_csv(output_path, index=False)
        artifact = DatasetArtifact(
            dataset_name=dataset_name,
            path=str(output_path.relative_to(self._output_dir.parent)),
            row_count=len(frame),
        )
        self._artifacts.append(artifact)
        return output_path

    def finalize(self, combined_frame: pd.DataFrame, manifest: Dict[str, str]) -> None:
        combined_path = self._output_dir / self._unified_filename
        combined_frame.to_csv(combined_path, index=False)

        manifest_payload = {
            "generated_at": datetime.now(UTC).isoformat(),
            "artifacts": [artifact.__dict__ for artifact in self._artifacts],
            "metadata": manifest,
        }

        manifest_path = self._output_dir / self._manifest_filename
        with manifest_path.open("w", encoding="utf-8") as stream:
            json.dump(manifest_payload, stream, ensure_ascii=False, indent=2)
