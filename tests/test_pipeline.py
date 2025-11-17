"""Integration test for the tourism ETL pipeline."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from funds_etl.configuration import DatasetSettings, Settings
from funds_etl.extractors.csv_extractor import CSVExtractor
from funds_etl.loaders.filesystem_loader import FileSystemLoader
from funds_etl.pipeline import TourismETLPipeline
from funds_etl.transformers.tourism_transformer import TourismTransformer


def _write_csv(path: Path, rows: list[dict]) -> None:
    frame = pd.DataFrame(rows)
    frame.to_csv(path, index=False)


def _build_settings(raw_dir: Path, processed_dir: Path) -> Settings:
    dataset = DatasetSettings(
        name="regiones",
        filename="regiones.csv",
        metric_group="Regiones",
        category_field="region",
        value_field="recuento",
        percentage_field=None,
        highlight_field=None,
        highlight_percentage_field=None,
    )
    return Settings(
        project_name="Test",
        owner="CI",
        raw_data_dir=raw_dir,
        processed_data_dir=processed_dir,
        datasets={dataset.name: dataset},
        unified_metrics_filename="combined.csv",
        dataset_manifest_filename="manifest.json",
    )


def test_pipeline_generates_processed_files(tmp_path: Path) -> None:
    raw_dir = tmp_path / "data" / "raw"
    processed_dir = tmp_path / "data" / "processed"
    raw_dir.mkdir(parents=True)

    _write_csv(
        raw_dir / "regiones.csv",
        rows=[{"region": "Los Ríos", "recuento": 10}, {"region": "Lagos", "recuento": 5}],
    )

    settings = _build_settings(raw_dir, processed_dir)
    pipeline = TourismETLPipeline(
        settings=settings,
        extractor=CSVExtractor(),
        transformer=TourismTransformer(settings.datasets),
        loader=FileSystemLoader(
            output_dir=settings.processed_data_dir,
            unified_filename=settings.unified_metrics_filename,
            manifest_filename=settings.dataset_manifest_filename,
        ),
    )

    result = pipeline.run()

    combined_path = processed_dir / settings.unified_metrics_filename
    manifest_path = processed_dir / settings.dataset_manifest_filename
    dataset_path = processed_dir / "regiones.csv"

    assert dataset_path.exists()
    assert combined_path.exists()
    assert manifest_path.exists()
    assert len(result.combined_frame) == 2
