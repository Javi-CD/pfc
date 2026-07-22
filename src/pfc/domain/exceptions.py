class ConversionError(Exception):
    """Base exception for all conversion errors."""
    pass


class UnsupportedFormatError(ConversionError):
    """Raised when a format conversion is not supported."""
    pass


class ConverterNotFoundError(ConversionError):
    """Raised when no suitable converter is found in the registry."""
    pass


class InvalidInputFileError(ConversionError):
    """Raised when the input file is invalid or does not exist."""
    pass


class OutputFileExistsError(ConversionError):
    """Raised when the destination file already exists and overwrite is disabled."""
    pass
