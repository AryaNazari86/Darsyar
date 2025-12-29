#!/usr/bin/env bash
set -euo pipefail

# Always run from the script's directory (repo root)
cd "$(dirname "$0")"

echo "==> Pulling latest code..."
git pull

echo "==> Stopping/removing container (if it exists)..."
podman rm -f darsyar_cont >/dev/null 2>&1 || true

echo "==> Building image..."
podman image build -t darsyar_image -f ./dockerfile .

echo "==> Starting container..."
podman run -d \
  -e PYTHONUNBUFFERED=1 \
  -p 6868:6868 \
  --name darsyar_cont \
  darsyar_image

echo "==> Done."
podman ps --filter name=darsyar_cont