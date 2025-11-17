"""CSV extractor implementation."""

from __future__ import annotations

from pathlib import Path
from typing import List

import pandas as pd

from funds_etl.contracts import Extractor


class CSVExtractor(Extractor):
    """Loads CSV files using pandas with basic validation."""

    def __init__(self, *, encoding: str = "utf-8", delimiter: str = ",") -> None:
        self._encoding = encoding
        self._delimiter = delimiter

    def extract(self, source: Path) -> pd.DataFrame:
        if not source.exists():
            raise FileNotFoundError(f"The dataset at {source} does not exist")

        with source.open("r", encoding=self._encoding) as handle:
            rows = [line.rstrip("\n") for line in handle]

        if not rows:
            raise ValueError(f"The dataset at {source} is empty")

        header = rows[0].split(self._delimiter)
        normalized_rows: List[List[str]] = []

        for raw_line in rows[1:]:
            if not raw_line.strip():
                continue
            cells = raw_line.split(self._delimiter)
            normalized_rows.append(self._normalize_row(cells, header))

        return pd.DataFrame(normalized_rows, columns=header)

    @staticmethod
    def _normalize_row(cells: List[str], header: List[str]) -> List[str]:
        """Normalizes rows that may contain commas inside categorical columns."""

        expected_length = len(header)
        if len(cells) == expected_length:
            return cells

        if len(cells) < expected_length:
            return cells + ["" for _ in range(expected_length - len(cells))]

        # Assume that the overflow belongs to the category column (index 1)
        tail_length = max(expected_length - 2, 0)
        tail = cells[-tail_length:] if tail_length else []
        category_parts = cells[1 : len(cells) - tail_length]
        merged_category = ", ".join(part.strip() for part in category_parts)
        normalized = [cells[0], merged_category]
        normalized.extend(tail)
        return normalized
