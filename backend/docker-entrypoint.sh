#!/bin/bash
set -e

echo "Starting M. abscessus Tolerance Platform Backend..."

# Wait for PostgreSQL
if [ -n "$POSTGRES_HOST" ]; then
    echo "Waiting for PostgreSQL at $POSTGRES_HOST:$POSTGRES_PORT..."
    while ! nc -z "$POSTGRES_HOST" "${POSTGRES_PORT:-5432}"; do
        sleep 1
    done
    echo "PostgreSQL is ready."
fi

# Wait for MongoDB
if [ -n "$MONGODB_HOST" ]; then
    echo "Waiting for MongoDB at $MONGODB_HOST:$MONGODB_PORT..."
    while ! nc -z "$MONGODB_HOST" "${MONGODB_PORT:-27017}"; do
        sleep 1
    done
    echo "MongoDB is ready."
fi

exec "$@"
