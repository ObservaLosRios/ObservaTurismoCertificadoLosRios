"""Domain entities used across the ETL pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class MetricRecord:
    """Normalized representation of a metric row."""

    metric_group: str
    category: str
    value: float
    percentage: Optional[float]
    highlight_value: Optional[float]
    highlight_percentage: Optional[float]


@dataclass(frozen=True)
class DatasetArtifact:
    """Metadata describing a stored dataset artifact."""

    dataset_name: str
    path: str
    row_count: int
