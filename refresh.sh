#!/usr/bin/env bash

echo ">>> Running: git pull"
git pull

echo ">>> Running: podman kill darsyar_cont"
podman kill darsyar_cont

echo ">>> Running: podman rm darsyar_cont"
podman rm darsyar_cont

echo ">>> Running: podman image build -t darsyar_image ./ -f ./dockerfile"
podman image build -t darsyar_image ./ -f ./dockerfile

echo ">>> Running: podman run -d -p 6868:6868 --name darsyar_cont darsyar_image"
podman run -d -p 6868:6868 --name darsyar_cont darsyar_image