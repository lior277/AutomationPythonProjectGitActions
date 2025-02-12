#!/bin/bash
set -e

# Ensure proper directory permissions
mkdir -p /app/test-results/{logs,screenshots,reports}
chown -R testuser:testuser /app/test-results
chmod -R 777 /app/test-results

# Start virtual framebuffer
Xvfb :99 -screen 0 1920x1080x24 > /dev/null 2>&1 &
sleep 2

# Run tests with coverage
python -m pytest tests/ui/ \
    -v \
    --html=/app/test-results/reports/report.html \
    --self-contained-html \
    --capture=tee-sys \
    --log-cli-level=INFO \
    --cov=src \
    --cov-report=xml:/app/test-results/coverage.xml \
    --cov-report=html:/app/test-results/coverage_html \
    "$@"