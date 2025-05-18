import json
import re

import pytest
from click.testing import CliRunner

from loggen import (
    generate_log_entry,
    main,
    pick_error_level,
    pick_status_code,
)


def test_generate_log_entry_raw():
    log = generate_log_entry(0.0, "raw")
    # Should contain an IP, a request, a status code, etc.
    assert isinstance(log, str)
    assert re.search(r"\d+\.\d+\.\d+\.\d+", log)
    assert '"' in log  # request is quoted
    assert re.search(r"\s(2|4|5)\d{2}\s", log)  # status code

def test_generate_log_entry_json():
    log = generate_log_entry(0.0, "json")
    data = json.loads(log)
    assert isinstance(data, dict)
    assert "remote_addr" in data
    assert "request" in data
    assert "status" in data
    assert isinstance(data["status"], int)
    assert 200 <= data["status"] < 600

@pytest.mark.parametrize("error_rate,expected_status_range", [
    (0.0, range(200, 300)),  # Only 2xx (ok)
    (1.0, list(range(400, 500)) + list(range(500, 600))),  # Only 4xx or 5xx (errors)
])
def test_pick_error_level_extremes(error_rate, expected_status_range):
    # With 0.0, always 2xx; with 1.0, always 4xx or 5xx
    for _ in range(20):
        level = pick_error_level(error_rate)
        code = pick_status_code(level)
        assert code in expected_status_range

@pytest.mark.parametrize("error_level", ["ok", "client_error", "server_error"])
def test_pick_status_code(error_level):
    code = pick_status_code(error_level)
    assert isinstance(code, int)
    if error_level == "ok":
        assert code in [200, 201, 202, 204]
    elif error_level == "client_error":
        assert code in [400, 401, 403, 404, 429]
    elif error_level == "server_error":
        assert code in [500, 502, 503, 504]

def test_cli_basic():
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '--sleep', '0',
            '--error-rate', '0',
            '--format', 'json',
            '--count', '1',
        ],
    )
    assert result.exit_code == 0
    assert '{' in result.output or 'info' in result.output

def test_cli_invalid_format():
    runner = CliRunner()
    result = runner.invoke(main, ['--format', 'invalid'])
    assert result.exit_code != 0
    assert 'Invalid value for' in result.output

def test_request_time_in_json():
    log = generate_log_entry(0.0, "json")
    data = json.loads(log)
    assert "request_time" in data
    assert isinstance(data["request_time"], float)
    assert 0.001 <= data["request_time"] <= 3.0
