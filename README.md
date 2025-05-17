[![CI](https://github.com/smana/loggen/actions/workflows/ci.yml/badge.svg)](https://github.com/smana/loggen/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/badge/Docker%20Image-ghcr.io%2Fsmana%2Floggen-blue)](https://ghcr.io/smana/loggen)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)

# loggen

A configurable log generator for testing and benchmarking log pipelines. It generates random  logs in webserver-style formats, making it ideal for demos and testing with logging solutions such as Loki, VictoriaLogs, and more.

## Prerequisites

- Python **>=3.13.0 <3.14.0**
- [uv](https://github.com/astral-sh/uv) **>=0.5.29**
- [pre-commit](https://pre-commit.com/) (optional)
- Docker (optional)

## Installation

1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd loggen
   ```
2. Install dependencies and create a virtual environment:
   ```sh
   uv venv
   source .venv/bin/activate
   uv pip install --editable .
   uv pip install -r pyproject.toml
   ```

## Usage

Run the log generator as a CLI:

```sh
loggen --sleep 1 --error-rate 0.2 --format json
```
Or directly with Python:
```sh
python -m loggen.main --sleep 1 --error-rate 0.2 --format json
```

- By default, loggen runs indefinitely. Use `--count N` to generate exactly N logs.
- Example: Generate 10 logs in JSON format:
  ```sh
  loggen --count 10 --format json
  ```
- All options:
  - `--sleep FLOAT`   : Seconds to sleep between logs (default: 0)
  - `--error-rate FLOAT` : Fraction of logs that are errors (default: 0.1)
  - `--format [raw|json]` : Log output format (default: raw)
  - `--count INT`     : Number of logs to generate (default: 0 for infinite)

## Project Structure

- `loggen/` — Python package
  - `main.py` — Main application and CLI entry point
  - `__init__.py` — Package marker and exports
- `tests/` — Unit tests
- `Dockerfile` — Container build file
- `pyproject.toml` — Project metadata and dependencies

## Testing

Run unit tests with [pytest](https://pytest.org/):

```sh
uv pip install .[test]
uv run pytest
```

## Docker

Build and run the production image:

```sh
docker build . -t loggen:latest
docker run -it --rm loggen:latest
```

Build and run the development image:

```sh
docker build . --target development -t loggen:dev
docker run -it --rm loggen:dev
```

## License

This project is licensed under the Apache-2.0 License.
