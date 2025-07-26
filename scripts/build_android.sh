#!/usr/bin/env bash
# build_android.sh — Automate frontend build, asset copy, and Android APK assembly

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/.."
FRONTEND_DIR="${PROJECT_ROOT}/frontend"
ANDROID_ROOT="${PROJECT_ROOT}/mobile/android_app"
STATIC_DIR="${ANDROID_ROOT}/app/src/main/python/app/static"

# 1) Build React frontend
echo "▶ Building React frontend..."
cd "${FRONTEND_DIR}"
npm install
npm run build

# 2) Copy build assets to Android static folder
echo "▶ Copying build to Android static assets..."
rm -rf "${STATIC_DIR}"
mkdir -p "${STATIC_DIR}"
cp -r build/* "${STATIC_DIR}/"

# 3) Assemble Android Release APK
echo "▶ Assembling Android release APK..."
cd "${ANDROID_ROOT}"
./gradlew assembleRelease

# 4) Locate and report APK
APK_PATH=$(find app/build/outputs/apk/release -name '*-release.apk' | head -n1)
echo -e "\n✅ Build complete: ${APK_PATH}"
ls -lh "${APK_PATH}"
