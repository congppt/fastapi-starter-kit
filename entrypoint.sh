#!/bin/sh
set -e

mkdir -p /dist/logs
chown -R appuser:appuser /dist/logs

exec gosu appuser env HOME=/tmp "$@"