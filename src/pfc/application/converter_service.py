import logging
from pathlib import Path

from pfc.application.conversion_registry import ConversionRegistry
from pfc.domain.exceptions import InvalidInputFileError, OutputFileExistsError
from pfc.domain.models import ConversionResult

logger = logging.getLogger(__name__)


class ConversionService:
    def __init__(self, registry: ConversionRegistry) -> None:
        self._registry = registry

    def convert(
        self,
        source: Path,
        destination: Path,
        source_format: str,
        target_format: str,
        overwrite: bool = False,
    ) -> ConversionResult:
        """Executes a conversion using the appropriate registered converter."""
        logger.info(f"Starting conversion: {source} -> {destination}")

        if not source.exists() or not source.is_file():
            logger.error(f"Invalid input file: {source}")
            raise InvalidInputFileError(f"Input file does not exist: {source}")

        if destination.exists():
            if not overwrite:
                logger.error(f"Output file already exists: {destination}")
                raise OutputFileExistsError(f"Destination already exists: {destination}")
            logger.info(f"Overwriting existing file: {destination}")

        converter = self._registry.get(source_format, target_format)
        result = converter.convert(source, destination)
        
        logger.info(f"Conversion completed successfully: {destination}")
        return result
