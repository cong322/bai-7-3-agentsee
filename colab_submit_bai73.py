"""Colab helper for Agent SEE bai 7.3 submission.

Chay file nay trong Google Colab:
1. Upload `submission-shot-dallas.png`
2. Script se in IP/geo hien tai
3. Submit bai
4. Verify lai vai lan de tranh tre cache/backend
"""

from __future__ import annotations

import io
import json
import time
from pathlib import Path

import requests

try:
    from google.colab import files
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Script nay de chay trong Google Colab.") from exc


SUBMIT_URL = (
    "https://trangden.vn/agentsee/api/bai-tap/3494/"
    "a090b38ae7f995af2caaa2a74c887e89/tuan-1/bai-7/cau-3"
)
VERIFY_URL = f"{SUBMIT_URL}/verify"
MAP_URL = "https://leafletjs.com"
AGENT_NAME = "Codex"


def fetch_runtime_info() -> dict:
    services = [
        "https://ipinfo.io/json",
        "https://ipapi.co/json/",
        "https://httpbin.org/ip",
    ]
    for url in services:
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            return {"source": url, "data": response.json()}
        except Exception:
            continue
    return {"source": None, "data": {"error": "Khong lay duoc thong tin IP runtime"}}


def upload_image() -> tuple[str, bytes]:
    uploaded = files.upload()
    if not uploaded:
        raise SystemExit("Chua upload file anh.")

    file_name, content = next(iter(uploaded.items()))
    return file_name, content


def submit_assignment(file_name: str, content: bytes) -> dict:
    files_payload = {
        "screenshot": (file_name, io.BytesIO(content), "image/png"),
    }
    data_payload = {
        "map_url": MAP_URL,
        "agent": AGENT_NAME,
    }

    response = requests.post(
        SUBMIT_URL,
        files=files_payload,
        data=data_payload,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def verify_assignment() -> dict:
    response = requests.post(VERIFY_URL, timeout=60)
    response.raise_for_status()
    return response.json()


def print_json(title: str, payload: dict) -> None:
    print(f"\n=== {title} ===")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def main() -> None:
    runtime_info = fetch_runtime_info()
    print_json("IP / Geo hien tai", runtime_info)

    file_name, content = upload_image()
    print(f"\nDa nhan file: {file_name} ({len(content):,} bytes)")
    print(f"Map URL: {MAP_URL}")

    submit_result = submit_assignment(file_name, content)
    print_json("Ket qua submit", submit_result)

    for attempt in range(1, 4):
        time.sleep(5)
        verify_result = verify_assignment()
        print_json(f"Ket qua verify lan {attempt}", verify_result)

        if verify_result.get("valid") is True:
            print("\nPASS roi. Nghi di, dung vat va nua.")
            return

    print("\nVan chua pass sau 3 lan verify.")
    print("Neu check cuoi van do, runtime Colab nay co the khong nam o My.")


if __name__ == "__main__":
    main()
