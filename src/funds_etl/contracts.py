"""Shared contracts enforcing SOLID design principles for the ETL pipeline."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Protocol

import pandas as pd


class Extractor(ABC):
    """Responsible for fetching raw data from a source."""

    @abstractmethod
    def extract(self, source: Path) -> pd.DataFrame:
        """Loads a dataset and returns it as a DataFrame."""


class Transformer(Protocol):
    """Transforms raw data into the normalized metric schema."""

    def transform(self, dataset_name: str, frame: pd.DataFrame) -> pd.DataFrame:
        """Returns the transformed DataFrame."""


class Loader(ABC):
    """Persists transformed data to a destination."""

    @abstractmethod
    def persist_dataset(self, dataset_name: str, frame: pd.DataFrame) -> Path:
        """Stores a dataset and returns the output path."""

    @abstractmethod
    def finalize(self, combined_frame: pd.DataFrame, manifest: dict) -> None:
        """Persists summary artifacts (combined dataset + manifest)."""
