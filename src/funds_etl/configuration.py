"""Utilities to load ETL settings from YAML files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

import yaml


@dataclass(frozen=True)
class DatasetSettings:
    """Represents the metadata configuration for a single dataset."""

    name: str
    filename: str
    metric_group: str
    category_field: str
    value_field: str
    percentage_field: Optional[str]
    highlight_field: Optional[str]
    highlight_percentage_field: Optional[str]


@dataclass(frozen=True)
class Settings:
    """Top-level configuration for the ETL pipeline."""

    project_name: str
    owner: str
    raw_data_dir: Path
    processed_data_dir: Path
    datasets: Dict[str, DatasetSettings]
    unified_metrics_filename: str
    dataset_manifest_filename: str


def load_settings(config_path: str | Path) -> Settings:
    """Loads the YAML configuration file into a strongly typed Settings object."""

    path = Path(config_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Config file not found at {path}")

    with path.open("r", encoding="utf-8") as stream:
        raw_config = yaml.safe_load(stream)

    project = raw_config.get("project", {})
    paths = raw_config.get("paths", {})
    datasets_section = raw_config.get("datasets", {})
    outputs = raw_config.get("outputs", {})

    datasets: Dict[str, DatasetSettings] = {}
    for dataset_name, dataset_config in datasets_section.items():
        datasets[dataset_name] = DatasetSettings(
            name=dataset_name,
            filename=dataset_config["filename"],
            metric_group=dataset_config["metric_group"],
            category_field=dataset_config["category_field"],
            value_field=dataset_config["value_field"],
            percentage_field=dataset_config.get("percentage_field"),
            highlight_field=dataset_config.get("highlight_field"),
            highlight_percentage_field=dataset_config.get("highlight_percentage_field"),
        )

    return Settings(
        project_name=project.get("name", "Unnamed Project"),
        owner=project.get("owner", "unknown"),
        raw_data_dir=(path.parent / paths["raw_data_dir"]).resolve(),
        processed_data_dir=(path.parent / paths["processed_data_dir"]).resolve(),
        datasets=datasets,
        unified_metrics_filename=outputs["unified_metrics_filename"],
        dataset_manifest_filename=outputs["dataset_manifest_filename"],
    )
