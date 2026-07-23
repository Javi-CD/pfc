from dataclasses import dataclass
from pathlib import Path
import os
import filetype  # type: ignore

from pfc.domain.exceptions import FileTooLargeError, SecurityViolationError

@dataclass(frozen=True)
class SecurityConfig:
    max_file_size_bytes: int = 100 * 1024 * 1024  # 100MB by default
    validate_mime_type: bool = True
    prevent_path_traversal: bool = True


def validate_file_size(file_path: Path, config: SecurityConfig) -> None:
    if not file_path.exists():
        return
    size = file_path.stat().st_size
    if size > config.max_file_size_bytes:
        raise FileTooLargeError(
            f"File '{file_path.name}' exceeds the maximum allowed size of {config.max_file_size_bytes} bytes."
        )

def validate_mime_type(file_path: Path, expected_extension: str, config: SecurityConfig) -> None:
    if not config.validate_mime_type:
        return
        
    text_extensions = {"txt", "csv", "json", "md", "html"}
    expected_extension = expected_extension.lower().lstrip(".")
    if expected_extension in text_extensions:
        return
        
    kind = filetype.guess(str(file_path))
    if kind is None:
        return
        
    equiv_map = {
        "jpg": {"jpg", "jpeg"},
        "jpeg": {"jpg", "jpeg"},
        "docx": {"docx", "zip"},
        "xlsx": {"xlsx", "zip"}
    }
    allowed_exts = equiv_map.get(expected_extension, {expected_extension})
    
    if kind.extension not in allowed_exts:
        raise SecurityViolationError(
            f"MIME type validation failed: Expected {expected_extension}, but detected {kind.extension}"
        )

def validate_safe_path(path: Path, config: SecurityConfig) -> None:
    if not config.prevent_path_traversal:
        return
        
    resolved_path = path.resolve()
    
    critical_prefixes = []
    if os.name == 'nt':
        win_dir = os.environ.get('WINDIR', 'C:\\Windows')
        prog_files = os.environ.get('ProgramFiles', 'C:\\Program Files')
        prog_files_x86 = os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)')
        critical_prefixes = [Path(win_dir).resolve(), Path(prog_files).resolve(), Path(prog_files_x86).resolve()]
    else:
        critical_prefixes = [Path('/etc'), Path('/bin'), Path('/usr'), Path('/sys'), Path('/proc'), Path('/boot')]
        
    for crit_dir in critical_prefixes:
        try:
            resolved_path.relative_to(crit_dir)
            raise SecurityViolationError(
                f"Path traversal protection triggered: Cannot write to protected system directory '{crit_dir}'"
            )
        except ValueError:
            pass
