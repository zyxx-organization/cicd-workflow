#!/usr/bin/env bash
set -e

PROJECT_NAME="$1"
BASE_DIR="/home/zyxx/projects"

echo "🚀 Deploying $PROJECT_NAME"

cd "$BASE_DIR/$PROJECT_NAME"

git pull --ff-only

sudo systemctl restart "$PROJECT_NAME"

echo "✅ $PROJECT_NAME deployed"
