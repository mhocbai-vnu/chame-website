#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export SESSION_SECURE=true
if ! curl --silent --fail --max-time 2 http://127.0.0.1:8000/ >/dev/null 2>&1; then
  nohup python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/chamea-preview.log 2>&1 </dev/null &
fi
for i in $(seq 1 30); do
  if curl --silent --fail --max-time 2 http://127.0.0.1:8000/ >/dev/null 2>&1; then
    echo "CHAMÉA đang chạy tại http://localhost:8000 — mở tab PORTS, cổng 8000, chọn Open in Browser."
    echo "GIỮ PORT VISIBILITY = PRIVATE. Thông tin đăng nhập quản trị nằm trong data/PREVIEW_LOGIN.txt."
    exit 0
  fi
  sleep 1
done
echo "CHAMÉA chưa khởi động thành công; kiểm tra /tmp/chamea-preview.log" >&2
tail -n 60 /tmp/chamea-preview.log >&2 || true
exit 1
