"""Pipeline orchestration logic."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import pandas as pd

from funds_etl.configuration import Settings
from funds_etl.contracts import Extractor, Loader
from funds_etl.transformers.tourism_transformer import TourismTransformer


@dataclass
class PipelineResult:
    """Represents the result of running the ETL pipeline."""

    combined_frame: pd.DataFrame
    manifest: Dict[str, str]


class TourismETLPipeline:
    """Coordinates the ETL workflow for the tourism datasets."""

    def __init__(
        self,
        *,
        settings: Settings,
        extractor: Extractor,
        transformer: TourismTransformer,
        loader: Loader,
    ) -> None:
        self._settings = settings
        self._extractor = extractor
        self._transformer = transformer
        self._loader = loader

    def run(self) -> PipelineResult:
        normalized_frames: List[pd.DataFrame] = []
        manifest: Dict[str, str] = {
            "project": self._settings.project_name,
            "owner": self._settings.owner,
        }

        for dataset_name, dataset_settings in self._settings.datasets.items():
            source_path = self._settings.raw_data_dir / dataset_settings.filename
            raw_frame = self._extractor.extract(source_path)
            transformed = self._transformer.transform(dataset_name, raw_frame)
            transformed = transformed.assign(dataset_name=dataset_name)
            self._loader.persist_dataset(dataset_name, transformed)
            normalized_frames.append(transformed)

        combined_frame = pd.concat(normalized_frames, ignore_index=True)
        self._loader.finalize(combined_frame, manifest)
        return PipelineResult(combined_frame=combined_frame, manifest=manifest)
