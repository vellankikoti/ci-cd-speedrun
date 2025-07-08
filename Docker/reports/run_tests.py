#!/usr/bin/env python3
import subprocess
import random
import time
from datetime import datetime
import sys
import os

# Emojis for fun logging
ROCKET = "🚀"
CHECK = "✅"
CROSS = "❌"
WARNING = "⚠️"
BOLT = "⚡"
CHAOS = "💥"
SPARKLES = "✨"

# Add some color for terminal output
def colorize(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

GREEN = "32"
RED = "31"
YELLOW = "33"
BLUE = "34"
CYAN = "36"

def log_info(msg):
    print(colorize(f"{SPARKLES} {msg}", BLUE))

def log_success(msg):
    print(colorize(f"{CHECK} {msg}", GREEN))

def log_warning(msg):
    print(colorize(f"{WARNING} {msg}", YELLOW))

def log_error(msg):
    print(colorize(f"{CROSS} {msg}", RED))

def chaos_delay():
    if random.choice([True, False]):
        delay = random.randint(3, 6)
        log_warning(f"{CHAOS} Chaos delay introduced: sleeping {delay} seconds...")
        time.sleep(delay)

def run_tests():
    log_info(f"Starting Test Run at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Randomly inject chaos delay before running tests
    chaos_delay()

    # Ensure reports folder exists
    os.makedirs("reports", exist_ok=True)

    log_info("Running pytest with HTML report...")

    result = subprocess.run(
        [
            "pytest",
            "tests/",
            "--html=reports/test-report.html",
            "--self-contained-html"
        ],
        capture_output=True,
        text=True
    )

    # Print stdout live
    print(result.stdout)

    if result.returncode == 0:
        log_success("All tests passed successfully! 🎉")
        log_info("View your beautiful HTML report at:")
        log_info(colorize("reports/test-report.html", CYAN))
    else:
        log_error("Some tests failed. Check the HTML report for details.")
        log_info(colorize("reports/test-report.html", CYAN))
        sys.exit(1)

if __name__ == "__main__":
    print(f"{ROCKET} Running CI/CD Chaos Workshop Tests...")
    run_tests()
