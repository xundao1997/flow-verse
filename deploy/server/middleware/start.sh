#!/usr/bin/env bash

set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

require_command() {
  local command_name="$1"

  if ! command -v "$command_name" >/dev/null 2>&1; then
    printf 'Required command not found: %s\n' "$command_name" >&2
    exit 1
  fi
}

generate_secret() {
  local target_path="$1"
  local format="$2"

  if [[ -s "$target_path" ]]; then
    chmod 600 "$target_path"
    return
  fi

  case "$format" in
    base64)
      openssl rand -base64 48 | tr -d '\n' > "$target_path"
      ;;
    hex)
      openssl rand -hex 16 | tr -d '\n' > "$target_path"
      ;;
    *)
      printf 'Unsupported secret format: %s\n' "$format" >&2
      exit 1
      ;;
  esac

  chmod 600 "$target_path"
  if [[ ! -s "$target_path" ]]; then
    printf 'Failed to generate secret file: %s\n' "$target_path" >&2
    exit 1
  fi
}

require_command docker
require_command openssl
if ! compose_version="$(docker compose version --short 2>/dev/null)"; then
  printf 'Docker Compose plugin is unavailable. Install Docker Compose v2.24 or newer.\n' >&2
  exit 1
fi
if [[ ! "$compose_version" =~ ^v?([0-9]+)\.([0-9]+)(\.[0-9]+)? ]]; then
  printf 'Unable to parse Docker Compose version: %s\n' "$compose_version" >&2
  exit 1
fi
if (( BASH_REMATCH[1] < 2 || (BASH_REMATCH[1] == 2 && BASH_REMATCH[2] < 24) )); then
  printf 'Docker Compose v2.24 or newer is required; found %s.\n' "$compose_version" >&2
  exit 1
fi

if [[ ! -e .env ]]; then
  cp .env.example .env
  chmod 600 .env
fi

mkdir -p secrets
chmod 700 secrets
umask 077

generate_secret secrets/postgres_password base64
generate_secret secrets/redis_password base64
generate_secret secrets/minio_root_user hex
generate_secret secrets/minio_root_password base64

printf 'Validating middleware configuration...\n'
docker compose config --quiet

printf 'Building pinned middleware images...\n'
docker compose build --pull

printf 'Starting middleware and waiting for health checks...\n'
docker compose up -d --wait --wait-timeout "${FLOWVERSE_WAIT_TIMEOUT_SECONDS:-300}"

docker compose ps
