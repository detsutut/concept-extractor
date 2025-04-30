#!/bin/bash
cd "$(dirname "$0")"
docker compose -f ../docker-compose.yml -p concept-extractor  --env-file ../.env up --detach