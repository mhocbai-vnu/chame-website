#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python -m pip install -r requirements.txt
python -m app.manage init
PYTHONPATH="${PWD}${PYTHONPATH:+:$PYTHONPATH}" python .devcontainer/create_preview_owner.py
echo "CHAMÉA: hoàn tất cài đặt. Mở data/PREVIEW_LOGIN.txt để xem thông tin quản trị thử nghiệm."
