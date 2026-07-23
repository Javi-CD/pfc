# Plugin Development Guide

Welcome! If you want **PFC** to support a new format (for example, converting `.mp4` to `.mp3`, or `.xml` to `.json`), you have come to the right place.

Thanks to our plugin-based architecture and *Entry Points*, **you can add new conversion formats without modifying a single line of the core system code.**

## 1. The Protocol: Rules of the Game

Any converter you want to add only has to fulfill a contract. In Python, we do this using a `Protocol` that lives in `src/pfc/domain/protocols.py`.

Your class must have two methods:

- `supports(source_format, target_format)`: Returns `True` if your converter knows how to convert from one format to another.
- `convert(source_path, target_path)`: Executes the actual conversion and returns a `ConversionResult` object.

## 2. Step by Step: Creating your first Plugin

Imagine we are going to create a `CSV` to `JSON` converter.

### Step A: Create your file

Create a new file inside the infrastructure layer, for example `src/pfc/infrastructure/converters/my_new_converter.py`.

### Step B: Write the class

Make sure to handle errors by catching exceptions and raising `ConversionError`.

```python
import json
import csv
from pathlib import Path
from pfc.domain.exceptions import ConversionError
from pfc.domain.models import ConversionResult

class CsvToJsonPlugin:
    def supports(self, source_format: str, target_format: str) -> bool:
        return source_format == "csv" and target_format == "json"

    def convert(self, source: Path, destination: Path) -> ConversionResult:
        try:
            # Your conversion logic here
            data = []
            with open(source, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
                    
            with open(destination, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
                
            return ConversionResult(
                source_path=source,
                target_path=destination,
                success=True,
                message="Successfully converted to JSON"
            )
        except Exception as e:
            # It is very important to wrap failures in our Domain exception
            raise ConversionError(f"Error processing CSV: {e}")
```

### Step C: Announce it to the world (Automatic Registration)

This is the best part. You don't have to import your class in `main.py` or manually register it. PFC uses Python's `entry_points` to find your plugin.

Open the `pyproject.toml` file located in the root of the project. Look for the `[project.entry-points."pfc.converters"]` section and add the path to your new class.

```toml
[project.entry-points."pfc.converters"]
csv_to_json = "pfc.infrastructure.converters.my_new_converter:CsvToJsonPlugin"
# format: 
# whatever_name = "module.path:YourClassName"
```

## 3. Test it

That's it! Now open your terminal and run:

```bash
pfc plugins
```

You should see `CsvToJsonPlugin` proudly listed as a registered converter in the system, dynamically loaded, and ready to be used with the `pfc convert` command.

Congratulations! You have extended the application following the **SOLID** principles (Specifically the Open/Closed principle).
