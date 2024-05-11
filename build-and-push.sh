#!/usr/bin/env bash
set -e

IMAGE_NAME="autogen-codility-tasks"

COMMIT_SHORT_TAG=$(git rev-parse --short HEAD)
IMAGE_LATEST_TAG="wojtek9502/${IMAGE_NAME}:latest"
IMAGE_COMMIT_TAG="wojtek9502/${IMAGE_NAME}:${COMMIT_SHORT_TAG}"

export DOCKER_BUILDKIT=1
docker build --progress=plain . -t "${IMAGE_LATEST_TAG}" -t "${IMAGE_COMMIT_TAG}"
docker push "${IMAGE_LATEST_TAG}"
docker push "${IMAGE_COMMIT_TAG}"
