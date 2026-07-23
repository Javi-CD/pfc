# Security Policy

## Supported Versions

Currently, the following versions of Python File Converter (PFC) are supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within PFC, please do **NOT** open a public issue.

Instead, please send an e-mail to the core maintainer team at `javierperezdeveloper@gmail.com`. All security vulnerabilities will be promptly addressed.

## Security Features

PFC implements several security controls by default (Level 8 Architecture):

- **Path Traversal Protection**: Prevents the tool from writing files into critical OS directories (`C:\Windows`, `/etc`, etc.).
- **MIME Validation**: Validates magic bytes to ensure files correspond to their extensions, preventing disguised executables.
- **File Size Limits**: Prevents loading excessive files into memory (default limit is 100MB).
