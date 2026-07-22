import csv
import json
from pathlib import Path

from pfc.domain.exceptions import ConversionError
from pfc.domain.models import ConversionResult


class JsonToCsvConverter:
    def supports(self, source_format: str, target_format: str) -> bool:
        return source_format.lower() == "json" and target_format.lower() == "csv"

    def convert(self, source: Path, destination: Path) -> ConversionResult:
        size_before = source.stat().st_size

        with open(source, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
            raise ConversionError("JSON must be an array of objects to convert to CSV.")

        if len(data) == 0:
            headers = []
        else:
            headers = list(data[0].keys())

        with open(destination, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)

        size_after = destination.stat().st_size

        return ConversionResult(
            source=source,
            destination=destination,
            source_format="json",
            target_format="csv",
            size_before=size_before,
            size_after=size_after,
        )
