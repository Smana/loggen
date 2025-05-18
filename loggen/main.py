import json
import random
import secrets
import sys
import time
from datetime import datetime, timedelta

import click

# Sample data for random generation
HTTP_METHODS = [
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "PATCH",
]
HTTP_PATHS = [
    "/homepage",
    "/login",
    "/api/data",
    "/products",
    "/about",
    "/contact",
]
HTTP_VERSIONS = ["HTTP/1.1", "HTTP/2"]
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "curl/7.68.0",
    "PostmanRuntime/7.28.4",
    "Mozilla/5.0 (Linux; Android 10; SM-G970F) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 "
    "Mobile Safari/537.36",
]
REFERERS = [
    "http://example.com/previous_page",
    "https://google.com/search?q=loggen",
    "-",
    "http://localhost/",
    "https://github.com/",
]
COUNTRY_CODES = [
    "US",
    "FR",
    "DE",
    "IN",
    "CN",
    "BR",
    "GB",
    "RU",
    "JP",
    "AU",
]
ERROR_LEVELS = ["info", "warning", "error"]

# HTTP status code pools
HTTP_CODES = {
    "info": [200, 201, 202, 204],
    "warning": [400, 401, 403, 404, 429],
    "error": [500, 502, 503, 504],
}


def random_ip():
    return ".".join(str(secrets.randbelow(255) + 1) for _ in range(4))

# random time in the last 30 days
def random_time():
    now = datetime.now()
    offset = -secrets.randbelow(60*60*24*30 + 1)
    dt = now + timedelta(seconds=offset)
    return dt.strftime("%d/%b/%Y:%H:%M:%S %z")

def random_request():
    method = secrets.choice(HTTP_METHODS)
    path = secrets.choice(HTTP_PATHS)
    version = secrets.choice(HTTP_VERSIONS)
    return f"{method} {path} {version}"

def random_bytes():
    return secrets.randbelow(5000 - 100 + 1) + 100

def random_user_agent():
    return secrets.choice(USER_AGENTS)

def random_referer():
    return secrets.choice(REFERERS)

def random_country():
    return secrets.choice(COUNTRY_CODES)

def random_request_time():
    # Simulate request time between 0.200 and 1.500 seconds
    return round(random.uniform(0.2, 1.5), 3)  # nosec

def pick_error_level(error_rate):
    # error_rate is the probability of an error (0-1)
    # warning_rate is half of error_rate
    r = secrets.randbelow(10**9) / 10**9
    if r < error_rate:
        return "error"
    elif r < error_rate * 2:
        return "warning"
    else:
        return "info"

def pick_status_code(error_type):
    return secrets.choice(HTTP_CODES[error_type])

def generate_log_entry(error_rate, output_format, latency=0.0):
    error_level = pick_error_level(error_rate)
    remote_addr = random_ip()
    remote_user = "-"  # Not used, but included for nginx compatibility
    time_local = random_time()
    request = random_request()
    status = pick_status_code(error_level)
    body_bytes_sent = random_bytes()
    http_referer = random_referer()
    http_user_agent = random_user_agent()
    country = random_country()
    request_time = round(random_request_time() + latency, 3)

    if output_format == "raw":
        log = (
            f"{remote_addr} {remote_user} [{time_local}] \"{request}\" "
            f"{status} {body_bytes_sent} \"{http_referer}\" "
            f'"{http_user_agent}" "{country}" {request_time} {error_level}'
        )
        return log
    else:
        log_dict = {
            "remote_addr": remote_addr,
            "remote_user": remote_user,
            "time_local": time_local,
            "request": request,
            "status": status,
            "body_bytes_sent": body_bytes_sent,
            "http_referer": http_referer,
            "http_user_agent": http_user_agent,
            "country": country,
            "request_time": request_time,
            "level": error_level,
        }
        return json.dumps(log_dict)

@click.command()
@click.option(
    '--sleep',
    type=float,
    default=0,
    help='Seconds to sleep between logs (default: 0)'
)
@click.option(
    '--error-rate',
    type=float,
    default=0.1,
    help='Fraction of logs that are errors (default: 0.1)'
)
@click.option(
    '--format',
    'output_format',
    type=click.Choice(['raw', 'json']),
    default='raw',
    help='Log output format (raw or json)'
)
@click.option(
    '--count',
    type=int,
    default=0,
    help='Number of logs to generate (default: 0 for infinite)'
)
@click.option(
    '--latency',
    type=float,
    default=0.0,
    help='Additional latency (in seconds) to add to request_time (default: 0)'
)
def main(sleep, error_rate, output_format, count, latency):
    """Continuous log generator."""
    try:
        i = 0
        while count == 0 or i < count:
            log_entry = generate_log_entry(error_rate, output_format, latency)
            print(log_entry, flush=True)
            if sleep > 0:
                time.sleep(sleep)
            i += 1
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()
