#!/usr/bin/env bash

set -e


echo "Runing virtual environment..."
source /app/.venv/bin/activate

echo "Run apply migrations.."

pogo apply

if [ $? -ne 0 ]; then
    echo "Failed to apply migrations"
    exit 1
fi

echo "Migrations applied!"

exec "$@"