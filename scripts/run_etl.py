"""Command-line entry point for the tourism ETL pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

from funds_etl.configuration import Settings, load_settings
from funds_etl.extractors.csv_extractor import CSVExtractor
from funds_etl.loaders.filesystem_loader import FileSystemLoader
from funds_etl.pipeline import TourismETLPipeline
from funds_etl.transformers.tourism_transformer import TourismTransformer


def build_pipeline(config_path: Path) -> tuple[TourismETLPipeline, Settings]:
    settings = load_settings(config_path)
    extractor = CSVExtractor()
    transformer = TourismTransformer(settings.datasets)
    loader = FileSystemLoader(
        output_dir=settings.processed_data_dir,
        unified_filename=settings.unified_metrics_filename,
        manifest_filename=settings.dataset_manifest_filename,
    )
    pipeline = TourismETLPipeline(
        settings=settings,
        extractor=extractor,
        transformer=transformer,
        loader=loader,
    )
    return pipeline, settings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Empresas Certificadas ETL pipeline")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/settings.yaml"),
        help="Path to the YAML configuration file",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pipeline, settings = build_pipeline(args.config)
    result = pipeline.run()
    print(
        f"✅ Generated {len(result.combined_frame)} rows across "
        f"{len(settings.datasets)} datasets."
    )


if __name__ == "__main__":
    main()
