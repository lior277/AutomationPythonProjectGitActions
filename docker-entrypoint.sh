#!/bin/bash
set -e

# Ensure directories exist with proper permissions
mkdir -p /app/test-results/logs
chown -R testuser:testuser /app/test-results
chmod 777 /app/test-results

# Start virtual framebuffer
Xvfb :99 -screen 0 1920x1080x24 &

# Wait for Xvfb to start
sleep 1

# Run tests
cd /app
python -m pytest tests/ui/ -v \
    --html=/app/test-results/report.html \
    --self-contained-html \
    --capture=tee-sys \
    --log-cli-level=INFO