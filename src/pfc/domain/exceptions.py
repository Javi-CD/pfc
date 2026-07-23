class ConversionError(Exception):
    """Base exception for all conversion errors."""


class UnsupportedFormatError(ConversionError):
    """Raised when a format conversion is not supported."""


class ConverterNotFoundError(ConversionError):
    """Raised when no suitable converter is found in the registry."""


class InvalidInputFileError(ConversionError):
    """Raised when the input file is invalid or does not exist."""


class OutputFileExistsError(ConversionError):
    """Raised when the destination file already exists and overwrite is disabled."""


class SecurityViolationError(ConversionError):
    """Raised when a security constraint is violated (MIME type mismatch, Path Traversal, etc.)."""


class FileTooLargeError(SecurityViolationError):
    """Raised when the input file exceeds the maximum allowed size."""
