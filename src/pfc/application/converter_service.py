import logging
from pathlib import Path

from pfc.application.conversion_registry import ConversionRegistry
from pfc.domain.exceptions import InvalidInputFileError, OutputFileExistsError
from pfc.domain.models import ConversionResult
from pfc.domain.security import (
    SecurityConfig,
    validate_file_size,
    validate_mime_type,
    validate_safe_path,
)

logger = logging.getLogger(__name__)


class ConversionService:
    def __init__(
        self,
        registry: ConversionRegistry,
        security_config: SecurityConfig | None = None,
    ) -> None:
        self._registry = registry
        self._security_config = security_config or SecurityConfig()

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
                raise OutputFileExistsError(
                    f"Destination already exists: {destination}"
                )
            logger.info(f"Overwriting existing file: {destination}")

        validate_safe_path(destination, self._security_config)
        validate_file_size(source, self._security_config)
        validate_mime_type(source, source_format, self._security_config)

        converter = self._registry.get(source_format, target_format)
        result = converter.convert(source, destination)

        logger.info(f"Conversion completed successfully: {destination}")
        return result
