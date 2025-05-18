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
    # Should contain info, an IP, a request, a status code, etc.
    assert isinstance(log, str)
    assert re.search(r"info|warning|error", log)
    assert re.search(r"\d+\.\d+\.\d+\.\d+", log)
    assert '"' in log  # request is quoted

def test_generate_log_entry_json():
    log = generate_log_entry(0.0, "json")
    data = json.loads(log)
    assert isinstance(data, dict)
    assert data["level"] == "info"
    assert "remote_addr" in data
    assert "request" in data
    assert "status" in data

@pytest.mark.parametrize("error_rate,expected", [
    (0.0, "info"),
    (1.0, "error"),
])
def test_pick_error_level_extremes(error_rate, expected):
    # With 0.0, always info; with 1.0, always error
    for _ in range(10):
        assert pick_error_level(error_rate) == expected

@pytest.mark.parametrize("error_level", ["info", "warning", "error"])
def test_pick_status_code(error_level):
    code = pick_status_code(error_level)
    assert isinstance(code, int)
    if error_level == "info":
        assert code in [200, 201, 202, 204]
    elif error_level == "warning":
        assert code in [400, 401, 403, 404, 429]
    elif error_level == "error":
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
