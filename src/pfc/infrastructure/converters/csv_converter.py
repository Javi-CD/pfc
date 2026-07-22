import csv
import json
from pathlib import Path

from pfc.domain.models import ConversionResult


class CsvToJsonConverter:
    def supports(self, source_format: str, target_format: str) -> bool:
        return source_format.lower() == "csv" and target_format.lower() == "json"

    def convert(self, source: Path, destination: Path) -> ConversionResult:
        size_before = source.stat().st_size

        data = []
        with open(source, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)

        with open(destination, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        size_after = destination.stat().st_size

        return ConversionResult(
            source=source,
            destination=destination,
            source_format="csv",
            target_format="json",
            size_before=size_before,
            size_after=size_after,
        )
