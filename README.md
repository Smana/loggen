[![CI](https://github.com/smana/loggen/actions/workflows/ci.yml/badge.svg)](https://github.com/smana/loggen/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/badge/Docker%20Image-ghcr.io%2Fsmana%2Floggen-blue)](https://ghcr.io/smana/loggen)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)

# loggen

A configurable log generator for testing and benchmarking log pipelines. It generates random  logs in **webserver-style** format, making it ideal for **demos** and testing with logging solutions such as Loki, VictoriaLogs, and more.

We simulate a log equivalent of what can be configured with the Nginx configuration

```nginx
# Example nginx log_format for loggen-style JSON logs
log_format logger_json escape=json '{'
    '"remote_addr":"$remote_addr",'
    '"remote_user":"$remote_user",'
    '"time_local":"$time_local",'
    '"request":"$request",'
    '"status":$status,'
    '"body_bytes_sent":$body_bytes_sent,'
    '"http_referer":"$http_referer",'
    '"http_user_agent":"$http_user_agent",'
    '"country":"$geoip2_data_country_code",'
    '"request_time":$request_time,'
    '"level":"$level"'
'}';
```

Example:

```console
loggen --sleep 0.5
145.181.141.29 - [19/Apr/2025:09:24:13 ] "GET /login HTTP/1.1" 403 113 "https://google.com/search?q=loggen" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" "JP" 1.05 warning
94.75.137.82 - [03/May/2025:17:52:47 ] "PATCH /homepage HTTP/1.1" 400 2616 "https://github.com/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15" "US" 1.464 warning
104.155.196.123 - [14/May/2025:16:02:49 ] "GET /login HTTP/2" 200 2409 "http://localhost/" "PostmanRuntime/7.28.4" "RU" 1.019 info
48.107.13.5 - [06/May/2025:21:26:22 ] "POST /products HTTP/1.1" 204 4425 "http://localhost/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15" "BR" 1.182 info
...
```

or using JSON output

```console
loggen --sleep 1 --error-rate 0.2 --format json
loggen --sleep 1 --error-rate 0.2 --format json --latency 0.5
{"remote_addr": "136.250.6.140", "remote_user": "-", "time_local": "13/May/2025:14:58:54 ", "request": "POST /products HTTP/1.1", "status": 204, "body_bytes_sent": 4431, "http_referer": "https://google.com/search?q=loggen", "http_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36", "country": "BR", "request_time": 1.286, "level": "info"}
{"remote_addr": "239.240.1.153", "remote_user": "-", "time_local": "21/Apr/2025:18:40:12 ", "request": "PUT /homepage HTTP/1.1", "status": 429, "body_bytes_sent": 2363, "http_referer": "-", "http_user_agent": "PostmanRuntime/7.28.4", "country": "DE", "request_time": 1.988, "level": "warning"}
{"remote_addr": "139.242.228.192", "remote_user": "-", "time_local": "05/May/2025:00:25:38 ", "request": "PATCH /about HTTP/1.1", "status": 202, "body_bytes_sent": 4718, "http_referer": "-", "http_user_agent": "PostmanRuntime/7.28.4", "country": "DE", "request_time": 1.003, "level": "info"}
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
