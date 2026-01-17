#!/usr/bin/env bash
set -e

PROJECT_NAME="$1"
BASE_DIR="/home/zyxx/projects"

echo "🚀 Deploying $PROJECT_NAME"

cd "$BASE_DIR/$PROJECT_NAME"

echo "🔄 Sync code from origin/master"
git fetch origin
git checkout master
git reset --hard origin/master

echo "🔁 Restart service"
sudo systemctl restart "$PROJECT_NAME"

echo "✅ $PROJECT_NAME deployed"
