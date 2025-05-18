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
112.166.192.213 - [02/May/2025:11:21:10 ] "GET /api/data HTTP/2" 204 4627 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" "FR" 0.94
168.129.163.41 - [29/Apr/2025:04:23:46 ] "PUT /login HTTP/2" 201 3474 "https://github.com/" "PostmanRuntime/7.28.4" "GB" 1.489
233.86.10.252 - [05/May/2025:11:18:41 ] "GET /homepage HTTP/2" 201 2407 "https://github.com/" "curl/7.68.0" "CN" 0.753
187.4.53.252 - [20/Apr/2025:18:44:47 ] "GET /homepage HTTP/2" 204 3119 "https://github.com/" "curl/7.68.0" "RU" 0.662
...
```

or using JSON output

```console
loggen --sleep 1 --error-rate 0.2 --format json
{"remote_addr": "208.175.166.30", "remote_user": "-", "time_local": "19/Apr/2025:02:11:56 ", "request": "PUT /contact HTTP/1.1", "status": 202, "body_bytes_sent": 3368, "http_referer": "https://github.com/", "http_user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15", "country": "AU", "request_time": 0.532}
{"remote_addr": "133.120.216.25", "remote_user": "-", "time_local": "29/Apr/2025:22:42:16 ", "request": "POST /products HTTP/2", "status": 200, "body_bytes_sent": 1966, "http_referer": "https://google.com/search?q=loggen", "http_user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15", "country": "CN", "request_time": 0.241}
{"remote_addr": "151.116.92.8", "remote_user": "-", "time_local": "12/May/2025:17:14:49 ", "request": "GET /products HTTP/1.1", "status": 200, "body_bytes_sent": 3324, "http_referer": "-", "http_user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15", "country": "JP", "request_time": 0.331}
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
  - `--error-rate FLOAT` : Fraction of logs that are errors (default: 0.1). The error rate is split evenly between 4xx (client_error) and 5xx (server_error). For example, `--error-rate 0.2` means 10% client_error, 10% server_error, 80% successful (2xx/other) responses.
  - `--format [raw|json]` : Log output format (default: raw)
  - `--count INT`     : Number of logs to generate (default: 0 for infinite)
  - `--latency FLOAT` : Additional latency (in seconds) to add to request_time (default: 0)

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
