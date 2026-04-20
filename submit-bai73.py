from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import requests


SUBMIT_URL = (
    "https://trangden.vn/agentsee/api/bai-tap/3494/"
    "a090b38ae7f995af2caaa2a74c887e89/tuan-1/bai-7/cau-3"
)
VERIFY_URL = f"{SUBMIT_URL}/verify"
MAP_URL = "https://leafletjs.com"
AGENT_NAME = "Codex-GitHub-Actions"
DEFAULT_IMAGE = "submission-shot-dallas-exact.png"


def print_json(title: str, payload: object) -> None:
    print(f"\n=== {title} ===")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def get_runtime_geo() -> dict:
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
        except Exception as exc:
            last_error = {"source": url, "error": str(exc)}
    return {"error": "Khong lay duoc geo", "last_attempt": last_error}


def submit(image_path: Path) -> dict:
    with image_path.open("rb") as image_file:
        response = requests.post(
            SUBMIT_URL,
            files={"screenshot": (image_path.name, image_file, "image/png")},
            data={"map_url": MAP_URL, "agent": AGENT_NAME},
            timeout=60,
        )
    response.raise_for_status()
    return response.json()


def verify() -> dict:
    response = requests.post(VERIFY_URL, timeout=60)
    response.raise_for_status()
    return response.json()


def main() -> int:
    image_path = Path(os.environ.get("BAI73_IMAGE", DEFAULT_IMAGE))
    if not image_path.exists():
        print(f"Khong tim thay anh: {image_path}", file=sys.stderr)
        return 2

    print_json("Runner IP / Geo", get_runtime_geo())
    print(f"\nDung file anh: {image_path}")
    print(f"Map URL: {MAP_URL}")

    submit_result = submit(image_path)
    print_json("Ket qua submit", submit_result)

    last_verify: dict | None = None
    for attempt in range(1, 6):
        time.sleep(6)
        last_verify = verify()
        print_json(f"Ket qua verify lan {attempt}", last_verify)
        if last_verify.get("valid") is True:
            print("\nPASS roi.")
            return 0

    print("\nVan chua pass sau 5 lan verify.", file=sys.stderr)
    return 1 if last_verify else 3


if __name__ == "__main__":
    raise SystemExit(main())
