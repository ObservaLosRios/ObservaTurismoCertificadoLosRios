"""Transformer for tourism-related datasets."""

from __future__ import annotations

from typing import Any

import pandas as pd

from funds_etl.configuration import DatasetSettings


class TourismTransformer:
    """Normaliza cualquier dataset definido en la configuración."""

    REQUIRED_COLUMNS = ("category_field", "value_field")

    def __init__(self, dataset_settings: dict[str, DatasetSettings]) -> None:
        self._dataset_settings = dataset_settings

    def transform(self, dataset_name: str, frame: pd.DataFrame) -> pd.DataFrame:
        if dataset_name not in self._dataset_settings:
            raise KeyError(f"Dataset '{dataset_name}' is not declared in the configuration")

        dataset_config = self._dataset_settings[dataset_name]
        self._validate_frame(frame, dataset_config)

        normalized = pd.DataFrame(
            {
                "metric_group": dataset_config.metric_group,
                "category": frame[dataset_config.category_field].astype(str),
                "value": frame[dataset_config.value_field].astype(float),
                "percentage": self._maybe_numeric(frame, dataset_config.percentage_field),
                "highlight_value": self._maybe_numeric(frame, dataset_config.highlight_field),
                "highlight_percentage": self._maybe_numeric(
                    frame, dataset_config.highlight_percentage_field
                ),
            }
        )

        return normalized

    @staticmethod
    def _maybe_numeric(frame: pd.DataFrame, column_name: str | None) -> pd.Series | None:
        if column_name is None or column_name not in frame.columns:
            return None
        return pd.to_numeric(frame[column_name], errors="coerce")

    @staticmethod
    def _validate_frame(frame: pd.DataFrame, config: DatasetSettings) -> None:
        missing_columns: list[str] = []
        for column_name in {config.category_field, config.value_field}:
            if column_name not in frame.columns:
                missing_columns.append(column_name)
        if missing_columns:
            raise ValueError(
                "Dataset is missing required columns: " + ", ".join(sorted(missing_columns))
            )

        if frame.empty:
            raise ValueError("Dataset is empty; cannot transform an empty frame")
