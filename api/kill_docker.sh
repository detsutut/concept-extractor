#!/bin/bash
cd "$(dirname "$0")"
docker compose -f ../docker-compose.yml down --remove-orphans