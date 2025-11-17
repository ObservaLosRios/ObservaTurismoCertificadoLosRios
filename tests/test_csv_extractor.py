"""Tests for the CSV extractor normalization rules."""

from __future__ import annotations

from pathlib import Path

from funds_etl.extractors.csv_extractor import CSVExtractor


def test_csv_extractor_merges_extra_commas(tmp_path: Path) -> None:
    csv_content = "grafico,clase,valor\nTipos,Bed and Breakfast, Familiar,10\n"
    dataset_path = tmp_path / "dataset.csv"
    dataset_path.write_text(csv_content, encoding="utf-8")

    extractor = CSVExtractor()
    frame = extractor.extract(dataset_path)

    assert frame.loc[0, "clase"] == "Bed and Breakfast, Familiar"
    assert frame.loc[0, "valor"] == "10"
