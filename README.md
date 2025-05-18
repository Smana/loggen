[![CI](https://github.com/smana/loggen/actions/workflows/ci.yml/badge.svg)](https://github.com/smana/loggen/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/badge/Docker%20Image-ghcr.io%2Fsmana%2Floggen-blue)](https://ghcr.io/smana/loggen)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)

# loggen

A configurable log generator for testing and benchmarking log pipelines. It generates random  logs in **webserver-style** format, making it ideal for **demos** and testing with logging solutions such as Loki, VictoriaLogs, and more.

Example:

```console
loggen --sleep 0.5
warning 111.189.30.118  [21/Apr/2025:16:30:14 ] "DELETE /about HTTP/1.1" 429 4150 "http://localhost/" "PostmanRuntime/7.28.4" "US"
info 85.148.104.58  [07/May/2025:11:52:01 ] "GET /contact HTTP/1.1" 200 708 "https://github.com/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" "RU"
warning 63.143.32.40  [15/May/2025:15:48:35 ] "PATCH /products HTTP/1.1" 401 4492 "https://google.com/search?q=loggen" "curl/7.68.0" "FR"
error 74.150.31.111  [04/May/2025:05:41:13 ] "POST /login HTTP/2" 504 1274 "http://example.com/previous_page" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" "US"
...
```

or using JSON output

```console
loggen --sleep 1 --error-rate 0.2 --format json
{"level": "warning", "remote_addr": "204.222.22.250", "time_local": "10/May/2025:21:37:20 ", "request": "POST /login HTTP/1.1", "status": 404, "body_bytes_sent": 1757, "http_referer": "-", "http_user_agent": "curl/7.68.0", "country": "IN"}
{"level": "error", "remote_addr": "223.85.90.31", "time_local": "03/May/2025:21:30:52 ", "request": "POST /homepage HTTP/2", "status": 502, "body_bytes_sent": 3822, "http_referer": "http://example.com/previous_page", "http_user_agent": "curl/7.68.0", "country": "IN"}
{"level": "error", "remote_addr": "208.92.13.189", "time_local": "23/Apr/2025:17:35:17 ", "request": "DELETE /homepage HTTP/1.1", "status": 500, "body_bytes_sent": 1952, "http_referer": "-", "http_user_agent": "Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36", "country": "RU"}
...
```

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
