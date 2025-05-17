import json
import re

import pytest
from click.testing import CliRunner

from loggen import (
    generate_log_entry,
    main,
    pick_error_type,
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
    assert data["type"] == "info"
    assert "remote_addr" in data
    assert "request" in data
    assert "status" in data

@pytest.mark.parametrize("error_rate,expected", [
    (0.0, "info"),
    (1.0, "error"),
])
def test_pick_error_type_extremes(error_rate, expected):
    # With 0.0, always info; with 1.0, always error
    for _ in range(10):
        assert pick_error_type(error_rate) == expected

@pytest.mark.parametrize("error_type", ["info", "warning", "error"])
def test_pick_status_code(error_type):
    code = pick_status_code(error_type)
    assert isinstance(code, int)
    if error_type == "info":
        assert code in [200, 201, 202, 204]
    elif error_type == "warning":
        assert code in [400, 401, 403, 404, 429]
    elif error_type == "error":
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
