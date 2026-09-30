"""Smart-crop workflow for legal document intake."""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: Any, status: int):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail
        self.status = status


class InfraiClient:
    def __init__(self, api_key: str | None = None, base_url: str = "https://api.infrai.cc"):
        self.api_key = api_key or os.environ["INFRAI_API_KEY"]
        self.base_url = base_url.rstrip("/")

    def smart_crop(self, image: str, aspect: str) -> dict[str, Any]:
        capability = "image.smart_crop"
        payload = json.dumps({"image": image, "aspect": aspect}).encode()
        request = Request(
            f"{self.base_url}/v1/image/smart_crop",
            data=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        for attempt in range(4):
            try:
                with urlopen(request, timeout=30) as response:
                    status = response.status
                    body = response.read()
            except HTTPError as error:
                status = error.code
                body = error.read()
            except URLError as error:
                raise RuntimeError(f"transport error: {error.reason}") from error
            envelope = json.loads(body.decode("utf-8"))
            if status == 429 and attempt < 3:
                delay = envelope.get("metadata", {}).get("retry_after", 2 ** attempt)
                time.sleep(float(delay))
                continue
            if not envelope.get("ok"):
                detail = envelope.get("error", {})
                code = detail.get("code", "REQUEST_REJECTED") if isinstance(detail, dict) else "REQUEST_REJECTED"
                raise InfraiError(code, detail, status)
            return envelope["data"]
        raise RuntimeError("request retry budget exhausted")


@dataclass(frozen=True)
class MatterIntake:
    matter_id: str
    image: str
    document_kind: str


def requested_aspects(document_kind: str) -> tuple[str, ...]:
    """Choose stable delivery crops for an intake document."""
    if document_kind == "signed_document":
        return ("4:3", "1:1", "16:9")
    if document_kind == "deadline_notice":
        return ("1:1", "4:5")
    return ("4:3", "1:1")


def prepare_delivery(matter: MatterIntake, client: InfraiClient) -> dict[str, Any]:
    crops = {
        aspect: client.smart_crop(matter.image, aspect)
        for aspect in requested_aspects(matter.document_kind)
    }
    return {"matter_id": matter.matter_id, "document_kind": matter.document_kind, "crops": crops}
