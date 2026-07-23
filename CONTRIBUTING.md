# CONTRIBUTING to PFC (Python File Converter)

First off, thank you for considering contributing to PFC! It's people like you that make the open source community such an amazing place to learn, inspire, and create.

## 1. Where do I go from here?

If you've noticed a bug or have a feature request, make sure to check our [Issues](https://github.com/Javi-CD/pfc/issues) if it has already been reported. If not, feel free to open a new issue.

## 2. Setting up the development environment

1. Clone the repository:

   ```bash
   git clone https://github.com/Javi-CD/pfc.git
   cd pfc
   ```

2. Install dependencies using `uv`:

   ```bash
   uv sync
   ```

3. Run the test suite to ensure everything is working:

   ```bash
   uv run pytest
   ```

## 3. Creating a Plugin (Converter)

PFC uses an Entry Point based Plugin Architecture. To add a new format converter, you don't need to modify the core application.
Simply create a class that implements the `Converter` protocol (must have `supports()` and `convert()` methods) and register it in `pyproject.toml` under `[project.entry-points."pfc.converters"]`.

Read the detailed guide in [docs/plugins.md](docs/plugins.md).

## 4. Pull Request Process

1. Create a feature branch (`git checkout -b feature/AmazingFeature`).
2. Make your changes.
3. Ensure the test suite passes (`uv run pytest`) and the linter is happy (`uv run ruff check .` & `uv run mypy src`).
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
5. Push to the branch (`git push origin feature/AmazingFeature`).
6. Open a Pull Request!

## 5. Code Style

We strictly enforce Clean Architecture and type hinting. Make sure you don't add external dependencies to the `pfc.domain` layer.

Thank you!
